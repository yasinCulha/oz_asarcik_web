
import random
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Egitmen, EhliyetSinifi, IletisimBasvurusu, Kursiyer, Randevu, SaatAraligi, Soru, YanlisSoru, SiteAyarlari
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponse
from urllib.parse import quote 
# Create your views here.

def index(request):
    ayarlar = SiteAyarlari.objects.first()
    ehliyet_listesi = EhliyetSinifi.objects.all()
    return render(request, 'index.html', {'ehliyet_listesi': ehliyet_listesi, 'ayarlar': ayarlar})

def siniflar(request):
    ehliyet_listesi=EhliyetSinifi.objects.all()
    return render(request, 'siniflar.html', {'ehliyet_listesi': ehliyet_listesi})


def hakkimizda(request):
    return render(request, 'hakkimizda.html')

def ehliyetDetay(request, slug):
    sinif=get_object_or_404(EhliyetSinifi, slug=slug)
    return render(request, 'ehliyet_detay.html', {'sinif': sinif})


def iletisim(request):
    # Ayarları her zaman en başta çekelim
    ayarlar = SiteAyarlari.objects.first()
    
    if request.method == 'POST':
        ad_soyad = request.POST.get('name')
        telefon = request.POST.get('phone')
        mesaj = request.POST.get('message')

        if ad_soyad and telefon and mesaj:
            # Veritabanına kaydet
            if any(char.isdigit() for char in ad_soyad):
                messages.error(
                    request, "Ad Soyad alanında sayı kullanılamaz! ❌"
                )
                return render(request, "iletisim.html", {"ayarlar": ayarlar})

            # 🔥 3. Kontrol: Telefon sadece sayılardan mı oluşuyor?
            if not telefon.isdigit():
                messages.error(
                    request,
                    "Telefon numarası sadece sayılardan oluşmalıdır! ❌",
                )
                return render(request, "iletisim.html", {"ayarlar": ayarlar})
            
            mesajKayit = IletisimBasvurusu.objects.create(
                ad_soyad=ad_soyad,
                telefon=telefon,
                mesaj=mesaj
            )

            # WhatsApp mesajını hazırla
            whatsapp_mesaj = quote(f"Merhaba, ben {ad_soyad}. {mesaj}")
            
            # Başarı mesajı ekle
            messages.success(request, "Mesajınız başarıyla iletildi!")

            # WhatsApp'a yönlendir (Kritik: Numara dinamik olsun istiyorsan ayarlar'dan çekmelisin)
            # Eğer ayarlar.whatsapp_numarasi doluysa onu kullan, yoksa sabit numaran kalsın
            hedef_no = ayarlar.whatsapp_numarasi if ayarlar and ayarlar.whatsapp_numarasi else "905055679595"
            return redirect(f"https://wa.me/{hedef_no}?text={whatsapp_mesaj}")
        
        else:
            messages.error(request, "Lütfen tüm alanları doldurun.")

    # GET isteğinde veya form hatalıysa burası çalışır
    return render(request, 'iletisim.html', {'ayarlar': ayarlar})

@login_required
def kursiyerPanel(request):

    if hasattr(request.user, 'egitmen'):
        return redirect('egitmen_paneli')

    try:
        kursiyer=get_object_or_404(Kursiyer, user=request.user)
        bugun = timezone.now().date()
        randevular= Randevu.objects.filter(kursiyer=kursiyer,dolu_mu=True,tarih__gte=bugun).order_by('tarih','saat_dilimi__sira')
        musait_randevular = Randevu.objects.filter(dolu_mu=False).order_by('tarih','saat_dilimi__sira')

        
        context= {
            'kursiyer': kursiyer,
            'randevular': randevular,
            'musait_randevular': musait_randevular,
            'saatler': SaatAraligi.objects.all().order_by('sira'),
            'egitmenler': Egitmen.objects.all(),
            'bugun': bugun
        }

        return render(request, 'kursiyerpanel.html', context)
    except Http404:
        # Eğer profil yoksa ana sayfaya at veya hata mesajı ver
        return HttpResponse("Kursiyer profiliniz bulunamadı!")
    
    

def kursiyerGiris(request):
    if request.method == 'POST':
        kullanici_adi = request.POST.get('username')
        sifre = request.POST.get('password')
        kursiyer=authenticate(request, username=kullanici_adi, password=sifre)
        if kursiyer is not None:

            if kursiyer.is_active :
                login(request, kursiyer)
                return redirect('kursiyerpanel')
            else:
                messages.error(request, 'Hesabınız pasif durumdadır. ')
        else:
            messages.error(request, 'Kayıt bulunamadı')
    return render(request, 'login.html')

