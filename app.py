import streamlit as st
import os

# --- 1. ข้อมูลวิชา (Database กลาง - ล็อกคาบสอบไว้ที่นี่) ---
all_courses_db = {
    # หมวด RAM
    "RAM1101": [3, "4", "A", "ภาษาไทย", "RAM"], "RAM1111": [3, "4", "B", "อังกฤษ 1", "RAM"],
    "RAM1112": [3, "3", "B", "อังกฤษ 2", "RAM"], "RAM1132": [3, "3", "A", "การใช้ห้องสมุด", "RAM"],
    "RAM1141": [3, "2", "A", "บุคลิกภาพ", "RAM"], "RAM1204": [3, "3", "B", "ทักษะการคิด", "RAM"],
    "RAM1213": [3, "3", "A", "วิชา RAM", "RAM"], "RAM1301": [3, "4", "B", "คุณธรรม", "RAM"],
    "RAM1303": [3, "2", "B", "วิทยาศาสตร์", "RAM"], "RAM1312": [3, "4", "B", "วิชา RAM", "RAM"],
    # หมวด LAW (รหัสผ่านการตรวจสอบแล้ว)
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
    # หมวดเลือก
    "LAW3133": [3, "3", "B", "อาชญากร", "ELECTIVE"], "LAW3138": [2, "1", "B", "เด็ก", "ELECTIVE"],
    "LAW4134": [2, "1", "B", "ทะเล", "ELECTIVE"], "LAW4156": [2, "2", "A", "อิ้งกฎหมาย", "ELECTIVE"],
    "วิชาเลือก 1": [3, "0", "0", "เลือกเสรี 1", "ELECTIVE"], "วิชาเลือก 2": [3, "0", "0", "เลือกเสรี 2", "ELECTIVE"]
}

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}

st.set_page_config(page_title="Safe Law Planner", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .exam-badge {
        background-color: #e3f2fd;
        color: #0d47a1;
        padding: 2px 8px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 14px;
        border: 1px solid #bbdefb;
    }
    .slot-box {
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 8px;
        background-color: #ffffff;
        min-height: 120px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Law GPA & Safe Planning")

tab1, tab2 = st.tabs(["📊 คำนวณเกรด", "📅 วางแผนลงทะเบียน (ล็อกคาบสอบ)"])

# --- TAB 1: คำนวณเกรด ---
with tab1:
    st.info("ติ๊กวิชาที่ผ่านแล้วเพื่อดู GPA สะสม")
    selected_gpa = []
    cats = {"หมวด RAM": "RAM", "หมวด LAW": "LAW", "หมวดเลือก": "ELECTIVE"}
    for label, cp in cats.items():
        with st.expander(label, expanded=(cp == "LAW")):
            cat_courses = {k: v for k, v in all_courses_db.items() if v[4] == cp}
            cols = st.columns(4)
            for idx, (code, info) in enumerate(cat_courses.items()):
                with cols[idx % 4]:
                    r = st.columns([1.2, 1])
                    if r[0].checkbox(code, key=f"g_{code}"):
                        g = r[1].selectbox("G", list(grade_map.keys()), key=f"s_{code}", label_visibility="collapsed")
                        selected_gpa.append({"credit": info[0], "grade": g})
    if selected_gpa:
        total_creds = sum(d['credit'] for d in selected_gpa)
        total_pts = sum(grade_map[d['grade']] * d['credit'] for d in selected_gpa)
        st.success(f"GPA: {total_pts/total_creds:.2f} | รวม {total_creds} นก.")

# --- TAB 2: วางแผนลงทะเบียน (ล็อกคาบสอบ) ---
with tab2:
    c_y, c_t, c_g = st.columns([1, 1, 1])
    y_sel = c_y.selectbox("ปีการศึกษา", [1, 2, 3, 4])
    t_sel = c_t.selectbox("เทอม", ["1", "2", "S"])
    is_grad = c_g.toggle("🎓 ขอจบการศึกษา (อนุญาตให้สอบซ้ำซ้อน)")

    st.divider()
    st.subheader(f"📍 ตารางจัดแผน: ปี {y_sel} เทอม {t_sel}")

    term_id = f"Y{y_sel}T{t_sel}"
    total_credits = 0
    exam_conflicts = []
    used_exams = {}
    options = ["-"] + sorted(list(all_courses_db.keys()))

    # แสดงผล 8 สล็อต
    rows = st.columns(4)
    for i in range(1, 9):
        with rows[(i-1) % 4]:
            st.markdown(f"**อันดับที่ {i}**")
            sub = st.selectbox("เลือกวิชา", options, key=f"slot_{term_id}_{i}")
            
            if sub != "-":
                info = all_courses_db[sub]
                total_credits += info[0]
                
                # แสดงคาบสอบแบบล็อก (ห้ามแก้)
                exam_code = f"{info[1]}{info[2]}" if info[1] != "0" else "ไม่มีสอบ"
                st.markdown(f"คาบสอบ: <span class='exam-badge'>{exam_code}</span>", unsafe_allow_html=True)
                st.caption(f"{info[3]} ({info[0]} นก.)")
                
                # เช็กสอบชน
                if exam_code != "ไม่มีสอบ":
                    if exam_code in used_exams:
                        exam_conflicts.append(f"{sub} ชนกับ {used_exams[exam_code]} ({exam_code})")
                    used_exams[exam_code] = sub
            else:
                st.write("---") # ช่องว่าง

    st.divider()
    limit = 30 if is_grad else (9 if t_sel == "S" else 22)
    st.metric("หน่วยกิตรวม", f"{total_credits} / {limit}")

    if exam_conflicts:
        if is_grad:
            st.warning("⚠️ พบวิชาสอบชนกัน (ใช้สิทธิ์สอบซ้ำซ้อนได้)")
            for c in exam_conflicts: st.write(f"- {c}")
        else:
            st.error("❌ สอบชนกัน! ระบบไม่อนุญาตให้ลงทะเบียน")
            for c in exam_conflicts: st.write(f"- {c}")
    elif total_credits > 0:
        st.success("✅ ตารางสอบสมบูรณ์ ไม่มีการสอบซ้ำซ้อน")

st.markdown("---")
if st.button("🧧 โดเนทสนับสนุน"):
    for ext in ["jpg", "jpeg", "png"]:
        if os.path.exists(f"donate.{ext}"):
            st.image(f"donate.{ext}", use_container_width=True)
