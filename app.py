import os

# ตรวจสอบไฟล์ก่อนเริ่มทำงาน
def check_files():
    files = ["template.pdf", "THSarabunNew.ttf"]
    for f in files:
        if not os.path.exists(f):
            st.error(f"❌ ไม่พบไฟล์: {f} ใน GitHub ของคุณ!")
            return False
    return True

if submit:
    if check_files():
        try:
            # โค้ดสร้าง PDF เดิมของคุณ...
            st.success("สร้างไฟล์สำเร็จ!")
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
