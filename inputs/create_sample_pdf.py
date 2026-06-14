from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_sample():
    c = canvas.Canvas("sample.pdf", pagesize=letter)
    width, height = letter
    
    # Add a title
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 100, "Typstify Test Document")
    
    # Add some text
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, "This is a sample document to test the PDF to Typst conversion.")
    c.drawString(100, height - 170, "It contains basic layout elements like a header, text blocks, and shapes.")
    
    # Add a rectangle
    c.setStrokeColorRGB(0.2, 0.4, 0.6)
    c.rect(100, height - 300, 400, 100, fill=0)
    c.drawString(110, height - 250, "This is text inside a blue rectangle.")
    
    c.showPage()
    c.save()
    print("sample.pdf created.")

if __name__ == "__main__":
    create_sample()
