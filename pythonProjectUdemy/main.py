# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sqlite3 as sql
conn = sql.connect('database.db')
print("Sqlite ile bağlantı kuruldu.")
cursor = conn.cursor()
print("Cursor oluşturuldu.")
cursor.execute("""DROP TABLE IF EXISTS oylar""")   # Bu satırdaki kod yorumlar adlı tablo varsa siler, yoksa hata vermez.
cursor.execute("""CREATE TABLE IF NOT EXISTS "oylar" (
"id"	INTEGER NOT NULL,
"kurs_adi" TEXT NOT NULL,
"en_yuksek_oy_alan_kursun_adi" TEXT,
"en_yuksek_oy_alan_kursun_oyu" INTEGER,
PRIMARY KEY(id AUTOINCREMENT)
);""")    # Bu satırdaki kodlar yorumlar adlı tablo yoksa oluşturur.
cursor.execute("""DROP TABLE IF EXISTS yorumlar""")   # Bu satırdaki kod yorumlar adlı tablo varsa siler, yoksa hata vermez.
cursor.execute("""CREATE TABLE IF NOT EXISTS "yorumlar" (
"id"	INTEGER NOT NULL,
"kurs_adi" TEXT NOT NULL,
"kurs_yorumlari"	TEXT,
"en_cok_yorumlanan_kursun_adi" TEXT,
PRIMARY KEY(id AUTOINCREMENT)
);""")    # Bu satırdaki kodlar yorumlar adlı tablo yoksa oluşturur.

# pythonProjectUdemy adlı dosyanın içindeki python projelerindeki gerekli modülleri içe aktarıldı
from pythonProjectUdemy.udemyProject2 import kurs_bul
from pythonProjectUdemy.comments import yorum_bul

# Kurs bul fonksiyonu çağır
kurs_bul()

# Yorum bul fonksiyonu çağır
yorum_bul()

conn.close()