def kursiyer_cikis(request):
    logout(request)
    return redirect('index')

def gecmisRandevular(request):
    kursiyer=get_object_or_404(Kursiyer, user=request.user)
    tum_randevular=Randevu.objects.filter(kursiyer=kursiyer).order_by('tarih','saat_dilimi__sira')
    return render(request, 'gecmis_randevular.html', {'tum_randevular': tum_randevular, 'kursiyer': kursiyer,'today': timezone.now().date()})

@login_required
def sinavlar(request):
    return render(request, 'sinavlar.html')

@login_required
def randevu_listele(request):
    # Sadece boş olan (dolu_mu=False) randevuları gösterelim
    bos_randevular = Randevu.objects.filter(dolu_mu=False).order_by('tarih','saat_dilimi__sira')
    return render(request, 'randevu_al.html', {'bos_randevular': bos_randevular})

@login_required
def randevu_olustur(request):
    if request.method == "POST":
        tarih = request.POST.get('tarih')
        saat_id = request.POST.get('baslik')
        egitmen_id = request.POST.get('egitmen')
        kursiyer = get_object_or_404(Kursiyer, user=request.user)

        # Çakışma Kontrolü: Aynı hoca, aynı gün ve saatte dolu mu?
        cakisma = Randevu.objects.filter(tarih=tarih, saat_dilimi_id=saat_id, egitmen_id=egitmen_id).exists()
        bugun = timezone.now().date()
        if(tarih < str(bugun)):
            messages.error(request, "Geçmiş tarihte randevu oluşturamazsınız!")
        if cakisma:
            messages.error(request, "Bu hoca o saatte dolu! Başka saat veya hoca seç.")
        else:
            Randevu.objects.create(
                kursiyer=kursiyer,
                tarih=tarih,
                saat_dilimi_id=saat_id,
                egitmen_id=egitmen_id,
                dolu_mu=True # Kursiyer seçtiği an doluyor
            )
            print("Kayıt başarıyla oluşturuldu!")
            messages.success(request, "Randevun oluşturuldu!")
        
        return redirect('kursiyerpanel')
    
    return redirect('kursiyerpanel')

def giris_kontrol(request):
    # Kullanıcı giriş yaptıktan sonra buraya yönlendirilecek ve hangi panelin gösterileceğine karar verilecek
    if hasattr(request.user, 'kursiyer'):
        return redirect('kursiyerpanel')
    elif hasattr(request.user, 'egitmen'):
        return redirect('egitmen_paneli')
    else:
        return redirect('admin:index') # Eğer adminse direkt Django admin
    
@login_required
def egitmen_paneli(request):
    if hasattr(request.user, 'kursiyer'):
        return redirect('kursiyerpanel')
    
    try:
        egitmen = request.user.egitmen
    except Egitmen.DoesNotExist:
        messages.error(request, "profiliniz bulunamadı!")
        return redirect('kursiyer_giris')
    
    bugun = timezone.now().date()
    derslerim = Randevu.objects.filter(egitmen=egitmen, tarih__gte=bugun).order_by('tarih','saat_dilimi__sira')
    return render(request, 'egitmen_paneli.html', {'egitmen': egitmen, 'derslerim': derslerim, 'bugun': bugun})



def sinav_listesi(request):
    # Kullanıcıdan gelen filtreleme parametrelerini alıyoruz
    kategori_sorgu = request.GET.get('kategori')
    tip_sorgu = request.GET.get('tip') # 'test', 'video' veya 'karisik'

    sorular = Soru.objects.all()

    # 1. Kategoriye göre filtrele
    if kategori_sorgu:
        sorular = sorular.filter(kategori=kategori_sorgu)

    # 2. Soru tipine göre filtrele
    if tip_sorgu == 'video':
        sorular = sorular.filter(is_animasyon=True)
    elif tip_sorgu == 'test':
        sorular = sorular.filter(is_animasyon=False)
    
    # 3. Eğer 'karışık' seçildiyse rastgele 50 tane getir
    if tip_sorgu == 'karisik':
        sorular = sorular.order_by('?')[:50]
    
    if not kategori_sorgu and not tip_sorgu:
        sorular = sorular[:50]

    return render(request, 'soru_listele.html', {'sorular': sorular})

