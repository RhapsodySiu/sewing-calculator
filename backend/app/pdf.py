from fpdf import FPDF
import io

def generate_pdf():
    pdf = FPDF(format="a3")
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Python!", ln=True, align="C")
    
    pdf.rect(20, 20, 120, 120, style='D', round_corners=True, corner_radius=20)
    pdf.set_dash_pattern(dash=2, gap=3)
    pdf.rect(10, 10, 140, 140, style='D', round_corners=True, corner_radius=20)
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return pdf_output
