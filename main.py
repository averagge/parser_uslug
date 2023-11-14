from bs4 import BeautifulSoup
import requests

url = "https://uslugio.com/"

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.837 YaBrowser/23.9.4.837 Yowser/2.5 Safari/537.36"}
req = requests.get("https://uslugio.com/", headers=headers)
soup = BeautifulSoup(req.content, "lxml")

city_links = []
city_list = soup.find_all("li")
for city in city_list:
    city_link = city.find("a").get("href")
    city_links.append(f"https://uslugio.com{city_link}")
for item in city_links:
    print(item)