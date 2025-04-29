"""Tests for WhatsApp messaging module"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.messaging import WhatsAppMessaging, MessageHandler
from modules.session import BookingState, UserSession

class TestWhatsAppMessaging(unittest.TestCase):
    """Test WhatsApp messaging functionality"""
    
    @patch('modules.messaging.Client')
    def test_send_message(self, mock_client):
        """Test sending a WhatsApp message"""
        # Setup
        mock_messages = MagicMock()
        mock_client.return_value.messages = mock_messages
        mock_messages.create.return_value = MagicMock(sid='TEST_SID')
        
        # Execute
        messaging = WhatsAppMessaging()
        result = messaging.send_message('+1234567890', 'Test message')
        
        # Assert
        self.assertTrue(result)
        mock_messages.create.assert_called_once()
        
    @patch('modules.messaging.Client')
    def test_send_message_with_error(self, mock_client):
        """Test sending a WhatsApp message with error"""
        # Setup
        mock_messages = MagicMock()
        mock_client.return_value.messages = mock_messages
        mock_messages.create.side_effect = Exception("Test error")
        
        # Execute
        messaging = WhatsAppMessaging()
        result = messaging.send_message('+1234567890', 'Test message')
        
        # Assert
        self.assertFalse(result)

class TestMessageHandler(unittest.TestCase):
    """Test message handling functionality"""
    
    @patch('modules.messaging.WhatsAppMessaging')
    @patch('modules.messaging.session_manager')
    def test_handle_wretro_message(self, mock_session_manager, mock_messaging):
        """Test handling #WRETRO message in initial state"""
        # Setup
        mock_session = MagicMock()
        mock_session.state = BookingState.INITIAL
        mock_session_manager.get_session.return_value = mock_session
        
        # Execute
        handler = MessageHandler()
        handler.messaging = mock_messaging
        handler.handle_message('+1234567890', '#WRETRO')
        
        # Assert
        mock_messaging.send_terms_and_conditions.assert_called_once_with('+1234567890', 'WRETRO')
        mock_session.update_state.assert_called_once_with(BookingState.ACCEPTED_TERMS)
        mock_session.update_data.assert_called_once_with('show_type', 'WRETRO')

if __name__ == '__main__':
    unittest.main() 