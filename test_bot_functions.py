#!/usr/bin/env python3
"""
Тест функций Telegram бота УЗРИ
"""
import requests
import json
import time
import sys

WEBHOOK_URL = 'http://localhost:8001/api/webhook/usersbox_telegram_bot_secure_webhook_2025'

def send_update(update):
    """Отправить обновление в webhook"""
    try:
        response = requests.post(WEBHOOK_URL, json=update, timeout=10)
        print(f"✅ Status: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_start_command():
    """Тест команды /start"""
    print("\n🧪 Testing /start command...")
    
    update = {
        'update_id': 1001,
        'message': {
            'message_id': 1,
            'from': {
                'id': 987654321,
                'is_bot': False,
                'first_name': 'Иван',
                'username': 'test_ivan'
            },
            'chat': {
                'id': 987654321,
                'first_name': 'Иван',
                'username': 'test_ivan',
                'type': 'private'
            },
            'date': 1640995200,
            'text': '/start'
        }
    }
    
    return send_update(update)

def test_menu_callback():
    """Тест меню callbacks"""
    print("\n🧪 Testing menu callback...")
    
    update = {
        'update_id': 1002,
        'callback_query': {
            'id': 'test_callback_123',
            'from': {
                'id': 987654321,
                'is_bot': False,
                'first_name': 'Иван',
                'username': 'test_ivan'
            },
            'message': {
                'message_id': 2,
                'chat': {
                    'id': 987654321,
                    'type': 'private'
                }
            },
            'data': 'menu_pricing'
        }
    }
    
    return send_update(update)

def test_search_query():
    """Тест поискового запроса"""
    print("\n🧪 Testing search query...")
    
    update = {
        'update_id': 1003,
        'message': {
            'message_id': 3,
            'from': {
                'id': 987654321,
                'is_bot': False,
                'first_name': 'Иван',
                'username': 'test_ivan'
            },
            'chat': {
                'id': 987654321,
                'first_name': 'Иван',
                'username': 'test_ivan',
                'type': 'private'
            },
            'date': 1640995200,
            'text': '+79123456789'
        }
    }
    
    return send_update(update)

def test_payment_callback():
    """Тест payment callbacks"""
    print("\n🧪 Testing payment callback...")
    
    update = {
        'update_id': 1004,
        'callback_query': {
            'id': 'test_payment_callback',
            'from': {
                'id': 987654321,
                'is_bot': False,
                'first_name': 'Иван',
                'username': 'test_ivan'
            },
            'message': {
                'message_id': 4,
                'chat': {
                    'id': 987654321,
                    'type': 'private'
                }
            },
            'data': 'pay_stars'
        }
    }
    
    return send_update(update)

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов Telegram бота УЗРИ")
    print("=" * 50)
    
    tests = [
        ("Start Command", test_start_command),
        ("Menu Callback", test_menu_callback),
        ("Search Query", test_search_query),
        ("Payment Callback", test_payment_callback)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        if test_func():
            passed += 1
            print(f"✅ {test_name} - PASSED")
        else:
            print(f"❌ {test_name} - FAILED")
        
        time.sleep(1)  # Небольшая пауза между тестами
    
    print("\n" + "=" * 50)
    print(f"📊 РЕЗУЛЬТАТЫ: {passed}/{total} тестов прошли успешно")
    
    if passed == total:
        print("🎉 Все тесты прошли успешно!")
        return True
    else:
        print("⚠️  Некоторые тесты не прошли")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)