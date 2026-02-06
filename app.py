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

st.set_page_config(page_title="Law GPA Pro", layout="wide")

# CSS ขั้นสูง: ซ่อนลูกศร Dropdown และปรับแต่งให้ตัวเกรดอยู่ตรงกลางชัดๆ
st.markdown("""
    <style>
    .stMainBlockContainer { padding-top: 1rem !important; }
    
    /* ซ่อนลูกศรใน Selectbox */
    [data-baseweb="select"] [data-testid="stHeaderActionElements"] {
        display: none !important;
    }
    
    /* ปรับแต่งช่อง Selectbox ให้เล็กและตัวอักษรอยู่ตรงกลาง */
    div[data-baseweb="select"] {
        min-height: 28px !important;
        height: 28px !important;
        border-radius: 4px !important;
    }
    
    div[data-baseweb="select"] > div {
        padding: 0px 2px !important;
        text-align: center !important;
    }

    /* ปรับ Font เกรดให้ตัวใหญ่และหนาขึ้นเล็กน้อย */
    div[data-testid="stMarkdownContainer"] p {
        font-size: 13px !important;
    }

    .result-box {
        padding: 4px;
        border: 1px solid #d1d1d1;
        border-radius: 4px;
        text-align: center;
        background-color: #ffffff;
        margin-bottom: 4px;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ ระบบคำนวณเกรดนิติศาสตร์")

selected_data = []

# --- ส่วนเลือกวิชา ---
for cat, courses in all_courses.items():
    with st.expander(f"📂 {cat}", expanded=True):
        cols = st.columns(4)
        for i, (name, credit) in enumerate(courses.items()):
            with cols[i % 4]:
                inner = st.columns([1.4, 1])
                if inner[0].checkbox(name, key=f"chk_{name}"):
                    # ใส่เกรดเริ่มต้นเป็น A เพื่อให้มองเห็นง่าย
                    g = inner[1].selectbox("G", list(grade_map.keys()), key=f"g_{name}", label_visibility="collapsed")
                    selected_data.append({"name": name, "credit": credit, "grade": g})

# --- ส่วนสรุปผล 6 คอลัมน์ ---
if selected_data:
    st.markdown("---")
    total_creds = sum(d['credit'] for d in selected_data)
    total_points = sum(grade_map[d['grade']] * d['credit'] for d in selected_data)
    gpa = total_points / total_creds if total_creds > 0 else 0

    col_res, col_pdf = st.columns([4, 1])
    col_res.success(f"### GPA รวม: {gpa:.2f} | ทั้งหมด {total_creds} หน่วยกิต")
    
    res_cols = st.columns(6)
    for idx, item in enumerate(selected_data):
        with res_cols[idx % 6]:
            st.markdown(f'<div class="result-box">{item["name"]}<br><b>{item["grade"]}</b></div>', unsafe_allow_html=True)

    if col_pdf.button("🖨️ พิมพ์ PDF", use_container_width=True):
        if os.path.exists("THSarabunNew.ttf"):
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font("THSarabun", "", "THSarabunNew.ttf")
            pdf.set_font("THSarabun", "", 18)
            pdf.cell(0, 10, "รายงานผลการเรียน", ln=True, align='C')
            pdf.set_font("THSarabun", "", 12)
            for d in selected_data:
                pdf.cell(60, 8, f" {d['name']}", 1)
                pdf.cell(60, 8, f" {d['credit']} นก.", 1)
                pdf.cell(60, 8, f" เกรด {d['grade']}", 1, ln=True)
            st.download_button("💾 บันทึก PDF", data=pdf.output(), file_name="GPA_Law.pdf")
