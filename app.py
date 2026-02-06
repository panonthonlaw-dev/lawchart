import streamlit as st
from fpdf import FPDF
import os
from io import BytesIO

# --- 1. ข้อมูลวิชาและตารางสอบ (Database) ---
# "รหัสวิชา": [หน่วยกิต, "วันสอบ", "คาบ", "ชื่อวิชา"]
all_courses_db = {
    "LAW1103": [3, "2", "A", "นิติกรรม"], "LAW2106": [3, "4", "A", "อาญา 1"],
    "LAW2101": [3, "2", "B", "ทรัพย์"], "LAW3101": [2, "1", "A", "อาญา 3"],
    "LAW3104": [2, "3", "A", "ธรรมนูญศาล"], "LAW3105": [3, "1", "B", "วิ.แพ่ง 1"],
    "LAW3106": [3, "4", "B", "วิอาญา 1"], "LAW3133": [3, "3", "B", "อาชญากร"],
    "RAM1141": [3, "2", "A", "บุคลิกภาพ"], "LAW2104": [3, "2", "B", "รธน."],
    "LAW3102": [3, "4", "B", "หุ้นส่วน"], "LAW3103": [3, "1", "B", "ครอบครัว"],
    "LAW3110": [2, "1", "A", "ล้มละลาย"], "LAW3112": [3, "1", "B", "ปกครอง"],
    "LAW2113": [3, "2", "A", "ตั๋วเงิน"], "LAW4108": [3, "2", "B", "ที่ดิน"],
    "RAM1112": [3, "3", "B", "อิ้ง 2"], "LAW2111": [2, "3", "A", "ตัวแทน"],
    "RAM1312": [3, "4", "B", "วิชา RAM"], "LAW3117": [2, "1", "A", "ป.วิมหาชน"],
    "LAW2110": [2, "1", "B", "ค้ำ จำนำ"], "LAW3111": [3, "2", "A", "พยาน"],
    "LAW4107": [2, "2", "B", "ปรัชญา"], "RAM1213": [3, "3", "A", "วิชา RAM"],
    "LAW3109": [3, "3", "B", "มรดก"], "LAW4109": [3, "4", "A", "ทรัพย์สินทางปัญญา"],
    "LAW2112": [2, "4", "B", "ประกัน"], "LAW4156": [2, "2", "A", "อิ้งกฎหมาย"],
    "LAW4104": [2, "2", "B", "แรงงาน"], "LAW4106": [2, "3", "A", "คดีบุคคล"],
    "LAW4103": [3, "4", "A", "คดีเมือง"], "LAW4101": [2, "1", "A", "ภาษี"],
    "LAW4110": [2, "1", "A", "ค้าระหว่างประเทศ"], "LAW3138": [2, "1", "B", "เด็ก"],
    "LAW4134": [2, "1", "B", "ทะเล"], "LAW4105": [2, "2", "A", "วิชาชีพทนาย"],
    "LAW4102": [3, "2", "B", "ว่าความ"],
    "LAW1102": [2, "4", "A", "เอกชน"], "RAM1204": [3, "3", "B", "ทักษะการคิด"],
    "RAM1301": [3, "4", "B", "คุณธรรม"], "RAM1303": [3, "2", "B", "วิทยาศาสตร์"],
    "RAM1132": [3, "3", "A", "ห้องสมุด"], "LAW1101": [2, "2", "A", "มหาชน"],
    "LAW2102": [3, "3", "A", "หนี้"], "LAW2105": [3, "4", "A", "ซื้อขาย"],
    "LAW2107": [3, "1", "B", "อาญา 2"], "LAW2018": [2, "1", "A", "เช่า จ้าง"],
    "LAW2109": [3, "3", "B", "ยืม ฝาก"], "RAM1111": [3, "4", "B", "อังกฤษ 1"]
}

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}

