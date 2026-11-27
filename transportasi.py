# ============================================================
#  SISTEM LAYANAN TRANSPORTASI TERPADU (Bus + Travel + Kereta)
#  Dibangun hanya dengan teknik dari contoh 1.py:
#  tuple, list, dict, fungsi, while, for, if, try/except, string
#  TANPA import apapun.
# ============================================================

# ---------- DATA LAYANAN ----------
# layanan: (kode, jenis, rute, harga, kapasitas, jadwal, estimator_kecepatan_km_per_jam, fasilitas)
layanan = (("BUS-01", "Bus", "Surabaya - Malang", 50000, 30, ("08.00", "12.00", "16.00"), 60, ("AC", "Reclining Seat")),
           ("BUS-02", "Bus", "Surabaya - Kediri", 65000, 30, ("07.00", "13.00", "19.00"), 55, ("AC", "Wifi")),
           ("BUS-03", "Bus", "Surabaya - Yogyakarta", 150000, 30, ("06.00", "09.00", "21.00"), 60, ("AC", "Toilet", "Snack")),
           ("TRV-01", "Travel", "Surabaya - Malang", 75000, 8, ("06.00", "10.00", "15.00"), 70, ("AC", "Wifi", "Air Mineral")),
           ("TRV-02", "Travel", "Surabaya - Semarang", 110000, 8, ("05.00", "11.00", "17.00"), 70, ("AC", "Wifi")),
           ("KRT-01", "Kereta", "Surabaya - Yogyakarta", 220000, 40, ("05.30", "13.30"), 80, ("AC", "Toilet", "Kantin")),
           ("KRT-02", "Kereta", "Surabaya - Semarang", 180000, 40, ("07.15", "15.45"), 80, ("AC", "Colokan Listrik")))

# jarak tiap rute (km) untuk estimasi waktu tempuh
jarak = {"Surabaya - Malang": 95,
         "Surabaya - Kediri": 120,
         "Surabaya - Yogyakarta": 330,
         "Surabaya - Semarang": 215}

kuota = [30, 30, 30, 30, 8, 8, 40, 40]
kursi_terisi = [[], [], [], [], [], [], [], []]
kelas_tiket = {1: ("Ekonomi", 0), 2: ("Bisnis", 25000), 3: ("Eksekutif", 50000)}
jenis_layanan = ("Bus", "Travel", "Kereta")

# kode promo: (nama, potongan_tetap, minimal_belanja, aktif)
promo = {"HEMAT10": (10000, 50000, True),
         "LIBURAN": (25000, 150000, True),
         "MUDIK": (50000, 300000, True)}

# driver / operator: (nama, kendaraan, rating_total, jumlah_ulasan)
crew = [("Pak Budi Santoso", "BUS-01", 47, 10),
        ("Bu Siti Aminah", "BUS-02", 41, 9),
        ("Pak Joko Susilo", "BUS-03", 58, 12),
        ("Mas Andi Pratama", "TRV-01", 33, 7),
        ("Bu Rina Wulandari", "TRV-02", 35, 8),
        ("Pak Hendra Gunawan", "KRT-01", 58, 12),
        ("Pak Slamet Riyadi", "KRT-02", 44, 10)]

riwayat = []
akun = []
ulasan = []
KODE_ADMIN = "admin123"
counter_kode = 0

# ---------- UTIL ----------
def input_angka(pesan, maksimal):
    while True:
        try:
            angka = int(input(pesan))
            if 1 <= angka <= maksimal:
                return angka
            print("Pilihan tidak tersedia!")
        except ValueError:
            print("Input harus berupa angka!")

