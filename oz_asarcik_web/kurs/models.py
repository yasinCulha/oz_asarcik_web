from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# 1. Ehliyet Sınıfları Tablosu
class EhliyetSinifi(models.Model):
    ad = models.CharField(max_length=50) # Örn: B Sınıfı
    slug = models.SlugField(unique=True, null=True, blank=True)
    aciklama = models.TextField()
    yas_siniri = models.IntegerField(default=18)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.ad) # Otomatik slug oluşturma
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ad

# 2. Kursiyer Bilgileri (Genişletilmiş User Modeli)
class Kursiyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    ad = models.CharField(max_length=50) 
    soyad = models.CharField(max_length=50)
    tc_no = models.CharField(max_length=11, unique=True)
    telefon = models.CharField(max_length=15)
    kayit_tarihi = models.DateField(auto_now_add=True)
    ehliyet_sinifi = models.ForeignKey(EhliyetSinifi, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    egitmen = models.ForeignKey('Egitmen', on_delete=models.SET_NULL, null=True, blank=True, related_name='kursiyerleri',verbose_name="Eğitmen")

    def __str__(self):
        return f"{self.ad} {self.soyad}" if self.ad else self.user.username

class SaatAraligi(models.Model):
    baslik = models.CharField(max_length=20, help_text="Örn: 13:00 - 14:00")
    sira = models.IntegerField(default=0, help_text="Listeleme sırası")

    class Meta:
        verbose_name = "Saat Aralığı"
        verbose_name_plural = "Saat Aralıkları"
        ordering = ['sira']

    def __str__(self):
        return self.baslik
class Egitmen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    ad = models.CharField(max_length=100)
    soyad = models.CharField(max_length=100)
    telefon = models.CharField(max_length=15)
    
    class Meta:
        verbose_name = "Eğitmen"
        verbose_name_plural = "Eğitmenler"

    def __str__(self):
        return f"{self.ad} {self.soyad}"
    
# 3. Direksiyon Randevu Tablosu
class Randevu(models.Model):
    kursiyer = models.ForeignKey(Kursiyer, on_delete=models.CASCADE, null=True, blank=True)
    tarih = models.DateField(null=True, blank=True,db_index=True)
    saat_dilimi = models.ForeignKey(SaatAraligi,on_delete=models.CASCADE,null=True, blank=True)
    egitmen = models.ForeignKey(Egitmen, on_delete=models.CASCADE, null=True, blank=True)
    ehliyet_sinifi = models.ForeignKey(EhliyetSinifi, on_delete=models.SET_NULL, null=True, blank=True)
    dolu_mu = models.BooleanField(default=False) 
    KATILIM_DURUMLARI = [
        ('beklemede', 'Beklemede'),
        ('geldi', 'Geldi'),
        ('gelmedi', 'Gelmedi'),
    ]
    katilim_durumu = models.CharField(max_length=20,choices=KATILIM_DURUMLARI, default='beklemede')

    def __str__(self):
        durum = "DOLU" if self.dolu_mu else "BOŞ"
        return f"{self.tarih} -{self.saat_dilimi}- {self.egitmen} ({durum})"

# 4. İletişim Formu Başvuruları
class IletisimBasvurusu(models.Model):
    ad_soyad = models.CharField(max_length=100)
    telefon = models.CharField(max_length=15)
    mesaj = models.TextField()
    tarih = models.DateTimeField(auto_now_add=True)
    arandi_mu = models.BooleanField(default=False) 

# Mevcut modellerinin altına ekle
class KayitEvrak(models.Model):
    ad = models.CharField(max_length=100) 
    aciklama = models.CharField(max_length=255, blank=True, null=True) 
    zorunlu_mu = models.BooleanField(default=True)

    ilgili_siniflar = models.ManyToManyField(EhliyetSinifi, related_name='evraklar', blank=True)

    def __str__(self):
        return self.ad

# models.py güncellenmiş hali
class Soru(models.Model):
    metin = models.TextField()
    secenek_a = models.CharField(max_length=255)
    secenek_b = models.CharField(max_length=255)
    secenek_c = models.CharField(max_length=255)
    secenek_d = models.CharField(max_length=255)
    dogru_cevap = models.CharField(max_length=1)


    KATEGORI_CHOICES = [
        ('trafik', 'Trafik ve Çevre'),
        ('saglik', 'İlk Yardım ve Sağlık'),
        ('motor', 'Motor ve Araç Tekniği'),
        ('adab', 'Trafik Adabı'),
    ]
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES,db_index=True)

    def __str__(self):
        return f"{self.get_kategori_display()} - {self.metin[:50]}"


class YanlisSoru(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='yanlis_sorular')
    soru = models.ForeignKey(Soru, on_delete=models.CASCADE)
    secilen_cevap = models.CharField(max_length=1, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'soru') # Bir kullanıcı bir soruyu yanlış listesine sadece 1 kere ekleyebilir.

    def __str__(self):
        return f"{self.user.username} - {self.soru.metin[:20]}"

class SiteAyarlari(models.Model):
    # İletişim Bilgileri
    whatsapp_numarasi = models.CharField(max_length=20, verbose_name="WhatsApp Numarası (Örn: 905xxxxxxxxx)")
    instagram_adresi = models.CharField(max_length=200, verbose_name="Instagram Profil Linki")
    eposta_adresi = models.EmailField(verbose_name="E-Posta Adresi")
    konum_linki = models.TextField(verbose_name="Google Haritalar Embed Kodu/Linki")
    adres_metni = models.TextField(verbose_name="Açık Adres", blank=True, null=True)
    
    # Ekstra (İleride lazım olur)
    site_basligi = models.CharField(max_length=100, default="Öz Asarcık Sürücü Kursu")

    class Meta:
        verbose_name = "Site Ayarı"
        verbose_name_plural = "Site Ayarları"

    def __str__(self):
        return self.site_basligi