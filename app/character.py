from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


class Character:

    def setNameRace(self, name, race, gender):
        self.name = name
        self.race = race
        self.gender = gender

    def setTheme(self, theme):
        self.theme = theme

    def setClass(self, cls):
        self.cls = cls

    def setImprovs(self, v):
        self.improvs = v

    def createPDF(self):
        packet = io.BytesIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(155, 753, self.name)  # Draw the name on the top
        can.drawString(215, 731, self.race)  # Draw our character race on the sheet
        can.drawString(165, 710, self.gender)  # Draw gender
        can.drawString(20, 730, self.charClass)  # Draw Class
        can.drawString(315, 730, self.theme)  # Theme
        can.save()

        # move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(open("original.pdf", "rb"))
        output = PdfFileWriter()
        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(0)
        page2 = existing_pdf.getPage(1)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        output.addPage(page2)
        # finally, write "output" to a real file
        outputStream = open("destination.pdf", "wb")
        output.write(outputStream)
        outputStream.close()
