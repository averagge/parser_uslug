from bs4 import BeautifulSoup
import requests
import json
import os

def takeservice(category3):
    category3_link = category3.get("href")
    category3_name = category3.text.replace("/", "_")
    page = ""
    page_num = 1
    service = []
    while page_num < 8:
        try:
            req = requests.get(f"https://uslugio.com{category3_link}{page}", headers=headers)
            soup = BeautifulSoup(req.content, "lxml")
            uslugi = soup.find_all("div", class_="item_data")
            for usluga in uslugi:
                title = usluga.find("div", class_="title showone").find("b").text
                adress = usluga.find("span", class_="addres").text
                description = usluga.find("div", class_="truncate-text").text.replace("\r", "")
                description = description.replace("\n", "")
                phone = usluga.find("strong", title="Номер телефона исполнителя").text
                try:
                    name = usluga.find("span", title="Имя исполнителя").text
                except Exception:
                    name = "No name"
                service.append(
                    {"title": title, "adress": adress, "description": description, "phone": phone,
                     "name": name})
            page_num += 1
            page = f"?page={page_num}"
        except Exception:
            break
    a = [category3_name, service]
    return a

url = "https://uslugio.com/"

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.837 YaBrowser/23.9.4.837 Yowser/2.5 Safari/537.36"}
req = requests.get("https://uslugio.com/", headers=headers)
soup = BeautifulSoup(req.content, "lxml")


city_list = soup.find_all("li")
for city in city_list:
    city_link = city.find("a").get("href")
    city_name = city.find("a").text
    os.mkdir(f"data/{city_name}")
    req = requests.get(f"https://uslugio.com{city_link}", headers=headers)
    soup = BeautifulSoup(req.content, "lxml")
    categories1 = soup.find("div", class_="row nav_cat_list").find_all("a")
    for category1 in categories1:
        category1_link = category1.get("href")
        category1_name = category1.text.replace("/", "_")
        os.mkdir(f"data/{city_name}/{category1_name}")
        req = requests.get(f"https://uslugio.com{category1_link}", headers=headers)
        soup = BeautifulSoup(req.content, "lxml")
        try:
            categories2 = soup.find("div", class_="row nav_cat_list").find_all("a")
            for category2 in categories2:
                category2_link = category2.get("href")
                category2_name = category2.text.replace("/", "_")
                os.mkdir(f"data/{city_name}/{category1_name}/{category2_name}")
                req = requests.get(f"https://uslugio.com{category2_link}", headers=headers)
                soup = BeautifulSoup(req.content, "lxml")
                try:
                    categories3 = soup.find("div", class_="row nav_theme").find_all("a")
                    for category3 in categories3:
                        category3_name = takeservice(category3)[0]
                        service = takeservice(category3)[1]
                        with open(f"data/{city_name}/{category1_name}/{category2_name}/{category3_name}.json", "w", encoding="utf-8") as file:
                            json.dump(service, file, indent=4, ensure_ascii=False)
                            print(f"Создан файл: data/{city_name}/{category1_name}/{category2_name}/{category3_name}.json")

                except Exception:
                    categories3 = soup.find("div", class_="row nav_cat_list").find_all("a")
                    for category3 in categories3:
                        category3_name = takeservice(category3)[0]
                        service = takeservice(category3)[1]
                        with open(f"data/{city_name}/{category1_name}/{category3_name}.json", "w", encoding="utf-8") as file:
                            json.dump(service, file, indent=4, ensure_ascii=False)
                            print(f"Создан файл: data/{city_name}/{category1_name}/{category3_name}.json")
        except Exception:
            req = requests.get(f"https://uslugio.com{category1_link}", headers=headers)
            soup = BeautifulSoup(req.content, "lxml")
            categories3 = soup.find("div", class_="row nav_theme").find_all("a")
            for category3 in categories3:
                category3_name = takeservice(category3)[0]
                service = takeservice(category3)[1]
                with open(f"data/{city_name}/{category1_name}/{category3_name}.json", "w",
                          encoding="utf-8") as file:
                    json.dump(service, file, indent=4, ensure_ascii=False)
                    print(f"Создан файл: data/{city_name}/{category1_name}/{category3_name}.json")