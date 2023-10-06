import fitz  # PyMuPDF
import tabula
import pandas as pd


pdf_file = 'yourgpt_llm/data/v.pdf'
start_page = 90
end_page = 94

pdf_document = fitz.open(pdf_file)
text = ""
tables = []
for page_num in range(start_page - 1, end_page):
    #page = pdf_document.load_page(page_num)
    #text += page.get_text()
    tables += tabula.read_pdf(pdf_file, pages=page_num, stream=True)

    #print(text)

df = tables[0]
df_cleaned = df.dropna(axis=1)
print(df)

