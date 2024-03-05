import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sqlite3 as sql
conn = sql.connect('database.db')
cursor = conn.cursor()

# Yorumları bulan fonksiyon oluşturuldu.
def yorum_bul():
    # undetected_chromedriver'ı başlatmak için
    uc.install()

    # Webdriver'ı başlatıldı. Tarayıcı olarak Chrome kullanıldı.Farklı bir tarayıcı da kullanılabilir.
    driver = uc.Chrome()
    driver.maximize_window()  # Tarayıcı penceresini maksimize etmek için
    url = "https://www.udemy.com/"
    driver.get(url)

    # Udemy web sitesinin ana sayfasındaki arama çubuğunu bulmak için ve 'Python Kursları' araması yapmak için
    search = driver.find_element('css selector', 'input[type="text"]')
    search.send_keys('Python Kursları' + Keys.RETURN)

    time.sleep(2)


    for _ in range(5):  # ihtiyaca göre sayıyı ayarlayabiliriz.
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(2)  # Bekleme süresi yüklenme tamamlanana kadar beklemek için ayarlanabilir. İhtiyaca göre artırılabilir.


    course_links = [link.get_attribute('href') for link in
                    driver.find_elements(By.XPATH, '//a[contains(@href, "/course/")]')]


    print(course_links)

    # Her bir kursun sayfasına girip yorumları çekmek için
    for link in course_links:
        driver.get(link)
        try:
            # Sayfanın tamamen yüklenmesi için
            time.sleep(5)
            print("************")
            kurs_adi = "course-card-title-module--title--2C6ac"
            element_kurs_adlari = driver.find_elements(By.CSS_SELECTOR, ".course-card-title-module--title--2C6ac")
            kurs_adi = element_kurs_adlari[0].text
            print("Kurs Adı:", kurs_adi)

            # Kategori bilgisini al
            try:
                kurs_kategori = driver.find_element(By.CLASS_NAME, "topic-menu-condensed").text
                print("Kategori:", kurs_kategori)
            except Exception as e:
                print(f"Kategori bulunamadı: {e}")

            # "Daha Fazla Göster" butonuna tıklatmak için
            more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content-anchor"]/div[5]/div/div[10]/button'))
            )
            more_button.click()

            # "Daha Fazla Görüntüle" butonuna 9 kez tıklatmak için (Her bir kursun yorumlarının bulunduğu ilk sayfada 12 yorum bulunmaktadır. 100 yorumun çekilmesi için )
            for _ in range(9):
                show_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-purpose="show-more-review-button"]'))
                )
                show_more_button.click()
                time.sleep(1)

            # Yorumları çekmek için sayfa kaynağı alınmalı.
            page_source = driver.page_source

            # BeautifulSoup modülü kullanarak veriyi çekmek için
            soup = BeautifulSoup(page_source, 'html.parser')


            comments = soup.find_all("div", class_='ud-text-md show-more-module--content--cjTh0')

            # Belirli bir class değerine sahip span etiketlerini bul
            date_class = 'ud-heading-xs review--time-since--37KF5'
            element_date_class = soup.find_all('span', class_=date_class)

            # Yorumları işlemek ve yazdırmak için
            for i, comment in enumerate(comments, start=1):
                print(f"* Yorum {i} *")
                print(comment.text)
                print("\n")
                # Bulunan span etiketlerinin içeriğini yazdır
            for span in element_date_class:
                print("* Tarih *")
                print(span.text)
                print("\n")

                cursor.execute(
                    "INSERT INTO yorumlar (kurs_adi,kurs_yorumlari) VALUES(?,?)",
                    (kurs_adi, comment.text))
                conn.commit()  # Yapılan işlemleri kaydetmek için

        except Exception as e:
            print(f"Hata: {e}")


    # Tarayıcıyı kapatın
    #driver.quit()

    # Udemy web sitesindeki "Python Kursları" adlı sayfadaki 'En fazla yorum alan' filtresiyle bulunan en çok yorum alan kursu bulmak için
    url1 = "https://www.udemy.com/courses/search/?q=Python+Kurslar%C4%B1&sort=most-reviewed&src=ukw"
    driver.get(url1)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".course-card-title-module--title--2C6ac"))
    )
    element_kurs_adlari1 = "course-card-title-module--title--2C6ac"
    element_kurs_adlari1 = driver.find_elements(By.CSS_SELECTOR, ".course-card-title-module--title--2C6ac")
    element_kurs_adlari1 = element_kurs_adlari1[0].text
    element_kurs_adlari1 = element_kurs_adlari1.replace("<strong>", "")
    element_kurs_adlari1 = element_kurs_adlari1.replace("</strong>", "")
    print("O sitedeki en çok yorumlanan kursun adı: {0} ".format(element_kurs_adlari1))

    cursor.execute(
        "INSERT INTO yorumlar (en_cok_yorumlanan_kursun_adi) VALUES(?)",
        (element_kurs_adlari1))
    conn.commit()  # Yapılan işlemleri kaydetmek için

    # Tarayıcıyı kapat
    driver.quit()
