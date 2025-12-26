import streamlit as st

# --- UI ส่วนการกรอกข้อมูลที่อยู่และรายละเอียดบุคคล ---
def input_person_details(label):
    st.subheader(f"ข้อมูล{label}")
    name = st.text_input(f"ชื่อ-นามสกุล {label}")
    id_card = st.text_input(f"เลขประจำตัวประชาชน {label}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: race = st.text_input(f"เชื้อชาติ {label}")
    with col2: nationality = st.text_input(f"สัญชาติ {label}")
    with col3: job = st.text_input(f"อาชีพ {label}")
    with col4: age = st.text_input(f"อายุ (ปี) {label}")

    col5, col6, col7, col8 = st.columns(4)
    with col5: house_no = st.text_input(f"อยู่บ้านเลขที่ {label}")
    with col6: moo = st.text_input(f"หมู่ที่ {label}")
    with col7: road = st.text_input(f"ถนน {label}")
    with col8: soi = st.text_input(f"ตรอก/ซอย {label}")

    col9, col10, col11, col12 = st.columns(4)
    with col9: sub_district = st.text_input(f"ตำบล/แขวง {label}")
    with col10: district = st.text_input(f"อำเภอ/เขต {label}")
    with col11: province = st.text_input(f"จังหวัด {label}")
    with col12: post_code = st.text_input(f"รหัสไปรษณีย์ {label}")

    col13, col14, col15 = st.columns(3)
    with col13: phone = st.text_input(f"โทรศัพท์ {label}")
    with col14: fax = st.text_input(f"โทรสาร {label}")
    with col15: email = st.text_input(f"ไปรษณีย์อิเล็กทรอนิกส์ {label}")
    
    return {
        "name": name, "id": id_card, "race": race, "nat": nationality,
        "job": job, "age": age, "h_no": house_no, "moo": moo,
        "road": road, "soi": soi, "sub_d": sub_district, "dist": district,
        "prov": province, "post": post_code, "tel": phone, "fax": fax, "email": email
    }

# ในหน้าหลักเรียกใช้แบบนี้
p_data = input_person_details("โจทก์")
d_data = input_person_details("จำเลย")
