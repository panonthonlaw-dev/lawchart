import streamlit as st
from fpdf import FPDF
import os

# ข้อมูลวิชา 140 นก.
all_courses = {
    "หมวดวิชา RAM": {"RAM1103": 3, "RAM1111": 3, "RAM1112": 3, "RAM1132": 3, "RAM1141": 3, "RAM1204": 3, "RAM1213": 3, "RAM1301": 3, "RAM1302": 3, "RAM1312": 3},
    "หมวดวิชา LAW": {
        "LAW1101": 2, "LAW1102": 2, "LAW1103": 3, "LAW1106": 3, "LAW2101": 3, "LAW2102": 3, "LAW2103": 2, "LAW2104": 3, "LAW2105": 2, "LAW2106": 3, "LAW2107": 2, "LAW2108": 2, "LAW2109": 2, "LAW2110": 2, "LAW2111": 2, "LAW2112": 2, "LAW2113": 2, "LAW3101": 2, "LAW3102": 2, "LAW3103": 2, "LAW3104": 2, "LAW3105": 3, "LAW3106": 3, "LAW3107": 2, "LAW3108": 2, "LAW3109": 2, "LAW3110": 2, "LAW3111": 2, "LAW3112": 3, "LAW3117": 2, "LAW4101": 2, "LAW4102": 2, "LAW4103": 3, "LAW4104": 2, "LAW4105": 2, "LAW4106": 3, "LAW4107": 2, "LAW4108": 2, "LAW4109": 2, "LAW4110": 2
    },
    "หมวดวิชาเลือก": {"เลือก 1": 3, "เลือก 2": 3, "กม.เลือก 1": 3, "กม.เลือก 2": 3, "กม.เลือก 3": 3, "กม.เลือก 4": 3}
}

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}

st.set_page_config(page_title="GPA Law Extreme", layout="wide")

# CSS เพื่อบังคับให้ Dropdown และช่องว่างเล็กจิ๋วที่สุด
st.markdown("""
    <style>
    /* ลดระยะห่างระหว่างบรรทัดและ Column */
    .stMainBlockContainer { padding-top: 20px !important; }
    div[data-testid="stExpander"] { margin-bottom: 0px !important; }
    div[data-testid="column"] { padding: 0px 2px !important; }
    
    /* ปรับแต่ง Dropdown (Selectbox) ให้เล็กลง */
    div[data-baseweb="select"] {
        min-height: 25px !important;
        height: 25px !important;
        font-size: 12px !important;
    }
    div[data-testid="stMarkdownContainer"] p {
        font-size: 13px !important;
        margin-bottom: 0px !important;
    }
    /* ปรับปุ่มเลือกวิชาให้เล็กลง */
    div[data-testid="stCheckbox"] {
        margin-bottom: -10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ GPA Law (Extreme Compact)")

if "selected" not in st.session_state:
    st.session_state.selected = {}

# --- 1. ส่วนเลือกวิชา (Grid 6 คอลัมน์) ---
for cat, courses in all_courses.items():
    with st.expander(f"📂 {cat}", expanded=True):
        cols = st.columns(6)
        for i, (name, credit) in enumerate(courses.items()):
            with cols[i % 6]:
                if st.checkbox(f"{name}", key=f"chk_{name}"):
                    st.session_state.selected[name] = credit
                else:
                    st.session_state.selected.pop(name, None)

# --- 2. ส่วนกรอกเกรด (Grid 5 คอลัมน์) ---
if st.session_state.selected:
    st.markdown("---")
    selected_sorted = dict(sorted(st.session_state.selected.items()))
    items = list(selected_sorted.items())
    
    total_creds, total_score, pdf_list = 0, 0, []

    # แสดงผล 5 วิชาต่อ 1 แถว (ใช้พื้นที่คุ้มค่าที่สุด)
    rows = (len(items) + 4) // 5
    for r in range(rows):
        cols = st.columns(5)
        for c in range(5):
            idx = r * 5 + c
            if idx < len(items):
                name, credit = items[idx]
                with cols[c]:
                    # ใช้ Column เล็กๆ ซ้อนกันเพื่อบีบชื่อและ Dropdown
                    inner = st.columns([1, 1])
                    inner[0].write(f"**{name}**")
                    g_letter = inner[1].selectbox(
                        "G", list(grade_map.keys()), 
                        key=f"grd_{name}", 
                        label_visibility="collapsed"
                    )
                    total_creds += credit
                    total_score += grade_map[g_letter] * credit
                    pdf_list.append([name, str(credit), g_letter])

    # ส่วนสรุปผล
    if total_creds > 0:
        gpa = total_score / total_creds
        col_res1, col_res2 = st.columns([2, 1])
        col_res1.info(f"**GPA: {gpa:.2f}** (รวม {total_creds} นก.)")
        
        if col_res2.button("🖨️ PDF", use_container_width=True):
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
                st.download_button("💾 Save PDF", data=pdf.output(), file_name="GPA.pdf")
