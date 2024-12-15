# 2) Зайти на сайт с Риком и Морти: https://rickandmortyapi.com/
# **************** Усложню и разобью всех персонажей для всех эпизодов ****************
# Определить в каких эпизодах появлялся персонаж с главной страницы. Выгрузить все фотографии персонажей из данного эпизода в папку, которая называется episode_N (N - номер эпизода)
# Для создания папок используйте модуль os


from operator import ilshift
from tabnanny import check
import requests
import json
import os

url = "https://rickandmortyapi.com/graphql"
headers = {
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36",
}
characters_image_path = os.path.join("./lesson_7/images")


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


def get_characters(chr_count, headers=headers):
    try:
        if not chr_count:
            return

        json_data = {
            "query": """
                query randomCharacters($ids: [ID!]!) {
                  charactersByIds(ids: $ids) {
                    #   Запрашиваем только нужные поля
                    id
                    name
                    image
                    episode{
                        id
                    }
                  }
                }
            """,
            "variables": {
                "ids": list(range(1, chr_count + 1)),
            },
        }

        response = requests.post(url, headers=headers, json=json_data)

        data = response.json()

        if response.status_code == 200:
            characters = list()

            for character in data["data"]["charactersByIds"]:
                characters.append(
                    {
                        "name": f"{character['name']} #{character['id']}",
                        "image": character["image"],
                        "episode": character[
                            "episode"
                        ],  # Не получаем подробную информацию об эпизоде из-за разделения ответственности
                    }
                )

            return characters
        else:
            raise Exception(f"Ошибка запроса ({response.status_code}): {response}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


def get_ep_by_characters(characters, headers=headers):
    """Получение всех эпизодов по героям"""
    try:
        if not characters:
            return
        episode_ids = sorted(
            set(
                int(episode["id"])
                for character in characters
                for episode in character["episode"]
            )
        )

        json_data = {
            "query": """
                query randomCharacters($ids: [ID!]!) {
                    episodesByIds(ids: $ids) {
                        id
                        episode
                        characters {
                            id
                            name
                            image
                        }
                    }
                }
            """,
            "variables": {
                "ids": episode_ids,
            },
        }
        response = requests.post(url, headers=headers, json=json_data)

        if response.status_code == 200:
            data = response.json()
            eps_image_links = list()

            for episode in data["data"]["episodesByIds"]:
                eps_image_links.append(
                    {
                        "name": f"episode_{episode['episode']}",
                        "characters": episode["characters"],
                    }
                )

            # Можно сделать отдельную функцию для создания папки эпизода, я пропущу
            for episode in eps_image_links:
                print(f"\n\n Загрузка {episode['name']} \n\n")
                download_img_characters(
                    episode["characters"],
                    os.path.join(f"./lesson_7/episodes/{episode['name']}"),
                )
                print(f"\n\n Загрузка {episode['name']} закончена\n\n")
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
            file_name = f"{img_character['name']} #{img_character['id']}.{img_character['image'].split('.')[-1]}".replace(
                " ", "_"
            )
            check_file_path = os.path.join(f"{characters_image_path}/{file_name}")

            if not os.path.exists(check_file_path):
                print(f"Скачивание изображения {file_name}")

                response = requests.get(img_character["image"])
                if response.status_code == 200:
                    with open(os.path.join(path, file_name), "wb") as f:
                        f.write(response.content)
                        print(f"Изображение {file_name} загружено.")
                else:
                    raise Exception(
                        f"Ошибка запроса ({response.status_code}): {response}"
                    )
            else:
                print(f"\nИзображение {file_name} существует. Копируем")
                # Можно использовать для копирования shutil.copy2 (оптимальнее)
                # Использую более простой в данный момент. Менее производительно
                # Без чанков - файлы маленькие
                with open(check_file_path, "rb") as source, open(
                    os.path.join(path, file_name), "wb"
                ) as destination:
                    destination.write(source.read())
                print(f"Файл {check_file_path} скопирован в {destination}.\n")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке изображения: {e}")


characters = get_characters(get_count_characters())
print(f"Получение эпизодов для {len(characters)} персонажей")
episodes = get_ep_by_characters(characters)
