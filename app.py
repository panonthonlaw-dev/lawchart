import streamlit as st
import os

# --- 1. ข้อมูลวิชาและตารางสอบ (Database) ---
# โครงสร้าง: "รหัสวิชา": [หน่วยกิต, "วันสอบ", "คาบ", "ชื่อวิชา", "หมวดหมู่"]
all_courses_db = {
    # หมวด RAM
    "RAM1101": [3, "4", "A", "Thai", "RAM"], "RAM1111": [3, "4", "B", "Eng 1", "RAM"],
    "RAM1112": [3, "3", "B", "Eng 2", "RAM"], "RAM1132": [3, "3", "A", "Library", "RAM"],
    "RAM1141": [3, "2", "A", "Personality", "RAM"], "RAM1204": [3, "3", "B", "Thinking", "RAM"],
    "RAM1213": [3, "3", "A", "RAM Subject", "RAM"], "RAM1301": [3, "4", "B", "Morality", "RAM"],
    "RAM1303": [3, "2", "B", "Science", "RAM"], "RAM1312": [3, "4", "B", "RAM Subject", "RAM"],
    # หมวด LAW
    "LAW1101": [2, "2", "A", "Public Law", "LAW"], "LAW1102": [2, "4", "A", "Private Law", "LAW"],
    "LAW1103": [3, "2", "A", "Juristic Acts", "LAW"], "LAW2101": [3, "2", "B", "Property", "LAW"],
    "LAW2102": [3, "3", "A", "Obligations", "LAW"], "LAW2104": [3, "2", "B", "Constitutional", "LAW"],
    "LAW2105": [3, "4", "A", "Sale", "LAW"], "LAW2106": [3, "4", "A", "Criminal 1", "LAW"],
    "LAW2107": [3, "1", "B", "Criminal 2", "LAW"], "LAW2109": [3, "3", "B", "Loan", "LAW"],
    "LAW2110": [2, "1", "B", "Suretyship", "LAW"], "LAW2111": [2, "3", "A", "Agency", "LAW"],
    "LAW2112": [2, "4", "B", "Insurance", "LAW"], "LAW2113": [3, "2", "A", "Bills of Exchange", "LAW"],
    "LAW2108": [2, "1", "A", "Hire of Property", "LAW"], "LAW3101": [2, "1", "A", "Criminal 3", "LAW"],
    "LAW3102": [3, "4", "B", "Partnership", "LAW"], "LAW3103": [3, "1", "B", "Family", "LAW"],
    "LAW3104": [2, "3", "A", "Court Organization", "LAW"], "LAW3105": [3, "1", "B", "Civil Pro 1", "LAW"],
    "LAW3106": [3, "4", "B", "Crim Pro 1", "LAW"], "LAW3109": [3, "3", "B", "Succession", "LAW"],
    "LAW3110": [2, "1", "A", "Bankruptcy", "LAW"], "LAW3111": [3, "2", "A", "Evidence", "LAW"],
    "LAW3112": [3, "1", "B", "Administrative", "LAW"], "LAW3117": [2, "1", "A", "Public Pro", "LAW"],
    "LAW4101": [2, "1", "A", "Tax", "LAW"], "LAW4102": [3, "2", "B", "Legal Practice", "LAW"],
    "LAW4103": [3, "4", "A", "Conflict of Laws", "LAW"], "LAW4104": [2, "2", "B", "Labor", "LAW"],
    "LAW4105": [2, "2", "A", "Legal Ethics", "LAW"], "LAW4106": [2, "3", "A", "Human Rights", "LAW"],
    "LAW4107": [2, "2", "B", "Philosophy", "LAW"], "LAW4108": [3, "2", "B", "Land", "LAW"],
    "LAW4109": [3, "4", "A", "Intellectual Prop", "LAW"], "LAW4110": [2, "1", "A", "Int Trade", "LAW"],
    # หมวดเลือก
    "LAW3133": [3, "3", "B", "Criminology", "ELECTIVE"], "LAW3138": [2, "1", "B", "Child", "ELECTIVE"],
    "LAW4134": [2, "1", "B", "Sea", "ELECTIVE"], "LAW4156": [2, "2", "A", "Legal Eng", "ELECTIVE"],
    "Free 1": [3, "0", "0", "Free Elective 1", "ELECTIVE"], "Free 2": [3, "0", "0", "Free Elective 2", "ELECTIVE"]
}

