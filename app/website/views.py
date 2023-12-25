from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.http import FileResponse, HttpResponse
import io


def generate_pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's an example.
    p.drawString(100, 100, "Hello World!")

    # Close the PDF object cleanly and we're done.
    p.showPage()
    p.save()

    # Set the buffer's position to the beginning.
    buffer.seek(0)

    # Create an inline response with the PDF content.
    response = HttpResponse(buffer, content_type="application/pdf")

    # Set the Content-Disposition header to inline, which displays the PDF in the browser.
    response["Content-Disposition"] = "inline; filename=report.pdf"

    return response
