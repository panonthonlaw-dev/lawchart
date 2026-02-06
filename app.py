import streamlit as st
import os

# --- 1. ข้อมูลวิชา (Database กลาง) ---
all_courses_db = {
    "RAM1101": [3, "4", "A", "ภาษาไทย", "RAM"], "RAM1111": [3, "4", "B", "อังกฤษ 1", "RAM"],
    "RAM1112": [3, "3", "B", "อังกฤษ 2", "RAM"], "RAM1132": [3, "3", "A", "การใช้ห้องสมุด", "RAM"],
    "RAM1141": [3, "2", "A", "บุคลิกภาพ", "RAM"], "RAM1204": [3, "3", "B", "ทักษะการคิด", "RAM"],
    "RAM1213": [3, "3", "A", "วิชา RAM", "RAM"], "RAM1301": [3, "4", "B", "คุณธรรม", "RAM"],
    "RAM1303": [3, "2", "B", "วิทยาศาสตร์", "RAM"], "RAM1312": [3, "4", "B", "วิชา RAM", "RAM"],
    "LAW1101": [2, "2", "A", "กฎหมายมหาชน", "LAW"], "LAW1102": [2, "4", "A", "กฎหมายเอกชน", "LAW"],
    "LAW1103": [3, "2", "A", "นิติกรรม", "LAW"], "LAW2101": [3, "2", "B", "ทรัพย์", "LAW"],
    "LAW2102": [3, "3", "A", "หนี้", "LAW"], "LAW2104": [3, "2", "B", "รัฐธรรมนูญ", "LAW"],
    "LAW2105": [3, "4", "A", "ซื้อขาย", "LAW"], "LAW2106": [3, "4", "A", "อาญา 1", "LAW"],
    "LAW2107": [3, "1", "B", "อาญา 2", "LAW"], "LAW2109": [3, "3", "B", "ยืม ฝาก", "LAW"],
    "LAW2110": [2, "1", "B", "ค้ำ จำนำ", "LAW"], "LAW2111": [2, "3", "A", "ตัวแทน", "LAW"],
    "LAW2112": [2, "4", "B", "ประกัน", "LAW"], "LAW2113": [3, "2", "A", "ตั๋วเงิน", "LAW"],
    "LAW2108": [2, "1", "A", "เช่า จ้าง", "LAW"], "LAW3101": [2, "1", "A", "อาญา 3", "LAW"],
    "LAW3102": [3, "4", "B", "หุ้นส่วน", "LAW"], "LAW3103": [3, "1", "B", "ครอบครัว", "LAW"],
    "LAW3104": [2, "3", "A", "ธรรมนูญศาล", "LAW"], "LAW3105": [3, "1", "B", "วิ.แพ่ง 1", "LAW"],
    "LAW3106": [3, "4", "B", "วิอาญา 1", "LAW"], "LAW3109": [3, "3", "B", "มรดก", "LAW"],
    "LAW3110": [2, "1", "A", "ล้มละลาย", "LAW"], "LAW3111": [3, "2", "A", "พยาน", "LAW"],
    "LAW3112": [3, "1", "B", "กฎหมายปกครอง", "LAW"], "LAW3117": [2, "1", "A", "ป.วิมหาชน", "LAW"],
    "LAW4101": [2, "1", "A", "ภาษี", "LAW"], "LAW4102": [3, "2", "B", "ว่าความ", "LAW"],
    "LAW4103": [3, "4", "A", "คดีเมือง", "LAW"], "LAW4104": [2, "2", "B", "แรงงาน", "LAW"],
    "LAW4105": [2, "2", "A", "วิชาชีพทนาย", "LAW"], "LAW4106": [2, "3", "A", "สิทธิมนุษยชน", "LAW"],
    "LAW4107": [2, "2", "B", "ปรัชญา", "LAW"], "LAW4108": [3, "2", "B", "ที่ดิน", "LAW"],
    "LAW4109": [3, "4", "A", "ทรัพย์สินทางปัญญา", "LAW"], "LAW4110": [2, "1", "A", "ค้าระหว่างประเทศ", "LAW"],
    "LAW3133": [3, "3", "B", "อาชญากร", "ELECTIVE"], "LAW3138": [2, "1", "B", "เด็ก", "ELECTIVE"],
    "LAW4134": [2, "1", "B", "ทะเล", "ELECTIVE"], "LAW4156": [2, "2", "A", "อิ้งกฎหมาย", "ELECTIVE"]
}

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}

st.set_page_config(page_title="Law GPA & Planner Pro", layout="wide")

