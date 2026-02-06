import streamlit as st
import os

# --- 1. ข้อมูลวิชา (Database กลาง) ---
all_courses_db = {
    "RAM1101": [3, "4", "A", "ภาษาไทย", "RAM"], "RAM1111": [3, "4", "B", "อังกฤษ 1", "RAM"],
    "RAM1112": [3, "3", "B", "อังกฤษ 2", "RAM"], "RAM1132": [3, "3", "A", "การใช้ห้องสมุด", "RAM"],
    "RAM1141": [3, "2", "A", "สุขภาพและบุคลิกภาพ", "RAM"], "RAM1204": [3, "3", "B", "ทักษะการคิด", "RAM"],
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

st.set_page_config(page_title="Law Planner Pro", layout="wide")

# --- 2. Initialize Session State ---
# ใช้สำหรับเก็บ "รุ่น" ของ Widget (เพื่อใช้ Reset)
if "reset_counters" not in st.session_state:
    st.session_state.reset_counters = {s: 0 for s in ["1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B"]}

# --- 3. CSS ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .slot-label { font-weight: bold; color: #1e3a8a; font-size: 15px; margin-bottom: 5px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 30px; padding: 0px; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Law GPA & Slot Planner")

tab1, tab2 = st.tabs(["📊 คำนวณเกรด", "📅 วางแผนลงทะเบียน (1A-4B)"])

# --- TAB 1: GPA ---
with tab1:
    st.info("ส่วนคำนวณเกรดสะสม")
    # (ใส่ Logic GPA เดิมที่นี่)

# --- TAB 2: Slot Planning (Fixed Delete) ---
with tab2:
    c1, c2, c3 = st.columns([1,1,1])
    y = c1.selectbox("ปีการศึกษา", [1,2,3,4])
    t = c2.selectbox("เทอม", ["1", "2", "S"])
    grad = c3.toggle("🎓 ขอจบ (ลงซ้ำซ้อนได้)")

    st.divider()
    
    slots = ["1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B"]
    total_c = 0
    selected_list = []

    rows = st.columns(4)
    for i, slot_name in enumerate(slots):
        with rows[i % 4]:
            st.markdown(f"<div class='slot-label'>📌 คาบ {slot_name}</div>", unsafe_allow_html=True)
            
            # กรองวิชาตามคาบสอบ
            day, period = slot_name[0], slot_name[1]
            valid_courses = ["-"] + [
                f"{code} | {info[3]}" for code, info in all_courses_db.items() 
                if info[1] == day and info[2] == period
            ]
            
            # ใช้ Key แบบ Dynamic ที่เปลี่ยนค่าได้เมื่อกดลบ
            # key = f"Y{y}T{t}_{slot_name}_rev{st.session_state.reset_counters[slot_name]}"
            current_key = f"select_{y}_{t}_{slot_name}_{st.session_state.reset_counters[slot_name]}"
            
            choice = st.selectbox(
                "วิชา",
                options=valid_courses,
                key=current_key,
                label_visibility="collapsed"
            )

            if choice != "-":
                code = choice.split(" | ")[0]
                total_c += all_courses_db[code][0]
                selected_list.append(f"{code} ({all_courses_db[code][3]})")
                
                # ปุ่มลบ: เมื่อกดจะบวกเลข Counter เพื่อเปลี่ยน Key ของ Selectbox ด้านบน
                if st.button(f"ลบ {slot_name}", key=f"btn_del_{slot_name}"):
                    st.session_state.reset_counters[slot_name] += 1
                    st.rerun()
            else:
                st.caption("ว่าง")

    st.divider()
    limit = 30 if grad else (9 if t == "S" else 22)
    
    st.metric("หน่วยกิตรวมเทอมนี้", f"{total_c} / {limit}")
    if total_c > limit:
        st.error("⚠️ หน่วยกิตเกิน!")
    
    if selected_list:
        st.write("**วิชาที่เลือก:**")
        for s in selected_list: st.text(f"• {s}")

    if st.button("♻️ ล้างแผนทั้งหมดของเทอมนี้"):
        for s in slots:
            st.session_state.reset_counters[s] += 1
        st.rerun()
