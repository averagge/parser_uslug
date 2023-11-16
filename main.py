from bs4 import BeautifulSoup
import requests
import os

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
                        category3_link = category3.get("href")
                        category3_name = category3.text.replace("/", "_")
                        os.mkdir(f"data/{city_name}/{category1_name}/{category2_name}/{category3_name}")
                        print(f"Создана папка: data/{city_name}/{category1_name}/{category2_name}/{category3_name}")
                except Exception:
                    continue
        except Exception:
            req = requests.get(f"https://uslugio.com{category1_link}", headers=headers)
            soup = BeautifulSoup(req.content, "lxml")
            categories3 = soup.find("div", class_="row nav_theme").find_all("a")
            for category3 in categories3:
                category3_link = category3.get("href")
                category3_name = category3.text.replace("/", "_")
                os.mkdir(f"data/{city_name}/{category1_name}/{category3_name}")
                print(f"Создана папка: data/{city_name}/{category1_name}/{category3_name}")




