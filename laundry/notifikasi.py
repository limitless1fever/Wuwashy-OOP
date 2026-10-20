"""Pembuat notifikasi pesanan.

Penerapan 4 pilar OOP di file ini:
  1. Abstraksi    : PembuatNotifikasi adalah kelas abstrak (ABC). Pemanggil hanya tahu `buat()`;
                    cara menyusun isi pesan diserahkan ke subkelas lewat method abstrak `isi()`.
  2. Pewarisan    : NotifBerbasisTeks mewarisi PembuatNotifikasi, lalu NotifDiterima, NotifDijemput, dst.
                    mewarisi NotifBerbasisTeks. NotifSelesai menimpa (override) `isi()` untuk menambah info poin.
  3. Polimorfisme : `kirim_notifikasi_status()` memanggil `.buat()` pada kelas apa pun dari DAFTAR tanpa
                    if/else per status; tiap kelas menghasilkan isi pesannya sendiri.
  4. Enkapsulasi  : data pesanan disimpan di atribut internal `_booking`, dan detail pencarian poin
                    disembunyikan di method internal `_teks_poin()`.
"""
from abc import ABC, abstractmethod

from .models import Notifikasi, PoinLog


class PembuatNotifikasi(ABC):
    """Kelas dasar abstrak: tidak bisa dibuat langsung, harus lewat subkelas yang mengimplementasikan isi()."""

    judul = ''

    def __init__(self, booking):
        self._booking = booking  # Enkapsulasi: atribut internal, tidak diakses dari luar kelas

    @abstractmethod
    def isi(self) -> str:
        """Teks isi notifikasi. Wajib diimplementasikan subkelas."""

    def buat(self):
        b = self._booking
        if not b.user_id:  # pesanan tamu tanpa akun: tidak ada penerima
            return None
        return Notifikasi.objects.create(user_id=b.user_id, booking=b, judul=self.judul, isi=self.isi())


class NotifBerbasisTeks(PembuatNotifikasi):
    """Perantara: isi pesan disusun dari templat teks milik subkelas (cukup isi `judul` dan `templat`)."""

    templat = ''

    def isi(self):
        b = self._booking
        return self.templat.format(resi=b.resi, layanan=b.nama_layanan)


class NotifDiterima(NotifBerbasisTeks):
    judul = 'Pesanan diterima'
    templat = 'Pesanan #{resi} ({layanan}) sudah kami terima. Kurir akan segera menjemput cucianmu.'


class NotifDijemput(NotifBerbasisTeks):
    judul = 'Pakaian sudah dijemput'
    templat = 'Pakaian untuk pesanan #{resi} sudah kami jemput dan sedang menuju outlet.'


class NotifDiproses(NotifBerbasisTeks):
    judul = 'Cucian sedang diproses'
    templat = 'Pesanan #{resi} ({layanan}) sedang kami cuci dan rapikan.'


class NotifSiap(NotifBerbasisTeks):
    judul = 'Cucian siap diambil'
    templat = 'Pesanan #{resi} sudah bersih dan siap diambil atau diantar.'


class NotifDiantar(NotifBerbasisTeks):
    judul = 'Cucian sedang diantar'
    templat = 'Kurir sedang mengantar pesanan #{resi}. Mohon siapkan penerima di alamat tujuan.'


class NotifDibatalkan(NotifBerbasisTeks):
    judul = 'Pesanan dibatalkan'
    templat = 'Pesanan #{resi} dibatalkan. Hubungi kami via WhatsApp bila ini tidak sesuai.'


class NotifSelesai(NotifBerbasisTeks):
    judul = 'Pesanan selesai'
    templat = 'Pesanan #{resi} sudah selesai. Terima kasih sudah memilih WuWashy!'

    def isi(self):  # Pewarisan: override isi() agar pesan selesai ikut menyebut poin
        return super().isi() + self._teks_poin()

    def _teks_poin(self):
        """Enkapsulasi: detail pencarian poin disembunyikan di sini."""
        log = PoinLog.objects.filter(booking=self._booking, jumlah__gt=0).first()
        return f' Kamu mendapat +{log.jumlah} poin.' if log else ''


# Status Booking -> kelas pembuat notifikasinya
DAFTAR = {
    'menunggu': NotifDiterima,
    'dijemput': NotifDijemput,
    'diproses': NotifDiproses,
    'siap': NotifSiap,
    'diantar': NotifDiantar,
    'selesai': NotifSelesai,
    'dibatalkan': NotifDibatalkan,
}


def kirim_notifikasi_status(booking):
    """Polimorfisme: satu pemanggilan `.buat()` untuk semua status; hasilnya berbeda sesuai kelasnya."""
    kelas = DAFTAR.get(booking.status)
    return kelas(booking).buat() if kelas else None
