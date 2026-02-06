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

st.set_page_config(page_title="Law Easy Planner", layout="wide")

# --- 2. CSS ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .slot-card {
        background-color: #f1f5f9;
        border: 2px solid #cbd5e1;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
    }
    .slot-label { font-weight: bold; color: #1e3a8a; font-size: 15px; margin-bottom: 5px; }
    div[data-testid="stExpander"] { border: none !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Law GPA & Slot Planner")

tab1, tab2 = st.tabs(["📊 คำนวณเกรดสะสม", "📅 วางแผนลงทะเบียน (1A-4B)"])

# --- TAB 1: GPA ---
with tab1:
    st.info("ทำเครื่องหมายหน้าวิชาที่สอบผ่านแล้ว")
    # (ส่วนคำนวณเกรดคงเดิมเพื่อความต่อเนื่อง)
    
# --- TAB 2: Slot Planning (เพิ่มฟังก์ชันลบ) ---
with tab2:
    c1, c2, c3 = st.columns([1,1,1])
    y = c1.selectbox("ปีการศึกษา", [1,2,3,4], key="y")
    t = c2.selectbox("เทอม", ["1", "2", "S"], key="t")
    grad = c3.toggle("🎓 ขอจบ (ลงซ้ำซ้อนได้)", key="grad")

    st.divider()
    
    term_key = f"Y{y}T{t}"
    slots = ["1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B"]
    total_c = 0
    selected_list = []

    # แสดงผล 8 สล็อต
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
            
            # ดึงค่าเดิมจาก Session State (ถ้ามี) เพื่อให้ปุ่มลบทำงานได้
            ss_key = f"val_{term_key}_{slot_name}"
            if ss_key not in st.session_state:
                st.session_state[ss_key] = "-"

            # ช่องเลือกวิชา
            choice = st.selectbox(
                f"S_{slot_name}", 
                options=valid_courses, 
                index=valid_courses.index(st.session_state[ss_key]) if st.session_state[ss_key] in valid_courses else 0,
                key=f"select_{term_key}_{slot_name}",
                label_visibility="collapsed"
            )
            
            # อัปเดต Session State เมื่อมีการเลือก
            st.session_state[ss_key] = choice

            if choice != "-":
                code = choice.split(" | ")[0]
                total_c += all_courses_db[code][0]
                selected_list.append(f"{code} ({all_courses_db[code][3]})")
                
                # --- ปุ่มลบ (Clear) ---
                if st.button(f"🗑️ ลบ {slot_name}", key=f"clear_{term_key}_{slot_name}"):
                    st.session_state[ss_key] = "-"
                    st.rerun()
            else:
                st.caption("ว่าง")

    st.divider()
    limit = 30 if grad else (9 if t == "S" else 22)
    
    col_res1, col_res2 = st.columns([1, 2])
    with col_res1:
        st.metric("หน่วยกิตรวม", f"{total_c} / {limit}")
        if total_c > limit:
            st.error("⚠️ หน่วยกิตเกินกำหนด!")
        elif total_c > 0:
            st.success("✅ ตารางสอบเรียบร้อย")

    with col_res2:
        st.write("**วิชาที่เลือกไว้:**")
        if selected_list:
            for s in selected_list: st.text(f"• {s}")
        else:
            st.write("- ยังไม่ได้เลือกวิชา -")

    if st.button("♻️ ล้างสล็อตทั้งหมดในเทอมนี้", use_container_width=True):
        for s in slots:
            st.session_state[f"val_{term_key}_{s}"] = "-"
        st.rerun()