st.set_page_config(page_title="Law GPA & Plan", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stMainBlockContainer { padding-top: 2rem !important; }
    
    /* ควบคุมกล่องวิชาในมือถือ */
    [data-testid="stExpander"] [data-testid="column"] {
        flex: 1 1 45% !important;
        min-width: 140px !important;
    }
    
    /* กล่องสรุปเกรด */
    .summary-grid { display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-start; padding: 10px 0; }
    .result-box {
        width: 100px; padding: 8px 4px; border: 2px solid #333; border-radius: 8px;
        text-align: center; background-color: #ffffff !important; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .result-box span { font-size: 11px !important; display: block; color: #333 !important; }
    .result-box b { font-size: 20px !important; display: block; color: #d32f2f !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ฟังก์ชันสนับสนุน ---
def reset_plan():
    for key in list(st.session_state.keys()):
        if key.startswith("plan_select_"):
            st.session_state.pop(key)
    st.rerun()

@st.dialog("สนับสนุนผู้พัฒนา 🙏")
def donate_dialog():
    st.write("ใช้ฟรี! หากถูกใจสามารถสนับสนุนเป็นค่าน้ำค่านมได้ที่นี่ครับ")
    # ลำดับการเช็กไฟล์ภาพ
    for ext in ["jpg", "jpeg", "png"]:
        path = f"donate.{ext}"
        if os.path.exists(path):
            st.image(path, use_container_width=True)
            return
    st.error("ไม่พบไฟล์รูปภาพ donate.jpg ใน GitHub ของคุณ")

# --- 4. หน้าจอหลัก ---
st.title("⚖️ Law GPA & Planner")

tab1, tab2 = st.tabs(["📊 คำนวณเกรด", "📅 วางแผนลงทะเบียน"])

with tab1:
    st.info("ติ๊กวิชาที่สอบผ่านแล้วเพื่อคำนวณ GPA สะสม")
    selected_gpa = []
    gpa_cols = st.columns(4)
    # แสดงรายชื่อวิชาเรียงตาม Dictionary
    for i, (code, info) in enumerate(all_courses_db.items()):
        with gpa_cols[i % 4]:
            c_row = st.columns([1.1, 1])
            if c_row[0].checkbox(f"{code}", key=f"gpa_{code}"):
                g = c_row[1].selectbox("G", list(grade_map.keys()), key=f"sel_{code}", label_visibility="collapsed")
                selected_gpa.append({"name": code, "credit": info[0], "grade": g})
    
    if selected_gpa:
        st.divider()
        total_creds = sum(d['credit'] for d in selected_gpa)
        total_points = sum(grade_map[d['grade']] * d['credit'] for d in selected_gpa)
        gpa_score = total_points / total_creds if total_creds > 0 else 0
        st.success(f"### GPA: {gpa_score:.2f} | รวม {total_creds} หน่วยกิต")
        
        # แสดงผลสรุปแบบการ์ด Grid
        sum_html = '<div class="summary-grid">'
        for d in selected_gpa:
            sum_html += f'<div class="result-box"><span>{d["name"]}</span><b>{d["grade"]}</b></div>'
        sum_html += '</div>'
        st.markdown(sum_html, unsafe_allow_html=True)

with tab2:
    st.subheader("จัดแผนการเรียน (ตรวจสอบสอบชน)")
    is_grad = st.toggle("🎓 ขอจบการศึกษา (ลงได้ 30 นก. / อนุญาตให้สอบซ้ำซ้อนได้)")
    if st.button("♻️ ล้างแผนที่เลือกไว้"): reset_plan()

    years = ["ปี 1", "ปี 2", "ปี 3", "ปี 4"]
    terms = ["ภาค 1", "ภาค 2", "ภาคฤดูร้อน (S)"]
    
    for year in years:
        with st.expander(f"📌 {year}", expanded=True):
            t_cols = st.columns(3)
            for i, term in enumerate(terms):
                t_key = f"{year}_{term}"
                with t_cols[i]:
                    st.markdown(f"**{term}**")
                    # กำหนดหน่วยกิตสูงสุดตามเงื่อนไข
                    max_c = 30 if is_grad else (9 if "ภาคฤดูร้อน" in term else 22)
                    
                    selected_subs = st.multiselect(
                        "เลือกวิชา", options=list(all_courses_db.keys()),
                        format_func=lambda x: f"{x} ({all_courses_db[x][3]})",
                        key=f"plan_select_{t_key}"
                    )
                    
                    cur_c = sum(all_courses_db[s][0] for s in selected_subs)
                    st.write(f"รวม: **{cur_c}/{max_c}** นก.")
                    
                    if cur_c > max_c: st.error(f"❌ เกิน {max_c} หน่วยกิต!")
                    
                    # ตรวจสอบสอบชน
                    days = {}
                    for s in selected_subs:
                        d_code = f"{all_courses_db[s][1]}{all_courses_db[s][2]}" # วัน+คาบ เช่น 1A
                        if d_code in days:
                            if is_grad: st.warning(f"⚠️ {s} ชนกับ {days[d_code]} (ใช้สิทธิ์ซ้ำซ้อน)")
                            else: st.error(f"❌ {s} สอบชนกับ {days[d_code]}!")
                        days[d_code] = s

# --- Footer ---
st.markdown("---")
if st.button("🧧 สนับสนุนค่าน้ำชา / โดเนท", use_container_width=True):
    donate_dialog()
