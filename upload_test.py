import requests
import os

API_BASE_URL = 'https://techvip.site/upload'
FILE_DOWNLOAD_BASE_URL = 'https://techvip.site/download'
local_file_path = r'D:\库\picture\天蝎座.png'

try:
    response = requests.post(f'{API_BASE_URL}/file-upload', data={
        'token': os.environ.get('TOKEN')
    }, files={
        'file': open(local_file_path, 'rb')
    })
    json_data = response.json()
    if json_data['code']==10000:
        print(f"{FILE_DOWNLOAD_BASE_URL}/{json_data['file']}")
    else:
        print(json_data['msg'])
except Exception as e:
    print(e)

