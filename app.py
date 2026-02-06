import streamlit as st
from fpdf import FPDF
import os
from io import BytesIO

# --- 1. ข้อมูลวิชาและตารางสอบ (Database) ---
# "รหัสวิชา": [หน่วยกิต, "วันสอบ", "คาบ", "ชื่อวิชา", "หมวดหมู่"]
all_courses_db = {
    # หมวด RAM
    "RAM1101": [3, "4", "A", "ไทย", "RAM"], "RAM1111": [3, "4", "B", "อังกฤษ 1", "RAM"],
    "RAM1112": [3, "3", "B", "อังกฤษ 2", "RAM"], "RAM1132": [3, "3", "A", "ห้องสมุด", "RAM"],
    "RAM1141": [3, "2", "A", "บุคลิกภาพ", "RAM"], "RAM1204": [3, "3", "B", "ทักษะการคิด", "RAM"],
    "RAM1213": [3, "3", "A", "วิชา RAM", "RAM"], "RAM1301": [3, "4", "B", "คุณธรรม", "RAM"],
    "RAM1303": [3, "2", "B", "วิทยาศาสตร์", "RAM"], "RAM1312": [3, "4", "B", "วิชา RAM", "RAM"],
    # หมวด LAW (พื้นฐาน & แกน)
    "LAW1101": [2, "2", "A", "มหาชน", "LAW"], "LAW1102": [2, "4", "A", "เอกชน", "LAW"],
    "LAW1103": [3, "2", "A", "นิติกรรม", "LAW"], "LAW2101": [3, "2", "B", "ทรัพย์", "LAW"],
    "LAW2102": [3, "3", "A", "หนี้", "LAW"], "LAW2104": [3, "2", "B", "รธน.", "LAW"],
    "LAW2105": [3, "4", "A", "ซื้อขาย", "LAW"], "LAW2106": [3, "4", "A", "อาญา 1", "LAW"],
    "LAW2107": [3, "1", "B", "อาญา 2", "LAW"], "LAW2109": [3, "3", "B", "ยืม ฝาก", "LAW"],
    "LAW2110": [2, "1", "B", "ค้ำ จำนำ", "LAW"], "LAW2111": [2, "3", "A", "ตัวแทน", "LAW"],
    "LAW2112": [2, "4", "B", "ประกัน", "LAW"], "LAW2113": [3, "2", "A", "ตั๋วเงิน", "LAW"],
    "LAW2108": [2, "1", "A", "เช่า จ้าง", "LAW"], # แก้ไขรหัสจาก 2018 เป็น 2108
    "LAW3101": [2, "1", "A", "อาญา 3", "LAW"], "LAW3102": [3, "4", "B", "หุ้นส่วน", "LAW"],
    "LAW3103": [3, "1", "B", "ครอบครัว", "LAW"], "LAW3104": [2, "3", "A", "ธรรมนูญศาล", "LAW"],
    "LAW3105": [3, "1", "B", "วิ.แพ่ง 1", "LAW"], "LAW3106": [3, "4", "B", "วิอาญา 1", "LAW"],
    "LAW3109": [3, "3", "B", "มรดก", "LAW"], "LAW3110": [2, "1", "A", "ล้มละลาย", "LAW"],
    "LAW3111": [3, "2", "A", "พยาน", "LAW"], "LAW3112": [3, "1", "B", "ปกครอง", "LAW"],
    "LAW3117": [2, "1", "A", "ป.วิมหาชน", "LAW"], 
    "LAW4101": [2, "1", "A", "ภาษี", "LAW"], "LAW4102": [3, "2", "B", "ว่าความ", "LAW"],
    "LAW4103": [3, "4", "A", "คดีเมือง", "LAW"], "LAW4104": [2, "2", "B", "แรงงาน", "LAW"],
    "LAW4105": [2, "2", "A", "วิชาชีพทนาย", "LAW"], "LAW4106": [2, "3", "A", "คดีบุคคล", "LAW"],
    "LAW4107": [2, "2", "B", "ปรัชญา", "LAW"], "LAW4108": [3, "2", "B", "ที่ดิน", "LAW"],
    "LAW4109": [3, "4", "A", "ทรัพย์สินทางปัญญา", "LAW"], "LAW4110": [2, "1", "A", "ค้าระหว่างประเทศ", "LAW"],
    # หมวดวิชาเลือก (Elective)
    "LAW3133": [3, "3", "B", "อาชญากร", "ELECTIVE"],
    "LAW3138": [2, "1", "B", "เด็ก", "ELECTIVE"],
    "LAW4134": [2, "1", "B", "ทะเล", "ELECTIVE"],
    "LAW4156": [2, "2", "A", "อิ้งกฎหมาย", "ELECTIVE"],
    "วิชาเลือก 1": [3, "0", "0", "เลือกเสรี 1", "ELECTIVE"],
    "วิชาเลือก 2": [3, "0", "0", "เลือกเสรี 2", "ELECTIVE"]
}

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}

