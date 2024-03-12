import requests
import datetime

url = 'https://dev.rightech.io/api/v1/objects/65d3418e5ef8890295f624d5'
headers = {
    'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2NWYwNmY5MGU2NWQ0ZjMxNGI4ZmQwNWYiLCJzdWIiOiI2NTk1YTE1ZjczNWY1ZDcxZTIwMWNhZmYiLCJncnAiOiI2NTk1YTE1ZjczNWY1ZDcxZTIwMWNhZmUiLCJvcmciOiI2NTk1YTE1ZjczNWY1ZDcxZTIwMWNhZmUiLCJsaWMiOiI1ZDNiNWZmMDBhMGE3ZjMwYjY5NWFmZTMiLCJ1c2ciOiJhcGkiLCJmdWxsIjpmYWxzZSwicmlnaHRzIjoxLjUsImlhdCI6MTcxMDI1NjAxNiwiZXhwIjoxNzEyNzc1NjAwfQ.y-uLltKvKDa_kRSQWnPha8vRJnuA6Sqr6eLIpULQQYU',
    'Content-Type': 'application/json'
}


def my_utc_from_timestamp(ts):
    return datetime.datetime.utcfromtimestamp(ts // 1000)


def timestamp_from_utc(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').timestamp()


def get_state(num):
    try:
        response = requests.get(url, headers=headers)
        # Проверяем успешность запроса
        if response.status_code == 200:
            data = response.json()  # Если ответ в формате JSON
            return (data["state"][f"temperature{num}"], data["state"][f"pressure{num}"])
        else:
            print(f'Ошибка запроса: {response.status_code}')
            print(response.text)

    except Exception as e:
        print(f'Произошла ошибка: {e}')