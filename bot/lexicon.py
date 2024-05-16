from typing import Dict

LEXICON: Dict[str, str] = {
    '/start': 'Здравствуйте! 👋\nЭтот бот предназначен для отслеживания новых объявлений на Авито. Чтобы начать отслеживание, добавьте интересующие Вас ссылки и нажмите *Начать отслеживание*.',
    'list_entry': '*Список отслеживаемых ссылок:*\n\n',
    'paste_new_link': 'Пожалуйста, отправьте полную ссылку на поисковую выдачу, которую хотите отслеживать. Она должна начинаться на "https…"',
    'paste_new_heading': 'Пожалуйста, напишите, как бы Вы хотели назвать ссылку?',
    'error_paste_new_link': 'Ссылка не корректна. Пожалуйста, проверьте ещё раз: ссылка должна быть полной и начинаться на "_https…_"',
    'empty_links': 'Отслеживаемые ссылки отсутствуют.',
    'existing_link': 'Данная ссылка уже отслеживается.',
    'abort': 'Действие отменено.',
    'success_new_link': 'Ссылка успешно добавлена.',
    'number_remove_link': 'Пожалуйста, введите номер ссылки, которую Вы хотите удалить.',
    'bad_number': 'Введённое Вами не является натуральным числом.',
    'not_existing_number': 'Такого номера не существует.',
    'success_remove_link': 'Ссылка успешно удалена.',
    'begin_tracking': 'Отслеживание объявлений активировано.',
    'stop_tracking': 'Отслеживание объявлений приостановлено.',
    'enter_new_freq': 'Пожалуйста, введите новую частоту отслеживания *в минутах*. Частота отслеживания должна быть *не меньше*, чем раз в *10 минут*.',
    'success_change_freq': 'Частота отслеживаний успешно обновлена с {prev_freq} мин. на {new_freq} мин.',
    'not_one_link': 'Данная функция пока что работает лишь с одной ссылкой.',
    'loading_realty': 'База данных создаётся, подождите, пожалуйста…',
    'bad_frequency': 'Введённое Вами не удовлетворяет условиям ввода.'
}
