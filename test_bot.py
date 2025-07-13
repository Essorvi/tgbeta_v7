#!/usr/bin/env python3
"""
Тестирование функций телеграм бота
"""

import requests
import json
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv('/app/backend/.env')

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
USERSBOX_TOKEN = os.environ['USERSBOX_TOKEN']
USERSBOX_BASE_URL = os.environ['USERSBOX_BASE_URL']

def test_phone_detection():
    """Тестирование распознавания телефонных номеров"""
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
    
    test_phones = [
        "+79123456789",
        "79123456789",
        "89123456789",
        "7(912)345-67-89",
        "8(912)345-67-89",
        "+7 912 345 67 89",
        "79123456789",
        "89123456789"
    ]
    
    print("=== ТЕСТИРОВАНИЕ РАСПОЗНАВАНИЯ ТЕЛЕФОНОВ ===")
    for phone in test_phones:
        result = detect_search_type(phone)
        print(f"Номер: {phone:20} -> {result}")
    
    return True

def test_usersbox_api():
    """Тестирование API Usersbox"""
    headers = {"Authorization": USERSBOX_TOKEN}
    url = f"{USERSBOX_BASE_URL}/search"
    
    # Тестовые номера
    test_numbers = [
        "+79123456789",
        "79123456789",
        "89123456789"
    ]
    
    print("\n=== ТЕСТИРОВАНИЕ API USERSBOX ===")
    for phone in test_numbers:
        try:
            response = requests.get(url, headers=headers, params={"q": phone}, timeout=10)
            data = response.json()
            
            print(f"\nНомер: {phone}")
            print(f"Статус: {response.status_code}")
            print(f"Ответ: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            if response.status_code == 200:
                if data.get('status') == 'success':
                    count = data.get('data', {}).get('count', 0)
                    print(f"✅ Найдено записей: {count}")
                else:
                    print(f"❌ Ошибка: {data.get('error', {}).get('message', 'Unknown')}")
            else:
                print(f"❌ HTTP ошибка: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка запроса: {e}")
        
        print("-" * 50)

def test_telegram_bot():
    """Тестирование Telegram бота"""
    print("\n=== ТЕСТИРОВАНИЕ TELEGRAM БОТА ===")
    
    # Проверка, что бот активен
    try:
        response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe", timeout=10)
        if response.status_code == 200:
            bot_info = response.json()
            print(f"✅ Бот активен: {bot_info['result']['username']}")
        else:
            print(f"❌ Бот не активен: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка проверки бота: {e}")

if __name__ == "__main__":
    print("Запуск тестов...")
    
    # Тест 1: Распознавание телефонов
    test_phone_detection()
    
    # Тест 2: API Usersbox
    test_usersbox_api()
    
    # Тест 3: Telegram бот
    test_telegram_bot()
    
    print("\n=== ТЕСТИРОВАНИЕ ЗАВЕРШЕНО ===")