from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('booking/', views.booking, name='booking'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('akun/', views.akun_saya, name='akun_saya'),
    path('alamat/', views.alamat_saya, name='alamat_saya'),
    path('pesanan/', views.pesanan_saya, name='pesanan_saya'),
    path('cari/', views.cari_pesanan, name='cari_pesanan'),
    path('riwayat/', views.riwayat_pesanan, name='riwayat_pesanan'),
    path('poin/', views.poin_hadiah, name='poin_hadiah'),
    path('panel/', views.admin_dashboard, name='admin_dashboard'),
    path('panel/pesanan/<int:pk>/', views.admin_pesanan_detail, name='admin_pesanan_detail'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
