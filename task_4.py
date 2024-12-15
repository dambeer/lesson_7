# 4) Написать программу, которая будет заходить на сайт с новостями: https://www.Benzinga.com/markets
# С помощью python и bs4 нужно забрать с главной страницы:
# - заголовок новости (если есть)
# - текст новости (если есть)
# - ссылку на новость
# Данные нужно сохранять в csv таблицу с колонками:
# время,заголовок новости,текст новости,ссылка
# время использовать то, в которое спарсили новость.

# Программа должна обновлять csv таблицу раз в N секунд (пареметр должен быть настраиваемым)
# Если новость уже есть в таблице, её добавлять заново не нужно


import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
import os
import csv
from datetime import datetime
import time

url = "https://www.Benzinga.com/markets"
headers = {
    "content-type": "application/json; charset=UTF-8",
    "user-agent": UserAgent().random,
}
default_path = os.path.join("./lesson_7")
selectors = {
    "card": ".content-feed-list .newsfeed-card",
    "card-title": ".post-card-title",
    "card-text": ".post-teaser",
    "card-link": ".post-card-article-link",
}
time_update = int(input("Введите интервал обновления в минутах: "))


def get_articles(selectors=selectors):
    try:
        response = requests.get(
            url,
            headers=headers,
        )

        if response.status_code == 200:
            soup = BS(response.content, "html.parser")
            cards = []

            for card_html in soup.select(selectors["card"]):
                title_element = card_html.select_one(selectors["card-title"])
                text_element = card_html.select_one(selectors["card-text"])
                link_element = card_html.select_one(selectors["card-link"])

                cards.append(
                    {
                        "title": (
                            title_element.get_text(strip=True)
                            if title_element
                            else None
                        ),
                        "text": (
                            text_element.get_text(strip=True) if text_element else None
                        ),
                        "link": link_element["href"] if link_element else None,
                    }
                )
            return cards

    except Exception as e:
        print(f"Ошибка: {e}")


def write_csv(articles, filepath):
    fieldnames = ["Время", "Заголовок", "Текст", "Ссылка"]
    # Если файл не существует, создаем его с заголовком
    if not os.path.exists(filepath):
        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    # Добавление новых записей
    with open(filepath, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for article in articles:
            print(f"Добавление новости: {article['title']}")
            writer.writerow(
                {
                    "Время": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "Заголовок": article["title"],
                    "Текст": article["text"],
                    "Ссылка": article["link"],
                }
            )


def get_existing_links(filepath):
    if not os.path.exists(filepath):
        return set()

    with open(filepath, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return {row["Ссылка"] for row in reader}


def main(filename):
    while True:  # Бесконечный цикл
        filepath = os.path.join(default_path, filename)
        existing_links = get_existing_links(filepath)
        articles = get_articles()

        new_articles = [
            article for article in articles if article["link"] not in existing_links
        ]

        if new_articles:  # записываем только новые статьи
            write_csv(
                new_articles, os.path.join(default_path, "news.csv")
            )  # записываем в новый файл с текущей датой и временем
        else:
            print("Новых новостей нет")

        print(
            f"Следующее обновление через {time_update} минут..."
        )  # выводим сообщение о следующем обновлении

        time.sleep(time_update * 60)


main("news.csv")
# write_csv(get_articles())
