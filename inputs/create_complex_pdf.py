from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_complex_pdf(filename="complex_sample.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    elements.append(Paragraph("Complex PDF with Tables Report", styles['Title']))
    elements.append(Spacer(1, 12))
    
    # Introduction
    elements.append(Paragraph("This document serves as a complex test case for Typstify, featuring varied layouts and intricate tables.", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Simple Table
    elements.append(Paragraph("1. Basic Inventory Table", styles['Heading2']))
    data1 = [
        ["ID", "Item Name", "Category", "Price", "Stock"],
        ["001", "Widget A", "Hardware", "$10.00", "50"],
        ["002", "Gadget B", "Electronics", "$25.50", "120"],
        ["003", "Tool C", "Hardware", "$15.75", "30"],
    ]
    t1 = Table(data1)
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t1)
    elements.append(Spacer(1, 24))
    
    # Complex Table with Colspan and Rowspan
    elements.append(Paragraph("2. Financial Performance (Merged Cells)", styles['Heading2']))
    data2 = [
        ["Quarter", "Revenue Details", "", "Profit"],
        ["", "Sales", "Services", ""],
        ["Q1", "$5000", "$2000", "$1500"],
        ["Q2", "$6000", "$2500", "$2000"],
        ["Total", "$11000", "$4500", "$3500"]
    ]
    t2 = Table(data2)
    t2.setStyle(TableStyle([
        # Header Merging
        ('SPAN', (1, 0), (2, 0)), # Revenue Details spans two columns
        ('SPAN', (0, 0), (0, 1)), # Quarter spans two rows
        ('SPAN', (3, 0), (3, 1)), # Profit spans two rows
        
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 1), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 24))
    
    # Multi-line text in table
    elements.append(Paragraph("3. Status Report with Long Text", styles['Heading2']))
    data3 = [
        ["Project", "Description", "Status"],
        ["Typstify", "An AI-powered agent that converts PDF files into high-quality Typst templates automatically.", "In Progress"],
        ["Marketing AI", "Automation suite for generating social media content and tracking engagement metrics.", "Planning"]
    ]
    # Set column widths to force wrapping
    t3 = Table(data3, colWidths=[100, 250, 80])
    t3.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightsteelblue),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))
    elements.append(t3)
    
    doc.build(elements)
    print(f"{filename} created.")

if __name__ == "__main__":
    create_complex_pdf()
