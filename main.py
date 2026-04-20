import sqlite3
#Sorensen-Dice Benzerligi
def sorensen_dice_benzerligi(metin1, metin2):
    # Kucuk harfe cevirip kelime kümelerini olustur
    kume1 = set(metin1.lower())
    kume2 = set(metin2.lower())

    # Metin bos girilirse sifira bolunme hatasini engelle
    if len(kume1) == 0 and len(kume2) == 0:
        return 0.0

    # Ortak kume sayisi
    kesisim_sayisi = len(kume1.intersection(kume2))

    # Formul: (2 * kesisim_sayisi) / (kume1 + kume2)
    oran = (2.0 * kesisim_sayisi) / (len(kume1) + len(kume2))

    return oran

def ana_program():
    # SQLite baglan, yoksa olustur
    baglanti = sqlite3.connect("dice_karsilastirma.db")
    imlec = baglanti.cursor()

    imlec.execute('''
                  CREATE TABLE IF NOT EXISTS MetinBenzerlik
                  (
                      id
                      INTEGER
                      PRIMARY
                      KEY
                      AUTOINCREMENT,
                      metin1
                      TEXT,
                      metin2
                      TEXT,
                      benzerlik_orani
                      REAL
                  )
                  ''')

    print("--- Sørensen-Dice Metin Benzerlik Hesaplayıcı ---")
    m1_girdi = input("Lütfen birinci metni girin: ")
    m2_girdi = input("Lütfen ikinci metni girin: ")

    # Benzerlik oranini hesapla
    oran = sorensen_dice_benzerligi(m1_girdi, m2_girdi)

    # SQLite'a yukle
    imlec.execute('''
                  INSERT INTO MetinBenzerlik (metin1, metin2, benzerlik_orani)
                  VALUES (?, ?, ?)
                  ''', (m1_girdi, m2_girdi, oran))
    baglanti.commit()

    # SQLite den oku ekrana yaz
    imlec.execute('''
                  SELECT metin1, metin2, benzerlik_orani
                  FROM MetinBenzerlik
                  ORDER BY id DESC LIMIT 1
                  ''')
    son_kayit = imlec.fetchone()

    print("\n--- Veritabanından Okunan Sonuç ---")
    print(f"Metin 1: {son_kayit[0]}")
    print(f"Metin 2: {son_kayit[1]}")
    print(f"Benzerlik Oranı: {son_kayit[2]:.4f} (Yaklaşık %{son_kayit[2] * 100:.1f} benzerlik)")

    baglanti.close()

if __name__ == "__main__":
    ana_program()