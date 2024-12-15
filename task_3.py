# 3) Зайти на сайт генерации юзернеймов: https://www.spinxo.com/
# Сгенерировать 100 рандомных юзернеймов и сохранить их в файл


import requests
import os

headers = {
    "content-type": "application/json; charset=UTF-8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36",
}
default_path = os.path.join("./lesson_7")

json_data = {
    "snr": {"Stub": "usernames", "Count": 100},
}

response = requests.post(
    "https://www.spinxo.com/services/NameService.asmx/GetNames",
    headers=headers,
    json=json_data,
)

if response.status_code == 200:
    data = response.json()
    with open(os.path.join(default_path, "names.txt"), "w") as f:
        f.write("\n".join(data["d"]["Names"]))
