from pypdf import PdfReader
import docx
import re
import unicodedata
import os
from datetime import datetime


class process_file:
    def __init__(self):
        self.text = ""
        self.metadata = {}

    @staticmethod
    def _clean_jp(s):
        """NFKC normalize + remove stray spaces between CJK chars (し ている → している)."""
        if not s:
            return s
        s = unicodedata.normalize("NFKC", s)
        s = re.sub(
            r'(?<=[\u3040-\u30ff\u4e00-\u9fff])\s+(?=[\u3040-\u30ff\u4e00-\u9fff])',
            '', s
        )
        return s

    def _base_metadata(self, filename, file_type):
        """Common metadata for any file — used by both PDF and DOCX."""
        return {
            "source_file": os.path.basename(filename),   # for display / citations
            "source_path": filename,                     # for re-opening the file
            "file_type": file_type,                      # "pdf" or "docx", for filtering
            "ingested_at": datetime.now().isoformat(),   # for freshness / re-indexing
            "char_count": 0,                             # filled in after extraction
        }

    def pdf_read(self, filename, password: str = ""):
        reader = PdfReader(filename)

        # Only decrypt if the PDF is actually encrypted.
        if reader.is_encrypted:
            if reader.decrypt(password) == 0:
                raise ValueError("Failed to decrypt PDF - wrong or missing password")

        pages = []
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                pages.append(self._clean_jp(extracted))
        self.text = "\n".join(pages)

        pdf_meta = reader.metadata or {}
        self.metadata = self._base_metadata(filename, "pdf")
        self.metadata.update({
            "page_count": len(reader.pages),
            "char_count": len(self.text),
            "pdf_title": pdf_meta.get("/Title", "") or "",
            "pdf_author": pdf_meta.get("/Author", "") or "",
        })

        return self.text

    def docx_read(self, filename):
        doc = docx.Document(filename)
        full_text = [self._clean_jp(p.text) for p in doc.paragraphs]
        self.text = "\n\n".join(full_text)

        self.metadata = self._base_metadata(filename, "docx")
        self.metadata.update({
            "page_count": 1,
            "char_count": len(self.text),
        })
        return self.text

    def fetch_document(self):
        pass

    def extract_document(self,file):
        #file = self.fetch_document()
        ext = file.rpartition(".")[2].lower()
        if ext == "pdf":
            return self.pdf_read(file)
        elif ext == "docx":
            return self.docx_read(file)
        else:
            raise ValueError("Document is not supported!")