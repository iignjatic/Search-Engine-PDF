from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

from fpdf import FPDF


def pdf_to_text(pdf_file_path):

    with open(pdf_file_path, 'rb') as pdf_file:
        resource_manager = PDFResourceManager()
        
        #prolazi kroz sve stranice i izvlaci tekst
        for page_num, page in enumerate(PDFPage.get_pages(pdf_file), start=1):

            output_string = StringIO()

            device = TextConverter(resource_manager, output_string, laparams=LAParams())

            interpreter = PDFPageInterpreter(resource_manager, device)
            
            # cita stranicu
            interpreter.process_page(page)
            # preuzima tekst iz stringio objekta
            text = output_string.getvalue()
            
            # sacuva u txt fajl
            output_file_path = f'txtPages/{page_num}.txt'
            with open(output_file_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)
            
            
            device.close()
            output_string.close()


def txt_to_pdf(txt_file, pdf_file, colored_words):
    pdf = FPDF()   
    pdf.add_page()
    pdf.set_font("Arial", size = 10)
    
    with open(txt_file, "r", encoding='utf-8') as f:
        for line in f:
            line = line.encode('latin-1', 'replace').decode('latin-1')
            words = line.split()
            
            line_height = 10
            space_width = pdf.get_string_width(' ')  # sirina razmaka
            pdf.ln(line_height)  # prelazak na novi red

            for word in words:
                word_width = pdf.get_string_width(word) + space_width  # sabira se sirina razmaka i sirina rijeci
                if pdf.get_x() + word_width > pdf.w - pdf.r_margin:  # provjera da li treba u novi red
                    pdf.ln(line_height)  

                if any(colored.lower() in word.lower() for colored in colored_words):

                    pdf.set_text_color(0, 255, 0)  # zelena boja za odabrane riječi
                    pdf.cell(word_width, line_height, txt=word, align='L')  
                    pdf.set_text_color(0, 0, 0)  # reset boje na crnu
                else:
                    pdf.cell(word_width, line_height, txt=word, align='L')  


    pdf.output(pdf_file)