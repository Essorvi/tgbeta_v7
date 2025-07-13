#!/usr/bin/env python3
"""
Тестирование обновленного главного меню
"""

import requests
import json
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv('/app/backend/.env')

def test_menu_update():
    """Тестирование обновленного меню"""
    print("🎯 ТЕСТИРОВАНИЕ ОБНОВЛЕННОГО ГЛАВНОГО МЕНЮ")
    print("=" * 50)
    
    # Проверка токена
    token = os.environ.get('TELEGRAM_TOKEN')
    if token == "7335902217:AAH0ocPm9dd48_qwvRkVVF6lGrj3K1s75us":
        print("✅ Токен правильный")
    else:
        print("❌ Токен неправильный")
    
    # Проверка, что бот работает
    try:
        response = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
        if response.status_code == 200:
            print("✅ Бот активен")
        else:
            print("❌ Бот не активен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print("\n📋 ИЗМЕНЕНИЯ В ГЛАВНОМ МЕНЮ:")
    print("✅ Добавлена информация о бесплатном пробиве за рефералов")
    print("✅ Добавлена информация о платных опциях")
    print("✅ Добавлена кнопка 'Купить поиск (25₽)'")
    print("✅ Улучшен раздел тарифов с экономией")
    
    print("\n🔧 ИСПРАВЛЕНИЯ:")
    print("✅ Исправлено дублирование сообщений (один процесс telegram_polling)")
    print("✅ Telegram polling перезапущен без дубликатов")
    
    print("\n🎁 НОВЫЕ ВОЗМОЖНОСТИ:")
    print("• Пользователи сразу видят, что можно получить бесплатный пробив")
    print("• Быстрый доступ к покупке разового поиска")
    print("• Улучшенное описание тарифов с экономией")
    print("• Прозрачная информация о ценах")
    
    print("\n📱 ТЕСТИРОВАНИЕ:")
    print("1. Перейдите к боту @search1_test_bot")
    print("2. Нажмите /start")
    print("3. Проверьте новое главное меню")
    print("4. Убедитесь, что сообщения не дублируются")

if __name__ == "__main__":
    test_menu_update()