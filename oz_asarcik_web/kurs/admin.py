from django.contrib import admin

# Register your models here.

#password:5555
from django.contrib import admin
from .models import Egitmen, EhliyetSinifi, KayitEvrak, Kursiyer, Randevu, IletisimBasvurusu, SaatAraligi, SiteAyarlari, Soru, SiteAyarlari

@admin.register(EhliyetSinifi)
class EhliyetSinifiAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('ad',)}
    list_display = ('ad', 'yas_siniri', 'fiyat')

@admin.register(Kursiyer)
class KursiyerAdmin(admin.ModelAdmin):
    list_display = ('user', 'tc_no', 'ehliyet_sinifi', 'kayit_tarihi')
    search_fields = ('tc_no', 'user__first_name', 'user__last_name')
    list_filter = ('ehliyet_sinifi',)

@admin.register(SaatAraligi)
class SaatAraligiAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'sira')
    
@admin.register(Randevu)
class RandevuAdmin(admin.ModelAdmin):
    list_display = ('tarih', 'saat_dilimi', 'egitmen', 'kursiyer', 'dolu_mu', 'katilim_durumu')
    list_filter = ('dolu_mu', 'egitmen')
    list_editable=('katilim_durumu','dolu_mu')

@admin.register(IletisimBasvurusu)
class IletisimBasvurusuAdmin(admin.ModelAdmin):
    list_display = ('ad_soyad', 'telefon', 'tarih', 'arandi_mu')
    list_filter = ('arandi_mu','tarih')
    list_editable = ('arandi_mu',)

@admin.register(KayitEvrak)
class KayitEvrakAdmin(admin.ModelAdmin):
    list_display = ('ad', 'zorunlu_mu')
    list_filter = ('zorunlu_mu', 'ilgili_siniflar')
    filter_horizontal = ('ilgili_siniflar',)

@admin.register(Egitmen)
class EgitmenAdmin(admin.ModelAdmin):
    list_display = ('ad', 'soyad', 'telefon')

@admin.register(Soru)
class SoruAdmin(admin.ModelAdmin):
    list_display = ('kategori','metin' )
    list_filter = ('kategori',)

@admin.register(SiteAyarlari)
class SiteAyarlarıAdmin(admin.ModelAdmin):
    list_display = ('site_basligi', 'whatsapp_numarasi', 'eposta_adresi')