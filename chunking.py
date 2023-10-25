def create_pdf_text_chunks(pdf_text, chunk_size = 200):
    # Split the PDF text into chunks
    chunks = [pdf_text[i:i + chunk_size] for i in range(0, len(pdf_text), chunk_size)]
    return chunks