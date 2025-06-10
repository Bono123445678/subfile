import requests
import json

# بيانات التطبيق (من صفحة تطبيق Reddit الذي أنشأته)
CLIENT_ID = 'RmYerz8EE1Sq4Wa6UrE4sg'
CLIENT_SECRET = 'DUf252nwhwTvlY8lOsn55m7SWTh1kQ'
USER_AGENT = 'homar'  # يمكن وضع أي اسم هنا
REDIRECT_URI = 'http://localhost:8000'

# بيانات الحساب (username و password)
USERNAME = 'Ok-Coach-8130'
PASSWORD = 'Raromero*084/123'

# نقطة النهاية للحصول على التوكن
token_url = 'https://www.reddit.com/api/v1/access_token'

# البيانات التي نحتاج لإرسالها
data = {
    'grant_type': 'password',
    'username': USERNAME,
    'password': PASSWORD,
}

# الهيدر الذي يطلبه Reddit
headers = {
    'User-Agent': USER_AGENT
}

# المعرّف (client_id) و السر (client_secret)
auth = (CLIENT_ID, CLIENT_SECRET)

# إرسال الطلب للحصول على التوكن
response = requests.post(token_url, data=data, headers=headers, auth=auth)

# التحقق من الاستجابة وطباعة التوكن
if response.status_code == 200:
    access_token = response.json()['access_token']
    print(f"Your access token is: {access_token}")
else:
    print(f"Failed to get token: {response.status_code}")
    print(response.json())
