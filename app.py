import streamlit as st
from fpdf import FPDF
import os

# ข้อมูลวิชา (140 นก.)
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
        "เลือก 1": 3, "เลือก 2": 3, "กม.เลือก 1": 3,
        "กม.เลือก 2": 3, "กม.เลือก 3": 3, "กม.เลือก 4": 3
    }
}

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}

st.set_page_config(page_title="GPA Ultra Compact", layout="wide")

# CSS เพื่อลดระยะห่างระหว่าง Element ให้ชิดกันยิ่งขึ้น
st.markdown("""
    <style>
    [data-testid="column"] {
        padding: 0px 5px !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        min-height: 30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ คำนวณเกรดนิติศาสตร์ (Ultra Compact)")

if "selected" not in st.session_state:
    st.session_state.selected = {}

# --- ส่วนเลือกวิชา (Grid 5 คอลัมน์) ---
for cat, courses in all_courses.items():
    with st.expander(f"📂 {cat}"):
        cols = st.columns(5)
        for i, (name, credit) in enumerate(courses.items()):
            with cols[i % 5]:
                if st.checkbox(f"{name}", key=f"chk_{name}"):
                    st.session_state.selected[name] = credit
                else:
                    st.session_state.selected.pop(name, None)

# --- ส่วนกรอกเกรด (Grid 4 คอลัมน์ + ชิดหน้ากระดาษ) ---
if st.session_state.selected:
    st.markdown("---")
    st.subheader("📝 ระบุเกรด")
    
    selected_sorted = dict(sorted(st.session_state.selected.items()))
    items = list(selected_sorted.items())
    
    total_creds, total_score = 0, 0
    pdf_list = []

    # แสดงผล 4 วิชาต่อ 1 แถวเพื่อความประหยัดพื้นที่
    rows = (len(items) + 3) // 4
    for r in range(rows):
        cols = st.columns(4)
        for c in range(4):
            idx = r * 4 + c
            if idx < len(items):
                name, credit = items[idx]
                with cols[c]:
                    # จัดวางแบบแนวนอน ชิดกันที่สุด
                    inner_cols = st.columns([1.2, 1])
                    inner_cols[0].markdown(f"**{name}**")
                    g_letter = inner_cols[1].selectbox(
                        "G", list(grade_map.keys()), 
                        key=f"grd_{name}", 
                        label_visibility="collapsed"
                    )
                    
                    total_creds += credit
                    total_score += grade_map[g_letter] * credit
                    pdf_list.append([name, str(credit), g_letter])

    if total_creds > 0:
        gpa = total_score / total_creds
        st.success(f"### GPA: {gpa:.2f} | {total_creds} หน่วยกิต")

        # ส่วน PDF
        if st.button("🖨️ พิมพ์ PDF"):
            if os.path.exists("THSarabunNew.ttf"):
                pdf = FPDF()
                pdf.add_page()
                pdf.add_font("THSarabun", "", "THSarabunNew.ttf")
                pdf.set_font("THSarabun", "", 24)
                pdf.cell(0, 15, "สรุปผลการเรียนนิติศาสตร์", ln=True, align='C')
                pdf.set_font("THSarabun", "", 14)
                # ตาราง 3 คอลัมน์ใน PDF
                pdf.cell(60, 10, "วิชา", 1); pdf.cell(60, 10, "หน่วยกิต", 1); pdf.cell(60, 10, "เกรด", 1, ln=True)
                for item in pdf_list:
                    pdf.cell(60, 8, f" {item[0]}", 1)
                    pdf.cell(60, 8, f" {item[1]}", 1)
                    pdf.cell(60, 8, f" {item[2]}", 1, ln=True)
                pdf.ln(5)
                pdf.cell(0, 10, f"รวม {total_creds} หน่วยกิต | GPA: {gpa:.2f}", ln=True)
                st.download_button("📥 โหลดไฟล์ PDF", data=pdf.output(), file_name="GPA_Ultra.pdf")
