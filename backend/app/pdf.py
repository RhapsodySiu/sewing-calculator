from typing import IO
import io
from fpdf import FPDF

def generate_pdf(name: str, width: float, height: float, thickness: float, roundness: float) -> IO[bytes]:
    pointerX = 0
    pointerY = 0
    cellWidth = 60
    cellHeight = 50

    zipperLen = int(round(width * 2 + height - roundness * 6 + 2 * roundness * 3.14 + 2))
    biasLen = int(round((width + height) * 4))

    widthInMm = width * 10
    heightInMm = height * 10
    thicknessInMm = thickness * 10
    roundnessInMm = roundness * 10
    seamAllowance = 10

    pdf = FPDF(orientation='P', unit='mm', format='A3')
    pdf.add_page()

    pdf.set_font("Arial", size=18)
    pdf.cell(0, 10, f"All-round pouch ({name}) sewing pattern", align='C')

    pdf.set_xy(0, 30)

    pdf.set_font("Arial", size=16)
    pdf.cell(0, 0, "Powered by fpdf2", align='C')

    pointerX = 10
    pointerY = 50

    pdf.set_xy(pointerX, pointerY)
    pdf.multi_cell(
        80, 
        None, 
        (
            'Ingredients:\n\n'
            '- Fabric\n'
            '- Lining\n'
            '- Fleece (optional)\n'
            f'- Zipper (at least {zipperLen}cm)\n'
            f'- Bias tape (at least {biasLen}cm)\n'
        ), 
        border=True, 
        align='L',
        padding=5
    )
    
    pointerX = 100
    pdf.set_xy(pointerX + (widthInMm - cellWidth) / 2 + seamAllowance, pointerY + (heightInMm - cellHeight) / 2 + seamAllowance)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(min(widthInMm, cellWidth), None, 'Cover:\n- Fabric x 2\n- Lining x 2\n- Fleece (optional) x 2 no SA', align='L')
    pdf.rect(pointerX + seamAllowance, pointerY + seamAllowance, widthInMm, heightInMm, style='D', round_corners=True, corner_radius=roundnessInMm)
    pdf.set_dash_pattern(dash=2, gap=3)
    pdf.rect(pointerX, pointerY, widthInMm + seamAllowance * 2, heightInMm + seamAllowance * 2, style='D', round_corners=True, corner_radius=roundnessInMm + seamAllowance)

    pointerX = 10    
    pointerY += heightInMm + seamAllowance * 2 + 10

    stripeWidth = heightInMm - roundnessInMm * 2
    pdf.set_xy(pointerX + (stripeWidth - cellWidth) / 2 + seamAllowance, pointerY + seamAllowance)
    pdf.multi_cell(min(stripeWidth, cellWidth), None, 'Spine:\n- Fabric & Lining\n- Fleece (optional) no SA', align='L', padding=5)
    pdf.rect(pointerX, pointerY, stripeWidth + seamAllowance * 2, thicknessInMm + seamAllowance * 2, style='D')
    pdf.set_dash_pattern()
    pdf.rect(pointerX + seamAllowance, pointerY + seamAllowance, stripeWidth, thicknessInMm, style='D')

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return pdf_output
