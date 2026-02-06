import streamlit as st
import os

# --- 1. Database (หน่วยกิตเป๊ะ 100%) ---
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
    "LAW4134": [2, "1", "B", "ทะเล", "ELECTIVE"], "LAW4156": [2, "2", "A", "อิ้งกฎหมาย", "ELECTIVE"],
    "วิชาเลือก 1": [3, "1", "A", "เลือกเสรี 1", "ELECTIVE"], "วิชาเลือก 2": [3, "1", "B", "เลือกเสรี 2", "ELECTIVE"]
}

grade_map = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}

st.set_page_config(page_title="Safe Law GPA & Planner", layout="wide")

# --- 2. State Management ---
if "study_plan" not in st.session_state:
    st.session_state.study_plan = {f"Y{y}T{t}": {s: "-" for s in ["1A","1B","2A","2B","3A","3B","4A","4B"]} 
                                  for y in range(1, 5) for t in ["1", "2", "S"]}
if "v_reset" not in st.session_state:
    st.session_state.v_reset = {f"Y{y}T{t}_{s}": 0 for y in range(1, 5) for t in ["1", "2", "S"] for s in ["1A","1B","2A","2B","3A","3B","4A","4B"]}

# --- 3. CSS (ดำเข้ม เห็นชัด) ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .overall-table { width: 100%; border-collapse: collapse; background-color: #ffffff; color: #000 !important; }
    .overall-table th, .overall-table td { border: 2px solid #000; padding: 6px; color: #000 !important; vertical-align: top; }
    .overall-table th { background-color: #1e3a8a; color: #fff !important; }
    .sub-tag { background: #e0f2fe; padding: 2px 4px; border-radius: 4px; display: block; margin-bottom: 2px; border-left: 3px solid #0369a1; font-size: 11px; color: #000 !important; font-weight: bold; }
    .result-box { width: 95px; padding: 5px; border: 2px solid #000; border-radius: 5px; text-align: center; background-color: #fff !important; color: #000 !important; }
    .result-box b { color: #d32f2f !important; font-size: 18px; }
    p, span, label, .stMetricValue { color: #000 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. Logic Functions ---
def handle_clear(tk, sn):
    st.session_state.study_plan[tk][sn] = "-"
    st.session_state.v_reset[f"{tk}_{sn}"] += 1

def handle_clear_all():
    for tk in st.session_state.study_plan:
        for sn in st.session_state.study_plan[tk]:
            st.session_state.study_plan[tk][sn] = "-"
            st.session_state.v_reset[f"{tk}_{sn}"] += 1

st.title("⚖️ ระบบคำนวณ GPA & วางแผนเรียน")
tab1, tab2 = st.tabs(["📊 คำนวณเกรดสะสม (GPA)", "📅 วางแผนลงทะเบียน 4 ปี"])

# --- TAB 1: GPA ---
with tab1:
    st.info("ทำเครื่องหมายวิชาที่ผ่านแล้วเพื่อคำนวณเกรด (วิชาเลือกเสรีอยู่ล่างสุด)")
    selected_gpa = []
    # แบ่งหมวดหมู่ให้เห็นชัดเจน
    cats = {"📂 หมวด RAM": "RAM", "📂 หมวด LAW": "LAW", "📂 หมวดวิชาเลือก/เสรี": "ELECTIVE"}
    for label, cp in cats.items():
        with st.expander(label, expanded=(cp == "LAW")):
            # ดึงวิชามาแสดงตามหมวด
            cat_courses = {k: v for k, v in all_courses_db.items() if v[4] == cp}
            cols = st.columns(4)
            for idx, (code, info) in enumerate(cat_courses.items()):
                with cols[idx % 4]:
                    r = st.columns([1.2, 1])
                    if r[0].checkbox(code, key=f"g_chk_{code}"):
                        g = r[1].selectbox("G", ["A","B+","B","C+","C","D+","D","F"], key=f"g_sel_{code}", label_visibility="collapsed")
                        selected_gpa.append({"name": code, "credit": info[0], "grade": g})
    if selected_gpa:
        st.divider()
        tc = sum(d['credit'] for d in selected_gpa); tp = sum(grade_map[d['grade']] * d['credit'] for d in selected_gpa)
        st.success(f"### GPA สะสม: {tp/tc:.2f} | รวม {tc} หน่วยกิต")
        h = '<div style="display:flex; flex-wrap:wrap; gap:8px;">'
        for d in selected_gpa: h += f'<div class="result-box"><span>{d["name"]}</span><br><b>{d["grade"]}</b></div>'
        st.markdown(h + '</div>', unsafe_allow_html=True)

# --- TAB 2: วางแผน (8 Slot) ---
with tab2:
    c1, c2, c3 = st.columns(3)
    yr = c1.selectbox("ปีการศึกษา", [1, 2, 3, 4], key="y_s")
    tm = c2.selectbox("เทอม", ["1", "2", "S"], key="t_s")
    grad = c3.toggle("🎓 ขอจบ (ขยายเพดานหน่วยกิต)")
    curr_tk = f"Y{yr}T{tm}"

    # คำนวณหน่วยกิตรวมเทอมนี้ (Single Source of Truth)
    total_c = sum([all_courses_db.get(v.split(" | ")[0], [0])[0] for v in st.session_state.study_plan[curr_tk].values() if v != "-"])
    limit = (12 if tm == "S" else 30) if grad else (9 if tm == "S" else 22)

    st.markdown(f"### 📍 จัดแผนปี {yr} เทอม {tm}")
    if total_c > limit:
        st.error(f"⚠️ หน่วยกิตเกิน! เทอม {tm} ลงได้ {limit} นก. (ตอนนี้ {total_c})")
    else: st.metric("หน่วยกิตรวมเทอมนี้", f"{total_c} / {limit}")

    st.divider()
    # กันลงซ้ำข้ามเทอม
    used = [v.split(" | ")[0] for tk, s in st.session_state.study_plan.items() if tk != curr_tk for v in s.values() if v != "-"]
    
    slots = ["1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B"]
    rows = st.columns(4)
    for i, sn in enumerate(slots):
        with rows[i % 4]:
            st.markdown(f"**📌 คาบ {sn}**")
            day, period = sn[0], sn[1]
            valid = ["-"] + [f"{c} | {all_courses_db[c][3]}" for c in all_courses_db if all_courses_db[c][1] == day and all_courses_db[c][2] == period and c not in used]
            
            vk = f"{curr_tk}_{sn}"
            saved = st.session_state.study_plan[curr_tk][sn]
            
            # Selectbox บังคับอัปเดต state
            choice = st.selectbox(f"S_{sn}", options=valid, index=valid.index(saved) if saved in valid else 0, key=f"w_{vk}_v{st.session_state.v_reset[vk]}", label_visibility="collapsed")
            
            if st.session_state.study_plan[curr_tk][sn] != choice:
                st.session_state.study_plan[curr_tk][sn] = choice
                st.rerun() # บังคับคำนวณหน่วยกิตทันที

            if choice != "-":
                st.button(f"🗑️ ลบ {sn}", key=f"del_{vk}", on_click=handle_clear, args=(curr_tk, sn))

    # ตารางสรุป 4 ปี
    st.divider()
    st.markdown("### 🗓️ สรุปแผนการเรียนภาพรวม 4 ปี")
    
    html = "<table class='overall-table'><tr><th>ชั้นปี</th><th>เทอม 1 (22)</th><th>เทอม 2 (22)</th><th>เทอม S (9)</th></tr>"
    for y in range(1, 5):
        html += f"<tr><td><b>ปี {y}</b></td>"
        for t in ["1", "2", "S"]:
            tk = f"Y{y}T{t}"; cell, tc = "", 0
            for sn, val in st.session_state.study_plan[tk].items():
                if val != "-":
                    c = val.split(" | ")[0]; cell += f"<span class='sub-tag'>{sn}: {val}</span>"; tc += all_courses_db.get(c, [0])[0]
            html += f"<td>{cell}<b style='color:#000'>รวม {tc} นก.</b></td>"
        html += "</tr>"
    st.markdown(html + "</table>", unsafe_allow_html=True)
    st.button("♻️ ล้างแผนทั้งหมด", on_click=handle_clear_all)

st.markdown("---")
if st.button("🧧 สนับสนุนค่าน้ำชาผู้พัฒนา", use_container_width=True):
    st.info("ขอบคุณที่ร่วมสนับสนุนครับ! (Pop-up QR Code จะแสดงตรงนี้)")
