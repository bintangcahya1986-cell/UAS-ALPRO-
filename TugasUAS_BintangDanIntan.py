# SISTEM PELAYANAN PEMESANAN TIKET BUS
# Pilihan Kelas Reguler, VIP, dan VVIP
# Data rute dan harga menggunakan Tuple
rute = (
    ("Surabaya - Malang", 50000),
    ("Surabaya - Kediri", 65000),
    ("Surabaya - Yogyakarta", 150000),
    ("Surabaya - Semarang", 120000)
)
# Data jadwal menggunakan Tuple
jadwal = ("08.00", "12.00", "16.00")
# Data kelas tiket menggunakan Dictionary
kelas_tiket = {
    "1": ("Reguler", 0),
    "2": ("VIP", 25000),
    "3": ("VVIP", 50000)
}
# List untuk menyimpan riwayat pemesanan
riwayat = []
# Set untuk menyimpan kode booking unik
kode_booking_set = set()
# Fungsi untuk mengubah angka menjadi format Rupiah
def format_rupiah(angka):
    return "Rp" + format(angka, ",").replace(",", ".")
# Fungsi untuk menerima input angka
def input_angka(pesan):
    benar = False
    while benar == False:
        try:
            angka = int(input(pesan))
            benar = True
        except ValueError:
            print("Input harus berupa angka!")
    return angka
# Fungsi menampilkan menu utama
def menu_utama():
    print("========================================")
    print("       SISTEM PEMESANAN TIKET BUS")
    print("========================================")
    print("1. Pesan Tiket")
    print("2. Riwayat Pemesanan")
    print("3. Daftar Harga")
    print("4. Keluar")
    print("========================================")
# Fungsi menampilkan daftar harga
def daftar_harga():
    print("========== DAFTAR HARGA TIKET ==========")
    for i in range(len(rute)):
        print(i + 1, ".", rute[i][0], "-", format_rupiah(rute[i][1]))
    print("Pilihan Kelas:")
    for nomor in kelas_tiket:
        nama = kelas_tiket[nomor][0]
        tambahan = kelas_tiket[nomor][1]
        print(nomor, ".", nama, "(+", format_rupiah(tambahan), ")")
    print("========================================")
# Fungsi pemesanan tiket
def pesan_tiket():
    print("========== PEMESANAN TIKET ==========")
    nama = input("Nama Pemesan: ")
    # Memilih rute
    print("Daftar Tujuan:")
    for i in range(len(rute)):
        print(i + 1, ".", rute[i][0])
    pilihan_rute = input_angka("Pilih tujuan: ")
    while pilihan_rute < 1 or pilihan_rute > len(rute):
        print("Pilihan tujuan tidak tersedia!")
        pilihan_rute = input_angka("Pilih tujuan: ")
    tujuan = rute[pilihan_rute - 1][0]
    harga_dasar = rute[pilihan_rute - 1][1]
    # Memilih jadwal
    print("Jadwal Keberangkatan:")
    for i in range(len(jadwal)):
        print(i + 1, ".", jadwal[i])
    pilihan_jadwal = input_angka("Pilih jadwal: ")
    while pilihan_jadwal < 1 or pilihan_jadwal > len(jadwal):
        print("Pilihan jadwal tidak tersedia!")
        pilihan_jadwal = input_angka("Pilih jadwal: ")
    waktu = jadwal[pilihan_jadwal - 1]
    # Memilih kelas tiket
    print("Pilihan Kelas Tiket:")
    for nomor in kelas_tiket:
        nama_kelas = kelas_tiket[nomor][0]
        tambahan = kelas_tiket[nomor][1]
        print(nomor, ".", nama_kelas, "(+", format_rupiah(tambahan), ")")
    pilihan_kelas = input("Pilih kelas: ")
    while pilihan_kelas not in kelas_tiket:
        print("Pilihan kelas tidak tersedia!")
        pilihan_kelas = input("Pilih kelas: ")
    nama_kelas = kelas_tiket[pilihan_kelas][0]
    tambahan_harga = kelas_tiket[pilihan_kelas][1]
    # Memasukkan jumlah tiket
    jumlah = input_angka("Jumlah tiket: ")
    while jumlah <= 0:
        print("Jumlah tiket harus lebih dari 0!")
        jumlah = input_angka("Jumlah tiket: ")
    # Menghitung harga
    harga_per_tiket = harga_dasar + tambahan_harga
    total = harga_per_tiket * jumlah
    print("========== RINCIAN PEMESANAN ==========")
    print("Nama Pemesan :", nama)
    print("Tujuan       :", tujuan)
    print("Jadwal       :", waktu)
    print("Kelas        :", nama_kelas)
    print("Jumlah Tiket :", jumlah)
    print("Harga Tiket  :", format_rupiah(harga_per_tiket))
    print("Total Bayar  :", format_rupiah(total))
    # Konfirmasi pesanan
    konfirmasi = input("Konfirmasi pesanan? (y/n): ").lower()
    if konfirmasi == "y":
        print("========== SIMULASI PEMBAYARAN ==========")
        print("Pembayaran sebesar", format_rupiah(total))
        print("Pembayaran berhasil!")
        # Membuat kode booking
        nomor_booking = len(riwayat) + 1
        kode_booking = "BUS" + str(nomor_booking).zfill(3)
        kode_booking_set.add(kode_booking)
        # Menyimpan data pemesanan menggunakan Dictionary
        pesanan = {
            "kode": kode_booking,
            "nama": nama,
            "tujuan": tujuan,
            "jadwal": waktu,
            "kelas": nama_kelas,
            "jumlah": jumlah,
            "total": total
        }
        riwayat.append(pesanan)
        # Menampilkan bukti pemesanan
        print("========== BUKTI PEMESANAN ==========")
        print("Pemesanan berhasil!")
        print("Kode Booking :", kode_booking)
        print("Nama         :", nama)
        print("Tujuan       :", tujuan)
        print("Jadwal       :", waktu)
        print("Kelas        :", nama_kelas)
        print("Jumlah Tiket :", jumlah)
        print("Total        :", format_rupiah(total))
        print("=====================================")
    else:
        print("Pemesanan dibatalkan.")
# Fungsi menampilkan riwayat pemesanan
def tampilkan_riwayat():
    print("========== RIWAYAT PEMESANAN ==========")
    if len(riwayat) == 0:
        print("Belum ada riwayat pemesanan.")
    else:
        for pesanan in riwayat:
            print("Kode Booking :", pesanan["kode"])
            print("Nama         :", pesanan["nama"])
            print("Tujuan       :", pesanan["tujuan"])
            print("Jadwal       :", pesanan["jadwal"])
            print("Kelas        :", pesanan["kelas"])
            print("Jumlah Tiket :", pesanan["jumlah"])
            print("Total        :", format_rupiah(pesanan["total"]))
    print("=======================================")
# Program utama
jalan = True
while jalan == True:
    menu_utama()
    pilihan = input_angka("Pilih menu: ")
    if pilihan == 1:
        pesan_tiket()
    elif pilihan == 2:
        tampilkan_riwayat()
    elif pilihan == 3:
        daftar_harga()
    elif pilihan == 4:
        print("Terima kasih telah menggunakan layanan kami.")
        jalan = False
    else:
        print("Pilihan menu tidak tersedia!")
#Wes YH Aku pe DOLAN!