def sinavlar(request):
    return render(request, 'sinavlar.html')

@login_required
def deneme_sinavi_view(request):
    # Belirlediğin dağılım oranları
    dağılım = {
        'trafik': 23,
        'adab': 12,
        'saglik': 9,
        'motor': 6
    }
    
    sinav_sorulari = []
    
    for kat, adet in dağılım.items():
        # Veritabanından her kategori için belirlenen adet kadar random çekiyoruz
        id_listesi = list(Soru.objects.filter(kategori=kat).values_list('id', flat=True))
        secilen_idler = random.sample(id_listesi, min(adet, len(id_listesi)))  # Mevcut sorulardan rastgele seç
        sorular = Soru.objects.filter(id__in=secilen_idler)
        sinav_sorulari.extend(sorular)
    
    # Tüm kategorileri birleştirdikten sonra blok blok durmasınlar diye karıştırıyoruz
    random.shuffle(sinav_sorulari)
    
    return render(request, 'deneme_sinavi.html', {'sorular': sinav_sorulari})

@login_required
def sinav_tamamla_view(request):
    if request.method == "POST":
        dogru_sayisi = 0
        yanlis_sayisi = 0
        
        # 1. Formdan gelen verileri ayıklayalım (Soru ID: Seçilen Cevap)
        cevaplar = {key.split('_')[1]: value for key, value in request.POST.items() if key.startswith('soru_')}
        soru_idleri = cevaplar.keys()

        # 2. TEK SORGUDA tüm soruları veritabanından çekelim 
        soru_nesneleri = Soru.objects.in_bulk(soru_idleri)

        # 3. Döngü içinde veritabanına gitmeden kontrolleri yapalım
        for soru_id, secilen_cevap in cevaplar.items():
            soru = soru_nesneleri.get(int(soru_id)) # Hafızadaki listeden alıyoruz
            
            if soru:
                if secilen_cevap == soru.dogru_cevap:
                    dogru_sayisi += 1
                else:
                    yanlis_sayisi += 1
                    # Yanlış kaydını burada yapıyoruz
                    YanlisSoru.objects.update_or_create(
                        user=request.user, 
                        soru=soru,
                        defaults={'secilen_cevap': secilen_cevap}
                    )

        toplam_soru = len(cevaplar)
        # MEB puanlama (50 soru üzerinden hesaplamak için toplam_soru kullanılır)
        puan = (dogru_sayisi * 2) if toplam_soru == 50 else (dogru_sayisi / toplam_soru * 100 if toplam_soru > 0 else 0)
        durum = "GEÇTİ" if puan >= 70 else "KALDI"

        context = {
            'dogru': dogru_sayisi,
            'yanlis': yanlis_sayisi,
            'bos': 50 - toplam_soru, 
            'puan': round(puan, 2),
            'durum': durum
        }
        return render(request, 'sinav_sonuc.html', context)
    
    return redirect('deneme_sinavi')
@login_required
def yanlislarim_view(request):
    # Kullanıcının yanlış yaptığı tüm kayıtları, soru detaylarıyla birlikte getiriyoruz
    yanlis_kayitlari = YanlisSoru.objects.filter(user=request.user).select_related('soru').order_by('-id')
    
    return render(request, 'yanlislarim.html', {'yanlislar': yanlis_kayitlari})

@login_required
def yanlis_sil_view(request, yanlis_id):
    # Kullanıcı "Ben bu konuyu öğrendim" derse yanlış listesinden silebilir
    yanlis = get_object_or_404(YanlisSoru, id=yanlis_id, user=request.user)
    yanlis.delete()
    messages.success(request, "Soru öğrenilenler listesine taşındı!")
    return redirect('yanlislarim')

@login_required
def konu_calismasi_view(request, kategori_slug):

    sorular = list(Soru.objects.filter(kategori=kategori_slug).order_by('?')[:20])  

    context= {
        'sorular': sorular,
        'kategori': kategori_slug.upper(),
        'calisma_modu': True
    }
    return render(request, 'deneme_sinavi.html', context)

@login_required
def yeni_nesil_sinav_view(request):

    sorular = list(Soru.objects.filter(kategori='animasyon').order_by('?')[:10])  

    context= {
        'sorular': sorular,
        'kategori': 'Yeni Nesil Animasyonlu Sorular',
        'calisma_modu': True
    }
    return render(request, 'deneme_sinavi.html', context)