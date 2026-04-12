from sys import excepthook

from pypdf import PdfReader
import docx

class process_file:
    def __init__(self):
        self.text = ""
    def pdf_read(self,filename,password:str=""):
        reader = PdfReader(filename)
        if reader.is_encrypted:
            reader.decrypt(f"{password}")
        pages = []
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                pages.append(extracted)
                self.text = "\n".join(pages)
        return self.text
    def docx_read(self,filename):
        doc = docx.Document(filename)
        fullText=[]
        for para in doc.paragraphs:
            fullText.append(para.text)
        self.text = '\n'.join(fullText)
        return self.text

    def fetch_document(self):
        pass
    def extract_document(self):
        file = self.fetch_document()

        name,ext = file.rsplit(".",1)
        if ext =="pdf":
            self.pdf_read(file)
        elif ext == "docx":
            self.docx_read(file)
        else:
            raise ValueError("Document is not supported!")
    def chunks(self):
        pass
    def output(self):   
        pass


