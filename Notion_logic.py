import requests
from datetime import datetime


DATA_BASE_ID 
NOTION_TOKEN 

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}


def get_info():
    """
    Получениие JSON c Notion
    """
    payload = {"page_size": 100}
    url = f"https://api.notion.com/v1/databases/{DATA_BASE_ID}/query"
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


#  with open('notion.json', 'w', encoding='utf-8') as f:
#  json.dump(get_info(), f, ensure_ascii=False, indent=4)


def date_check(test_date):
    """
    Проверка просрочки
    """
    now = datetime.now()
    test_date = datetime.strptime(test_date, "%Y-%m-%d")

    if (now - test_date).days == 0:
        return "flag"

    return now > test_date


def form_message(properties, flag=None):
    """
    Формирование сообщения для отправки
    """
    date = datetime.strptime(properties["ПДО"]["date"]["start"],
                             "%Y-%m-%d").strftime('%d/%m/%Y')

    try:
        name = properties["Клиент"]["title"][0]["text"]["content"]
    except IndexError:
        return ("Одно из значений в колонке \"Клиент\" отсутсвует. "
                f"Значение в столбце \"ПДО\": {date}. "
                "Пожалуйста, укажите наименование клиента в Notion таблице.")

    summ = properties["СУММА"]["number"]
    if not summ:
        return (f'У должника: {name} не указана сумма долга. '
                f"Значение в столбце \"ПДО\": {date}. "
                'Пожалуйста, укажите нужную сумму в Notion таблице')

    if flag == 'flag':
        return (f'Здравствуйте, {name}!\n'
                'Сегодня Вы должны провести оплату на '
                f'сумму : {summ}. Просьба провести ее в ближайшее время.')

    return (f'Здравствуйте, {name}!\n'
            f'Вы должны были провести оплату: {date} '
            f'на сумму: {summ}. Просьба провести ее в ближайшее время.')


def get_message():
    """
    Получение нужных данных из JSON
    """
    one_day_messages = []
    messages = []

    for page in get_info()['results']:
        properties = page['properties']

        try:
            date = properties['ПДО']['date']['start']
        except TypeError:
            alarm = ('В Notion таблице поле \"ПДО\" отсутвует. '
                     'Пожалуйста проверьте таблицу.')
            messages.append(alarm), one_day_messages.append(alarm)
            continue

        if date_check(date) == "flag":
            one_day_messages.append(form_message(properties, "flag"))
            messages.append(form_message(properties, "flag"))
            continue

        if date_check(date):
            messages.append(form_message(properties))

    return [messages, one_day_messages]
