rute = (("Surabaya - Malang", 50000),
    ("Surabaya - Kediri", 65000),
    ("Surabaya - Yogyakarta", 150000),
    ("Surabaya - Semarang", 120000))
jadwal = ("08.00", "12.00", "16.00")
kelas_tiket = {1: ("Reguler", 0), 2: ("VIP", 25000), 3: ("VVIP", 50000)}
riwayat = []
def input_angka(pesan, maksimal):
    while True:
        try:
            angka = int(input(pesan))
            if angka >= 1 and angka <= maksimal:
                return angka
            print("Pilihan tidak tersedia!")
        except ValueError:
            print("Input harus berupa angka!")
def daftar_harga():
    print("DAFTAR HARGA: ")
    for i in range(len(rute)):
        print(i + 1, ".", rute[i][0], "- Rp", rute[i][1])
    for nomor in kelas_tiket:
        print(nomor, ".", kelas_tiket[nomor][0], "(+ Rp", kelas_tiket[nomor][1], ")")
def pesan_tiket():
    nama = input("Nama Pemesan: ")
    print("Daftar Tujuan:")
    for i in range(len(rute)):
        print(i + 1, ".", rute[i][0])
    pilih = input_angka("Pilih tujuan: ", len(rute))
    tujuan = rute[pilih - 1][0]
    harga = rute[pilih - 1][1]
    print("Jadwal:")
    for i in range(len(jadwal)):
        print(i + 1, ".", jadwal[i])
    pilih = input_angka("Pilih jadwal: ", len(jadwal))
    waktu = jadwal[pilih - 1]
    print("Kelas:")
    for nomor in kelas_tiket:
        print(nomor, ".", kelas_tiket[nomor][0], "(+ Rp", kelas_tiket[nomor][1], ")")
    pilih = input_angka("Pilih kelas: ", len(kelas_tiket))
    kelas = kelas_tiket[pilih][0]
    harga = harga + kelas_tiket[pilih][1]
    jumlah = input_angka("Jumlah tiket: ", 100)
    total = harga * jumlah
    print("Total Bayar: Rp", total)
    if input("Konfirmasi pesanan? (y/n): ").lower() == "y":
        kode = "BUS" + str(len(riwayat) + 1)
        pesanan = {"kode": kode, "nama": nama, "tujuan": tujuan,
                   "jadwal": waktu, "kelas": kelas,
                   "jumlah": jumlah, "total": total}
        riwayat.append(pesanan)
        print("Pemesanan berhasil! Kode Booking:", kode)
    else:
        print("Pemesanan dibatalkan.( Anda hanya dapat menginput kan y/n saja )")
def tampilkan_riwayat():
    print("RIWAYAT: ")
    if len(riwayat) == 0:
        print("Belum ada riwayat.")
    else:
        for p in riwayat:
            print(p["kode"], "|", p["nama"], "|", p["tujuan"], "|", p["jadwal"],
                  "|", p["kelas"], "|", p["jumlah"], "tiket | Rp", p["total"])
while True:
    print("TIKET BUS: ")
    print("1. Pesan Tiket")
    print("2. Riwayat")
    print("3. Daftar Harga")
    print("4. Keluar")
    menu = input_angka("Pilih menu: ", 4)
    if menu == 1:
        pesan_tiket()
    elif menu == 2:
        tampilkan_riwayat()
    elif menu == 3:
        daftar_harga()
    else:
        print("Terima kasih!")
        break