def uang(nominal):
    s = ""
    n = nominal
    if n == 0:
        return "0"
    while n > 0:
        tiga = n - (n // 1000) * 1000
        sisa = n // 1000
        if sisa > 0 and tiga < 10:
            s = "00" + str(tiga) + s
        elif sisa > 0 and tiga < 100:
            s = "0" + str(tiga) + s
        else:
            s = str(tiga) + s
        if sisa > 0:
            s = "." + s
        n = sisa
    return s

def estimasi_waktu(idx_layanan):
    r = layanan[idx_layanan][2]
    km = jarak[r]
    kecepatan = layanan[idx_layanan][6]
    menit = (km * 60) // kecepatan
    jam = menit // 60
    sisa = menit - (jam * 60)
    hasil = ""
    if jam > 0:
        hasil = hasil + str(jam) + " jam "
    hasil = hasil + str(sisa) + " menit"
    return hasil

def buat_kode(jenis):
    global counter_kode
    counter_kode = counter_kode + 1
    if jenis == "Bus":
        awal = "BB"
    elif jenis == "Travel":
        awal = "TT"
    else:
        awal = "KK"
    return awal + str(counter_kode)

def cari_layanan(kata):
    # pencarian rute / jenis berdasarkan kata kunci
    hasil = []
    kata = kata.lower()
    for i in range(len(layanan)):
        if kata in layanan[i][2].lower() or kata in layanan[i][1].lower():
            hasil.append(i)
    return hasil

def tampilkan_daftar(idx_hanya=None, urut_harga=False):
    daftar = []
    for i in range(len(layanan)):
        if idx_hanya == None or i in idx_hanya:
            daftar.append(i)
    if urut_harga:
        # insertion sort manual, hanya variabel dari contoh
        for a in range(1, len(daftar)):
            b = a
            while b > 0 and layanan[daftar[b]][3] < layanan[daftar[b - 1]][3]:
                simpan = daftar[b]
                daftar[b] = daftar[b - 1]
                daftar[b - 1] = simpan
                b = b - 1
    if len(daftar) == 0:
        print("Tidak ada layanan yang cocok.")
        return
    print("-" * 70)
    print("KODE  JENIS   RUTE                     HARGA      KAPASITAS")
    for i in daftar:
        if kuota[i] == 0:
            ket = "PENUH"
        else:
            ket = "sisa " + str(kuota[i])
        spasi = ""
        for _ in range(24 - len(layanan[i][2])):
            spasi = spasi + " "
        print(layanan[i][0], "|", layanan[i][1], "|", layanan[i][2] + spasi, "| Rp", uang(layanan[i][3]), "|", ket)
        print("      Jadwal:", layanan[i][5], "| Estimasi:", estimasi_waktu(i), "| Fasilitas:", layanan[i][7])
    print("-" * 70)

# ---------- AKUN ----------
def registrasi():
    print("Registrasi akun baru")
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
    if input("Masukkan kode admin (kosongkan bila user biasa): ") == KODE_ADMIN:
        role = "admin"
    else:
        role = "user"
    akun.append({"username": username, "password": password, "role": role,
                 "saldo": 0, "poin": 0, "member": "Reguler"})
    print("Registrasi berhasil sebagai", role + "! Silakan login.")

def login():
    username = input("Username: ").strip()
    password = input("Password: ")
    percobaan = 0
    for a in akun:
        if a["username"].lower() == username.lower() and a["password"] == password:
            print("Login berhasil! Selamat datang,", a["username"])
            print("Member:", a["member"], "| Poin:", a["poin"], "| Saldo: Rp", uang(a["saldo"]))
            return a
    print("Username atau password salah!")
    return None

# ---------- SALDO & POIN ----------
def cek_member(akun_user):
    # poin naikkan level member: Reguler -> Silver -> Gold
    if akun_user["poin"] >= 200 and akun_user["member"] != "Gold":
        akun_user["member"] = "Gold"
        print("Selamat! Kamu naik menjadi member GOLD (diskon 10%)!")
    elif akun_user["poin"] >= 50 and akun_user["member"] == "Reguler":
        akun_user["member"] = "Silver"
        print("Selamat! Kamu naik menjadi member SILVER (diskon 5%)!")

def diskon_member(akun_user):
    if akun_user["member"] == "Gold":
        return 10
    elif akun_user["member"] == "Silver":
        return 5
    return 0

def top_up(akun_user):
    nominal = input_angka("Nominal top-up (1-100): (dalam ribu rupiah) ", 100) * 1000
    akun_user["saldo"] = akun_user["saldo"] + nominal
    print("Top-up berhasil! Saldo sekarang: Rp", uang(akun_user["saldo"]))
    poin = nominal // 20000
    akun_user["poin"] = akun_user["poin"] + poin
    if poin > 0:
        print("Kamu mendapat", poin, "poin dari top-up.")
    cek_member(akun_user)

def tukar_poin(akun_user):
    print("Poin kamu:", akun_user["poin"])
    print("1. 50 poin  -> potongan Rp 10.000")
    print("2. 150 poin -> potongan Rp 35.000")
    print("3. 200 poin -> potongan Rp 50.000")
    pilih = input_angka("Pilih: ", 3)
    biaya_poin = (50, 150, 200)
    nilai = (10000, 35000, 50000)
    if akun_user["poin"] < biaya_poin[pilih - 1]:
        print("Poin tidak cukup!")
        return
    akun_user["poin"] = akun_user["poin"] - biaya_poin[pilih - 1]
    akun_user["saldo"] = akun_user["saldo"] + nilai[pilih - 1]
    print("Berhasil! Poin ditukar jadi saldo. Saldo sekarang: Rp", uang(akun_user["saldo"]))

# ---------- PEMESANAN ----------
def pilih_kursi(idx, jumlah):
    kapasitas = layanan[idx][4]
    print("Kursi terisi:", kursi_terisi[idx])
    kursi_dipilih = []
    while len(kursi_dipilih) < jumlah:
        no = input_angka("Pilih kursi ke-" + str(len(kursi_dipilih) + 1) + " (1-" + str(kapasitas) + "): ", kapasitas)
        if no in kursi_terisi[idx] or no in kursi_dipilih:
            print("Kursi sudah terisi!")
        else:
            kursi_dipilih.append(no)
    return kursi_dipilih

def pesan_tiket(akun_user):
    print("1. Lihat semua layanan")
    print("2. Cari layanan (kata kunci)")
    print("3. Lihat termurah dulu")
    pilih = input_angka("Pilih: ", 3)
    if pilih == 2:
        kata = input("Kata kunci (contoh: malang / kereta): ")
        hasil = cari_layanan(kata)
        tampilkan_daftar(hasil)
        if len(hasil) == 0:
            return
        pilih_l = input_angka("Pilih nomor layanan (1-" + str(len(hasil)) + "): ", len(hasil))
        idx = hasil[pilih_l - 1]
    elif pilih == 3:
        daftar = []
        for i in range(len(layanan)):
            daftar.append(i)
        tampilkan_daftar(None, True)
        pilih_l = input_angka("Pilih nomor urut pada daftar (1-" + str(len(daftar)) + "): ", len(daftar))
        # hitung idx sesuai urutan termurah
        for a in range(1, len(daftar)):
            b = a
            while b > 0 and layanan[daftar[b]][3] < layanan[daftar[b - 1]][3]:
                simpan = daftar[b]
                daftar[b] = daftar[b - 1]
                daftar[b - 1] = simpan
                b = b - 1
        idx = daftar[pilih_l - 1]
    else:
        tampilkan_daftar()
        idx = input_angka("Pilih nomor layanan (1-" + str(len(layanan)) + "): ", len(layanan)) - 1
    if kuota[idx] == 0:
        print("Maaf, kuota layanan ini sudah habis!")
        return
    kode_l = layanan[idx][0]
    tujuan = layanan[idx][2]
    # cek pemesanan ganda rute sama masih aktif
    for p in riwayat:
        if p["kode_layanan"] == kode_l and p["pembeli"] == akun_user["username"] and p["status"] == "Aktif":
            print("Kamu sudah punya tiket aktif di layanan ini!")
            return
    print("Jadwal tersedia:", layanan[idx][5])
    pilih_j = input_angka("Pilih jadwal: ", len(layanan[idx][5]))
    waktu = layanan[idx][5][pilih_j - 1]
    print("Kelas tiket:")
    for nomor in kelas_tiket:
        print(nomor, ".", kelas_tiket[nomor][0], "(+ Rp", uang(kelas_tiket[nomor][1]), ")")
    pilih_k = input_angka("Pilih kelas: ", len(kelas_tiket))
    kelas = kelas_tiket[pilih_k][0]
    harga_satuan = layanan[idx][3] + kelas_tiket[pilih_k][1]
    jumlah = input_angka("Jumlah tiket (maks " + str(kuota[idx]) + "): ", kuota[idx])
    total = harga_satuan * jumlah
    print("Estimasi perjalanan:", estimasi_waktu(idx))
    # promo
    potongan = 0
    if input("Pakai kode promo? (y/n): ").lower() == "y":
        kode_p = input("Kode promo: ").upper()
        if kode_p in promo and promo[kode_p][2]:
            if total >= promo[kode_p][1]:
                potongan = potongan + promo[kode_p][0]
                print("Promo", kode_p, "berhasil! Potongan Rp", uang(promo[kode_p][0]))
            else:
                print("Minimal belanja Rp", uang(promo[kode_p][1]), "untuk promo ini.")
        else:
            print("Kode promo tidak valid!")
    # diskon member
    persen = diskon_member(akun_user)
    potongan = potongan + (total * persen) // 100
    if persen > 0:
        print("Diskon member", akun_user["member"] + ":", persen, "%")
    total = total - potongan
    if total < 0:
        total = 0
    print("Total Bayar : Rp", uang(total))
    print("Saldo kamu : Rp", uang(akun_user["saldo"]))
    if akun_user["saldo"] < total:
        print("Saldo kurang! Silakan top-up dulu.")
        return
    kursi = pilih_kursi(idx, jumlah)
    if input("Konfirmasi pesanan? (y/n): ").lower() == "y":
        kode = buat_kode(layanan[idx][1])
        akun_user["saldo"] = akun_user["saldo"] - total
        kuota[idx] = kuota[idx] - jumlah
        kursi_terisi[idx] = kursi_terisi[idx] + kursi
        poin_baru = total // 25000
        akun_user["poin"] = akun_user["poin"] + poin_baru
        pesanan = {"kode": kode, "pembeli": akun_user["username"], "idx": idx,
                   "kode_layanan": kode_l, "jenis": layanan[idx][1], "tujuan": tujuan,
                   "jadwal": waktu, "kelas": kelas, "kursi": kursi,
                   "jumlah": jumlah, "total": total, "potongan": potongan,
                   "status": "Aktif", "rating": 0}
        riwayat.append(pesanan)
        print("Pemesanan berhasil! Kode Booking:", kode)
        print("Kursi        :", kursi)
        print("Poin didapat :", poin_baru)
        cek_member(akun_user)
    else:
        print("Pemesanan dibatalkan.")

def ubah_jadwal(akun_user):
    kode = input("Masukkan kode booking: ").upper()
    for p in riwayat:
        if p["kode"] == kode and p["pembeli"] == akun_user["username"] and p["status"] == "Aktif":
            print("Jadwal sekarang:", p["jadwal"])
            idx = p["idx"]
            print("Jadwal tersedia:", layanan[idx][5])
            baru = input_angka("Pilih jadwal baru: ", len(layanan[idx][5]))
            biaya = 10000
            if akun_user["saldo"] < biaya:
                print("Saldo kurang untuk biaya ubah jadwal (Rp 10.000).")
                return
            if input("Ubah jadwal jadi " + layanan[idx][5][baru - 1] + "? (y/n): ").lower() == "y":
                akun_user["saldo"] = akun_user["saldo"] - biaya
                p["jadwal"] = layanan[idx][5][baru - 1]
                print("Jadwal berhasil diubah! Saldo berkurang Rp", uang(biaya))
            return
    print("Kode booking tidak ditemukan / tiket tidak aktif!")

def beri_rating(akun_user):
    kode = input("Masukkan kode booking: ").upper()
    for p in riwayat:
        if p["kode"] == kode and p["pembeli"] == akun_user["username"]:
            if p["rating"] > 0:
                print("Kamu sudah memberi rating untuk tiket ini.")
                return
            print("Perjalanan", p["tujuan"], "bersama", p["jenis"])
            nilai = input_angka("Rating (1-5): ", 5)
            p["rating"] = nilai
            for c in range(len(crew)):
                if crew[c][1] == p["kode_layanan"]:
                    crew[c] = (crew[c][0], crew[c][1], crew[c][2] + nilai, crew[c][3] + 1)
            ulasan.append({"kode": kode, "user": akun_user["username"], "rating": nilai,
                           "komentar": input("Komentar (boleh dikosongkan): ")})
            print("Terima kasih atas ratingnya!")
            return
    print("Kode booking tidak ditemukan!")

def batalkan_tiket(akun_user):
    kode = input("Masukkan kode booking: ").upper()
    for p in riwayat:
        if p["kode"] == kode and p["pembeli"] == akun_user["username"]:
            if p["status"] == "Dibatalkan":
                print("Tiket ini sudah dibatalkan.")
            elif input("Yakin batalkan? (y/n): ").lower() == "y":
                p["status"] = "Dibatalkan"
                kuota[p["idx"]] = kuota[p["idx"]] + p["jumlah"]
                for k in p["kursi"]:
                    kursi_terisi[p["idx"]].remove(k)
                # refund 80% masuk saldo
                refund = (p["total"] * 80) // 100
                akun_user["saldo"] = akun_user["saldo"] + refund
                print("Tiket dibatalkan. Refund 80% = Rp", uang(refund), "masuk saldo.")
            else:
                print("Pembatalan dibatalkan.")
            return
    print("Kode booking tidak ditemukan!")

def cetak_tiket(akun_user):
    kode = input("Masukkan kode booking: ").upper()
    for p in riwayat:
        if p["kode"] == kode and p["pembeli"] == akun_user["username"]:
            print("=" * 40)
            print("        E-TIKET LAYANAN TRANSPORTASI")
            print("=" * 40)
            print("Kode      :", p["kode"])
            print("Pembeli   :", p["pembeli"])
            print("Layanan   :", p["jenis"], "(", p["kode_layanan"], ")")
            print("Rute      :", p["tujuan"])
            print("Jadwal    :", p["jadwal"])
            print("Estimasi  :", estimasi_waktu(p["idx"]))
            print("Kelas     :", p["kelas"])
            print("Kursi     :", p["kursi"])
            print("Jumlah    :", p["jumlah"], "tiket")
            print("Potongan  : Rp", uang(p["potongan"]))
            print("Total     : Rp", uang(p["total"]))
            print("Status    :", p["status"])
            print("=" * 40)
            return
    print("Kode booking tidak ditemukan!")

def tampilkan_riwayat(akun_user=None):
    ada = False
    for p in riwayat:
        if akun_user == None or p["pembeli"] == akun_user["username"]:
            ada = True
            print(p["kode"], "|", p["pembeli"], "|", p["jenis"], "|", p["tujuan"],
                  "|", p["jadwal"], "|", p["kelas"], "|", p["jumlah"], "tiket | Rp", uang(p["total"]))
            print("   Kursi:", p["kursi"], "| Status:", p["status"], "| Rating:", p["rating"])
    if not ada:
        print("Belum ada riwayat pemesanan.")

# ---------- ADMIN ----------
def laporan_pendapatan():
    print("Pendapatan per layanan (tiket Aktif saja):")
    total_semua = 0
    for i in range(len(layanan)):
        subtotal = 0
        terjual = 0
        for p in riwayat:
            if p["idx"] == i and p["status"] == "Aktif":
                subtotal = subtotal + p["total"]
                terjual = terjual + p["jumlah"]
        print(layanan[i][0], layanan[i][2] + ":", "Rp", uang(subtotal), "| tiket terjual:", terjual)
        total_semua = total_semua + subtotal
    print("Total pendapatan: Rp", uang(total_semua))
    dibatalkan = 0
    for p in riwayat:
        if p["status"] == "Dibatalkan":
            dibatalkan = dibatalkan + 1
    print("Pembatalan:", dibatalkan, "pesanan")

def laporan_crew():
    print("RATING CREW / OPERATOR")
    for c in crew:
        if c[3] == 0:
            rata = 0
        else:
            rata = c[2] / c[3]
        tampil = str(rata)
        # potong jadi 1 angka desimal tanpa fungsi format
        if "." in tampil:
            bagian = tampil.split(".")
            if len(bagian[1]) > 1:
                tampil = bagian[0] + "." + bagian[1][0] + "/" + str(c[3]) + " ulasan"
            else:
                tampil = tampil + "/" + str(c[3]) + " ulasan"
        else:
            tampil = tampil + "/" + str(c[3]) + " ulasan"
        print(c[0], "-", c[1], ":", tampil, "bintang")

def lihat_ulasan():
    if len(ulasan) == 0:
        print("Belum ada ulasan.")
        return
    for u in ulasan:
        print(u["kode"], "|", u["user"], "|", u["rating"], "bintang")
        if u["komentar"] != "":
            print('   "', u["komentar"], '"')

def kelola_promo():
    print("Daftar promo saat ini:")
    for k in promo:
        status = "AKTIF"
        if not promo[k][2]:
            status = "NONAKTIF"
        print(k, "| potongan Rp", uang(promo[k][0]), "| min belanja Rp", uang(promo[k][1]), "|", status)
    print("1. Aktifkan/Nonaktifkan promo")
    print("2. Tambah promo baru")
    pilih = input_angka("Pilih: ", 2)
    if pilih == 1:
        nama = input("Nama promo: ").upper()
        if nama in promo:
            data = promo[nama]
            promo[nama] = (data[0], data[1], not data[2])
            print("Status promo", nama, "diubah.")
        else:
            print("Promo tidak ditemukan!")
    else:
        nama = input("Nama promo baru: ").upper()
        if nama == "":
            print("Nama tidak boleh kosong!")
            return
        potongan = input_angka("Potongan (1-500): ", 500) * 1000
        minimal = input_angka("Minimal belanja (1-1000): ", 1000) * 1000
        promo[nama] = (potongan, minimal, True)
        print("Promo", nama, "ditambahkan!")

def statistik_layanan():
    terlaris = 0
    idx_terlaris = 0
    for i in range(len(layanan)):
        terjual = 0
        for p in riwayat:
            if p["idx"] == i and p["status"] == "Aktif":
                terjual = terjual + p["jumlah"]
        okupansi = (terjual * 100) // layanan[i][4]
        print(layanan[i][0], layanan[i][2], "| terjual:", terjual, "| okupansi:", okupansi, "%")
        if terjual > terlaris:
            terlaris = terjual
            idx_terlaris = i
    print("Rute terlaris:", layanan[idx_terlaris][0], "-", layanan[idx_terlaris][2], "(" + str(terlaris), "tiket)")

# ---------- MENU ----------
def menu_user(akun_user):
    while True:
        print()
        print("MENU PENUMPANG -", akun_user["username"])
        print("Member:", akun_user["member"], "| Poin:", akun_user["poin"], "| Saldo: Rp", uang(akun_user["saldo"]))
        print("1. Pesan Tiket")
        print("2. Riwayat Saya")
        print("3. Batalkan Tiket (refund 80%)")
        print("4. Ubah Jadwal")
        print("5. Cetak E-Tiket")
        print("6. Beri Rating & Ulasan")
        print("7. Top-Up Saldo")
        print("8. Tukar Poin")
        print("9. Logout")
        menu = input_angka("Pilih menu: ", 9)
        if menu == 1:
            pesan_tiket(akun_user)
        elif menu == 2:
            tampilkan_riwayat(akun_user)
        elif menu == 3:
            batalkan_tiket(akun_user)
        elif menu == 4:
            ubah_jadwal(akun_user)
        elif menu == 5:
            cetak_tiket(akun_user)
        elif menu == 6:
            beri_rating(akun_user)
        elif menu == 7:
            top_up(akun_user)
        elif menu == 8:
            tukar_poin(akun_user)
        else:
            print("Berhasil logout.")
            break

def menu_admin(nama):
    while True:
        print()
        print("MENU ADMIN -", nama)
        print("1. Laporan Pendapatan")
        print("2. Statistik Layanan & Rute Terlaris")
        print("3. Semua Riwayat Pemesanan")
        print("4. Rating Crew")
        print("5. Lihat Ulasan Penumpang")
        print("6. Kelola Promo")
        print("7. Logout")
        menu = input_angka("Pilih menu: ", 7)
        if menu == 1:
            laporan_pendapatan()
        elif menu == 2:
            statistik_layanan()
        elif menu == 3:
            tampilkan_riwayat()
        elif menu == 4:
            laporan_crew()
        elif menu == 5:
            lihat_ulasan()
        elif menu == 6:
            kelola_promo()
        else:
            print("Berhasil logout.")
            break

# ---------- PROGRAM UTAMA ----------
print("=" * 50)
print("   SELAMAT DATANG DI LAYANAN TRANSPORTASI TERPADU")
print("   Bus antar kota, Travel, dan Kereta dalam satu sistem")
print("=" * 50)
while True:
    print()
    print("1. Registrasi")
    print("2. Login")
    print("3. Lihat Daftar Layanan (tanpa login)")
    print("4. Keluar")
    menu = input_angka("Pilih menu: ", 4)
    if menu == 1:
        registrasi()
    elif menu == 2:
        pengguna = login()
        if pengguna != None:
            if pengguna["role"] == "admin":
                menu_admin(pengguna["username"])
            else:
                menu_user(pengguna)
    elif menu == 3:
        tampilkan_daftar()
    else:
        print("Terima kasih! Sampai jumpa di perjalanan berikutnya.")
        break
