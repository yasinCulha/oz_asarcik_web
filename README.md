# Öz Asarcık - Sürücü Kursu Otomasyonu & Web Yönetim Sistemi 🚗💨

Bu proje; bir sürücü kursunun hem masaüstü yönetim süreçlerini (kursiyer takibi, sınıf yönetimi, sınav soruları) kolaylaştırmak hem de kursun dijital dünyadaki yüzünü (canlı web sitesi, WhatsApp entegrasyonu, dinamik yönetim paneli) oluşturmak amacıyla geliştirilmiş **hibrit (Masaüstü + Web)** bir otomasyon sistemidir.

Masaüstü ve Web uygulamaları, bulut tabanlı ortak bir veritabanı mimarisi üzerinden gerçek zamanlı (real-time) olarak birbiriyle konuşmaktadır.

---

## 🛠️ Kullanılan Teknolojiler ve Mimari

### 💻 Masaüstü Otomasyonu (Desktop Application)
* **Dil / Framework:** C# | .NET Windows Forms
* **Veritabanı Sürücüsü:** Npgsql (PostgreSQL Client)
* **Mimari Yapı:** Formlar arası dinamik yaşam döngüsü yönetimi (`FormClosed` ve ana thread optimizasyonları yapılmıştır).
* **Dağıtım Modu:** Taşınabilir (Portable) - Kuruluma ihtiyaç duymadan, internet olan her bilgisayarda flash bellek üzerinden doğrudan çalışabilir.

### 🌐 Web Sitesi & Yönetim Paneli (Web Application)
* **Backend Framework:** Python | Django MVT
* **Veritabanı / ORM:** Django ORM & PostgreSQL
* **Canlı Yayın (Deployment):** Render Cloud Platform
* **Ek Özellikler:** Dinamik WhatsApp yönlendirme sistemi, responsive (mobil uyumlu) arayüz, statik dosya (WhiteNoise) optimizasyonları.

### ☁️ Bulut Veritabanı (Cloud Database)
* **Altyapı:** Neon Tech (Serverless PostgreSQL)
* **Özellik:** Hem C# masaüstü uygulaması hem de Django web sitesi verileri ortak bir şema üzerinden anlık olarak çeker ve günceller.

---

## 🚀 Proje Özellikleri

### 👨‍💼 Masaüstü Paneli Özellikleri
- **Kursiyer Yönetimi:** Kursiyer kayıt, listeleme ve durum güncelleme işlemleri.
- **Sınıf & Sekme Yönetimi:** Dinamik sınıflar arası geçiş ve temiz bellek yönetimiyle optimize edilmiş ekranlar.
- **Sınav Soruları Havuzu:** Sürücü kursu sınavlarına yönelik yerel veritabanından buluta göç ettirilmiş binlerce satırlık soru havuzunun listelenmesi ve yönetimi.

### 🕸️ Web Sitesi Özellikleri
- **Dinamik WhatsApp Butonu:** Müşterilerin kurs ile doğrudan (uluslararası numara formatı optimizasyonlu) iletişime geçebileceği hızlı buton.
- **Gelişmiş Yönetim Paneli:** Django Admin üzerinden tüm kurs içeriğinin, sınav sorularının ve iletişim bilgilerinin canlı olarak güncellenebilmesi.

---

## ⚙️ Kurulum ve Çalıştırma


### 1. Web Projesini Yerelde Çalıştırma
```bash
# Projeyi klonlayın
git clone [https://github.com/KULLANICI_ADIN/REPOS_ADIN.git](https://github.com/KULLANICI_ADIN/REPOS_ADIN.git)

# Proje klasörüne girin
cd oz_asarcik_web

# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# Veritabanı geçişlerini yapın
python manage.py migrate

# Projeyi ayağa kaldırın
python manage.py runserver
