# 🏕️ Kamp Alanı Rezervasyon ve Yönetim Sistemi

**BMT210 Veri Yapıları Dersi — Gazi Üniversitesi 2026**  
Python + PyQt6 | 2 Kişilik Grup Projesi

---

## Kurulum & Çalıştırma

```bash
pip install PyQt6
python main.py                        # GUI açılır
python tests/birim_testleri.py        # 55+ birim testini çalıştırır
python generate_data.py               # Küçük/orta/büyük veri seti üretir
python tests/performans_testleri.py   # Performans benchmark'larını çalıştırır
```

---

## Proje Yapısı

```
kamp_sistemi/
├── main.py                          # Giriş noktası → GUI açılır
├── models.py                        # Ziyaretci, Alan, Ekipman, Rezervasyon
├── data_structures/
│   └── structures.py                # 10 veri yapısı
├── modules/
│   └── sistem.py                    # İş mantığı + JSON kalıcılık
├── gui/
│   └── uygulama.py                  # PyQt6 GUI — 5 sekme
├── tests/
│   └── birim_testleri.py            # 55 birim testi
└── kayitlar/                        # JSON veri dosyaları (otomatik)
```

---

## 11 Veri Yapısı & Görev Dağılımı

| # | Veri Yapısı   | Kullanım                             | Karmaşıklık      | Sorumlu   |
|---|---------------|--------------------------------------|-----------------|-----------|
| 1 | HashMap       | O(1) rezervasyon/ziyaretçi erişimi   | O(1) ort.       | 1. Kişi   |
| 2 | BST           | Tarih bazlı sıralı sorgu             | O(log n)        | 1. Kişi   |
| 3 | LinkedList    | Ziyaretçi rezervasyon geçmişi        | O(1) ekle       | 1. Kişi   |
| 4 | CampSet       | Bakımdaki alan O(1) kontrol          | O(1)            | 1. Kişi   |
| 5 | Matrix2D      | Alan tipi × gün doluluk matrisi      | O(1) erişim     | 1. Kişi   |
| 6 | PriorityQueue | VIP/Engelli öncelikli atama          | O(log n)        | 2. Kişi   |
| 7 | Queue         | Bekleme listesi FIFO                 | O(1)            | 2. Kişi   |
| 8 | Stack         | Son işlemi geri alma LIFO            | O(1)            | 2. Kişi   |
| 9 | MaxHeap       | Popüler alan sıralaması              | O(log n)        | 2. Kişi   |
|10 | Graph         | Alanlar arası komşuluk BFS/DFS       | O(V+E)          | 2. Kişi   |
|11 | CampTree      | Mekansal hiyerarşi (N-ary ağaç)      | O(1) erişim     | 2. Kişi   |

---

## GUI Sekmeleri

| Sekme         | Özellikler                                              |
|---------------|---------------------------------------------------------|
| 👤 Ziyaretçiler | Ekle / Güncelle / Sil / Ara / Öncelik (VIP-Engelli)  |
| 🏕️ Alanlar     | Ekle / Sil / Bakıma Al / Bakımdan Çıkar               |
| 📋 Rezervasyonlar | Oluştur / İptal / Stack ile Geri Al / BST Sorgu   |
| 🎒 Ekipman     | Stok Yönetimi / Ödünç Ver / İade Al                   |
| 📊 Raporlar    | 6 Stat Kartı / Popüler Alanlar / Performans Testleri   |

---

## Veri Kalıcılığı

Tüm veriler `kayitlar/` klasöründe JSON olarak saklanır.
Program kapanınca otomatik kaydedilir, açılınca yüklenir.

---

## Performans Testleri

İki farklı şekilde çalıştırılabilir:

### Terminal (ölçümlü karşılaştırma)

```bash
python tests/performans_testleri.py
```

Küçük (10), orta (100) ve büyük (1000) veri setleri üzerinde:

| # | Karşılaştırma                        | Beklenen Sonuç         |
|---|--------------------------------------|------------------------|
| 1 | Array (lineer) vs HashMap (O(1))     | HashMap ~10-100x hızlı |
| 2 | Lineer Arama vs BST Arama            | BST O(log n) avantajlı |
| 3 | Bubble Sort vs Heap Sort             | Heap O(n log n) kazanır|
| 4 | Liste vs Set — eleman varlık kontrolü| Set O(1) kazanır       |

### GUI (Raporlar Sekmesi)

Raporlar sekmesindeki **"Testleri Çalıştır"** butonuyla yukarıdaki testler görsel olarak da çalıştırılabilir.