st.set_page_config(page_title="GPA Law Pro", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stMainBlockContainer { padding-top: 1.5rem !important; }
    [data-testid="stExpander"] [data-testid="column"] { flex: 1 1 45% !important; min-width: 140px !important; }
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
        if key.startswith("plan_select_"): st.session_state.pop(key)
    st.rerun()

@st.dialog("สนับสนุนผู้พัฒนา 🙏")
def donate_dialog():
    st.write("ใช้ฟรี! หากถูกใจสนับสนุนค่าน้ำชาได้ที่นี่ครับ")
    for ext in ["jpg", "jpeg", "png"]:
        path = f"donate.{ext}"
        if os.path.exists(path):
            st.image(path, use_container_width=True)
            return
    st.error("ไม่พบไฟล์รูปภาพ donate.jpg")

# --- 4. หน้าจอหลัก ---
st.title("⚖️ Law GPA & Planning")

tab1, tab2 = st.tabs(["📊 คำนวณเกรด", "📅 วางแผนลงทะเบียน"])

with tab1:
    st.info("เปิดหมวดหมู่เพื่อเลือกวิชาที่สอบผ่านแล้ว")
    selected_gpa = []
    cats = {"📂 หมวด RAM": "RAM", "📂 หมวด LAW": "LAW", "📂 หมวดวิชาเลือก": "ELECTIVE"}
    
    for label, code_prefix in cats.items():
        with st.expander(label, expanded=(code_prefix == "LAW")):
            cat_courses = {k: v for k, v in all_courses_db.items() if v[4] == code_prefix}
            gpa_cols = st.columns(4)
            for idx, (code, info) in enumerate(cat_courses.items()):
                with gpa_cols[idx % 4]:
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
        
        sum_html = '<div class="summary-grid">'
        for d in selected_gpa:
            sum_html += f'<div class="result-box"><span>{d["name"]}</span><b>{d["grade"]}</b></div>'
        sum_html += '</div>'
        st.markdown(sum_html, unsafe_allow_html=True)

with tab2:
    st.subheader("จัดแผนการเรียน (กันลงซ้ำและสอบชน)")
    is_grad = st.toggle("🎓 ขอจบการศึกษา (ลงได้ 30 นก. / สอบซ้ำซ้อนได้)")
    if st.button("♻️ ล้างแผนทั้งหมด"): reset_plan()

    years = ["ปี 1", "ปี 2", "ปี 3", "ปี 4"]
    terms_list = ["ภาค 1", "ภาค 2", "ภาคฤดูร้อน (S)"]
    
    # รวบรวมวิชาที่เลือกไปแล้วเพื่อใช้กรองออก
    used_subjects = []
    for y in years:
        for t in terms_list:
            key = f"plan_select_{y}_{t}"
            if key in st.session_state:
                used_subjects.extend(st.session_state[key])

    for year in years:
        with st.expander(f"📌 {year}", expanded=True):
            t_cols = st.columns(3)
            for i, term in enumerate(terms_list):
                t_key = f"plan_select_{year}_{term}"
                with t_cols[i]:
                    st.markdown(f"**{term}**")
                    
                    # กรองวิชาไม่ให้ซ้ำเทอมอื่น
                    current_term_selected = st.session_state.get(t_key, [])
                    available_options = [
                        code for code in all_courses_db.keys() 
                        if code not in used_subjects or code in current_term_selected
                    ]

                    def format_func(code):
                        info = all_courses_db[code]
                        exam = f"{info[1]}{info[2]}" if info[1] != "0" else "ไม่มีสอบ"
                        return f"{code} | {info[3]} (สอบ: {exam})"

                    selected_subs = st.multiselect(
                        "เลือกวิชา", 
                        options=available_options,
                        format_func=format_func,
                        key=t_key
                    )
                    
                    max_c = 30 if is_grad else (9 if "S" in term else 22)
                    cur_c = sum(all_courses_db[s][0] for s in selected_subs)
                    st.write(f"รวม: **{cur_c}/{max_c}** นก.")
                    
                    if cur_c > max_c: st.error("เกินหน่วยกิต!")
                    
                    days = {}
                    for s in selected_subs:
                        info = all_courses_db[s]
                        d_code = f"{info[1]}{info[2]}"
                        if d_code != "00" and d_code in days:
                            if is_grad: st.warning(f"⚠️ {s} ชน {days[d_code]}")
                            else: st.error(f"❌ {s} ชน {days[d_code]}!")
                        days[d_code] = s

st.markdown("---")
if st.button("🧧 สนับสนุนค่าน้ำชา / โดเนท", use_container_width=True):
    donate_dialog()
