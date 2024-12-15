# Практика:
# **************** Чуть усложнил и собрал вообще всех персонажей ****************
# 1) Зайти на сайт с Риком и Морти: https://rickandmortyapi.com/
# Выгрузить с сайта все изображения персонажей с главной страницы (задача делается через запросы, а не через BS4)

from operator import ilshift
import requests
import json
import os

url = "https://rickandmortyapi.com/graphql"
headers = {
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36",
}


def get_count_characters(headers=headers):
    try:
        # На основе docs API Rick and Morty
        json_data = {
            "query": """
                query {
                    characters {
                        info {
                            count
                        }
                    }
                }
            """
        }

        response = requests.post(url, headers=headers, json=json_data)

        if response.status_code == 200:
            count = response.json()["data"]["characters"]["info"]["count"]
            print(f"Количество персонажей: {count}")

            return count if count else count
        else:
            raise Exception(f"Ошибка запроса ({response.status_code}): {response}")

    except Exception as e:
        print(f"Не удалось получить общее количество персонажей: {e}")
        return False


# def get_img_characters(headers=headers):
#     try:
#         pass
#     except Exception as e:
#         print(f"Не удалось получить изображения персонажей: {e}")
#         return False


def get_img_characters(chr_count, headers=headers):
    try:
        if not chr_count:
            return

        json_data = {
            "query": """
                query allCharacters($ids: [ID!]!) {
                  charactersByIds(ids: $ids) {
                    #   Запрашиваем только нужные поля
                    id
                    name
                    image
                  }
                }
            """,
            "variables": {
                "ids": list(range(1, chr_count + 1)),
            },
        }

        response = requests.post(url, headers=headers, json=json_data)
        response.raise_for_status()
        data = response.json()

        if response.status_code == 200:
            images_links = list()

            for character in data["data"]["charactersByIds"]:
                images_links.append(
                    {
                        "name": f"{character['name']} #{character['id']}",
                        "src": character["image"],
                    }
                )

            return images_links
        else:
            raise Exception(f"Ошибка запроса ({response.status_code}): {response}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


def download_img_characters(img_characters, path):
    """Загружает изображение по URL и сохраняет в указанную папку."""

    try:
        # Создаём директорию, если она отсутствует
        os.makedirs(path, exist_ok=True)

        for img_character in img_characters:
            print(f"Скачивание изображения {img_character['name']}")

            response = requests.get(img_character["src"])
            if response.status_code == 200:
                file_name = os.path.join(
                    path,
                    f"{img_character['name'].replace(' ', '_')}.{img_character['src'].split('.')[-1]}",
                )
                with open(
                    file_name, "wb"
                ) as f:  # Открываем файл в бинарном режиме для записи
                    f.write(response.content)
                    print(f"Изображение {file_name} загружено.")
            else:
                raise Exception(f"Ошибка запроса ({response.status_code}): {response}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке изображения: {e}")


# get_and_download_characters(get_count_characters(headers))
img_characters = get_img_characters(get_count_characters(headers))
print(f"Передача {len(img_characters)} объектов в закачку \n\n")
download_img_characters(img_characters, os.path.join("lesson_7", "images"))
