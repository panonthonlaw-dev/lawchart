import streamlit as st
from fpdf import FPDF
import os

# --- 1. ข้อมูลวิชา 140 หน่วยกิตเป๊ะ ---
all_courses = {
    "หมวดวิชา RAM (30 นก.)": {
        "RAM1103": 3, "RAM1111": 3, "RAM1112": 3, "RAM1132": 3, 
        "RAM1141": 3, "RAM1204": 3, "RAM1213": 3, "RAM1301": 3, 
        "RAM1302": 3, "RAM1312": 3
    },
    "หมวดวิชา LAW (92 นก.)": {
        "LAW1101": 2, "LAW1102": 2, "LAW1103": 3, "LAW1106": 3,
        "LAW2101": 3, "LAW2102": 3, "LAW2103": 2, "LAW2104": 3,
        "LAW2105": 2, "LAW2106": 3, "LAW2107": 2, "LAW2108": 2,
        "LAW2109": 2, "LAW2110": 2, "LAW2111": 2, "LAW2112": 2,
        "LAW2113": 2, "LAW3101": 2, "LAW3102": 2, "LAW3103": 2,
        "LAW3104": 2, "LAW3105": 3, "LAW3106": 3, "LAW3107": 2,
        "LAW3108": 2, "LAW3109": 2, "LAW3110": 2, "LAW3111": 2,
        "LAW3112": 3, "LAW3117": 2, "LAW4101": 2, "LAW4102": 2,
        "LAW4103": 3, "LAW4104": 2, "LAW4105": 2, "LAW4106": 3,
        "LAW4107": 2, "LAW4108": 2, "LAW4109": 2, "LAW4110": 2
    },
    "หมวดวิชาเลือก (18 นก.)": {
        "วิชาเลือก 1": 3, "วิชาเลือก 2": 3, "วิชาเลือกกฎหมาย 1": 3,
        "วิชาเลือกกฎหมาย 2": 3, "วิชาเลือกกฎหมาย 3": 3, "วิชาเลือกกฎหมาย 4": 3
    }
}

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}

# --- 2. ตั้งค่าหน้าเว็บและ CSS ---
st.set_page_config(page_title="GPA Law Compact", layout="wide")

st.markdown("""
    <style>
    /* ซ่อนลูกศร Dropdown และปุ่มกากบาท */
    [data-baseweb="select"] [data-testid="stHeaderActionElements"], 
    svg[class^="StyledIcon"], .stSelectbox svg {
        display: none !important;
    }
    /* ปรับแต่งช่อง Selectbox ให้เล็กจิ๋วและตัวอักษรอยู่ตรงกลาง */
    div[data-baseweb="select"] {
        min-height: 28px !important; height: 28px !important;
        background-color: #f0f2f6 !important;
    }
    div[data-baseweb="select"] [data-testid="stMarkdownContainer"] p {
        text-align: center !important; font-weight: bold !important; font-size: 14px !important;
    }
    /* บีบระยะห่าง */
    .stMainBlockContainer { padding-top: 1rem !important; }
    div[data-testid="column"] { padding: 0px 4px !important; }
    .stCheckbox { margin-bottom: -15px !important; }
    
    /* สไตล์กล่องสรุป 6 คอลัมน์ด้านล่าง */
    .result-box {
        padding: 4px; border: 1px solid #ddd; border-radius: 4px;
        text-align: center; background-color: white; margin-bottom: 5px; font-size: 11px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ เครื่องมือคำนวณเกรดนิติศาสตร์")

selected_data = []

# --- 3. ส่วนการเลือกวิชา (แสดงผล 4 คอลัมน์) ---
for cat, courses in all_courses.items():
    with st.expander(f"📂 {cat}", expanded=True):
        cols = st.columns(4)
        for i, (name, credit) in enumerate(courses.items()):
            with cols[i % 4]:
                inner = st.columns([1.3, 1])
                if inner[0].checkbox(name, key=f"chk_{name}"):
                    # ช่องเกรดจะโผล่มาเมื่อติ๊กถูก ชิดกับชื่อวิชา และไม่มีลูกศร
                    g = inner[1].selectbox("", list(grade_map.keys()), key=f"g_{name}", label_visibility="collapsed")
                    selected_data.append({"name": name, "credit": credit, "grade": g})

# --- 4. ส่วนสรุปผลและสร้าง PDF ---
if selected_data:
    st.divider()
    total_creds = sum(d['credit'] for d in selected_data)
    total_points = sum(grade_map[d['grade']] * d['credit'] for d in selected_data)
    gpa = total_points / total_creds if total_creds > 0 else 0

    col_res, col_pdf = st.columns([4, 1])
    col_res.success(f"### GPA: {gpa:.2f} | ทั้งหมด {total_creds} หน่วยกิต")
    
    # แสดงสรุปวิชาแบบ 6 คอลัมน์
    res_cols = st.columns(6)
    for idx, item in enumerate(selected_data):
        with res_cols[idx % 6]:
            st.markdown(f'<div class="result-box">{item["name"]}<br><b>{item["grade"]}</b></div>', unsafe_allow_html=True)

    # ฟังก์ชันสร้าง PDF (แก้ไข Error unsupported_error)
    if col_pdf.button("🖨️ พิมพ์ PDF", use_container_width=True):
        if os.path.exists("THSarabunNew.ttf"):
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.add_font("THSarabun", "", "THSarabunNew.ttf")
                pdf.set_font("THSarabun", "", 20)
                pdf.cell(0, 10, "รายงานผลการเรียนเฉลี่ย", ln=True, align='C')
                
                pdf.set_font("THSarabun", "", 12)
                pdf.ln(5)
                # หัวตาราง
                pdf.cell(80, 8, "วิชา", 1); pdf.cell(50, 8, "หน่วยกิต", 1); pdf.cell(50, 8, "เกรด", 1, ln=True)
                
                for d in selected_data:
                    pdf.cell(80, 8, f" {d['name']}", 1)
                    pdf.cell(50, 8, f" {d['credit']} นก.", 1)
                    pdf.cell(50, 8, f" {d['grade']}", 1, ln=True)
                
                pdf.ln(5)
                pdf.set_font("THSarabun", "", 16)
                pdf.cell(0, 10, f"เกรดเฉลี่ยสะสม (GPA): {gpa:.2f} | รวมหน่วยกิต: {total_creds}", ln=True)
                
                # แปลงเป็น Bytes ให้ Streamlit รองรับ
                pdf_bytes = pdf.output()
                if isinstance(pdf_bytes, str): # ป้องกันกรณี fpdf คืนค่าเป็น string
                    pdf_bytes = pdf_bytes.encode('latin-1')
                
                st.download_button(
                    label="💾 คลิกเพื่อดาวน์โหลด PDF",
                    data=pdf_bytes,
                    file_name="GPA_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.error("ไม่พบไฟล์ฟอนต์ THSarabunNew.ttf กรุณาตรวจสอบใน Repo")
else:
    st.info("👈 เริ่มต้นโดยการติ๊กเลือกวิชาที่คุณสอบผ่านแล้วจากเมนูด้านบน")
