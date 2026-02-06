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
    "LAW4134": [2, "1", "B", "ทะเล", "ELECTIVE"], "LAW4156": [2, "2", "A", "อิ้งกฎหมาย", "ELECTIVE"],
    "วิชาเลือก 1": [3, "0", "0", "เลือกเสรี 1", "ELECTIVE"], "วิชาเลือก 2": [3, "0", "0", "เลือกเสรี 2", "ELECTIVE"]
}

st.set_page_config(page_title="Easy Law Planner", layout="wide")

# --- 2. Initialize Session State (ตรวจสอบชื่อ Key ให้ตรงกัน) ---
if "study_plan" not in st.session_state:
    # สร้างชื่อ Key เป็นภาษาไทยให้ตรงกับที่จะใช้ในตาราง
    st.session_state.study_plan = {f"ปี {y} เทอม {t}": [] for y in range(1, 5) for t in ["1", "2", "S"]}

# --- 3. CSS ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .overall-table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 14px; background-color: white; }
    .overall-table th, .overall-table td { border: 1px solid #ddd; padding: 10px; text-align: left; vertical-align: top; }
    .overall-table th { background-color: #2c3e50; color: white; }
    .sub-item { font-size: 11px; background: #e8f4fd; padding: 2px 5px; border-radius: 4px; margin-bottom: 3px; display: block; border-left: 3px solid #3498db; color: #2c3e50; }
    .credit-tag { font-weight: bold; color: #e74c3c; font-size: 12px; display: block; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Law GPA & Planning")

tab1, tab2 = st.tabs(["📊 คำนวณเกรด (GPA)", "📅 วางแผนลงทะเบียน"])

with tab1:
    st.info("ส่วนคำนวณเกรด (GPA)")
    # สามารถนำ Logic การเลือกเกรดมาใส่ตรงนี้ได้เลย

with tab2:
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        st.subheader("1. เพิ่มวิชาเข้าแผน")
        # ตรวจสอบชื่อเทอมให้ตรงกับ Key ที่สร้างไว้
        target_term = st.selectbox("เลือกเทอมที่ต้องการจัด:", list(st.session_state.study_plan.keys()))
        is_grad = st.toggle("🎓 ขอจบการศึกษา (30 นก. / ซ้ำซ้อน)")
        
        cat = st.radio("หมวดหมู่:", ["RAM", "LAW", "ELECTIVE"], horizontal=True)
        used_subs = [item for sublist in st.session_state.study_plan.values() for item in sublist]
        available = {k: v for k, v in all_courses_db.items() if v[4] == cat and k not in used_subs}
        
        for code, info in available.items():
            if st.button(f"ADD: {code} {info[3]} ({info[1]}{info[2]})", key=f"p_add_{code}"):
                st.session_state.study_plan[target_term].append(code)
                st.rerun()

    with col_r:
        st.subheader(f"2. รายชื่อวิชาใน {target_term}")
        current_list = st.session_state.study_plan.get(target_term, [])
        if not current_list:
            st.write("ยังไม่ได้เลือกวิชา")
        else:
            total_c = 0
            exam_check = {}
            for sub in current_list:
                info = all_courses_db[sub]
                total_c += info[0]
                c_s, c_d = st.columns([5, 1])
                c_s.write(f"**{sub}** {info[3]} ({info[1]}{info[2]})")
                if c_d.button("DEL", key=f"p_del_{sub}"):
                    st.session_state.study_plan[target_term].remove(sub)
                    st.rerun()
                
                # เช็กสอบชน
                d_code = f"{info[1]}{info[2]}"
                if d_code != "00":
                    if d_code in exam_check:
                        if is_grad: st.warning(f"ชน: {sub} กับ {exam_check[d_code]}")
                        else: st.error(f"ชน: {sub} กับ {exam_check[d_code]}!")
                    exam_check[d_code] = sub
            
            max_c = 30 if is_grad else (9 if "เทอม S" in target_term else 22)
            st.metric("หน่วยกิตรวม", f"{total_c} / {max_c}")

    # --- ส่วนตารางภาพรวม 4 ปี (แก้ไขจุดที่ทำให้เกิด KeyError) ---
    st.divider()
    st.markdown("### 🗓️ ตารางสรุปแผนการเรียนภาพรวม 4 ปี")
    
    html = "<table class='overall-table'><tr><th>ชั้นปี</th><th>เทอม 1</th><th>เทอม 2</th><th>เทอม S</th></tr>"
    
    for y in range(1, 5):
        html += f"<tr><td><b>ปีที่ {y}</b></td>"
        for t in ["1", "2", "S"]:
            t_key = f"ปี {y} เทอม {t}"
            # ใช้ .get() เพื่อป้องกัน KeyError หากหา Key ไม่เจอ
            subs = st.session_state.study_plan.get(t_key, [])
            
            cell = ""
            current_t_creds = 0
            for s in subs:
                cell += f"<span class='sub-item'>{s} {all_courses_db[s][3]}</span>"
                current_t_creds += all_courses_db[s][0]
            
            html += f"<td>{cell}<span class='credit-tag'>รวม {current_t_creds} นก.</span></td>"
        html += "</tr>"
    
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)
    
    if st.button("♻️ ล้างแผนทั้งหมด"):
        st.session_state.study_plan = {f"ปี {y} เทอม {t}": [] for y in range(1, 5) for t in ["1", "2", "S"]}
        st.rerun()