# --- 2. Initialize Session State (สำหรับปุ่มลบ) ---
if "reset_counters" not in st.session_state:
    st.session_state.reset_counters = {s: 0 for s in ["1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B"]}

# --- 3. CSS ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .slot-label { font-weight: bold; color: #1e3a8a; font-size: 15px; margin-bottom: 5px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 30px; font-size: 12px; padding: 0; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Law GPA & Planning System")

tab1, tab2 = st.tabs(["📊 คำนวณเกรดสะสม", "📅 วางแผน (แยกตามคาบสอบ)"])

# --- TAB 1: คำนวณเกรด (GPA) ---
with tab1:
    st.info("ติ๊กวิชาที่สอบผ่านแล้วเพื่อคำนวณ GPA")
    selected_gpa = []
    cats = {"📂 หมวด RAM": "RAM", "📂 หมวด LAW": "LAW", "📂 หมวดวิชาเลือก": "ELECTIVE"}
    
    for label, cp in cats.items():
        with st.expander(label, expanded=(cp == "LAW")):
            cat_courses = {k: v for k, v in all_courses_db.items() if v[4] == cp}
            gpa_cols = st.columns(4)
            for idx, (code, info) in enumerate(cat_courses.items()):
                with gpa_cols[idx % 4]:
                    r = st.columns([1.2, 1])
                    if r[0].checkbox(code, key=f"gpa_chk_{code}"):
                        g = r[1].selectbox("G", list(grade_map.keys()), key=f"gpa_sel_{code}", label_visibility="collapsed")
                        selected_gpa.append({"credit": info[0], "grade": g})
    
    if selected_gpa:
        st.divider()
        total_creds = sum(d['credit'] for d in selected_gpa)
        total_pts = sum(grade_map[d['grade']] * d['credit'] for d in selected_gpa)
        gpa_score = total_pts / total_creds if total_creds > 0 else 0
        st.success(f"### GPA สะสม: {gpa_score:.2f} | รวม {total_creds} หน่วยกิต")

# --- TAB 2: วางแผนลงทะเบียน (ล็อกคาบสอบ) ---
with tab2:
    col1, col2, col3 = st.columns(3)
    y = col1.selectbox("ปีการศึกษา", [1, 2, 3, 4])
    t = col2.selectbox("เทอม", ["1", "2", "S"])
    grad = col3.toggle("🎓 ขอจบ (ลงซ้ำซ้อนได้)")

    st.divider()
    slots = ["1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B"]
    total_c = 0
    selected_plan = []

    rows = st.columns(4)
    for i, slot_name in enumerate(slots):
        with rows[i % 4]:
            st.markdown(f"<div class='slot-label'>📌 คาบ {slot_name}</div>", unsafe_allow_html=True)
            
            # กรองวิชาตามคาบสอบ
            day, period = slot_name[0], slot_name[1]
            valid_list = ["-"] + [
                f"{code} | {info[3]}" for code, info in all_courses_db.items() 
                if info[1] == day and info[2] == period
            ]
            
            # ใช้ Dynamic Key เพื่อให้ปุ่มลบทำงานได้จริง
            current_key = f"plan_{y}_{t}_{slot_name}_v{st.session_state.reset_counters[slot_name]}"
            
            choice = st.selectbox("วิชา", options=valid_list, key=current_key, label_visibility="collapsed")

            if choice != "-":
                code = choice.split(" | ")[0]
                total_c += all_courses_db[code][0]
                selected_plan.append(f"{code} - {all_courses_db[code][3]}")
                
                # ปุ่มลบรายสล็อต
                if st.button(f"🗑️ ลบ {slot_name}", key=f"del_btn_{slot_name}"):
                    st.session_state.reset_counters[slot_name] += 1
                    st.rerun()
            else:
                st.caption("ว่าง")

    st.divider()
    limit = 30 if grad else (9 if t == "S" else 22)
    st.metric("หน่วยกิตรวมเทอมนี้", f"{total_c} / {limit}")
    
    if total_c > limit:
        st.error("⚠️ หน่วยกิตเกินกำหนด!")
    
    if selected_plan:
        st.write("**วิชาที่เลือก:**")
        for item in selected_plan: st.text(f"• {item}")

    if st.button("♻️ ล้างแผนทั้งหมดของเทอมนี้"):
        for s in slots: st.session_state.reset_counters[s] += 1
        st.rerun()

st.markdown("---")
if st.button("🧧 โดเนทสนับสนุน"):
    for ext in ["jpg", "jpeg", "png"]:
        if os.path.exists(f"donate.{ext}"):
            st.image(f"donate.{ext}", use_container_width=True)
