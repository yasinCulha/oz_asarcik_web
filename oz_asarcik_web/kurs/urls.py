from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('siniflar/', views.siniflar, name='siniflar'),
    path('iletisim/', views.iletisim, name='iletisim'),
    path('kursiyerpanel/', views.kursiyerPanel, name='kursiyerpanel'),
    path('hakkimizda/', views.hakkimizda, name='hakkimizda'),
    path('ehliyet-detay/<str:slug>/', views.ehliyetDetay, name='ehliyet_detay'),
    path('kursiyer-giris/', views.kursiyerGiris, name='kursiyer_giris'),
    path('kursiyer-cikis/', views.kursiyer_cikis, name='kursiyer_cikis'),
    path('gecmis-randevular/', views.gecmisRandevular, name='gecmis_randevular'),
    path('randevu-al/', views.randevu_listele, name='randevu_listele'),
    path('randevu-kaydet/', views.randevu_olustur, name='randevu_olustur'),
    path('kontrol/', views.giris_kontrol, name='giris_kontrol'),
    path('egitmen-paneli/', views.egitmen_paneli, name='egitmen_paneli'),
    path('sinavlar/', views.sinavlar, name='sinavlar'),
    path('sinav-listesi/', views.sinav_listesi, name='sinav_listesi'),
    path('deneme/', views.deneme_sinavi_view, name='deneme_sinavi'),
    path('deneme/tamamla/', views.sinav_tamamla_view, name='sinav_tamamla'),
    path('profil/yanlislarim/', views.yanlislarim_view, name='yanlislarim'),
    path('profil/yanlislarim/sil/<int:yanlis_id>/', views.yanlis_sil_view, name='yanlis_sil'),
    path('calisma/<str:kategori_slug>/', views.konu_calismasi_view, name='konu_calisma'),
    path('yeni-nesil-sorular/', views.yeni_nesil_sinav_view, name='yeni_nesil_sinav'),
    
]