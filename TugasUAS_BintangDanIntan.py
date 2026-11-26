rute = (("Surabaya - Malang", 50000),
    ("Surabaya - Kediri", 65000),
    ("Surabaya - Yogyakarta", 150000),
    ("Surabaya - Semarang", 120000))
kuota = [30, 30, 30, 30]
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
def pesan_tiket():
    nama = input("Nama Pemesan: ")
    for p in riwayat:
        if p["nama"].lower() == nama.lower():
            print("Nama tersebut sudah pernah melakukan pemesanan!")
            return
    print("Daftar Tujuan:")
    for i in range(len(rute)):
        if kuota[i] == 0:
            ket = "PENUH"
        else:
            ket = "sisa " + str(kuota[i]) + " tiket"
        print(i + 1, ".", rute[i][0], "- Rp", rute[i][1], "|", ket)
    pilih = input_angka("Pilih tujuan: ", len(rute))
    idx = pilih - 1
    if kuota[idx] == 0:
        print("Maaf, tiket tujuan ini sudah habis!")
        return
    tujuan = rute[idx][0]
    harga = rute[idx][1]
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
    jumlah = input_angka("Jumlah tiket (maks " + str(kuota[idx]) + "): ", kuota[idx])
    total = harga * jumlah
    print("Total Bayar: Rp", total)
    if input("Konfirmasi pesanan? (y/n): ").lower() == "y":
        kode = "BUS" + str(len(riwayat) + 1)
        kuota[idx] = kuota[idx] - jumlah
        pesanan = {"kode": kode, "nama": nama, "tujuan": tujuan, "idx": idx,
                   "jadwal": waktu, "kelas": kelas,
                   "jumlah": jumlah, "total": total, "status": "Aktif"}
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
                  "|", p["kelas"], "|", p["jumlah"], "tiket | Rp", p["total"],
                  "|", p["status"])
def batalkan_tiket():
    kode = input("Masukkan kode booking: ").upper()
    for p in riwayat:
        if p["kode"] == kode:
            if p["status"] == "Dibatalkan":
                print("Tiket ini sudah dibatalkan.")
            elif input("Yakin batalkan? (y/n): ").lower() == "y":
                p["status"] = "Dibatalkan"
                kuota[p["idx"]] = kuota[p["idx"]] + p["jumlah"]
                print("Tiket berhasil dibatalkan.")
            else:
                print("Pembatalan dibatalkan.")
            return
    print("Kode booking tidak ditemukan!")
while True:
    print("TIKET BUS: ")
    print("1. Pesan Tiket")
    print("2. Riwayat")
    print("3. Batalkan Tiket")
    print("4. Keluar")
    menu = input_angka("Pilih menu: ", 4)
    if menu == 1:
        pesan_tiket()
    elif menu == 2:
        tampilkan_riwayat()
    elif menu == 3:
        batalkan_tiket()
    else:
        print("Terima kasih!")
        break