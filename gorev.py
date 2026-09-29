import requests
from bs4 import BeautifulSoup
import csv
import time


# Görev1: Alıntıları Çekme

response = requests.get("https://quotes.toscrape.com")
soup = BeautifulSoup(response.text, "html.parser")


alıntilar = soup.find_all("div", class_="quote")

for alinti in alıntilar:
    metin = alinti.find("span", class_="text").get_text()
    yazar = alinti.find("small", class_="author").get_text()

    etiket_str = ""
    for e in alinti.find_all("a", class_="tag"):
        etiket_str += e.get_text() + " "

    print(yazar, metin, etiket_str)


# Görev2: csv ye kaydetme

yildiz_sayisi = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

tum_kitaplar = []
sayfa_url = "https://books.toscrape.com/catalogue/page-1.html"

while True:
    response = requests.get(sayfa_url)
    soup = BeautifulSoup(response.text, "html.parser")

    for kitap in soup.find_all("article", class_="product_pod"):
        ad = kitap.find("h3").find("a")["title"]

        fiyat = kitap.find("p", class_="price_color").get_text()
        fiyat = fiyat.replace("£", "").replace("Â", "").strip()
        fiyat = float(fiyat)

        stok = kitap.find("p", class_="instock").get_text().strip()

        yildiz_kelime = kitap.find("p", class_="star-rating")["class"][1]
        yildiz = yildiz_sayisi[yildiz_kelime]

        tum_kitaplar.append([ad, fiyat, stok, yildiz])

    sonraki = soup.find("li", class_="next")
    if sonraki:
        sonraki_href = sonraki.find("a")["href"]
        sayfa_url = "https://books.toscrape.com/catalogue/" + sonraki_href
        time.sleep(0.5)
    else:
        break

with open("kitaplar.csv", "w", newline="") as f:
    yazici = csv.writer(f)
    yazici.writerow(["ad", "fiyat", "stok", "yildiz"])
    yazici.writerows(tum_kitaplar)



# Görev3: veri analizi

print("Toplam kitap sayısı:", len(tum_kitaplar))

toplam_fiyat = 0
for k in tum_kitaplar:
    toplam_fiyat += k[1]
ortalama = toplam_fiyat / len(tum_kitaplar)
print("Ortalama fiyat:", round(ortalama, 2))

sirali = sorted(tum_kitaplar, key=lambda k: k[1], reverse=True)
print("En pahalı 5 kitap:")
for i in range(5):
    print(i + 1, sirali[i][0], sirali[i][1])

bes_yildizli = 0
for k in tum_kitaplar:
    if k[3] == 5:
        bes_yildizli += 1
print("5 yıldızlı kitap sayısı:", bes_yildizli)



