rute = (("Surabaya - Malang", 50000),
        ("Surabaya - Kediri", 65000),
        ("Surabaya - Yogyakarta", 150000),
        ("Surabaya - Semarang", 120000))
kuota = [30, 30, 30, 30]
kursi_terisi = [[], [], [], []]
jadwal = ("08.00", "12.00", "16.00")
kelas_tiket = {1: ("Reguler", 0), 2: ("VIP", 25000), 3: ("VVIP", 50000)}
riwayat = []
akun = []
KODE_ADMIN = "admin123"
def input_angka(pesan, maksimal):
    while True:
        try:
            angka = int(input(pesan))
            if 1 <= angka <= maksimal:
                return angka
            print("Pilihan tidak tersedia!")
        except ValueError:
            print("Input harus berupa angka!")
# ===== AKUN =====
def registrasi():
    print("Daftar sebagai:")
    print("1. User")
    print("2. Admin")
    pilih = input_angka("Pilih: ", 2)
    role = "user"
    if pilih == 2:
        if input("Masukkan kode admin: ") != KODE_ADMIN:
            print("Kode admin salah! Registrasi dibatalkan.")
            return
        role = "admin"
    username = input("Username: ").strip()
    if username == "":
        print("Username tidak boleh kosong!")
        return
    for a in akun:
        if a["username"].lower() == username.lower():
            print("Username sudah dipakai!")
            return
    password = input("Password: ")
    if password == "":
        print("Password tidak boleh kosong!")
        return
    akun.append({"username": username, "password": password, "role": role})
    print("Registrasi berhasil sebagai", role + "! Silakan login.")
def login():
    username = input("Username: ").strip()
    password = input("Password: ")
    for a in akun:
        if a["username"].lower() == username.lower() and a["password"] == password:
            print("Login berhasil! Selamat datang,", a["username"])
            return a
    print("Username atau password salah!")
    return None
# ===== FITUR TIKET =====
def pilih_kursi(idx, jumlah):
    print("Kursi terisi:", kursi_terisi[idx])
    kursi_dipilih = []
    while len(kursi_dipilih) < jumlah:
        no = input_angka("Pilih kursi ke-" + str(len(kursi_dipilih) + 1) + " (1-30): ", 30)
        if no in kursi_terisi[idx] or no in kursi_dipilih:
            print("Kursi sudah terisi!")
        else:
            kursi_dipilih.append(no)
    return kursi_dipilih
def pesan_tiket(nama):
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
    # cek nama yang sama dengan rute yang sama
    for p in riwayat:
        if p["nama"].lower() == nama.lower() and p["tujuan"] == tujuan and p["status"] == "Aktif":
            print("Kamu sudah memesan rute ini!")
            return
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
    kursi = pilih_kursi(idx, jumlah)
    if input("Konfirmasi pesanan? (y/n): ").lower() == "y":
        kode = "BUS" + str(len(riwayat) + 1)
        kuota[idx] = kuota[idx] - jumlah
        kursi_terisi[idx] = kursi_terisi[idx] + kursi

        pesanan = {"kode": kode, "nama": nama, "tujuan": tujuan, "idx": idx,
                   "jadwal": waktu, "kelas": kelas, "kursi": kursi,
                   "jumlah": jumlah, "total": total, "status": "Aktif"}
        riwayat.append(pesanan)
        print("Pemesanan berhasil! Kode Booking:", kode)
        print("Kursi        :", kursi)
    else:
        print("Pemesanan dibatalkan.")
def tampilkan_riwayat(nama=None):
    # nama diisi -> riwayat milik user itu saja, kosong -> semua (untuk admin)
    ada = False
    for p in riwayat:
        if nama == None or p["nama"] == nama:
            ada = True
            print(p["kode"], "|", p["nama"], "|", p["tujuan"], "|", p["jadwal"],
                  "|", p["kelas"], "|", p["jumlah"], "tiket | Rp", p["total"])
            print("   Kursi:", p["kursi"], "| Status:", p["status"])
    if not ada:
        print("Belum ada riwayat pemesanan.")
def batalkan_tiket(nama):
    kode = input("Masukkan kode booking: ").upper()
    for p in riwayat:
        if p["kode"] == kode and p["nama"] == nama:
            if p["status"] == "Dibatalkan":
                print("Tiket ini sudah dibatalkan.")
            elif input("Yakin batalkan? (y/n): ").lower() == "y":
                p["status"] = "Dibatalkan"
                kuota[p["idx"]] = kuota[p["idx"]] + p["jumlah"]
                for k in p["kursi"]:
                    kursi_terisi[p["idx"]].remove(k)
                print("Tiket berhasil dibatalkan.")
            else:
                print("Pembatalan dibatalkan.")
            return
    print("Kode booking tidak ditemukan!")
def cetak_tiket(nama):
    kode = input("Masukkan kode booking: ").upper()
    for p in riwayat:
        if p["kode"] == kode and p["nama"] == nama:
            print("=" * 32)
            print("          E-TIKET BUS")
            print("=" * 32)
            print("Kode    :", p["kode"])
            print("Nama    :", p["nama"])
            print("Tujuan  :", p["tujuan"])
            print("Jadwal  :", p["jadwal"])
            print("Kelas   :", p["kelas"])
            print("Kursi   :", p["kursi"])
            print("Jumlah  :", p["jumlah"], "tiket")
            print("Total   : Rp", p["total"])
            print("Status  :", p["status"])
            print("=" * 32)
            return
    print("Kode booking tidak ditemukan!")
def laporan_pendapatan():
    total_semua = 0
    for i in range(len(rute)):
        subtotal = 0
        for p in riwayat:
            if p["idx"] == i and p["status"] == "Aktif":
                subtotal = subtotal + p["total"]
        print(rute[i][0], ": Rp", subtotal)
        total_semua = total_semua + subtotal
    print("Total pendapatan: Rp", total_semua)
# ===== MENU PER ROLE =====
def menu_user(nama):
    while True:
        print()
        print("MENU USER -", nama)
        print("1. Pesan Tiket")
        print("2. Riwayat Saya")
        print("3. Batalkan Tiket")
        print("4. Cetak E-Tiket")
        print("5. Logout")
        menu = input_angka("Pilih menu: ", 5)
        if menu == 1:
            pesan_tiket(nama)
        elif menu == 2:
            tampilkan_riwayat(nama)
        elif menu == 3:
            batalkan_tiket(nama)
        elif menu == 4:
            cetak_tiket(nama)
        else:
            print("Berhasil logout.")
            break
def menu_admin(nama):
    while True:
        print()
        print("MENU ADMIN -", nama)
        print("1. Laporan Pendapatan")
        print("2. Semua Riwayat Pemesanan")
        print("3. Logout")
        menu = input_angka("Pilih menu: ", 3)
        if menu == 1:
            laporan_pendapatan()
        elif menu == 2:
            tampilkan_riwayat()
        else:
            print("Berhasil logout.")
            break
# ===== PROGRAM UTAMA =====
while True:
    print()
    print("TIKET BUS")
    print("1. Registrasi")
    print("2. Login")
    print("3. Keluar")
    menu = input_angka("Pilih menu: ", 3)
    if menu == 1:
        registrasi()
    elif menu == 2:
        pengguna = login()
        if pengguna != None:
            if pengguna["role"] == "admin":
                menu_admin(pengguna["username"])
            else:
                menu_user(pengguna["username"])
    else:
        print("Terima kasih!")
        break