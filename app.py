import streamlit as st
import os

# --- 1. ข้อมูลวิชา (Database กลาง) ---
all_courses_db = {
    # รหัสวิชา: [หน่วยกิต, "วันสอบ", "คาบ", "ชื่อวิชา", "หมวดหมู่"]
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

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}

st.set_page_config(page_title="Law Exam Slot Planner", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .slot-label {
        background-color: #1e3a8a;
        color: white;
        padding: 5px;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
        font-size: 14px;
    }
    .stSelectbox label { display: none; }
    .summary-box {
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 8px;
        background-color: #f8fafc;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Law GPA & Exam Planner")

tab1, tab2 = st.tabs(["📊 คำนวณเกรด", "📅 วางแผน (ล็อกคาบสอบ)"])

# --- TAB 1: GPA ---
with tab1:
    st.info("คำนวณผลการเรียนสะสม")
    selected_gpa = []
    for label, cp in {"RAM": "RAM", "LAW": "LAW", "Elective": "ELECTIVE"}.items():
        with st.expander(f"📂 {label}", expanded=(cp=="LAW")):
            cat_courses = {k: v for k, v in all_courses_db.items() if v[4] == cp}
            cols = st.columns(4)
            for idx, (code, info) in enumerate(cat_courses.items()):
                with cols[idx % 4]:
                    r = st.columns([1.2, 1])
                    if r[0].checkbox(code, key=f"gpa_c_{code}"):
                        g = r[1].selectbox("G", list(grade_map.keys()), key=f"gpa_s_{code}", label_visibility="collapsed")
                        selected_gpa.append({"credit": info[0], "grade": g})
    if selected_gpa:
        total_creds = sum(d['credit'] for d in selected_gpa)
        total_pts = sum(grade_map[d['grade']] * d['credit'] for d in selected_gpa)
        st.success(f"GPA: {total_pts/total_creds:.2f} | รวม {total_creds} นก.")

# --- TAB 2: Slot Planning ---
with tab2:
    st.subheader("จัดตารางเรียนแยกตามคาบสอบ (1A - 4B)")
    col_y, col_t, col_g = st.columns([1, 1, 1])
    y_sel = col_y.selectbox("ปีการศึกษา", [1, 2, 3, 4], key="sel_y")
    t_sel = col_t.selectbox("เทอม", ["1", "2", "S"], key="sel_t")
    is_grad = col_g.toggle("🎓 ขอจบ (ลงซ้ำซ้อนได้)", key="is_grad")

    st.divider()
    
    # กำหนด Key ของเทอมปัจจุบัน
    term_key = f"Y{y_sel}T{t_sel}"
    slots = ["1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B"]
    total_credits = 0
    final_subjects = []

    # แสดงผลสล็อต 4 คอลัมน์
    rows = st.columns(4)
    
    for i, slot_name in enumerate(slots):
        with rows[i % 4]:
            st.markdown(f"<div class='slot-label'>คาบสอบ {slot_name}</div>", unsafe_allow_html=True)
            
            # กรองวิชาที่สอบตรงคาบนี้
            day = slot_name[0]   # "1", "2"
            period = slot_name[1] # "A", "B"
            
            valid_courses = ["-"] + [
                f"{code} | {info[3]}" for code, info in all_courses_db.items() 
                if info[1] == day and info[2] == period
            ]
            
            # แก้ไข NameError โดยใช้ term_key ที่ประกาศไว้ด้านบน
            user_choice = st.selectbox(
                f"Select {slot_name}", 
                options=valid_courses, 
                key=f"slot_select_{term_key}_{slot_name}"
            )
            
            if user_choice != "-":
                code = user_choice.split(" | ")[0]
                total_credits += all_courses_db[code][0]
                final_subjects.append(f"{code} ({all_courses_db[code][3]})")
                st.caption(f"✅ {all_courses_db[code][0]} นก.")

    st.divider()
    
    # สรุปผลด้านล่าง
    c1, c2 = st.columns([1, 2])
    with c1:
        limit = 30 if is_grad else (9 if t_sel == "S" else 22)
        st.metric("หน่วยกิตรวม", f"{total_credits} / {limit}")
        if total_credits > limit:
            st.error("เกินกำหนด!")
            
    with c2:
        st.markdown("**วิชาที่ลงทะเบียนในเทอมนี้:**")
        if final_subjects:
            for s in final_subjects:
                st.write(f"- {s}")
        else:
            st.write("ยังไม่ได้เลือกวิชา")

st.markdown("---")
if st.button("🧧 โดเนทสนับสนุน"):
    for ext in ["jpg", "jpeg", "png"]:
        if os.path.exists(f"donate.{ext}"):
            st.image(f"donate.{ext}", use_container_width=True)
