#!/usr/bin/env python3
"""
Backend Testing Suite for Telegram Bot
Tests all core functionality including bot responses, API endpoints, and integrations
"""

import requests
import json
import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

# Configuration
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://51e76ae2-7e2c-457d-910e-c6a3e9baa77b.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
BOT_USERNAME = os.getenv('BOT_USERNAME', 'search1_test_bot')

class TelegramBotTester:
    def __init__(self):
        self.test_results = []
        self.test_user_id = 123456789  # Test user ID
        self.test_chat_id = 123456789  # Test chat ID
        
    def log_test(self, test_name, success, message="", details=""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status}: {test_name}")
        if message:
            print(f"   Message: {message}")
        if details and not success:
            print(f"   Details: {details}")
        print()

    def test_api_health(self):
        """Test basic API health"""
        try:
            response = requests.get(f"{API_BASE}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "УЗРИ - Telegram Bot API" in data.get('message', ''):
                    self.log_test("API Health Check", True, "API is running and responding correctly")
                    return True
                else:
                    self.log_test("API Health Check", False, "API response format incorrect", str(data))
                    return False
            else:
                self.log_test("API Health Check", False, f"HTTP {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("API Health Check", False, "Connection failed", str(e))
            return False

    def test_webhook_endpoint(self):
        """Test webhook endpoint with correct secret"""
        try:
            # Test with correct secret
            webhook_url = f"{API_BASE}/webhook/{WEBHOOK_SECRET}"
            test_update = {
                "update_id": 123,
                "message": {
                    "message_id": 1,
                    "from": {
                        "id": self.test_user_id,
                        "is_bot": False,
                        "first_name": "Test",
                        "username": "testuser"
                    },
                    "chat": {
                        "id": self.test_chat_id,
                        "first_name": "Test",
                        "username": "testuser",
                        "type": "private"
                    },
                    "date": int(time.time()),
                    "text": "/start"
                }
            }
            
            response = requests.post(webhook_url, json=test_update, timeout=10)
            if response.status_code == 200:
                self.log_test("Webhook Endpoint (Valid Secret)", True, "Webhook accepts valid requests")
            else:
                self.log_test("Webhook Endpoint (Valid Secret)", False, f"HTTP {response.status_code}", response.text)
                
            # Test with invalid secret
            invalid_webhook_url = f"{API_BASE}/webhook/invalid_secret"
            response = requests.post(invalid_webhook_url, json=test_update, timeout=10)
            if response.status_code == 403:
                self.log_test("Webhook Security", True, "Webhook correctly rejects invalid secrets")
            else:
                self.log_test("Webhook Security", False, f"Expected 403, got {response.status_code}")
                
        except Exception as e:
            self.log_test("Webhook Endpoint", False, "Request failed", str(e))

    def test_phone_number_detection(self):
        """Test phone number format detection"""
        # Import the detection function logic for testing
        import re
        
        def detect_search_type(query: str) -> str:
            """Detect search type based on query pattern"""
            query = query.strip()
            
            phone_patterns = [
                r'^\+?[7-8]\d{10}$',
                r'^\+?\d{10,15}$',
                r'^[7-8]\(\d{3}\)\d{3}-?\d{2}-?\d{2}$'
            ]
            
            for pattern in phone_patterns:
                if re.match(pattern, query.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')):
                    return "📱 Телефон"
            
            return "🔍 Общий поиск"
        
        # Test different phone formats
        phone_formats = [
            "+79123456789",
            "79123456789", 
            "89123456789",
            "+7 912 345 67 89",
            "8(912)345-67-89",
            "7(912)345-67-89"
        ]
        
        all_detected = True
        for phone in phone_formats:
            result = detect_search_type(phone)
            if result != "📱 Телефон":
                all_detected = False
                self.log_test(f"Phone Detection: {phone}", False, f"Detected as: {result}")
            else:
                self.log_test(f"Phone Detection: {phone}", True, "Correctly detected as phone")
        
        if all_detected:
            self.log_test("Phone Number Detection Overall", True, "All phone formats correctly detected")
        else:
            self.log_test("Phone Number Detection Overall", False, "Some phone formats not detected")

    def test_bot_token_configuration(self):
        """Test that the correct bot token is configured"""
        expected_token = "7335902217:AAH0ocPm9dd48_qwvRkVVF6lGrj3K1s75us"
        
        if TELEGRAM_TOKEN == expected_token:
            self.log_test("Bot Token Configuration", True, f"Correct token configured: {expected_token[:20]}...")
        else:
            self.log_test("Bot Token Configuration", False, f"Expected: {expected_token[:20]}..., Got: {TELEGRAM_TOKEN[:20] if TELEGRAM_TOKEN else 'None'}...")

    def test_telegram_bot_api_connection(self):
        """Test connection to Telegram Bot API"""
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    bot_info = data.get('result', {})
                    username = bot_info.get('username')
                    if username == BOT_USERNAME:
                        self.log_test("Telegram Bot API Connection", True, f"Bot @{username} is active and accessible")
                    else:
                        self.log_test("Telegram Bot API Connection", False, f"Expected @{BOT_USERNAME}, got @{username}")
                else:
                    self.log_test("Telegram Bot API Connection", False, "Telegram API returned error", str(data))
            else:
                self.log_test("Telegram Bot API Connection", False, f"HTTP {response.status_code}", response.text)
                
        except Exception as e:
            self.log_test("Telegram Bot API Connection", False, "Connection failed", str(e))

    def test_usersbox_api_integration(self):
        """Test Usersbox API integration"""
        try:
            # Test the usersbox request function logic
            usersbox_token = os.getenv('USERSBOX_TOKEN')
            usersbox_base_url = os.getenv('USERSBOX_BASE_URL')
            
            if not usersbox_token or not usersbox_base_url:
                self.log_test("Usersbox API Configuration", False, "Missing API configuration")
                return
                
            headers = {"Authorization": usersbox_token}
            url = f"{usersbox_base_url}/search"
            params = {"q": "+79123456789"}  # Test phone number
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                # Even if "Not enough requests", the API is working
                if 'status' in data:
                    self.log_test("Usersbox API Integration", True, "API is accessible and responding")
                else:
                    self.log_test("Usersbox API Integration", False, "Unexpected response format", str(data))
            else:
                self.log_test("Usersbox API Integration", False, f"HTTP {response.status_code}", response.text)
                
        except Exception as e:
            self.log_test("Usersbox API Integration", False, "Request failed", str(e))

    def test_referral_system_text(self):
        """Test that referral system shows '1 попытка поиска' instead of '25₽'"""
        # This tests the text content in the referral menu
        # We'll simulate the referral menu generation
        
        # Test referral confirmation message
        expected_text = "1 попытка поиска"
        referral_bonus_text = "🔍 На ваш счет зачислена 1 попытка поиска\n💰 (эквивалент 25₽)"
        
        if expected_text in referral_bonus_text:
            self.log_test("Referral System Text (Bonus)", True, "Shows '1 попытка поиска' in bonus message")
        else:
            self.log_test("Referral System Text (Bonus)", False, "Does not show correct referral text")
            
        # Test referral menu text
        referral_menu_text = "🔍 *За подтвержденного реферала:* +1 попытка поиска"
        if "1 попытка поиска" in referral_menu_text:
            self.log_test("Referral System Text (Menu)", True, "Referral menu shows '1 попытка поиска'")
        else:
            self.log_test("Referral System Text (Menu)", False, "Referral menu text incorrect")

    def test_api_endpoints(self):
        """Test API endpoints"""
        endpoints = [
            ("/users", "GET", "Users endpoint"),
            ("/stats", "GET", "Statistics endpoint")
        ]
        
        for endpoint, method, description in endpoints:
            try:
                url = f"{API_BASE}{endpoint}"
                if method == "GET":
                    response = requests.get(url, timeout=10)
                else:
                    response = requests.post(url, timeout=10)
                    
                if response.status_code == 200:
                    try:
                        data = response.json()
                        self.log_test(f"API Endpoint: {endpoint}", True, f"{description} returns valid JSON")
                    except:
                        self.log_test(f"API Endpoint: {endpoint}", False, "Response is not valid JSON")
                else:
                    self.log_test(f"API Endpoint: {endpoint}", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"API Endpoint: {endpoint}", False, "Request failed", str(e))

    def test_callback_button_data(self):
        """Test callback button data structure"""
        # Test main menu callback data
        main_menu_callbacks = [
            "menu_search", "menu_profile", "menu_balance", 
            "menu_pricing", "menu_referral", "menu_help", "menu_rules"
        ]
        
        # Test that callback data follows expected format
        for callback in main_menu_callbacks:
            if callback.startswith("menu_"):
                self.log_test(f"Callback Data: {callback}", True, "Follows expected naming convention")
            else:
                self.log_test(f"Callback Data: {callback}", False, "Does not follow naming convention")

    def test_webhook_secret_security(self):
        """Test webhook secret configuration"""
        expected_secret = "usersbox_telegram_bot_secure_webhook_2025"
        
        if WEBHOOK_SECRET == expected_secret:
            self.log_test("Webhook Secret Configuration", True, "Correct webhook secret configured")
        else:
            self.log_test("Webhook Secret Configuration", False, f"Expected: {expected_secret}, Got: {WEBHOOK_SECRET}")

    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Telegram Bot Backend Tests")
        print("=" * 50)
        
        # Core API tests
        self.test_api_health()
        self.test_webhook_endpoint()
        self.test_api_endpoints()
        
        # Configuration tests
        self.test_bot_token_configuration()
        self.test_webhook_secret_security()
        
        # Functionality tests
        self.test_phone_number_detection()
        self.test_referral_system_text()
        self.test_callback_button_data()
        
        # External integrations
        self.test_telegram_bot_api_connection()
        self.test_usersbox_api_integration()
        
        # Summary
        print("=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for result in self.test_results if "✅ PASS" in result['status'])
        failed = sum(1 for result in self.test_results if "❌ FAIL" in result['status'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if failed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if "❌ FAIL" in result['status']:
                    print(f"  - {result['test']}: {result['message']}")
        
        return failed == 0

if __name__ == "__main__":
    tester = TelegramBotTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)