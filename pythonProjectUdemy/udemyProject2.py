from selenium import webdriver
import time
""" undetected_chromedriver modülü, normalde tarayıcı otomasyonu yapan siteler tarafından kullanılan otomatik algılama 
tekniklerini atlamaya yardımcı olan bir Python kütüphanesidir. """
import undetected_chromedriver as uc

# Selenium kütüphanesinden gerekli modüller içe aktarıldı.
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import sqlite3 as sql
conn = sql.connect('database.db')
cursor = conn.cursor()

# Kursları bulan fonksiyon oluşturuldu.
def kurs_bul():

    en_yuksek_oy_alan_urunun_oyu = 0
    en_yuksek_oy_alan_urunun_adi = ""

    # undetected_chromedriver'ı başlatmak için
    uc.install()
    # Webdriver'ı başlatıldı. Tarayıcı olarak Chrome kullanıldı.Farklı bir tarayıcı da kullanılabilir.
    driver = uc.Chrome()
    driver.maximize_window() # Tarayıcı penceresini maksimize etmek için
    driver.get("https://www.udemy.com/")
    toplam_kurs_sayisi = 0
    sayfa_sayma = 1

    while toplam_kurs_sayisi < 100:
        try:
            # Udemy web sitesinin ana sayfasındaki arama çubuğunu bulmak için ve 'Python Kursları' araması yapmak için
            search = driver.find_element('css selector', 'input[type="text"]')
            search.send_keys('Python Kursları' + Keys.RETURN)
            for sayfa_sayma in range(1, 8):
                yeni_url = f"https://www.udemy.com/courses/search/?p={sayfa_sayma}&q=Python+Kurslar%C4%B1&src=ukw"
                driver.get(yeni_url)
                # Sayfa aşağı kaydırma işlemi yapmak için
                actions = ActionChains(driver)
                for _ in range(20):  # ihtiyaca göre sayıyı ayarlayabiliriz.
                    actions.send_keys(Keys.PAGE_DOWN).perform()
                    time.sleep(0.25)
                # Kurs bilgilerini bulabilmek için bekleme işlemi yaptırır.
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".course-card-title-module--title--2C6ac"))
                )

                time.sleep(10)
                kurs_adi = "course-card-title-module--title--2C6ac"
                hazirlayan_kisi = "course-card-instructors-module--instructor-list--37tO6"
                kurs_fiyati = "course-card-module--price-text-container--2oBPb"
                kurs_yildiz = "course-card-ratings-module--row--1EHHW"

                yildiz = 0
                i = 0

                element_kurs_adlari = driver.find_elements(By.CSS_SELECTOR, ".course-card-title-module--title--2C6ac")
                element_hazirlayan_kisiler = driver.find_elements(By.CSS_SELECTOR,
                                                                  ".course-card-instructors-module--instructor-list--37tO6")
                element_kurs_fiyatlar = driver.find_elements(By.CSS_SELECTOR,
                                                             ".course-card-module--price-text-container--2oBPb")
                element_kurs_yildizlar = driver.find_elements(By.CSS_SELECTOR, ".course-card-ratings-module--row--1EHHW")

                for i in range(len(element_kurs_adlari)):
                    print("************")

                    # Kurs Adları
                    kurs_adi = element_kurs_adlari[i].text
                    kurs_adi=kurs_adi.replace("<strong>", "")
                    kurs_adi = kurs_adi.replace("</strong>", "")
                    print("Kurs Adı:", kurs_adi)

                    # Hazırlayan Kişiler
                    hazirlayan_kisi = element_hazirlayan_kisiler[i].text
                    print("Hazırlayan Kişi:", hazirlayan_kisi) #Marka ifadesi yerine hazırlayan kişi ifadesi alındı.

                    # Kurs Fiyatları
                    try:
                        kurs_fiyati = element_kurs_fiyatlar[i].text
                        print("Kurs Fiyatı:", kurs_fiyati) #Model ifadesi yerine kurs fiyatı ifadesi alındı.
                    except IndexError:
                        print("Kurs Fiyatı bulunamadı.")

                    # Kurs Yıldızları
                    try:
                        kurs_yildizi = element_kurs_yildizlar[i].text
                        print("Kurs Yıldızı ve Toplam Puanlayan Kişi Sayısı:", kurs_yildizi) #Cinsiyet ifadesi yerine kursu toplam puanlayan kişi sayısı alındı
                        yildiz =kurs_yildizi[14:17]
                        yildiz = yildiz.replace(",", ".")
                        if float(yildiz) > en_yuksek_oy_alan_urunun_oyu:
                            en_yuksek_oy_alan_urunun_oyu = float(yildiz)
                            en_yuksek_oy_alan_urunun_adi = kurs_adi
                    except IndexError:
                        print("Kurs Yıldızı bulunamadı.")

                    toplam_kurs_sayisi += 1
                    if toplam_kurs_sayisi >= 100:
                        break

                    cursor.execute(
                        "INSERT INTO oylar (kurs_adi,en_yuksek_oy_alan_kursun_adi,en_yuksek_oy_alan_kursun_oyu) VALUES(?,?,?)",
                        (kurs_adi,en_yuksek_oy_alan_urunun_adi, en_yuksek_oy_alan_urunun_oyu))
                    conn.commit()  # Yapılan işlemleri kaydetmek için

        except Exception as e:
            print(f"Hata oluştu: {e}")
            break

    print("En yüksek puan alan kursun adı: {0} \nEn yüksek puan alan kursun puanı: {1} ".format(en_yuksek_oy_alan_urunun_adi, en_yuksek_oy_alan_urunun_oyu))



    # Tarayıcıyı kapat
    driver.quit()