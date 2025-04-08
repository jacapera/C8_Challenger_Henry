import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from main import Chatbot

@pytest.fixture
def chatbot():
    return Chatbot()

def test_init(chatbot):
    assert chatbot.conversation_history == []

@patch('requests.post')
def test_search_internet(mock_post, chatbot):
    # Mock de respuesta de Serper
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'organic': [
            {'title': 'Test Title 1', 'link': 'http://test1.com'},
            {'title': 'Test Title 2', 'link': 'http://test2.com'}
        ]
    }
    mock_post.return_value = mock_response

    results = chatbot.search_internet("test query")
    assert len(results) == 2
    assert results[0]['title'] == 'Test Title 1'
    assert results[0]['link'] == 'http://test1.com'

@patch('requests.get')
def test_extract_text_from_url(mock_get, chatbot):
    # Mock de respuesta HTML
    mock_response = MagicMock()
    mock_response.text = """
    <html>
        <body>
            <script>console.log('test')</script>
            <p>Test content</p>
        </body>
    </html>
    """
    mock_get.return_value = mock_response

    text = chatbot.extract_text_from_url("http://test.com")
    assert "Test content" in text
    assert "console.log" not in text

def test_conversation_history(chatbot):
    # Simular una conversación
    with patch.object(chatbot, 'search_internet', return_value=[]):
        with patch.object(chatbot, 'stream_response', return_value="Test response"):
            chatbot.chat("Test question")

    assert len(chatbot.conversation_history) == 2
    assert chatbot.conversation_history[0]['role'] == 'user'
    assert chatbot.conversation_history[0]['content'] == 'Test question'
    assert chatbot.conversation_history[1]['role'] == 'assistant'
    assert chatbot.conversation_history[1]['content'] == 'Test response'