st.set_page_config(page_title="Easy Law Planner", layout="wide")

# --- 2. Initialize Session State ---
if "study_plan" not in st.session_state:
    st.session_state.study_plan = {f"Year {y} Term {t}": [] for y in range(1, 5) for t in ["1", "2", "S"]}
if "current_term" not in st.session_state:
    st.session_state.current_term = "Year 1 Term 1"

# --- 3. CSS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; text-align: left; padding: 5px; font-size: 13px; margin-bottom: 2px; }
    .term-container { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
    .header-style { color: #1f77b4; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("Law GPA & Planning Tool")

tab1, tab2 = st.tabs(["GPA Calculation", "Registration Planner"])

with tab1:
    st.info("GPA calculation section (as previous version)")
    # Logic เดิมสำหรับคำนวณเกรดสามารถยกมาวางที่นี่ได้

with tab2:
    # ส่วนหัวสำหรับเลือกเทอมที่จะจัด
    st.subheader("Plan Your Semester")
    col_term1, col_term2 = st.columns([2, 1])
    
    with col_term1:
        st.session_state.current_term = st.selectbox(
            "Select Term to Add Subjects:", 
            list(st.session_state.study_plan.keys()),
            key="term_selector"
        )
    
    with col_term2:
        is_grad = st.toggle("Graduation Request (30 Credits / Double Exam)")

    st.divider()

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("<p class='header-style'>Available Subjects (Click to Add)</p>", unsafe_allow_html=True)
        
        # กรองวิชาที่ใช้ไปแล้ว
        used_subs = [item for sublist in st.session_state.study_plan.values() for item in sublist]
        
        cat = st.radio("Category:", ["RAM", "LAW", "ELECTIVE"], horizontal=True)
        
        # แสดงวิชาในหมวดที่เลือก
        cat_courses = {k: v for k, v in all_courses_db.items() if v[4] == cat and k not in used_subs}
        
        for code, info in cat_courses.items():
            exam_info = f"({info[1]}{info[2]})" if info[1] != "0" else ""
            if st.button(f"ADD: {code} {info[3]} {exam_info}", key=f"btn_add_{code}"):
                st.session_state.study_plan[st.session_state.current_term].append(code)
                st.rerun()

    with col_right:
        st.markdown(f"<p class='header-style'>Current Plan: {st.session_state.current_term}</p>", unsafe_allow_html=True)
        
        current_list = st.session_state.study_plan[st.session_state.current_term]
        
        if not current_list:
            st.write("No subjects added. Click 'ADD' from the left panel.")
        else:
            total_credits = 0
            exam_check = {}
            
            for sub in current_list:
                info = all_courses_db[sub]
                total_credits += info[0]
                
                # แสดงวิชาพร้อมปุ่มลบ
                c_sub, c_del = st.columns([5, 1])
                c_sub.write(f"**{sub}** - {info[3]} ({info[1]}{info[2]})")
                if c_del.button("DEL", key=f"btn_del_{sub}"):
                    st.session_state.study_plan[st.session_state.current_term].remove(sub)
                    st.rerun()
                
                # ตรวจสอบสอบชน
                d_code = f"{info[1]}{info[2]}"
                if d_code != "00":
                    if d_code in exam_check:
                        if is_grad: st.warning(f"Warning: Exam Conflict {sub} with {exam_check[d_code]}")
                        else: st.error(f"Error: Exam Conflict {sub} with {exam_check[d_code]}!")
                    exam_check[d_code] = sub

            # สรุปหน่วยกิต
            max_c = 30 if is_grad else (9 if "Term S" in st.session_state.current_term else 22)
            st.metric("Total Credits", f"{total_credits} / {max_c}")
            if total_credits > max_c:
                st.error("Too many credits for this term!")

    st.divider()
    if st.button("Reset All Plans"):
        st.session_state.study_plan = {f"Year {y} Term {t}": [] for y in range(1, 5) for t in ["1", "2", "S"]}
        st.rerun()
