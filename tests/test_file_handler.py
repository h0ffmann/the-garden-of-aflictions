import pytest
from unittest.mock import mock_open, patch
from obsidian_analyzer.file_handler import read_file

class TestFileHandler:
    @patch('builtins.open', mock_open(read_data="Test content"))
    def test_read_txt_file(self):
        """Test reading txt file"""
        content = read_file("test.txt")
        assert content == "Test content"

    @patch('pypdf.PdfReader')
    @patch('os.path.join')
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.print')
    def test_read_pdf_file(self, mock_print, mock_isfile, mock_join, mock_pdf):
        """Test reading pdf file"""
        # Setup mock PDF reader
        mock_page = type('Page', (), {'extract_text': lambda self: "PDF content"})
        mock_pdf.return_value.pages = [mock_page()]
        mock_pdf.return_value.is_encrypted = False
    
        # Mock path joining to return the input path
        mock_join.side_effect = lambda *args: args[-1]
    
        # Mock the file handler to use our mocked PDF reader
        with patch('obsidian_analyzer.file_handler.PdfReader', mock_pdf):
            content = read_file("test.pdf")
            assert content == "PDF content"
            mock_print.assert_not_called()

    def test_read_nonexistent_file(self):
        """Test reading nonexistent file"""
        content = read_file("nonexistent.txt")
        assert content is None

    def test_read_unsupported_format(self):
        """Test reading unsupported file format"""
        content = read_file("test.unsupported")
        assert content is None
