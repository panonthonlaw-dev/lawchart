import streamlit as st
from fpdf import FPDF
import os
from io import BytesIO

# --- 1. ข้อมูลวิชา 140 หน่วยกิต ---
all_courses = {
    "หมวดวิชา RAM": {"RAM1103": 3, "RAM1111": 3, "RAM1112": 3, "RAM1132": 3, "RAM1141": 3, "RAM1204": 3, "RAM1213": 3, "RAM1301": 3, "RAM1302": 3, "RAM1312": 3},
    "หมวดวิชา LAW": {
        "LAW1101": 2, "LAW1102": 2, "LAW1103": 3, "LAW1106": 3, "LAW2101": 3, "LAW2102": 3, "LAW2103": 2, "LAW2104": 3, "LAW2105": 2, "LAW2106": 3, "LAW2107": 2, "LAW2108": 2, "LAW2109": 2, "LAW2110": 2, "LAW2111": 2, "LAW2112": 2, "LAW2113": 2, "LAW3101": 2, "LAW3102": 2, "LAW3103": 2, "LAW3104": 2, "LAW3105": 3, "LAW3106": 3, "LAW3107": 2, "LAW3108": 2, "LAW3109": 2, "LAW3110": 2, "LAW3111": 2, "LAW3112": 3, "LAW3117": 2, "LAW4101": 2, "LAW4102": 2, "LAW4103": 3, "LAW4104": 2, "LAW4105": 2, "LAW4106": 3, "LAW4107": 2, "LAW4108": 2, "LAW4109": 2, "LAW4110": 2
    },
    "หมวดวิชาเลือก": {"วิชาเลือก 1": 3, "วิชาเลือก 2": 3, "กม.เลือก 1": 3, "กม.เลือก 2": 3, "กม.เลือก 3": 3, "กม.เลือก 4": 3}
}

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}

st.set_page_config(page_title="GPA Law Pro", layout="wide")

# --- 2. ฟังก์ชัน Popup โดเนท ---
@st.dialog("สนับสนุนผู้พัฒนา 🙏")
def donate_dialog():
    st.write("ใช้ฟรี! หากอยากโดเนทเพื่อให้กำลังใจ สามารถสแกนได้ที่นี่ครับ")
    img_file = "donate.png" if os.path.exists("donate.png") else "donate.jpg"
    if os.path.exists(img_file):
        st.image(img_file, use_container_width=True)
    else:
        st.error("ไม่พบไฟล์รูป donate.png")

def reset_all():
    for key in list(st.session_state.keys()):
        if key.startswith("chk_") or key.startswith("g_"):
            st.session_state[key] = False if key.startswith("chk_") else "A"

