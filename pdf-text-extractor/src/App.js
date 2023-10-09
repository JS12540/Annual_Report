import React, { useState } from 'react';
import './PdfTextExtractor.css';

function PdfTextExtractor() {
  const [pdfFile, setPdfFile] = useState(null);
  const [startPage, setStartPage] = useState('');
  const [endPage, setEndPage] = useState('');
  const [extractedText, setExtractedText] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setPdfFile(file);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('pdf_path', pdfFile);
    formData.append('start_page', startPage);
    formData.append('end_page', endPage);

    try {
      const response = await fetch('http://localhost:8000/extract-text/', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setExtractedText(data.text);
      } else {
        alert('Error extracting text from PDF');
      }
    } catch (error) {
      alert('An error occurred: ' + error.message);
    }
  };

  return (
    <div className="pdf-text-extractor">
      <h1>PDF Text Extractor</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          required
        />
        <br />
        <br />
        <div className="page-inputs">
          <div className="page-input">
            Start Page:{' '}
            <input
              type="number"
              value={startPage}
              onChange={(e) => setStartPage(e.target.value)}
              required
            />
          </div>
          <div className="page-input">
            End Page:{' '}
            <input
              type="number"
              value={endPage}
              onChange={(e) => setEndPage(e.target.value)}
              required
            />
          </div>
        </div>
        <br />
        <button type="submit">Extract Text</button>
      </form>
      {extractedText && (
        <div className="result">
          <h2>Extracted Text:</h2>
          <pre>{extractedText}</pre>
        </div>
      )}
    </div>
  );
}

export default PdfTextExtractor;
