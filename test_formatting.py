#!/usr/bin/env python3

def format_search_results(results, query, search_type):
    """Format usersbox API results for Telegram"""
    if results.get('status') == 'error':
        return f"❌ *Ошибка:* {results.get('error', {}).get('message', 'Неизвестная ошибка')}"

    data = results.get('data', {})
    total_count = data.get('count', 0)
    
    if total_count == 0:
        return f"🔍 *Поиск:* `{query}`\n{search_type}\n\n❌ *Результатов не найдено*\n\n💡 *Попробуйте изменить формат запроса*"
    
    formatted_text = f"🎯 *РЕЗУЛЬТАТЫ ПОИСКА*\n\n"
    formatted_text += f"🔍 *Запрос:* `{query}`\n"
    formatted_text += f"📂 *Тип:* {search_type}\n"
    formatted_text += f"📊 *Найдено:* {total_count} записей\n\n"

    if 'items' in data and isinstance(data['items'], list):
        formatted_text += "📋 *ДАННЫЕ ИЗ БАЗ:*\n\n"
        
        for i, source_data in enumerate(data['items'][:5], 1):
            if 'source' in source_data and 'hits' in source_data:
                source = source_data['source']
                hits = source_data['hits']
                hits_count = hits.get('hitsCount', hits.get('count', 0))
                
                db_names = {
                    'yandex': '🟡 Яндекс',
                    'avito': '🟢 Авито',
                    'vk': '🔵 ВКонтакте',
                    'ok': '🟠 Одноклассники',
                    'delivery_club': '🍕 Delivery Club',
                    'cdek': '📦 СДЭК'
                }
                
                db_display = db_names.get(source.get('database', ''), f"📊 {source.get('database', 'N/A')}")
                
                formatted_text += f"*{i}. {db_display}*\n"
                formatted_text += f"📁 База: {source.get('collection', 'N/A')}\n"
                formatted_text += f"🔢 Записей: {hits_count}\n"

                if 'items' in hits and hits['items']:
                    formatted_text += "💾 *Данные:*\n"
                    for item in hits['items'][:2]:
                        for key, value in item.items():
                            if key.startswith('_'):
                                continue
                            
                            if key in ['phone', 'телефон', 'tel', 'mobile']:
                                formatted_text += f"📞 {value}\n"
                            elif key in ['email', 'почта', 'mail', 'e_mail']:
                                formatted_text += f"📧 {value}\n"
                            elif key in ['full_name', 'name', 'имя', 'фио', 'first_name', 'last_name']:
                                formatted_text += f"👤 {value}\n"
                            elif key in ['birth_date', 'birthday', 'дата_рождения', 'bdate']:
                                formatted_text += f"🎂 {value}\n"
                            elif key in ['address', 'адрес', 'city', 'город']:
                                formatted_text += f"🏠 {value}\n"
                            elif key in ['sex', 'gender', 'пол']:
                                gender_map = {'1': 'Ж', '2': 'М', 'male': 'М', 'female': 'Ж'}
                                formatted_text += f"⚥ {gender_map.get(str(value), value)}\n"
                
                formatted_text += "\n"

    formatted_text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    formatted_text += "🔒 *Конфиденциальность:* Используйте данные ответственно"
    
    return formatted_text

# Test with mock data
mock_response = {
    'status': 'success',
    'data': {
        'count': 3,
        'items': [
            {
                'source': {'database': 'yandex', 'collection': 'eda'},
                'hits': {
                    'hitsCount': 2,
                    'count': 2,
                    'items': [
                        {'phone': '+79123456789', 'first_name': 'Иван', 'email': 'test@mail.ru'},
                        {'phone': '+79987654321', 'first_name': 'Петр', 'city': 'Москва'}
                    ]
                }
            },
            {
                'source': {'database': 'avito', 'collection': 'users'},
                'hits': {
                    'hitsCount': 1,
                    'count': 1,
                    'items': [
                        {'phone': '+79123456789', 'full_name': 'Иван Петров', 'birth_date': '1990-01-01'}
                    ]
                }
            }
        ]
    }
}

if __name__ == "__main__":
    result = format_search_results(mock_response, 'test@mail.ru', '📧 Email')
    print('=== Форматированный результат ===')
    print(result)