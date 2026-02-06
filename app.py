import streamlit as st
from fpdf import FPDF
import os
from io import BytesIO  # เพิ่มการจัดการหน่วยความจำสำหรับไฟล์

# --- 1. ข้อมูลวิชา 140 หน่วยกิต ---
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

st.set_page_config(page_title="GPA Law Compact", layout="wide")

# --- 2. ฟังก์ชันล้างค่า ---
def reset_all():
    for key in st.session_state.keys():
        if key.startswith("chk_") or key.startswith("g_"):
            if key.startswith("chk_"):
                st.session_state[key] = False
            else:
                st.session_state[key] = "A"

# --- 3. CSS (ซ่อน Top Bar + ปรับระยะขอบบน + ซ่อนลูกศร) ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stMainBlockContainer { padding-top: 4rem !important; }
    
    /* ซ่อนลูกศร Dropdown */
    [data-baseweb="select"] [data-testid="stHeaderActionElements"], 
    svg[class^="StyledIcon"], .stSelectbox svg { display: none !important; }
    
    div[data-baseweb="select"] { 
        min-height: 28px !important; height: 28px !important; background-color: #f0f2f6 !important; 
    }
    div[data-baseweb="select"] [data-testid="stMarkdownContainer"] p { 
        text-align: center !important; font-weight: bold !important; font-size: 14px !important; 
    }
    
    div[data-testid="column"] { padding: 0px 4px !important; }
    .stCheckbox { margin-bottom: -15px !important; }
    .result-box { padding: 4px; border: 1px solid #ddd; border-radius: 4px; text-align: center; background-color: white; margin-bottom: 5px; font-size: 11px; }
    </style>
    """, unsafe_allow_html=True)

# ส่วนหัวเรื่อง
head_col1, head_col2 = st.columns([5, 1])
head_col1.title("⚖️ คำนวณเกรดนิติศาสตร์")
if head_col2.button("♻️ ล้างค่า", on_click=reset_all, use_container_width=True):
    st.rerun()

selected_data = []

# --- 4. ส่วนเลือกวิชา ---
for cat, courses in all_courses.items():
    with st.expander(f"📂 {cat}", expanded=True):
        cols = st.columns(4)
        for i, (name, credit) in enumerate(courses.items()):
            with cols[i % 4]:
                inner = st.columns([1.3, 1])
                chk_key = f"chk_{name}"
                if chk_key not in st.session_state: st.session_state[chk_key] = False
                
                is_checked = inner[0].checkbox(name, key=chk_key)
                if is_checked:
                    grd_key = f"g_{name}"
                    if grd_key not in st.session_state: st.session_state[grd_key] = "A"
                    g = inner[1].selectbox("", list(grade_map.keys()), key=grd_key, label_visibility="collapsed")
                    selected_data.append({"name": name, "credit": credit, "grade": g})

# --- 5. สรุปผลและ PDF ---
if selected_data:
    st.divider()
    total_creds = sum(d['credit'] for d in selected_data)
    total_points = sum(grade_map[d['grade']] * d['credit'] for d in selected_data)
    gpa = total_points / total_creds if total_creds > 0 else 0

    col_res, col_pdf = st.columns([4, 1])
    col_res.success(f"### GPA: {gpa:.2f} | ทั้งหมด {total_creds} หน่วยกิต")
    
    res_cols = st.columns(6)
    for idx, item in enumerate(selected_data):
        with res_cols[idx % 6]:
            st.markdown(f'<div class="result-box">{item["name"]}<br><b>{item["grade"]}</b></div>', unsafe_allow_html=True)

    # --- ส่วนการทำ PDF ที่แก้ไข Error ---
    if col_pdf.button("🖨️ พิมพ์ PDF", use_container_width=True):
        if os.path.exists("THSarabunNew.ttf"):
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font("THSarabun", "", "THSarabunNew.ttf")
            pdf.set_font("THSarabun", "", 20)
            pdf.cell(0, 10, "รายงานผลการเรียน", ln=True, align='C')
            
            pdf.set_font("THSarabun", "", 12)
            pdf.ln(5)
            pdf.cell(80, 8, "วิชา", 1); pdf.cell(50, 8, "หน่วยกิต", 1); pdf.cell(50, 8, "เกรด", 1, ln=True)
            for d in selected_data:
                pdf.cell(80, 8, f" {d['name']}", 1)
                pdf.cell(50, 8, f" {d['credit']} นก.", 1)
                pdf.cell(50, 8, f" {d['grade']}", 1, ln=True)
            
            # แก้ไขตรงนี้: ใช้ BytesIO เพื่อทำให้ข้อมูลเป็น Bytes ที่ Streamlit รับได้แน่นอน
            pdf_bytes = pdf.output()
            st.download_button(
                label="📥 ดาวน์โหลดไฟล์ที่นี่", 
                data=bytes(pdf_bytes), 
                file_name="GPA_Report.pdf", 
                mime="application/pdf", 
                use_container_width=True
            )
        else:
            st.error("ไม่พบไฟล์ฟอนต์")
else:
    st.info("👈 ติ๊กเลือกวิชาด้านบนเพื่อเริ่มคำนวณ")
