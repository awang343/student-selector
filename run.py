import requests
from class_class import Class

lecture3 = Class("class_list.csv")
token = "7471389599:AAHs5JDdVqWIYgMQkLqNkUTwgGQO2IuCOnc"

url = f'https://api.telegram.org/bot{token}/sendMessage'
data = {'chat_id': {YOUR_CHAT_ID}, 'text': 'python msg'}
requests.post(url, data).json()

[lecture3.volunteer(id=i) for i in range(12)]
