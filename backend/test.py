from app.pdf import generate_pdf

# Generate the PDF
pdf_content = generate_pdf("test", 10, 10, 2, 2)

# Save the result to the current directory as file.pdf
with open('file.pdf', 'wb') as f:
    f.write(pdf_content.getvalue())