import unittest
import sys
import os
import tempfile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools.pdf_loader import PDFLoader

class TestPDFLoader(unittest.TestCase):
    def setUp(self):
        self.pdf_loader = PDFLoader()

    def test_pdf_loader_initialization(self):
        """Test that PDFLoader initializes correctly"""
        self.assertIsNotNone(self.pdf_loader.text_splitter)
        self.assertEqual(self.pdf_loader.text_splitter._chunk_size, 1000)
        self.assertEqual(self.pdf_loader.text_splitter._chunk_overlap, 200)

    def test_load_and_split_with_sample_pdf(self):
        """Test loading and splitting the sample PDF"""
        pdf_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'documents', 'sample_document.pdf')
        
        if os.path.exists(pdf_path):
            chunks = self.pdf_loader.load_and_split(pdf_path)
            
            self.assertIsInstance(chunks, list)
            self.assertGreater(len(chunks), 0)
            
            # Check that chunks have content
            for chunk in chunks:
                self.assertTrue(hasattr(chunk, 'page_content'))
                self.assertTrue(hasattr(chunk, 'metadata'))
                self.assertIsInstance(chunk.page_content, str)
                self.assertGreater(len(chunk.page_content.strip()), 0)
        else:
            self.skipTest("Sample PDF not found")

if __name__ == '__main__':
    unittest.main()