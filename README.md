# **Takım İsmi**

Takım 173

# Ürün İle İlgili Bilgiler

## Takım Elemanları

- Zehra Nur Derin: Product Owner / Scrum Master / Data Scientist & Developer

## Ürün İsmi

--Montee--

## Ürün Açıklaması

- Montee, kullanıcıların karmaşık banka hesap hareketlerini ve harcamalarını yapay zekâ desteğiyle analiz ederek bütçe takibini kolaylaştıran ve finansal okuryazarlığı artıran akıllı bir finans asistanıdır. İsmini "Money" (Para) ve "Mentee" (Rehberlik Alan) kavramlarının sentezinden alan Montee, kullanıcısına finansal dünyada akıllı bir mentor gibi rehberlik eder.

## Ürün Özellikleri

- Otomatik Harcama Kategorizasyonu
- Akıllı Bütçe Yönetimi
- Abonelik Takibi
- Kişiselleştirilmiş Tasarruf Mentorluğu

## Hedef Kitle

- Dijital Bankacılık Kullanıcıları
- Bütçe Kontrolü ve Birikim Hedefi Olanlar
- Gençler ve Öğrenciler

## Product Backlog URL

[Miro Backlog Board](https://miro.com/app/live-embed/uXjVH-peL5Y=/?embedMode=view_only_without_ui&moveToViewport=-1748%2C-723%2C2339%2C1301&embedId=267636883746)

---

# Sprint 1

- **Backlog düzeni ve Story seçimleri**:: Backlog, veri toplama → veri temizleme → sentetik veri zenginleştirme → ilk model eğitimi → dokümantasyon şeklinde mantıksal bir akışa göre sıralanmıştır.

- Sprint Kapsamında Yapılanlar:

Kaggle'dan uygun banka işlem veri seti indirildi (BudgetWise Finance Dataset, ~31.700 satır)
Kategori alanındaki 200+ yazım hatası varyantı fuzzy matching ile 15 kanonik kategoriye normalize edildi
Regex tabanlı pipeline ile tarih, tutar, ödeme yöntemi ve lokasyon alanları temizlendi
Faker ile gerçekçi sentetik işlem açıklamaları üretilip gerçek veriyle birleştirildi
TF-IDF + Random Forest ile ilk harcama sınıflandırma modeli eğitildi (Accuracy: %81, F1-macro: %77)
Ürün ismi "Montee" olarak kilitlendi, README hazırlandı

Miro Board'da gözüken kırmızı item'lar yapılacak işleri (task) gösterirken, mavi item'lar story'leri temsil etmektedir.

- **Daily Scrum**: Takım tek kişiden oluştuğu için Daily Scrum toplantısı yapılmamıştır.

- **Sprint board update**: Sprint board screenshotları: 
![Backlog 1]<img width="931" height="505" alt="Screenshot 2026-07-05 at 21 18 58" src="https://github.com/user-attachments/assets/696ad38a-2cbf-4c67-8f70-20dcf77f0601" />

![Backlog 2]<img width="984" height="394" alt="Screenshot 2026-07-05 at 22 18 17" src="https://github.com/user-attachments/assets/2973bd16-1c88-4f39-9439-1aa5dac1fac6" />

![Backlog 3] <img width="988" height="525" alt="Screenshot 2026-07-05 at 23 29 36" src="https://github.com/user-attachments/assets/ef9621cc-2fc3-41f8-9b07-1772fab557d2" />


- **Ürün Durumu**: Ekran görüntüleri:
  ![Screenshot 1](https://github.com/OyunveUygulamaAkademisi/BootcampScrumTemplate/blob/main/ProjectManagement/Sprint1Documents/productss1.png?raw=true)
  ![Screenshot 2](https://github.com/OyunveUygulamaAkademisi/BootcampScrumTemplate/blob/main/ProjectManagement/Sprint1Documents/productss2.png?raw=true)

- **Sprint Review**: 
Gerçek veri setlerindeki açıklama metinlerinin kategoriyle anlamsal ilişkisi olmadığı tespit edilmiş; gerçek veri (yapı için) ve sentetik veri (metin sinyali için) birleştirilerek çözülmüştür. İlk model %81 doğrulukla eğitilmiş, sonuç gerçekçi bulunmuştur.

- **Sprint Retrospective:**
-Veri kalitesi kontrolü, veri toplama sürecinin hemen ardından yapılmalı
-İlk sentetik veri denemesi aşırı temizdi (%100 doğruluk = overfitting), gerçekçi gürültü eklenerek düzeltildi
-Unit test'lere ayrılan süre bir sonraki sprintte artırılmalı


---

# Sprint 2


---

# Sprint 3

---
