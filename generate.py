import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

# Invoice Data Path
filename = 'invoice_data.csv' 

with open(filename, 'r') as file:
    reader = csv.DictReader(file)

    for row in reader:
        # Extract customer_data and invoice_data from each row
        customer_data = {
            'name': row['name'],
            'handle_id': row['handle_id'],
            'state': row['state'],
            'pin_code': row['pin_code'],
            'country': row['country']
        }

        invoice_data = {
            'invoice_no': row['invoice_no'],
            'invoice_date': row['invoice_date'],
            'invoice_type': row['invoice_type'],
            'handle_id': row['handle_id'],
            'payment_terms': row['payment_terms'],
            'particulars': 'Virtual Item/Service',
            'hsn_sac': row['hsn_sac'],
            'rate': row['rate'],
            'taxable_value': row['taxable_value'],
            'cgst': row.get('cgst', ''),
            'sgst': row.get('sgst', ''),
            'igst': row.get('igst', ''),
            'total_amount': row['total_amount']
        }

        # Create a unique name for each output PDF based on the invoice number
        output_pdf = f"{row['invoice_no']}_invoice.pdf"

        c = canvas.Canvas(output_pdf, pagesize=letter)
        width, height = letter

        # Margin
        margin = 28  # Adjusted margin to approximately 1 cm

        # Add Tax Invoice Header
        c.setFont("Helvetica-Bold", 12)
        invoice_text = 'Tax Invoice'
        x_center = width / 2  # x-coordinate of the center of the page
        y_position = height - margin  # y-coordinate of the text
        c.drawCentredString(x_center, y_position, invoice_text)

        # Underline the "Tax Invoice" text
        text_width = c.stringWidth(invoice_text, 'Helvetica-Bold', 12)
        line_start_x = x_center - (text_width / 2)
        line_end_x = x_center + (text_width / 2)
        line_y = y_position - 2
        c.line(line_start_x, line_y, line_end_x, line_y)

        style = ParagraphStyle(
            'Normal',
            fontSize=10,
        )

        # Top Three Columns inside a Table
        c.setFont("Helvetica", 10)
        column1_text = '''
                    <b>Random Company Private Limited</b><br/>
                    Company Address Line 1<br/>
                    Company Address Line 2<br/>
                    Company Address Line 3<br/><br/>
                    GSTIN/UIN: 11XXXXX111X1XX<br/>
                    State Name: Delhi<br/>
                    E-Mail : accounts@randomcompany.com<br/>
                    '''

        column2_text = f'''
                    <b>Invoice No:</b><br/>
                    {invoice_data['invoice_no']}<br/>
                    <b>Buyer:</b><br/>
                    User ID: {customer_data['handle_id']}<br/>
                    <b>Customer:</b><br/>
                    {customer_data['name']}<br/>
                    State Name: {customer_data['state']}<br/>
                    Pin Code: {customer_data['pin_code']}<br/>
                    Country: {customer_data['country']}<br/>
                    '''

        column3_text = f'''
                    <b>Date:</b> {invoice_data['invoice_date']}<br/>
                    <b>Invoice Type:</b> B2C<br/><br/>
                    <b>User ID:</b><br/>
                    {invoice_data['handle_id']}<br/><br/>
                    <b>Mode/Terms of Payment:</b><br/>
                    {invoice_data['payment_terms']}<br/>
                    '''

        column1 = Paragraph(column1_text, style)
        column2 = Paragraph(column2_text, style)
        column3 = Paragraph(column3_text, style)

        data = [[column1, column2, column3]]
        available_width = width - 2 * margin
        col_widths = [
            available_width * 38.36 / 100,
            available_width * 30.27 / 100,
            available_width * 31.36 / 100]

        table = Table(data, colWidths=col_widths, rowHeights=120)
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOX', (0, 0), (-1, 0), 1, colors.black),
            ('LINEBEFORE', (1, 0), (1, 0), 1, colors.black),
            ('LINEAFTER', (1, 0), (1, 0), 1, colors.black),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ]))
        table.wrapOn(c, width, height)
        table.drawOn(c, margin, height - 200)

        # Particulars Header and Data in Tabular Format
        table_headers = ['S.No', 'Particulars', 'HSN/SAC', 'Rate', 'Taxable Value', 'IGST@18%', 'Total Amount']
        data_entry = ['1',
                      invoice_data['particulars'],
                      invoice_data['hsn_sac'],
                      invoice_data['rate'],
                      invoice_data['taxable_value'],
                      invoice_data['igst'],
                      invoice_data['total_amount']
                      ]

        # Adjusted column widths proportionally with header text
        available_width = width - 2 * margin
        col_widths = [available_width * 8/100,
                      available_width * 28/100,
                      available_width * 11/100,
                      available_width * 11/100,
                      available_width * 14/100,
                      available_width * 14/100]

        data = [table_headers, data_entry]

        table = Table(data, colWidths=col_widths, rowHeights=[30, 50])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        table.wrapOn(c, width, height)
        table.drawOn(c, margin, height - 320)

        # Declaration
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin, height - 370, 'Declaration:-')
        c.setFont("Helvetica", 10)

        # Break the declaration text into multiple lines
        line_height = 15
        y_coord = height - 385
        declaration_text_lines = [
            'We declare that this invoice shows the actual',
            'price of the goods described and that all',
            'particulars are true and correct.'
        ]

        # Draw each line separately
        for line in declaration_text_lines:
            c.drawString(margin, y_coord, line)
            y_coord -= line_height  # Move to the next line

        # Authorisation
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(width - margin, height - 415, 'For Random Company Private Limited')
        c.setFont("Helvetica", 10)
        c.drawRightString(width - margin, height - 430, 'Authorised Signatory')

        # Leave some space
        space_between = 50

        # Computer Generated Invoice Note
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(width / 2, height - 455 - space_between, 'This is a Computer Generated Invoice no signature required')
        c.setLineWidth(1)

        # Define the text to draw the line under
        text = 'This is a Computer Generated Invoice no signature required'

        x_left = (width - c.stringWidth(text, 'Helvetica-Bold', 10)) / 2
        x_right = (width + c.stringWidth(text, 'Helvetica-Bold', 10)) / 2
        y = height - 456 - space_between - 2

        c.line(x_left, y, x_right, y)

        # Save the PDF
        c.save()

        print(f'Invoice {output_pdf} Generated Successfully!')