# --- 3. CSS ฉบับ Mobile First (บังคับ Column) ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stMainBlockContainer { padding-top: 2rem !important; }
    
    /* บังคับให้ Grid แสดงผลหลายคอลัมน์แม้ในมือถือ */
    [data-testid="stExpander"] [data-testid="column"] {
        flex: 1 1 45% !important; /* บังคับให้กว้างประมาณครึ่งหน้าจอ (2 คอลัมน์) */
        min-width: 150px !important;
    }
    
    /* ซ่อนลูกศรและแต่ง Dropdown */
    [data-baseweb="select"] [data-testid="stHeaderActionElements"], svg[class^="StyledIcon"], .stSelectbox svg { display: none !important; }
    div[data-baseweb="select"] { min-height: 28px !important; height: 28px !important; background-color: #f0f2f6 !important; }
    div[data-baseweb="select"] [data-testid="stMarkdownContainer"] p { text-align: center !important; font-weight: bold !important; font-size: 14px !important; }
    
    .stCheckbox { margin-bottom: -10px !important; }
    .result-box { padding: 4px; border: 1px solid #ddd; border-radius: 4px; text-align: center; background-color: white; margin-bottom: 5px; font-size: 11px; }
    
    /* ปรับแต่งปุ่มและหัวข้อ */
    .stButton button { padding: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

# ส่วนหัวเรื่อง
head_col1, head_col2 = st.columns([4, 1.5])
head_col1.title("⚖️ คำนวณเกรดนิติศาสตร์")
if head_col2.button("♻️ ล้างค่า", on_click=reset_all, use_container_width=True):
    st.rerun()

selected_by_cat = {cat: [] for cat in all_courses.keys()}

# --- 4. ส่วนเลือกวิชา ---
for cat, courses in all_courses.items():
    with st.expander(f"📂 {cat}", expanded=True):
        cols = st.columns(4) # ในคอมจะเป็น 4 ในมือถือจะพยายามคงไว้ 2 ด้วย CSS
        for i, (name, credit) in enumerate(courses.items()):
            with cols[i % 4]:
                # จัดรูปแบบ [Checkbox][Selectbox] ในบรรทัดเดียว
                c_row = st.columns([1.2, 1])
                chk_key = f"chk_{name}"
                if chk_key not in st.session_state: st.session_state[chk_key] = False
                
                if c_row[0].checkbox(name, key=chk_key):
                    grd_key = f"g_{name}"
                    if grd_key not in st.session_state: st.session_state[grd_key] = "A"
                    g = c_row[1].selectbox("", list(grade_map.keys()), key=grd_key, label_visibility="collapsed")
                    selected_by_cat[cat].append({"name": name, "credit": credit, "grade": g})

# --- 5. สรุปผล ---
all_selected = [item for sublist in selected_by_cat.values() for item in sublist]
if all_selected:
    st.divider()
    total_creds = sum(d['credit'] for d in all_selected)
    total_points = sum(grade_map[d['grade']] * d['credit'] for d in all_selected)
    gpa = total_points / total_creds if total_creds > 0 else 0

    st.success(f"### GPA: {gpa:.2f} | รวม {total_creds} หน่วยกิต")
    
    # แสดงรายชื่อวิชา (ใช้ columns ปกติซึ่งจะเรียงแนวตั้งในมือถือเพื่อให้กดอ่านง่าย)
    res_cols = st.columns(3) if total_creds > 0 else st.columns(1)
    for idx, item in enumerate(all_selected):
        with res_cols[idx % (3 if total_creds > 0 else 1)]:
            st.markdown(f'<div class="result-box">{item["name"]} - <b>{item["grade"]}</b></div>', unsafe_allow_html=True)

    if st.button("🖨️ พิมพ์ PDF", use_container_width=True):
        if os.path.exists("THSarabunNew.ttf"):
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font("THSarabun", "", "THSarabunNew.ttf")
            pdf.set_font("THSarabun", "", 22)
            pdf.cell(0, 15, "รายงานสรุปผลการเรียน", ln=True, align='C')
            for c, items in selected_by_cat.items():
                if items:
                    pdf.set_font("THSarabun", "", 16); pdf.set_fill_color(230, 230, 230)
                    pdf.cell(0, 10, f" {c}", ln=True, fill=True)
                    pdf.set_font("THSarabun", "", 12)
                    for i, d in enumerate(items):
                        side = i % 2
                        if side == 0 and i > 0: pdf.set_y(pdf.get_y() + 8)
                        pdf.set_xy(10 if side == 0 else 105, pdf.get_y())
                        pdf.cell(63, 8, f" {d['name']}", 1); pdf.cell(27, 8, f"{d['grade']}", 1, align='C')
                    pdf.set_y(pdf.get_y() + 12)
            pdf_bytes = pdf.output()
            st.download_button("📥 บันทึกไฟล์ PDF", data=bytes(pdf_bytes), file_name="GPA_Law.pdf", mime="application/pdf", use_container_width=True)

# --- 6. Footer โดเนท ---
st.markdown("---")
st.markdown('<p style="text-align:center; color:#888;">โปรแกรมนี้ใช้ฟรี! หากต้องการสนับสนุนผู้พัฒนา</p>', unsafe_allow_html=True)
if st.button("🧧 สนับสนุนค่าน้ำชา / โดเนท", use_container_width=True):
    donate_dialog()
