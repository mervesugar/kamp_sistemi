"""
Örnek Veri Seti Üretici
Kullanım: python generate_data.py
Çıktı: kayitlar/veri_10.json / veri_100.json / veri_1000.json
"""
import json, os, random, uuid
from datetime import date, timedelta

CIKTI = os.path.join(os.path.dirname(__file__), "kayitlar")
os.makedirs(CIKTI, exist_ok=True)

ISIMLER = ["Ahmet","Fatma","Mehmet","Ayşe","Ali","Zeynep","Mustafa","Elif","Hüseyin","Merve"]
SOYADLAR = ["Yılmaz","Kaya","Demir","Çelik","Şahin","Yıldız","Öztürk","Aydın","Arslan","Koç"]
TIPLER = ["Çadır","Karavan","Bungalov"]
FIYATLAR = {"Çadır":150,"Karavan":350,"Bungalov":600}

def uret(rezervasyon_sayisi: int):
    n_alan = max(5, rezervasyon_sayisi // 10)
    n_ziyaretci = max(5, rezervasyon_sayisi // 5)

    ziyaretciler = [
        {"ziyaretci_id": f"Z{i:04d}", "ad": random.choice(ISIMLER),
         "soyad": random.choice(SOYADLAR), "telefon": f"05{random.randint(10,59)}{random.randint(1000000,9999999)}",
         "oncelik": random.choice([0,0,0,5,10])}
        for i in range(n_ziyaretci)
    ]

    alanlar = [
        {"alan_id": f"A{i:03d}", "alan_tipi": (t := random.choice(TIPLER)),
         "kapasite": random.choice([2,4,6]), "fiyat": FIYATLAR[t],
         "rezervasyon_sayisi": 0, "bakimda": random.random() < 0.05}
        for i in range(n_alan)
    ]
    musait = [a["alan_id"] for a in alanlar if not a["bakimda"]]
    alan_rez = {aid: 0 for aid in musait}

    baslangic = date(2025, 1, 1)
    rezervasyonlar = []
    for i in range(rezervasyon_sayisi):
        giris = baslangic + timedelta(days=random.randint(0, 364))
        cikis = giris + timedelta(days=random.randint(1, 7))
        aid = random.choice(musait)
        zid = random.choice(ziyaretciler)["ziyaretci_id"]
        fiyat = FIYATLAR[next(a["alan_tipi"] for a in alanlar if a["alan_id"] == aid)]
        rezervasyonlar.append({
            "rezervasyon_id": f"R{i:05d}",
            "ziyaretci_id": zid, "alan_id": aid,
            "giris_tarihi": giris.isoformat(), "cikis_tarihi": cikis.isoformat(),
            "toplam_ucret": round((cikis - giris).days * fiyat, 2),
            "aktif": random.random() > 0.1
        })
        alan_rez[aid] += 1

    for a in alanlar:
        a["rezervasyon_sayisi"] = alan_rez.get(a["alan_id"], 0)

    veri = {"ziyaretciler": ziyaretciler, "alanlar": alanlar,
            "ekipmanlar": [], "rezervasyonlar": rezervasyonlar}

    dosya = os.path.join(CIKTI, f"veri_{rezervasyon_sayisi}.json")
    with open(dosya, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)
    print(f"✅ veri_{rezervasyon_sayisi}.json  |  {n_ziyaretci} ziyaretçi, {n_alan} alan, {rezervasyon_sayisi} rezervasyon")

if __name__ == "__main__":
    print("Örnek veri setleri üretiliyor...\n")
    for n in [10, 100, 1000]:
        uret(n)
    print("\nTamamlandı → kayitlar/ klasörüne kaydedildi.")
