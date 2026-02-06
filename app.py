# --- ส่วนการสร้าง PDF (ภาษาไทย) ---
            from fpdf import FPDF

            class GPA_PDF(FPDF):
                def header(self):
                    # เพิ่มฟอนต์ไทย (ต้องมีไฟล์ THSarabunNew.ttf อยู่ในโฟลเดอร์เดียวกับโค้ด)
                    self.add_font('THSarabun', '', 'THSarabunNew.ttf', uni=True)
                    self.set_font('THSarabun', '', 20)
                    self.cell(0, 10, 'รายงานผลการเรียนเฉลี่ย (GPA Report)', ln=True, align='C')
                    self.ln(5)

            pdf = GPA_PDF()
            pdf.add_page()
            pdf.add_font('THSarabun', '', 'THSarabunNew.ttf', uni=True)
            
            # หัวตาราง
            pdf.set_font('THSarabun', '', 16)
            pdf.cell(80, 10, 'ชื่อวิชา', border=1, align='C')
            pdf.cell(50, 10, 'หน่วยกิต', border=1, align='C')
            pdf.cell(50, 10, 'เกรด', border=1, align='C', ln=True)

            # รายละเอียดวิชา
            pdf.set_font('THSarabun', '', 14)
            for item in summary_data:
                pdf.cell(80, 10, f"  {item[0]}", border=1)
                pdf.cell(50, 10, f"{item[1]}", border=1, align='C')
                pdf.cell(50, 10, f"{item[2]}", border=1, align='C', ln=True)

            # สรุปผลด้านท้าย
            pdf.ln(10)
            pdf.set_font('THSarabun', '', 18)
            pdf.cell(0, 10, f"จำนวนหน่วยกิตสะสมรวม: {total_credits} หน่วยกิต", ln=True)
            pdf.cell(0, 10, f"เกรดเฉลี่ยสะสม (GPA): {gpa:.2f}", ln=True)

            # ส่งไฟล์ให้ผู้ใช้ Download
            pdf_output = pdf.output(dest='S').encode('latin-1', errors='ignore')
            st.download_button(
                label="📥 กดเพื่อดาวน์โหลด PDF (ภาษาไทย)",
                data=pdf_output,
                file_name="GPA_Report.pdf",
                mime="application/pdf"
            )
