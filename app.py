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

st.set_page_config(page_title="Law GPA No-Arrow", layout="wide")

# CSS เพื่อทำความสะอาดช่อง Selectbox ให้ไม่มีลูกศรและกะทัดรัด
st.markdown("""
    <style>
    /* 1. ซ่อนลูกศร (Arrow) และปุ่มลบ (Clear icon) ทั้งหมด */
    [data-testid="stHeaderActionElements"], 
    svg[class^="StyledIcon"], 
    .stSelectbox svg {
        display: none !important;
    }
    
    /* 2. บีบช่องว่างด้านขวาที่เคยมีลูกศรให้เหลือพื้นที่โชว์ตัวอักษร */
    div[data-baseweb="select"] > div:first-child {
        padding-right: 2px !important;
    }

    /* 3. ปรับขนาดช่องให้จิ๋วและจัดตัวอักษรให้อยู่ตรงกลาง */
    div[data-baseweb="select"] {
        min-height: 28px !important;
        height: 28px !important;
        background-color: #f0f2f6 !important;
    }
    
    div[data-baseweb="select"] [data-testid="stMarkdownContainer"] p {
        text-align: center !important;
        width: 100% !important;
        font-weight: bold !important;
        font-size: 14px !important;
    }

    /* 4. ตกแต่งส่วนแสดงผลสรุปด้านล่าง */
    .result-box {
        padding: 4px;
        border: 1px solid #ddd;
        border-radius: 4px;
        text-align: center;
        background-color: white;
        margin-bottom: 5px;
        font-size: 11px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ คำนวณเกรดนิติศาสตร์")

selected_data = []

# --- ส่วนการเลือกวิชา ---
for cat, courses in all_courses.items():
    with st.expander(f"📂 {cat}", expanded=True):
        cols = st.columns(4)
        for i, (name, credit) in enumerate(courses.items()):
            with cols[i % 4]:
                inner = st.columns([1.3, 1])
                # ถ้าติ๊กถูก ช่องเกรดจะโผล่มา
                if inner[0].checkbox(name, key=f"chk_{name}"):
                    g = inner[1].selectbox("", list(grade_map.keys()), key=f"g_{name}", label_visibility="collapsed")
                    selected_data.append({"name": name, "credit": credit, "grade": g})

# --- ส่วนแสดงผลลัพธ์ ---
if selected_data:
    st.divider()
    total_creds = sum(d['credit'] for d in selected_data)
    total_points = sum(grade_map[d['grade']] * d['credit'] for d in selected_data)
    gpa = total_points / total_creds if total_creds > 0 else 0

    col_res, col_pdf = st.columns([4, 1])
    col_res.success(f"### GPA: {gpa:.2f} | {total_creds} หน่วยกิต")
    
    # แสดง 6 คอลัมน์แบบกล่องสรุป
    res_cols = st.columns(6)
    for idx, item in enumerate(selected_data):
        with res_cols[idx % 6]:
            st.markdown(f'<div class="result-box">{item["name"]}<br><b>{item["grade"]}</b></div>', unsafe_allow_html=True)

    if col_pdf.button("🖨️ PDF", use_container_width=True):
        if os.path.exists("THSarabunNew.ttf"):
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font("THSarabun", "", "THSarabunNew.ttf")
            pdf.set_font("THSarabun", "", 20)
            pdf.cell(0, 10, "รายงานผลการเรียน", ln=True, align='C')
            pdf.set_font("THSarabun", "", 12)
            for d in selected_data:
                pdf.cell(60, 8, f" {d['name']}", 1)
                pdf.cell(60, 8, f" {d['credit']} นก.", 1)
                pdf.cell(60, 8, f" เกรด {d['grade']}", 1, ln=True)
            st.download_button("💾 Save PDF", data=pdf.output(), file_name="GPA_Report.pdf")
