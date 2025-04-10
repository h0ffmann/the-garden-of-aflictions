import pytest
from unittest.mock import mock_open, patch
from obsidian_analyzer.file_handler import read_file

class TestFileHandler:
    @patch('builtins.open', mock_open(read_data="Test content"))
    def test_read_txt_file(self):
        """Test reading txt file"""
        content = read_file("test.txt")
        assert content == "Test content"

    @patch('PyPDF2.PdfReader')
    def test_read_pdf_file(self, mock_pdf):
        """Test reading pdf file"""
        mock_page = type('Page', (), {'extract_text': lambda self: "PDF content"})
        mock_pdf.return_value.pages = [mock_page()]
        
        content = read_file("test.pdf")
        assert content == "PDF content"

    def test_read_nonexistent_file(self):
        """Test reading nonexistent file"""
        content = read_file("nonexistent.txt")
        assert content is None

    def test_read_unsupported_format(self):
        """Test reading unsupported file format"""
        content = read_file("test.unsupported")
        assert content is None
