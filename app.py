import streamlit as st
from fpdf import FPDF
import os

# ข้อมูลวิชา 140 นก. เป๊ะ
all_courses = {
    "หมวดวิชา RAM": {"RAM1103": 3, "RAM1111": 3, "RAM1112": 3, "RAM1132": 3, "RAM1141": 3, "RAM1204": 3, "RAM1213": 3, "RAM1301": 3, "RAM1302": 3, "RAM1312": 3},
    "หมวดวิชา LAW": {
        "LAW1101": 2, "LAW1102": 2, "LAW1103": 3, "LAW1106": 3, "LAW2101": 3, "LAW2102": 3, "LAW2103": 2, "LAW2104": 3, "LAW2105": 2, "LAW2106": 3, "LAW2107": 2, "LAW2108": 2, "LAW2109": 2, "LAW2110": 2, "LAW2111": 2, "LAW2112": 2, "LAW2113": 2, "LAW3101": 2, "LAW3102": 2, "LAW3103": 2, "LAW3104": 2, "LAW3105": 3, "LAW3106": 3, "LAW3107": 2, "LAW3108": 2, "LAW3109": 2, "LAW3110": 2, "LAW3111": 2, "LAW3112": 3, "LAW3117": 2, "LAW4101": 2, "LAW4102": 2, "LAW4103": 3, "LAW4104": 2, "LAW4105": 2, "LAW4106": 3, "LAW4107": 2, "LAW4108": 2, "LAW4109": 2, "LAW4110": 2
    },
    "หมวดวิชาเลือก": {"เลือก 1": 3, "เลือก 2": 3, "กม.เลือก 1": 3, "กม.เลือก 2": 3, "กม.เลือก 3": 3, "กม.เลือก 4": 3}
}

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}

st.set_page_config(page_title="Law GPA Quick", layout="wide")

# CSS บีบช่องว่างและลดขนาด Dropdown ให้จิ๋วที่สุด
st.markdown("""
    <style>
    .stMainBlockContainer { padding-top: 1rem !important; }
    div[data-testid="column"] { padding: 0px 5px !important; }
    .stSelectbox div[data-baseweb="select"] { min-height: 25px !important; height: 25px !important; font-size: 12px !important; }
    .stCheckbox { margin-bottom: -15px !important; }
    p { font-size: 13px !important; margin: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ คำนวณเกรดนิติศาสตร์")

total_creds = 0
total_score = 0
pdf_list = []

# แบ่งหมวดหมู่ด้วย Expander
for cat, courses in all_courses.items():
    with st.expander(f"📂 {cat}", expanded=True):
        # แสดงผล 4 คอลัมน์ต่อแถว
        cols = st.columns(4)
        for i, (name, credit) in enumerate(courses.items()):
            with cols[i % 4]:
                # สร้าง Row ย่อยข้างใน [Checkbox ชื่อวิชา | Dropdown เกรด]
                inner_cols = st.columns([1.5, 1])
                is_selected = inner_cols[0].checkbox(f"{name}", key=f"chk_{name}")
                
                if is_selected:
                    g_letter = inner_cols[1].selectbox(
                        "G", list(grade_map.keys()), 
                        key=f"grd_{name}", 
                        label_visibility="collapsed"
                    )
                    total_creds += credit
                    total_score += grade_map[g_letter] * credit
                    pdf_list.append([name, str(credit), g_letter])

# --- ส่วนแสดงผลสรุป (ลอยด้านล่าง) ---
if total_creds > 0:
    st.divider()
    gpa = total_score / total_creds
    
    # โชว์ผลแบบกระชับ
    res_col1, res_col2 = st.columns([3, 1])
    res_col1.success(f"### GPA: {gpa:.2f} | ทั้งหมด {total_creds} หน่วยกิต")
    
    if res_col2.button("🖨️ PDF", use_container_width=True):
        if os.path.exists("THSarabunNew.ttf"):
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font("THSarabun", "", "THSarabunNew.ttf")
            pdf.set_font("THSarabun", "", 18)
            pdf.cell(0, 10, "รายงานผลการเรียน", ln=True, align='C')
            pdf.set_font("THSarabun", "", 12)
            for item in pdf_list:
                pdf.cell(60, 7, f" {item[0]}", 1)
                pdf.cell(60, 7, f" {item[1]} นก.", 1)
                pdf.cell(60, 7, f" เกรด {item[2]}", 1, ln=True)
            pdf.ln(5)
            pdf.cell(0, 10, f"รวม {total_creds} หน่วยกิต | GPA: {gpa:.2f}", ln=True)
            st.download_button("💾 Save PDF", data=pdf.output(), file_name="GPA_Law.pdf")
        else:
            st.error("ไม่พบไฟล์ฟอนต์")
