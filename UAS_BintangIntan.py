layanan = (
    ("BUS-01","Bus",   "Surabaya - Malang",     50000,30,("08.00","12.00","16.00"),60,("AC","Reclining Seat"),"Hino RN 285"),
    ("BUS-02","Bus",   "Surabaya - Kediri",     65000,30,("07.00","13.00","19.00"),55,("AC","Wifi"),"Mercedes OH 1526"),
    ("BUS-03","Bus",   "Surabaya - Yogyakarta",150000,30,("06.00","09.00","21.00"),60,("AC","Toilet","Snack"),"Scania K360"),
    ("BUS-04","Bus",   "Malang - Yogyakarta",  120000,30,("07.00","14.00"),        60,("AC","Toilet"),"Hino RN 285"),
    ("TRV-01","Travel","Surabaya - Malang",     75000, 8,("06.00","10.00","15.00"),70,("AC","Wifi","Air Mineral"),"Toyota HiAce"),
    ("TRV-02","Travel","Surabaya - Semarang",  110000, 8,("05.00","11.00","17.00"),70,("AC","Wifi"),"Isuzu Elf"),
    ("TRV-03","Travel","Malang - Semarang",     95000, 8,("06.00","13.00"),        65,("AC","Snack"),"Toyota HiAce"),
    ("KRT-01","Kereta","Surabaya - Yogyakarta",220000,40,("05.30","13.30"),        80,("AC","Toilet","Kantin"),"KA Sancaka"),
    ("KRT-02","Kereta","Surabaya - Semarang",  180000,40,("07.15","15.45"),        80,("AC","Colokan"),"KA Harina"),
    ("KRT-03","Kereta","Semarang - Yogyakarta", 80000,40,("06.00","12.00","18.00"),75,("AC","Colokan"),"KA Kamandaka"),
)

# Kota yang bisa jadi titik transit
kota_simpul = ("Surabaya", "Malang", "Kediri", "Yogyakarta", "Semarang")

# Jarak antar kota dalam km (untuk hitung estimasi waktu)
jarak = {
    "Surabaya - Malang":     95,
    "Surabaya - Kediri":    120,
    "Surabaya - Yogyakarta":330,
    "Surabaya - Semarang":  215,
    "Malang - Yogyakarta":  260,
    "Malang - Semarang":    275,
    "Semarang - Yogyakarta":115,
}

# Kuota kursi tersisa per layanan (urut sesuai tuple layanan)
kuota = [30, 30, 30, 30, 8, 8, 8, 40, 40, 40]

# Daftar nomor kursi yang sudah terisi per layanan
kursi_terisi = [[], [], [], [], [], [], [], [], [], []]

# Pilihan kelas: nomor -> (nama kelas, tambahan harga)
kelas_tiket = {
    1: ("Ekonomi",    0),
    2: ("Bisnis",  25000),
    3: ("Eksekutif",50000),
}

# Paket asuransi: nomor -> (nama, premi, limit_kecelakaan, limit_barang)
paket_asuransi = {
    1: ("Tanpa Asuransi",    0,          0,         0),
    2: ("Basic Cover",   15000,  50000000,   5000000),
    3: ("Plus Cover",    30000, 100000000,  10000000),
    4: ("Premium Cover", 50000, 200000000,  25000000),
}

# Promo: kode -> (potongan, min_belanja, nama, aktif, sudah_pakai, maks_pakai)
promo = {
    "HEMAT10": (10000,  50000, "Hemat Harian",  True, 0, 999),
    "LIBURAN": (25000, 150000, "Promo Liburan", True, 0, 100),
    "MUDIK":   (50000, 300000, "Paket Mudik",   True, 0,  50),
}

# Crew: [nama, kode_layanan, total_rating, jumlah_ulasan, aktif]
crew = [
    ["Pak Budi Santoso",   "BUS-01", 47, 10, True],
    ["Bu Siti Aminah",     "BUS-02", 41,  9, True],
    ["Pak Joko Susilo",    "BUS-03", 58, 12, True],
    ["Pak Eko Prasetyo",   "BUS-04", 36,  8, True],
    ["Mas Andi Pratama",   "TRV-01", 33,  7, True],
    ["Bu Rina Wulandari",  "TRV-02", 35,  8, True],
    ["Pak Dedy Kurniawan", "TRV-03", 29,  6, True],
    ["Pak Hendra Gunawan", "KRT-01", 58, 12, True],
    ["Pak Slamet Riyadi",  "KRT-02", 44, 10, True],
    ["Bu Dewi Lestari",    "KRT-03", 50, 11, True],
]

# Level member: (nama, min_poin, diskon_persen)
TIER = (
    ("Reguler",   0,  0),
    ("Silver",   50,  5),
    ("Gold",    200, 10),
    ("Platinum",500, 15),
)

# Variabel global yang berubah saat program berjalan
riwayat       = []   # semua pesanan
waitlist      = []   # antrian waitlist
ulasan        = []   # semua ulasan dari user
notifikasi    = {}   # username -> list pesan
log_aktivitas = []   # catatan semua aksi
akun          = []   # semua akun terdaftar
counter_kode  = [0]  # pakai list agar bisa diubah di dalam fungsi
KODE_ADMIN    = "admin123"


# ================================================================
#  BAGIAN 1 - FUNGSI UTILITAS (alat bantu umum)
# ================================================================

def input_angka(pesan, maksimal, minimal=1):
    """Minta input angka dari user. Ulangi sampai valid."""
    while True:
        try:
            angka = int(input(pesan))
            if minimal <= angka <= maksimal:
                return angka
            print("  Pilihan tidak tersedia! Masukkan angka", minimal, "-", maksimal)
        except ValueError:
            print("  Input tidak valid! Harus berupa angka.")

def input_angka_atau_batal(pesan, maksimal, minimal=1):
    """
    Sama seperti input_angka, tapi angka 0 berarti batal/kembali.
    Mengembalikan -1 jika user ketik 0.
    """
    while True:
        try:
            angka = int(input(pesan))
            if angka == 0:
                return -1
            if minimal <= angka <= maksimal:
                return angka
            print("  Pilihan tidak tersedia! (0=Batal,", minimal, "-", str(maksimal) + ")")
        except ValueError:
            print("  Input tidak valid! Harus berupa angka.")

def input_teks(pesan, boleh_kosong=False):
    """
    Minta input teks dari user.
    Jika boleh_kosong=False, ulangi sampai user isi sesuatu.
    """
    while True:
        teks = input(pesan).strip()
        if teks != "":
            return teks
        if boleh_kosong:
            return ""
        print("  Input tidak boleh kosong!")

def input_ya_tidak(pesan):
    """Minta konfirmasi y/n. Ulangi sampai valid."""
    while True:
        jawab = input(pesan).strip().lower()
        if jawab == "y" or jawab == "n":
            return jawab
        print("  Ketik y (ya) atau n (tidak).")

def uang(n):
    """Ubah angka jadi format rupiah. Contoh: 150000 -> '150.000'"""
    if n == 0:
        return "0"
    s = ""
    while n > 0:
        tiga = n % 1000
        n    = n // 1000
        if n > 0:
            if tiga < 10:
                s = ".00" + str(tiga) + s
            elif tiga < 100:
                s = ".0"  + str(tiga) + s
            else:
                s = "."   + str(tiga) + s
        else:
            s = str(tiga) + s
    return s

def desimal1(x):
    """Tampilkan float dengan 1 angka desimal. Contoh: 4.666 -> '4.6'"""
    bagian = str(x).split(".")
    if len(bagian) == 1:
        return bagian[0] + ".0"
    return bagian[0] + "." + bagian[1][0]

def bintang(n, dari=5):
    """Buat tampilan bintang. Contoh: bintang(3) -> '***  '"""
    s = ""
    for i in range(dari):
        if i < n:
            s = s + "*"
        else:
            s = s + "."
    return s

def bar(nilai, maksimal, lebar=20):
    """Buat progress bar ASCII. Contoh: [####----] 4/10"""
    if maksimal == 0:
        isi = 0
    else:
        isi = (nilai * lebar) // maksimal
    return "[" + "#" * isi + "-" * (lebar - isi) + "] " + str(nilai) + "/" + str(maksimal)

def tambah_notif(username, pesan):
    """Tambahkan notifikasi ke inbox user."""
    if username not in notifikasi:
        notifikasi[username] = []
    notifikasi[username].append(pesan)

def catat_log(username, aksi, detail=""):
    """Catat aktivitas user ke log."""
    log_aktivitas.append({"username": username, "aksi": aksi, "detail": detail})

def buat_kode_booking(jenis):
    """Buat kode booking unik. Contoh: BB0001, TT0002, KK0003"""
    counter_kode[0] = counter_kode[0] + 1
    if jenis == "Bus":
        prefix = "BB"
    elif jenis == "Travel":
        prefix = "TT"
    else:
        prefix = "KK"
    nomor = str(counter_kode[0])
    while len(nomor) < 4:
        nomor = "0" + nomor
    return prefix + nomor

def hitung_jam_tiba(idx, jadwal_str):
    """Hitung jam tiba berdasarkan jadwal berangkat + estimasi durasi."""
    rute  = layanan[idx][2]
    km    = jarak.get(rute, 0)
    kec   = layanan[idx][6]
    total = (km * 60) // kec          # total menit perjalanan

    bagian = jadwal_str.split(".")
    jam    = int(bagian[0])
    mnt    = int(bagian[1]) if len(bagian) > 1 else 0
    total  = total + mnt + jam * 60   # tambah jam berangkat

    jt = (total // 60) % 24
    mt = total % 60
    if mt < 10:
        return str(jt) + ".0" + str(mt)
    return str(jt) + "." + str(mt)

def hitung_durasi(idx):
    """Hitung durasi perjalanan dalam format '2 jam 30 menit'."""
    rute = layanan[idx][2]
    km   = jarak.get(rute, 0)
    kec  = layanan[idx][6]
    mnt  = (km * 60) // kec
    return str(mnt // 60) + " jam " + str(mnt % 60) + " menit"

def garis(karakter="-", panjang=60):
    """Cetak garis pemisah."""
    print(karakter * panjang)


# ================================================================
#  BAGIAN 2 - TAMPILAN DAFTAR LAYANAN
# ================================================================

def tampilkan_layanan(idx_hanya=None, urut_harga=False, urut_rating=False):
    """
    Tampilkan daftar layanan tersedia.
    idx_hanya = list indeks yang ingin ditampilkan (None = semua).
    """
    # Kumpulkan indeks yang akan ditampilkan
    daftar = []
    for i in range(len(layanan)):
        if idx_hanya == None or i in idx_hanya:
            daftar.append(i)

    if len(daftar) == 0:
        print("  Tidak ada layanan yang cocok.")
        return

    # Urutkan berdasarkan harga (insertion sort)
    if urut_harga:
        for a in range(1, len(daftar)):
            b = a
            while b > 0 and layanan[daftar[b]][3] < layanan[daftar[b-1]][3]:
                daftar[b], daftar[b-1] = daftar[b-1], daftar[b]
                b = b - 1

    # Urutkan berdasarkan rating crew (insertion sort, terbesar dulu)
    if urut_rating:
        for a in range(1, len(daftar)):
            b = a
            while b > 0:
                # Ambil rating crew untuk dua indeks yang dibandingkan
                r1 = 0.0
                r2 = 0.0
                for c in crew:
                    if c[1] == layanan[daftar[b]][0] and c[3] > 0:
                        r1 = c[2] / c[3]
                    if c[1] == layanan[daftar[b-1]][0] and c[3] > 0:
                        r2 = c[2] / c[3]
                if r1 > r2:
                    daftar[b], daftar[b-1] = daftar[b-1], daftar[b]
                    b = b - 1
                else:
                    break

    # Cetak header
    garis("=", 70)
    print("NO  KODE    JENIS    RUTE                      HARGA      SISA KURSI")
    garis("=", 70)

    for no in range(len(daftar)):
        i = daftar[no]

        # Status kursi
        if kuota[i] == 0:
            status_kursi = "PENUH"
        else:
            status_kursi = str(kuota[i]) + " kursi"

        # Hitung antrian waitlist
        wl = 0
        for w in waitlist:
            if w["idx"] == i:
                wl = wl + 1
        if wl > 0:
            status_kursi = status_kursi + " (WL:" + str(wl) + ")"

        # Cetak baris utama layanan
        print(str(no + 1).rjust(2), layanan[i][0], "|",
              layanan[i][1].ljust(7), "|",
              layanan[i][2].ljust(25), "|",
              "Rp " + uang(layanan[i][3]).rjust(8), "|",
              status_kursi)

        # Cetak detail: jadwal, durasi, rating, fasilitas
        for c in crew:
            if c[1] == layanan[i][0] and c[4]:
                if c[3] > 0:
                    rat = desimal1(c[2] / c[3])
                    bint = bintang(c[2] // c[3])
                else:
                    rat = "0.0"
                    bint = bintang(0)
                print("     Jadwal:", layanan[i][5],
                      "| Durasi:", hitung_durasi(i),
                      "| Rating:", bint, rat,
                      "| Fasilitas:", layanan[i][7],
                      "| Armada:", layanan[i][8])

    garis("=", 70)


# ================================================================
#  BAGIAN 3 - RUTE CONNECTING (transit)
# ================================================================

def cari_rute_langsung(asal, tujuan):
    """Cari indeks layanan yang rutenya asal-tujuan."""
    target = asal + " - " + tujuan
    hasil = []
    for i in range(len(layanan)):
        if layanan[i][2].lower() == target.lower():
            hasil.append(i)
    return hasil

def cari_connecting(asal, tujuan):
    """
    Cari pasangan rute dengan 1 kota transit.
    Contoh: Surabaya -> Yogyakarta via Malang
    Return: list of (idx_kaki1, idx_kaki2, kota_transit)
    """
    hasil = []
    for transit in kota_simpul:
        if transit == asal or transit == tujuan:
            continue
        kaki1 = cari_rute_langsung(asal, transit)
        kaki2 = cari_rute_langsung(transit, tujuan)
        if len(kaki1) > 0 and len(kaki2) > 0:
            for a in kaki1:
                for b in kaki2:
                    hasil.append((a, b, transit))
    return hasil

def tampilkan_connecting(pasangan):
    """Tampilkan opsi rute connecting yang ditemukan."""
    garis("-", 65)
    for no in range(len(pasangan)):
        a, b, transit = pasangan[no]
        total_harga = layanan[a][3] + layanan[b][3]
        mnt1 = (jarak.get(layanan[a][2], 0) * 60) // layanan[a][6]
        mnt2 = (jarak.get(layanan[b][2], 0) * 60) // layanan[b][6]
        print(str(no + 1) + ". VIA " + transit +
              " | Total estimasi: " + str((mnt1 + mnt2) // 60) + " jam++" +
              " | Harga mulai Rp " + uang(total_harga))
        print("   Kaki 1:", layanan[a][0], layanan[a][2],
              "| Rp", uang(layanan[a][3]), "| Jadwal:", layanan[a][5])
        print("   Kaki 2:", layanan[b][0], layanan[b][2],
              "| Rp", uang(layanan[b][3]), "| Jadwal:", layanan[b][5])
    garis("-", 65)


# ================================================================
#  BAGIAN 4 - WAITLIST & NOTIFIKASI
# ================================================================

def daftar_waitlist(akun_user, idx, jadwal, kelas_str, jumlah):
    """Daftarkan user ke waitlist jika kuota habis."""
    # Cek apakah sudah ada di waitlist layanan ini
    for w in waitlist:
        if w["username"] == akun_user["username"] and w["idx"] == idx:
            print("  Kamu sudah ada di waitlist layanan ini.")
            return
    waitlist.append({
        "username": akun_user["username"],
        "idx": idx,
        "jadwal": jadwal,
        "kelas": kelas_str,
        "jumlah": jumlah
    })
    tambah_notif(akun_user["username"],
                 "Kamu masuk waitlist " + layanan[idx][0] + " " + layanan[idx][2])
    print("  Berhasil masuk waitlist!")

def proses_waitlist(idx):
    """
    Dipanggil setelah ada pembatalan tiket.
    Kirim notifikasi ke user yang ada di waitlist layanan ini.
    """
    for w in waitlist:
        if w["idx"] == idx and kuota[idx] >= w["jumlah"]:
            tambah_notif(w["username"],
                         "[WAITLIST] Kursi tersedia! " +
                         layanan[idx][0] + " " + layanan[idx][2] +
                         " - Segera pesan sebelum habis.")

def lihat_notifikasi(akun_user):
    """Tampilkan semua notifikasi user."""
    daftar = notifikasi.get(akun_user["username"], [])
    if len(daftar) == 0:
        print("  Tidak ada notifikasi.")
        return
    garis("-", 50)
    print("  NOTIFIKASI")
    garis("-", 50)
    for i in range(len(daftar)):
        print("  " + str(i + 1) + ".", daftar[i])
    garis("-", 50)
    if input_ya_tidak("  Hapus semua notifikasi? (y/n): ") == "y":
        notifikasi[akun_user["username"]] = []
        print("  Notifikasi dihapus.")


# ================================================================
#  BAGIAN 5 - AKUN (registrasi, login, ganti password)
# ================================================================

def registrasi():
    """Daftarkan akun baru sebagai user atau admin."""
    garis()
    print("  REGISTRASI AKUN BARU")
    garis()
    print("  (Ketik 0 pada username untuk batal)")

    # Validasi username
    username = input_teks("  Username: ")
    if username == "0":
        print("  Registrasi dibatalkan.")
        return
    # Cek huruf dan angka saja (tidak ada spasi)
    for huruf in username:
        if huruf == " ":
            print("  Username tidak boleh mengandung spasi!")
            return
    # Cek apakah username sudah dipakai
    for a in akun:
        if a["username"].lower() == username.lower():
            print("  Username sudah dipakai!")
            return

    # Validasi password
    password = input("  Password (min 4 karakter, 0=batal): ").strip()
    if password == "0":
        print("  Registrasi dibatalkan.")
        return
    if len(password) < 4:
        print("  Password terlalu pendek! Minimal 4 karakter.")
        return
    if password == "":
        print("  Password tidak boleh kosong!")
        return

    # Tentukan role (user atau admin)
    kode_a = input("  Kode admin (kosongkan jika user biasa): ").strip()
    if kode_a == KODE_ADMIN:
        role = "admin"
    else:
        role = "user"

    # Simpan akun baru
    akun.append({
        "username": username,
        "password": password,
        "role": role,
        "saldo": 0,
        "poin": 0,
        "member": "Reguler",
        "banned": False,
        "total_transaksi": 0,
        "jumlah_beli": 0,
    })
    print("  Registrasi berhasil sebagai", role + "!")
    catat_log(username, "REGISTRASI", role)

def login():
    """Login ke akun yang sudah terdaftar."""
    garis()
    print("  LOGIN")
    garis()
    print("  (Ketik 0 pada username untuk batal)")

    username = input("  Username: ").strip()
    if username == "0" or username == "":
        print("  Kembali ke menu utama.")
        return None

    password = input("  Password: ").strip()
    if password == "":
        print("  Password tidak boleh kosong!")
        return None

    # Cari akun yang cocok
    for a in akun:
        if a["username"].lower() == username.lower() and a["password"] == password:
            if a["banned"]:
                print("  Akun kamu diblokir. Hubungi admin.")
                return None
            jml_notif = len(notifikasi.get(a["username"], []))
            print("  Login berhasil! Selamat datang,", a["username"])
            if jml_notif > 0:
                print("  [!]", jml_notif, "notifikasi belum dibaca.")
            print("  Member:", a["member"],
                  "| Poin:", a["poin"],
                  "| Saldo: Rp", uang(a["saldo"]))
            catat_log(username, "LOGIN")
            return a

    print("  Username atau password salah!")
    return None

def ganti_password(akun_user):
    """Ganti password akun user."""
    garis()
    print("  GANTI PASSWORD")
    garis()

    lama = input("  Password lama (0=batal): ").strip()
    if lama == "0":
        print("  Dibatalkan.")
        return
    if lama == "":
        print("  Password tidak boleh kosong!")
        return
    if lama != akun_user["password"]:
        print("  Password lama salah!")
        return

    baru = input("  Password baru (min 4 karakter): ").strip()
    if len(baru) < 4:
        print("  Terlalu pendek! Minimal 4 karakter.")
        return
    if baru == "":
        print("  Password tidak boleh kosong!")
        return

    akun_user["password"] = baru
    print("  Password berhasil diubah.")
    catat_log(akun_user["username"], "GANTI_PASSWORD")


# ================================================================
#  BAGIAN 6 - SALDO, POIN, DAN LEVEL MEMBER
# ================================================================

def cek_tier(akun_user):
    """Periksa apakah level member user perlu naik."""
    tier_baru = TIER[0]
    for t in TIER:
        if akun_user["poin"] >= t[1]:
            tier_baru = t
    if akun_user["member"] != tier_baru[0]:
        akun_user["member"] = tier_baru[0]
        print("  Selamat! Level member kamu naik ke", tier_baru[0],
              "(diskon " + str(tier_baru[2]) + "%)")
        tambah_notif(akun_user["username"],
                     "Level member naik ke " + tier_baru[0] + "!")

def diskon_member(akun_user):
    """Kembalikan persentase diskon sesuai level member."""
    for t in TIER:
        if akun_user["member"] == t[0]:
            return t[2]
    return 0

def top_up(akun_user):
    """Top-up saldo akun user."""
    garis()
    print("  TOP-UP SALDO")
    garis()
    print("  Saldo saat ini: Rp", uang(akun_user["saldo"]))

    nominal_rb = input_angka_atau_batal(
        "  Nominal top-up (dalam ribuan, 0=Batal, 1-500): ", 500)
    if nominal_rb == -1:
        print("  Dibatalkan.")
        return

    nominal = nominal_rb * 1000
    akun_user["saldo"] = akun_user["saldo"] + nominal

    # Tiap Rp 20.000 dapat 1 poin
    poin = nominal // 20000
    akun_user["poin"] = akun_user["poin"] + poin

    print("  Top-up Rp", uang(nominal), "berhasil!")
    print("  Saldo sekarang: Rp", uang(akun_user["saldo"]),
          "| +" + str(poin), "poin")

    cek_tier(akun_user)
    catat_log(akun_user["username"], "TOP_UP", "Rp " + uang(nominal))

def tukar_poin(akun_user):
    """Tukar poin menjadi saldo."""
    opsi = ((50, 10000), (100, 25000), (200, 50000), (500, 150000))

    garis()
    print("  TUKAR POIN")
    garis()
    print("  Poin kamu:", akun_user["poin"])
    print("  0. Batal")
    for i in range(len(opsi)):
        print("  " + str(i + 1) + ".",
              opsi[i][0], "poin -> Rp", uang(opsi[i][1]))

    pilih = input_angka_atau_batal("  Pilih: ", len(opsi))
    if pilih == -1:
        print("  Dibatalkan.")
        return

    if akun_user["poin"] < opsi[pilih - 1][0]:
        print("  Poin tidak cukup! Poin kamu:", akun_user["poin"])
        return

    akun_user["poin"]  = akun_user["poin"]  - opsi[pilih - 1][0]
    akun_user["saldo"] = akun_user["saldo"] + opsi[pilih - 1][1]
    print("  Berhasil! Saldo sekarang: Rp", uang(akun_user["saldo"]))
    catat_log(akun_user["username"], "TUKAR_POIN",
              str(opsi[pilih - 1][0]) + " poin")

def profil_saya(akun_user):
    """Tampilkan profil dan progress tier user."""
    garis()
    print("  PROFIL")
    garis()
    print("  Username        :", akun_user["username"])
    print("  Level Member    :", akun_user["member"])
    print("  Poin            :", akun_user["poin"])
    print("  Saldo           : Rp", uang(akun_user["saldo"]))
    print("  Total Transaksi : Rp", uang(akun_user["total_transaksi"]))
    print("  Jumlah Beli     :", akun_user["jumlah_beli"], "kali")

    # Tampilkan progress ke tier berikutnya
    tier_saat = 0
    for t in range(len(TIER)):
        if TIER[t][0] == akun_user["member"]:
            tier_saat = t

    if tier_saat < len(TIER) - 1:
        poin_butuh = TIER[tier_saat + 1][1] - akun_user["poin"]
        if poin_butuh < 0:
            poin_butuh = 0
        print("  Progress ke " + TIER[tier_saat + 1][0] + ": butuh",
              str(poin_butuh), "poin lagi")
        print("  " + bar(akun_user["poin"], TIER[tier_saat + 1][1]))
    else:
        print("  Sudah tier tertinggi (Platinum)!")


# ================================================================
#  BAGIAN 7 - PEMESANAN TIKET
# ================================================================

def peta_kursi(idx):
    """Tampilkan peta kursi visual (layout 4 kolom seperti bus)."""
    kapasitas = layanan[idx][4]
    print("  --- PETA KURSI ---")
    print("  [XX] = Terisi   [no] = Tersedia")

    baris_no = 1
    while baris_no <= kapasitas:
        baris_str = "  "
        for kursi_no in range(baris_no, min(baris_no + 4, kapasitas + 1)):
            if kursi_no in kursi_terisi[idx]:
                baris_str = baris_str + "[XX]"
            else:
                label = str(kursi_no)
                if kursi_no < 10:
                    label = " " + label
                baris_str = baris_str + "[" + label + "]"
            # Tambah lorong tengah setelah kursi ke-2
            if kursi_no == baris_no + 1:
                baris_str = baris_str + "  "
        print(baris_str)
        baris_no = baris_no + 4

def pilih_kursi(idx, jumlah):
    """
    Minta user pilih nomor kursi satu per satu.
    Mengembalikan list nomor kursi, atau [] jika dibatalkan.
    """
    kapasitas = layanan[idx][4]
    peta_kursi(idx)
    kursi_dipilih = []

    while len(kursi_dipilih) < jumlah:
        no = input_angka_atau_batal(
            "  Pilih kursi ke-" + str(len(kursi_dipilih) + 1) +
            " (0=Batal, 1-" + str(kapasitas) + "): ",
            kapasitas)
        if no == -1:
            print("  Pemilihan kursi dibatalkan.")
            return []
        if no in kursi_terisi[idx] or no in kursi_dipilih:
            print("  Kursi", no, "sudah terisi! Pilih yang lain.")
        else:
            kursi_dipilih.append(no)
            print("  Kursi", no, "berhasil dipilih.")

    return kursi_dipilih

def pilih_asuransi():
    """
    Tampilkan opsi asuransi dan minta user pilih nomor.
    Mengembalikan (nomor_paket, premi).
    """
    garis("-", 60)
    print("  PILIH PAKET ASURANSI")
    garis("-", 60)
    for nomor in paket_asuransi:
        p = paket_asuransi[nomor]
        if nomor == 1:
            print("  " + str(nomor) + ". " + p[0])
        else:
            print("  " + str(nomor) + ". " + p[0] +
                  " | Premi: Rp " + uang(p[1]) +
                  " | Kecelakaan s.d. Rp " + uang(p[2]) +
                  " | Barang s.d. Rp " + uang(p[3]))

    pilih = input_angka("  Pilih nomor asuransi: ", len(paket_asuransi))
    p = paket_asuransi[pilih]

    if pilih == 1:
        print("  Tanpa asuransi.")
    else:
        print("  Paket", p[0], "dipilih. Premi: Rp", uang(p[1]))

    return pilih, p[1]

def cetak_ringkasan(akun_user, idx, jadwal, kelas_str, jumlah,
                    total_bersih, potongan, premi_as, nomor_as):
    """Tampilkan ringkasan pesanan sebelum konfirmasi."""
    grand = total_bersih + premi_as
    nama_as = paket_asuransi[nomor_as][0]

    garis("+", 50)
    print("  RINGKASAN PESANAN")
    garis("+", 50)
    print("  Layanan    :", layanan[idx][1], layanan[idx][0])
    print("  Rute       :", layanan[idx][2])
    print("  Jadwal     :", jadwal, "-> tiba est.", hitung_jam_tiba(idx, jadwal))
    print("  Kelas      :", kelas_str)
    print("  Jumlah     :", jumlah, "tiket")
    print("  Potongan   : Rp", uang(potongan))
    print("  Asuransi   :", nama_as, "| Premi: Rp", uang(premi_as))
    print("  TOTAL      : Rp", uang(grand))
    print("  Saldo kamu : Rp", uang(akun_user["saldo"]))
    print("  Sisa saldo : Rp", uang(akun_user["saldo"] - grand))
    garis("+", 50)

def proses_pesan(akun_user, idx):
    """
    Proses pemesanan tiket untuk satu layanan.
    Dipanggil dari menu pesan tiket maupun connecting route.
    """
    # Cek kuota
    if kuota[idx] == 0:
        print("  Kuota habis untuk layanan ini!")
        if input_ya_tidak("  Mau masuk waitlist? (y/n): ") == "y":
            # Pilih jadwal untuk waitlist
            print("  Jadwal tersedia:")
            for i in range(len(layanan[idx][5])):
                print("  " + str(i + 1) + ".", layanan[idx][5][i])
            print("  0. Batal")
            pilih_j = input_angka_atau_batal("  Pilih jadwal: ",
                                             len(layanan[idx][5]))
            if pilih_j == -1:
                return
            jadwal = layanan[idx][5][pilih_j - 1]

            # Pilih kelas untuk waitlist
            print("  Kelas:")
            for k in kelas_tiket:
                print("  " + str(k) + ".", kelas_tiket[k][0])
            print("  0. Batal")
            pilih_k = input_angka_atau_batal("  Pilih kelas: ", len(kelas_tiket))
            if pilih_k == -1:
                return

            # Pilih jumlah tiket
            pilih_jml = input_angka_atau_batal(
                "  Jumlah tiket (0=Batal, 1-" + str(layanan[idx][4]) + "): ",
                layanan[idx][4])
            if pilih_jml == -1:
                return

            daftar_waitlist(akun_user, idx,
                            jadwal, kelas_tiket[pilih_k][0], pilih_jml)
        return

    kode_l = layanan[idx][0]
    tujuan = layanan[idx][2]

    # Cek apakah user sudah punya tiket aktif di rute ini
    for p in riwayat:
        if (p["kode_layanan"] == kode_l and
                p["pembeli"] == akun_user["username"] and
                p["status"] == "Aktif"):
            print("  Kamu sudah punya tiket aktif di layanan ini!")
            return

    # ---- Pilih jadwal ----
    print("  Jadwal tersedia:")
    for i in range(len(layanan[idx][5])):
        print("  " + str(i + 1) + ".", layanan[idx][5][i])
    print("  0. Kembali")
    pilih_j = input_angka_atau_batal("  Pilih jadwal: ", len(layanan[idx][5]))
    if pilih_j == -1:
        return
    jadwal = layanan[idx][5][pilih_j - 1]

    # ---- Pilih kelas ----
    print("  Kelas:")
    for k in kelas_tiket:
        print("  " + str(k) + ".", kelas_tiket[k][0],
              "(+Rp " + uang(kelas_tiket[k][1]) + ")")
    print("  0. Kembali")
    pilih_k = input_angka_atau_batal("  Pilih kelas: ", len(kelas_tiket))
    if pilih_k == -1:
        return
    kelas_str = kelas_tiket[pilih_k][0]
    harga_sat = layanan[idx][3] + kelas_tiket[pilih_k][1]

    # ---- Pilih jumlah tiket ----
    pilih_jml = input_angka_atau_batal(
        "  Jumlah tiket (0=Batal, 1-" + str(kuota[idx]) + "): ",
        kuota[idx])
    if pilih_jml == -1:
        return
    jumlah = pilih_jml
    total  = harga_sat * jumlah

    # ---- Promo ----
    potongan = 0
    if input_ya_tidak("  Punya kode promo? (y/n): ") == "y":
        kode_p = input("  Kode promo (0=lewati): ").strip().upper()
        if kode_p != "0" and kode_p != "":
            if kode_p in promo:
                pr = promo[kode_p]
                if not pr[3]:
                    print("  Promo tidak aktif.")
                elif pr[4] >= pr[5]:
                    print("  Kuota promo sudah habis.")
                elif total < pr[1]:
                    print("  Minimal belanja Rp", uang(pr[1]),
                          "untuk promo ini.")
                else:
                    potongan = pr[0]
                    # Update jumlah pemakaian promo
                    promo[kode_p] = (pr[0], pr[1], pr[2],
                                     pr[3], pr[4] + 1, pr[5])
                    print("  Promo berhasil! Potongan Rp", uang(potongan))
            else:
                print("  Kode promo tidak valid.")

    # ---- Diskon level member ----
    persen   = diskon_member(akun_user)
    pot_tier = (total * persen) // 100
    if persen > 0:
        print("  Diskon member", akun_user["member"] + ":",
              str(persen) + "% (Rp " + uang(pot_tier) + ")")
    potongan = potongan + pot_tier

    # Pastikan total tidak negatif
    if total > potongan:
        total = total - potongan
    else:
        total = 0

    # ---- Pilih asuransi (by nomor) ----
    nomor_as, premi_as = pilih_asuransi()

    # ---- Tampilkan ringkasan ----
    cetak_ringkasan(akun_user, idx, jadwal, kelas_str, jumlah,
                    total, potongan, premi_as, nomor_as)

    grand_total = total + premi_as

    # Cek saldo
    if akun_user["saldo"] < grand_total:
        print("  Saldo tidak cukup!")
        print("  Butuh Rp", uang(grand_total),
              "| Punya Rp", uang(akun_user["saldo"]))
        return

    # ---- Pilih kursi ----
    kursi = pilih_kursi(idx, jumlah)
    if len(kursi) == 0:
        print("  Pemesanan dibatalkan.")
        return

    # ---- Konfirmasi ----
    if input_ya_tidak("  Konfirmasi pemesanan? (y/n): ") != "y":
        print("  Pemesanan dibatalkan.")
        return

    # ---- Simpan pesanan ----
    kode = buat_kode_booking(layanan[idx][1])

    akun_user["saldo"]           = akun_user["saldo"] - grand_total
    kuota[idx]                   = kuota[idx] - jumlah
    kursi_terisi[idx]            = kursi_terisi[idx] + kursi
    poin_baru                    = grand_total // 25000
    akun_user["poin"]            = akun_user["poin"] + poin_baru
    akun_user["total_transaksi"] = akun_user["total_transaksi"] + grand_total
    akun_user["jumlah_beli"]     = akun_user["jumlah_beli"] + 1

    pesanan = {
        "kode"          : kode,
        "pembeli"       : akun_user["username"],
        "idx"           : idx,
        "kode_layanan"  : kode_l,
        "jenis"         : layanan[idx][1],
        "tujuan"        : tujuan,
        "jadwal"        : jadwal,
        "jam_tiba"      : hitung_jam_tiba(idx, jadwal),
        "kelas"         : kelas_str,
        "kursi"         : kursi,
        "jumlah"        : jumlah,
        "total"         : grand_total,
        "potongan"      : potongan,
        "nomor_asuransi": nomor_as,
        "premi"         : premi_as,
        "status"        : "Aktif",
        "rating"        : 0,
        "sudah_berangkat": False,
    }
    riwayat.append(pesanan)
    cek_tier(akun_user)

    garis("=", 45)
    print("  PEMESANAN BERHASIL!")
    print("  Kode Booking :", kode)
    print("  Kursi        :", kursi)
    print("  Poin dapat   :", poin_baru)
    garis("=", 45)
    catat_log(akun_user["username"], "PESAN", kode + " " + tujuan)

def menu_pesan_tiket(akun_user):
    """Sub-menu pemilihan cara melihat layanan sebelum memesan."""
    while True:
        garis()
        print("  PESAN TIKET")
        garis()
        print("  1. Lihat semua layanan")
        print("  2. Cari berdasarkan kata kunci")
        print("  3. Urut dari yang termurah")
        print("  4. Urut dari rating terbaik")
        print("  5. Rute connecting (via kota transit)")
        print("  0. Kembali ke menu utama")

        pilih = input_angka_atau_batal("  Pilih: ", 5)
        if pilih == -1:
            return

        # --- Rute connecting ---
        if pilih == 5:
            print("  Kota tersedia:", kota_simpul)
            asal = input("  Kota asal (0=Batal): ").strip().title()
            if asal == "0" or asal == "":
                continue
            tujuan = input("  Kota tujuan (0=Batal): ").strip().title()
            if tujuan == "0" or tujuan == "":
                continue
            pasangan = cari_connecting(asal, tujuan)
            if len(pasangan) == 0:
                print("  Tidak ada rute connecting tersedia.")
                continue
            tampilkan_connecting(pasangan)
            print("  0. Kembali")
            pilih_c = input_angka_atau_batal("  Pilih opsi rute: ", len(pasangan))
            if pilih_c == -1:
                continue
            idx_a, idx_b, transit = pasangan[pilih_c - 1]
            print("  === Kaki 1:", layanan[idx_a][2], "===")
            proses_pesan(akun_user, idx_a)
            print("  === Kaki 2:", layanan[idx_b][2], "===")
            proses_pesan(akun_user, idx_b)
            return

        # --- Tentukan daftar layanan yang ditampilkan ---
        if pilih == 2:
            kata = input("  Kata kunci (0=Batal): ").lower().strip()
            if kata == "0" or kata == "":
                continue
            hasil = []
            for i in range(len(layanan)):
                if kata in layanan[i][2].lower() or kata in layanan[i][1].lower():
                    hasil.append(i)
            if len(hasil) == 0:
                print("  Tidak ada layanan yang cocok.")
                continue
            tampilkan_layanan(hasil)
            print("  0. Kembali")
            pilih_l = input_angka_atau_batal("  Pilih nomor layanan: ", len(hasil))
            if pilih_l == -1:
                continue
            idx = hasil[pilih_l - 1]

        elif pilih == 3:
            tampilkan_layanan(urut_harga=True)
            print("  0. Kembali")
            pilih_l = input_angka_atau_batal(
                "  Pilih nomor layanan: ", len(layanan))
            if pilih_l == -1:
                continue
            idx = pilih_l - 1

        elif pilih == 4:
            tampilkan_layanan(urut_rating=True)
            print("  0. Kembali")
            pilih_l = input_angka_atau_batal(
                "  Pilih nomor layanan: ", len(layanan))
            if pilih_l == -1:
                continue
            idx = pilih_l - 1

        else:
            tampilkan_layanan()
            print("  0. Kembali")
            pilih_l = input_angka_atau_batal(
                "  Pilih nomor layanan: ", len(layanan))
            if pilih_l == -1:
                continue
            idx = pilih_l - 1

        proses_pesan(akun_user, idx)
        return


# ================================================================
#  BAGIAN 8 - MANAJEMEN TIKET (batal, ubah jadwal, upgrade, cetak)
# ================================================================

def batalkan_tiket(akun_user):
    """Batalkan tiket aktif, refund 80% ke saldo."""
    garis()
    print("  BATALKAN TIKET")
    garis()

    kode = input("  Kode booking (0=Batal): ").strip().upper()
    if kode == "0" or kode == "":
        print("  Dibatalkan.")
        return

    for p in riwayat:
        if p["kode"] == kode and p["pembeli"] == akun_user["username"]:
            if p["status"] == "Dibatalkan":
                print("  Tiket ini sudah dibatalkan sebelumnya.")
                return
            if p["sudah_berangkat"]:
                print("  Tidak bisa batalkan tiket yang sudah berangkat.")
                return

            print("  Total dibayar : Rp", uang(p["total"]))
            print("  Refund (80%)  : Rp", uang(p["total"] * 80 // 100))

            if input_ya_tidak("  Yakin batalkan? (y/n): ") == "y":
                # Kembalikan kursi dan kuota
                p["status"] = "Dibatalkan"
                kuota[p["idx"]] = kuota[p["idx"]] + p["jumlah"]
                for k in p["kursi"]:
                    kursi_terisi[p["idx"]].remove(k)

                # Refund 80% ke saldo
                refund = p["total"] * 80 // 100
                akun_user["saldo"] = akun_user["saldo"] + refund
                print("  Tiket dibatalkan. Refund Rp", uang(refund), "masuk saldo.")

                # Notif user di waitlist
                proses_waitlist(p["idx"])
                catat_log(akun_user["username"], "BATAL", kode)
            else:
                print("  Pembatalan dibatalkan.")
            return

    print("  Kode booking tidak ditemukan!")

def ubah_jadwal(akun_user):
    """Ubah jadwal keberangkatan tiket aktif (biaya Rp 10.000)."""
    garis()
    print("  UBAH JADWAL")
    garis()

    kode = input("  Kode booking (0=Batal): ").strip().upper()
    if kode == "0" or kode == "":
        print("  Dibatalkan.")
        return

    for p in riwayat:
        if (p["kode"] == kode and
                p["pembeli"] == akun_user["username"] and
                p["status"] == "Aktif"):

            if p["sudah_berangkat"]:
                print("  Sudah berangkat, tidak bisa ubah jadwal.")
                return

            idx = p["idx"]
            print("  Jadwal sekarang:", p["jadwal"])
            print("  Jadwal tersedia:")
            for i in range(len(layanan[idx][5])):
                print("  " + str(i + 1) + ".", layanan[idx][5][i])
            print("  0. Batal")

            pilih_j = input_angka_atau_batal("  Jadwal baru: ",
                                             len(layanan[idx][5]))
            if pilih_j == -1:
                print("  Dibatalkan.")
                return

            biaya = 10000
            print("  Biaya ubah jadwal: Rp", uang(biaya))

            if akun_user["saldo"] < biaya:
                print("  Saldo tidak cukup! Butuh Rp", uang(biaya))
                return

            if input_ya_tidak("  Konfirmasi? (y/n): ") == "y":
                akun_user["saldo"] = akun_user["saldo"] - biaya
                p["jadwal"]   = layanan[idx][5][pilih_j - 1]
                p["jam_tiba"] = hitung_jam_tiba(idx, p["jadwal"])
                print("  Jadwal diubah ke", p["jadwal"],
                      "| Tiba est.", p["jam_tiba"])
                catat_log(akun_user["username"], "UBAH_JADWAL",
                          kode + " -> " + p["jadwal"])
            return

    print("  Kode booking tidak ditemukan atau tiket tidak aktif!")

def upgrade_kelas(akun_user):
    """Upgrade kelas tiket (Ekonomi -> Bisnis -> Eksekutif)."""
    garis()
    print("  UPGRADE KELAS")
    garis()

    kode = input("  Kode booking (0=Batal): ").strip().upper()
    if kode == "0" or kode == "":
        print("  Dibatalkan.")
        return

    for p in riwayat:
        if (p["kode"] == kode and
                p["pembeli"] == akun_user["username"] and
                p["status"] == "Aktif"):

            if p["sudah_berangkat"]:
                print("  Sudah berangkat, tidak bisa upgrade.")
                return

            kelas_urutan = ["Ekonomi", "Bisnis", "Eksekutif"]
            idx_kls = 0
            for ki in range(len(kelas_urutan)):
                if kelas_urutan[ki] == p["kelas"]:
                    idx_kls = ki

            if idx_kls == len(kelas_urutan) - 1:
                print("  Sudah kelas tertinggi (Eksekutif)!")
                return

            kls_baru   = kelas_urutan[idx_kls + 1]
            harga_lama = 0
            harga_baru = 0
            for k in kelas_tiket:
                if kelas_tiket[k][0] == p["kelas"]:
                    harga_lama = kelas_tiket[k][1]
                if kelas_tiket[k][0] == kls_baru:
                    harga_baru = kelas_tiket[k][1]

            biaya = (harga_baru - harga_lama) * p["jumlah"]
            print("  Upgrade ke", kls_baru,
                  "| Biaya tambahan: Rp", uang(biaya))

            if akun_user["saldo"] < biaya:
                print("  Saldo tidak cukup!")
                return

            if input_ya_tidak("  Lanjut upgrade? (y/n): ") == "y":
                akun_user["saldo"] = akun_user["saldo"] - biaya
                p["kelas"] = kls_baru
                p["total"] = p["total"] + biaya
                print("  Upgrade berhasil ke kelas", kls_baru)
                catat_log(akun_user["username"], "UPGRADE",
                          kode + " -> " + kls_baru)
            return

    print("  Kode booking tidak ditemukan!")

def cetak_tiket(akun_user):
    """Cetak e-tiket pemesanan."""
    garis()
    print("  CETAK E-TIKET")
    garis()

    kode = input("  Kode booking (0=Batal): ").strip().upper()
    if kode == "0" or kode == "":
        print("  Dibatalkan.")
        return

    for p in riwayat:
        if p["kode"] == kode and p["pembeli"] == akun_user["username"]:
            nama_as = paket_asuransi[p["nomor_asuransi"]][0]

            garis("=", 50)
            print("  " + "E-TIKET TRANSPORTASI TERPADU".center(46))
            garis("=", 50)
            print("  Kode Booking :", p["kode"])
            print("  Penumpang    :", p["pembeli"])
            print("  Layanan      :", p["jenis"], p["kode_layanan"])
            print("  Rute         :", p["tujuan"])
            print("  Berangkat    :", p["jadwal"])
            print("  Tiba (est.)  :", p["jam_tiba"])
            print("  Kelas        :", p["kelas"])
            print("  Kursi        :", p["kursi"])
            print("  Jumlah       :", p["jumlah"], "tiket")
            print("  Potongan     : Rp", uang(p["potongan"]))
            print("  Asuransi     :", nama_as, "| Premi: Rp", uang(p["premi"]))
            print("  TOTAL BAYAR  : Rp", uang(p["total"]))
            print("  Status       :", p["status"])
            garis("=", 50)
            return

    print("  Kode booking tidak ditemukan!")

def tandai_berangkat(akun_user):
    """Tandai tiket sudah boarding (syarat untuk beri rating)."""
    garis()
    print("  TANDAI SUDAH BERANGKAT")
    garis()

    kode = input("  Kode booking (0=Batal): ").strip().upper()
    if kode == "0" or kode == "":
        print("  Dibatalkan.")
        return

    for p in riwayat:
        if (p["kode"] == kode and
                p["pembeli"] == akun_user["username"] and
                p["status"] == "Aktif"):
            if p["sudah_berangkat"]:
                print("  Tiket ini sudah ditandai berangkat.")
                return
            p["sudah_berangkat"] = True
            print("  Selamat menikmati perjalanan ke", p["tujuan"] + "!")
            tambah_notif(akun_user["username"],
                         "Jangan lupa beri rating untuk perjalanan " +
                         p["tujuan"] + "!")
            return

    print("  Kode booking tidak ditemukan!")

def beri_rating(akun_user):
    """Beri rating dan komentar untuk perjalanan yang sudah selesai."""
    garis()
    print("  BERI RATING & ULASAN")
    garis()

    kode = input("  Kode booking (0=Batal): ").strip().upper()
    if kode == "0" or kode == "":
        print("  Dibatalkan.")
        return

    for p in riwayat:
        if p["kode"] == kode and p["pembeli"] == akun_user["username"]:
            if not p["sudah_berangkat"]:
                print("  Tandai keberangkatan dulu (menu 7) sebelum beri rating.")
                return
            if p["rating"] > 0:
                print("  Kamu sudah memberi rating untuk tiket ini.")
                return

            print("  0. Batal")
            nilai = input_angka_atau_batal("  Rating (0=Batal, 1-5): ", 5)
            if nilai == -1:
                print("  Dibatalkan.")
                return

            komentar = input("  Komentar (boleh kosong): ").strip()

            # Simpan rating ke tiket
            p["rating"] = nilai

            # Update rating crew
            for c in crew:
                if c[1] == p["kode_layanan"]:
                    c[2] = c[2] + nilai
                    c[3] = c[3] + 1

            # Simpan ulasan
            ulasan.append({
                "kode"    : kode,
                "user"    : akun_user["username"],
                "layanan" : p["kode_layanan"],
                "rating"  : nilai,
                "komentar": komentar,
            })

            # Bonus poin untuk memberikan ulasan
            akun_user["poin"] = akun_user["poin"] + 5
            print("  Rating tersimpan! +5 poin bonus. Terima kasih!")
            catat_log(akun_user["username"], "RATING",
                      kode + " bintang=" + str(nilai))
            return

    print("  Kode booking tidak ditemukan!")

def lihat_riwayat(akun_user):
    """Tampilkan semua riwayat pemesanan milik user."""
    garis()
    print("  RIWAYAT PEMESANAN")
    garis()
    ada = False
    for p in riwayat:
        if p["pembeli"] == akun_user["username"]:
            ada = True
            tanda = "[OK]" if p["status"] == "Aktif" else "[XX]"
            print("  " + tanda, p["kode"], "|",
                  p["jenis"], "|", p["tujuan"], "|",
                  p["jadwal"], "->", p["jam_tiba"], "|",
                  p["kelas"], "|", p["jumlah"], "tiket |",
                  "Rp", uang(p["total"]))
            if p["nomor_asuransi"] > 1:
                print("    Asuransi:", paket_asuransi[p["nomor_asuransi"]][0])
            print("    Kursi:", p["kursi"],
                  "| Status:", p["status"],
                  "| Rating:", bintang(p["rating"]))
    if not ada:
        print("  Belum ada riwayat pemesanan.")

def lihat_waitlist_saya(akun_user):
    """Tampilkan antrian waitlist milik user."""
    garis()
    print("  WAITLIST SAYA")
    garis()
    ada = False
    for w in waitlist:
        if w["username"] == akun_user["username"]:
            ada = True
            print("  ", layanan[w["idx"]][0], layanan[w["idx"]][2],
                  "| Jadwal:", w["jadwal"],
                  "| Kelas:", w["kelas"],
                  "| Kuota sekarang:", kuota[w["idx"]])
    if not ada:
        print("  Kamu tidak ada di waitlist manapun.")


# ================================================================
#  BAGIAN 9 - MENU USER
# ================================================================

def menu_user(akun_user):
    """Menu utama untuk penumpang/user."""
    while True:
        garis("=", 40)
        print("  MENU PENUMPANG")
        print("  " + akun_user["username"] + " | " + akun_user["member"])
        print("  Poin:", akun_user["poin"],
              "| Saldo: Rp", uang(akun_user["saldo"]))
        garis("=", 40)
        print("   1. Pesan Tiket")
        print("   2. Riwayat Saya")
        print("   3. Batalkan Tiket (refund 80%)")
        print("   4. Ubah Jadwal (Rp 10.000)")
        print("   5. Upgrade Kelas")
        print("   6. Cetak E-Tiket")
        print("   7. Tandai Sudah Berangkat")
        print("   8. Beri Rating & Ulasan")
        print("   9. Waitlist Saya")
        print("  10. Notifikasi")
        print("  11. Top-Up Saldo")
        print("  12. Tukar Poin ke Saldo")
        print("  13. Profil & Progress Tier")
        print("  14. Ganti Password")
        print("  15. Logout")
        garis("-", 40)

        menu = input_angka("  Pilih menu: ", 15)

        if   menu ==  1: menu_pesan_tiket(akun_user)
        elif menu ==  2: lihat_riwayat(akun_user)
        elif menu ==  3: batalkan_tiket(akun_user)
        elif menu ==  4: ubah_jadwal(akun_user)
        elif menu ==  5: upgrade_kelas(akun_user)
        elif menu ==  6: cetak_tiket(akun_user)
        elif menu ==  7: tandai_berangkat(akun_user)
        elif menu ==  8: beri_rating(akun_user)
        elif menu ==  9: lihat_waitlist_saya(akun_user)
        elif menu == 10: lihat_notifikasi(akun_user)
        elif menu == 11: top_up(akun_user)
        elif menu == 12: tukar_poin(akun_user)
        elif menu == 13: profil_saya(akun_user)
        elif menu == 14: ganti_password(akun_user)
        else:
            print("  Logout berhasil. Sampai jumpa,",
                  akun_user["username"] + "!")
            catat_log(akun_user["username"], "LOGOUT")
            break


# ================================================================
#  BAGIAN 10 - FITUR ADMIN
# ================================================================

def laporan_pendapatan():
    """Laporan pendapatan per layanan dengan grafik bar ASCII."""
    garis()
    print("  LAPORAN PENDAPATAN")
    garis()

    # Cari nilai terbesar untuk skala bar
    maks = 1
    for i in range(len(layanan)):
        sub = 0
        for p in riwayat:
            if p["idx"] == i and p["status"] == "Aktif":
                sub = sub + p["total"]
        if sub > maks:
            maks = sub

    total_semua = 0
    for i in range(len(layanan)):
        subtotal = 0
        terjual  = 0
        for p in riwayat:
            if p["idx"] == i and p["status"] == "Aktif":
                subtotal = subtotal + p["total"]
                terjual  = terjual  + p["jumlah"]
        print("  " + layanan[i][0], layanan[i][2])
        print("    Rp", uang(subtotal).rjust(10),
              "| tiket:", str(terjual).rjust(3),
              "|", bar(subtotal, maks))
        total_semua = total_semua + subtotal

    garis("-")
    print("  TOTAL PENDAPATAN: Rp", uang(total_semua))

    # Hitung konversi (tiket aktif vs dibatalkan)
    batal = 0
    aktif = 0
    for p in riwayat:
        if p["status"] == "Dibatalkan":
            batal = batal + 1
        elif p["status"] == "Aktif":
            aktif = aktif + 1
    total_trx = aktif + batal
    if total_trx > 0:
        konversi = desimal1(aktif * 100 / total_trx)
    else:
        konversi = "0.0"
    print("  Aktif:", aktif,
          "| Dibatalkan:", batal,
          "| Konversi:", konversi + "%")

def statistik_layanan():
    """Statistik penjualan tiket dan okupansi per layanan."""
    garis()
    print("  STATISTIK LAYANAN")
    garis()

    maks_jual = 1
    for i in range(len(layanan)):
        t = 0
        for p in riwayat:
            if p["idx"] == i and p["status"] == "Aktif":
                t = t + p["jumlah"]
        if t > maks_jual:
            maks_jual = t

    terlaris_idx = 0
    terlaris_val = 0
    for i in range(len(layanan)):
        terjual = 0
        for p in riwayat:
            if p["idx"] == i and p["status"] == "Aktif":
                terjual = terjual + p["jumlah"]
        okupansi = (terjual * 100) // layanan[i][4]
        print("  " + layanan[i][0], layanan[i][2])
        print("    Terjual:", str(terjual).rjust(3),
              "| Okupansi:", str(okupansi).rjust(3), "%",
              "|", bar(terjual, maks_jual))
        if terjual > terlaris_val:
            terlaris_val = terjual
            terlaris_idx = i

    garis("-")
    print("  TERLARIS:", layanan[terlaris_idx][0], "-",
          layanan[terlaris_idx][2],
          "(" + str(terlaris_val), "tiket)")

def laporan_crew():
    """Laporan rating crew, diurutkan dari tertinggi."""
    garis()
    print("  RATING CREW")
    garis()

    # Buat salinan list crew untuk diurutkan (bubble sort)
    cs = []
    for c in crew:
        cs.append(c)

    for i in range(len(cs)):
        for j in range(len(cs) - i - 1):
            r1 = cs[j][2]     / cs[j][3]     if cs[j][3]     > 0 else 0.0
            r2 = cs[j+1][2]   / cs[j+1][3]   if cs[j+1][3]   > 0 else 0.0
            if r1 < r2:
                cs[j], cs[j+1] = cs[j+1], cs[j]

    for c in cs:
        rata   = c[2] / c[3] if c[3] > 0 else 0.0
        status = "AKTIF" if c[4] else "NONAKTIF"
        print("  " + c[1].ljust(7), "|",
              c[0].ljust(22), "|",
              bintang(round(rata)), desimal1(rata), "|",
              str(c[3]).rjust(3), "ulasan |", status)

def lihat_ulasan():
    """Lihat semua ulasan, bisa filter per layanan."""
    garis()
    print("  ULASAN PENUMPANG")
    garis()

    if len(ulasan) == 0:
        print("  Belum ada ulasan.")
        return

    print("  1. Semua ulasan")
    print("  2. Filter per layanan")
    print("  0. Kembali")
    pilih = input_angka_atau_batal("  Pilih: ", 2)
    if pilih == -1:
        return

    kode_filter = ""
    if pilih == 2:
        kode_filter = input("  Kode layanan (mis. BUS-01): ").strip().upper()
        if kode_filter == "":
            print("  Kode tidak boleh kosong!")
            return

    for u in ulasan:
        if kode_filter == "" or u["layanan"] == kode_filter:
            print("  " + u["kode"], "|", u["user"], "|",
                  u["layanan"], "|", bintang(u["rating"]))
            if u["komentar"] != "":
                print('    "' + u["komentar"] + '"')

def kelola_promo():
    """Kelola daftar promo (tambah, hapus, aktifkan/nonaktifkan)."""
    while True:
        garis()
        print("  KELOLA PROMO")
        garis()
        for k in promo:
            pr     = promo[k]
            status = "AKTIF" if pr[3] else "NONAKTIF"
            print("  " + k.ljust(10), pr[2].ljust(18),
                  "| -Rp", uang(pr[0]).rjust(7),
                  "| min Rp", uang(pr[1]),
                  "| pakai:", str(pr[4]) + "/" + str(pr[5]),
                  "|", status)
        garis("-")
        print("  1. Aktifkan / Nonaktifkan promo")
        print("  2. Tambah promo baru")
        print("  3. Hapus promo")
        print("  0. Kembali")

        pilih = input_angka_atau_batal("  Pilih: ", 3)
        if pilih == -1:
            return

        if pilih == 1:
            kode = input("  Kode promo (0=Batal): ").strip().upper()
            if kode == "0" or kode == "":
                continue
            if kode in promo:
                pr = promo[kode]
                promo[kode] = (pr[0], pr[1], pr[2], not pr[3], pr[4], pr[5])
                status_baru = "AKTIF" if promo[kode][3] else "NONAKTIF"
                print("  Promo", kode, "sekarang:", status_baru)
            else:
                print("  Promo tidak ditemukan!")

        elif pilih == 2:
            kode = input("  Kode promo baru (0=Batal): ").strip().upper()
            if kode == "0" or kode == "":
                continue
            if kode in promo:
                print("  Kode sudah ada!")
                continue
            nama = input_teks("  Nama/deskripsi promo: ")
            pilih_pot = input_angka_atau_batal(
                "  Potongan dalam ribuan (0=Batal, 1-500): ", 500)
            if pilih_pot == -1:
                continue
            pilih_min = input_angka_atau_batal(
                "  Min belanja dalam ribuan (0=Batal, 1-1000): ", 1000)
            if pilih_min == -1:
                continue
            maks = input_angka_atau_batal(
                "  Maks pemakaian (0=Batal, 1-9999): ", 9999)
            if maks == -1:
                continue
            promo[kode] = (pilih_pot * 1000, pilih_min * 1000,
                           nama, True, 0, maks)
            print("  Promo", kode, "berhasil ditambahkan!")

        else:
            kode = input("  Kode promo yang dihapus (0=Batal): ").strip().upper()
            if kode == "0" or kode == "":
                continue
            if kode in promo:
                del promo[kode]
                print("  Promo", kode, "dihapus.")
            else:
                print("  Promo tidak ditemukan!")

def kelola_akun():
    """Kelola akun user: ban/unban, reset saldo, kirim notifikasi."""
    while True:
        garis()
        print("  KELOLA AKUN PENGGUNA")
        garis()
        for a in akun:
            status = "BANNED" if a["banned"] else "OK    "
            print("  " + a["username"].ljust(15),
                  a["role"].ljust(6),
                  "| Member:", a["member"].ljust(9),
                  "| Poin:", str(a["poin"]).rjust(4),
                  "| Saldo: Rp", uang(a["saldo"]).rjust(10),
                  "|", status)
        garis("-")
        print("  1. Ban / Unban user")
        print("  2. Reset saldo user")
        print("  3. Kirim notifikasi / broadcast")
        print("  0. Kembali")

        pilih = input_angka_atau_batal("  Pilih: ", 3)
        if pilih == -1:
            return

        if pilih == 1:
            usr = input("  Username (0=Batal): ").strip()
            if usr == "0" or usr == "":
                continue
            ditemukan = False
            for a in akun:
                if a["username"].lower() == usr.lower():
                    a["banned"] = not a["banned"]
                    status = "BANNED" if a["banned"] else "AKTIF"
                    print("  " + a["username"], "->", status)
                    ditemukan = True
            if not ditemukan:
                print("  User tidak ditemukan!")

        elif pilih == 2:
            usr = input("  Username (0=Batal): ").strip()
            if usr == "0" or usr == "":
                continue
            ditemukan = False
            for a in akun:
                if a["username"].lower() == usr.lower():
                    nominal_rb = input_angka_atau_batal(
                        "  Saldo baru dalam ribuan (0=Batal, 1-10000): ",
                        10000)
                    if nominal_rb == -1:
                        break
                    a["saldo"] = nominal_rb * 1000
                    print("  Saldo", a["username"],
                          "di-set ke Rp", uang(a["saldo"]))
                    ditemukan = True
            if not ditemukan:
                print("  User tidak ditemukan!")

        else:
            usr = input("  Username (kosong=semua, 0=Batal): ").strip()
            if usr == "0":
                continue
            pesan = input_teks("  Isi pesan: ")
            if usr == "":
                for a in akun:
                    tambah_notif(a["username"], "[ADMIN] " + pesan)
                print("  Broadcast terkirim ke", len(akun), "akun.")
            else:
                tambah_notif(usr, "[ADMIN] " + pesan)
                print("  Notifikasi terkirim ke", usr + ".")

def kelola_crew():
    """Kelola crew: aktifkan/nonaktifkan, pindah penugasan."""
    while True:
        garis()
        print("  KELOLA CREW")
        garis()
        for i in range(len(crew)):
            status = "AKTIF" if crew[i][4] else "NONAKTIF"
            print("  " + str(i + 1) + ".",
                  crew[i][1].ljust(8),
                  crew[i][0].ljust(22), "|", status)
        garis("-")
        print("  1. Aktifkan / Nonaktifkan crew")
        print("  2. Pindah crew ke layanan lain")
        print("  0. Kembali")

        pilih = input_angka_atau_batal("  Pilih: ", 2)
        if pilih == -1:
            return

        no_crew = input_angka_atau_batal(
            "  Nomor crew (0=Batal): ", len(crew))
        if no_crew == -1:
            continue
        no_crew = no_crew - 1

        if pilih == 1:
            crew[no_crew][4] = not crew[no_crew][4]
            status = "AKTIF" if crew[no_crew][4] else "NONAKTIF"
            print("  " + crew[no_crew][0], "->", status)

        else:
            print("  Daftar layanan:")
            for i in range(len(layanan)):
                print("  " + str(i + 1) + ".", layanan[i][0], layanan[i][2])
            print("  0. Batal")
            tujuan_idx = input_angka_atau_batal(
                "  Pindah ke layanan nomor: ", len(layanan))
            if tujuan_idx == -1:
                continue
            crew[no_crew][1] = layanan[tujuan_idx - 1][0]
            print("  " + crew[no_crew][0],
                  "dipindah ke", layanan[tujuan_idx - 1][0])

def lihat_semua_riwayat():
    """Tampilkan semua riwayat pemesanan dari semua user."""
    garis()
    print("  SEMUA RIWAYAT PEMESANAN")
    garis()
    if len(riwayat) == 0:
        print("  Belum ada transaksi.")
        return
    for p in riwayat:
        tanda = "[OK]" if p["status"] == "Aktif" else "[XX]"
        print("  " + tanda, p["kode"], "|",
              p["pembeli"], "|", p["jenis"], "|",
              p["tujuan"], "|", p["jadwal"], "|",
              p["kelas"], "| Rp", uang(p["total"]), "|",
              p["status"])

def lihat_log():
    """Tampilkan log aktivitas terakhir (50 baris)."""
    garis()
    print("  LOG AKTIVITAS (50 terakhir)")
    garis()
    if len(log_aktivitas) == 0:
        print("  Log kosong.")
        return
    mulai = max(0, len(log_aktivitas) - 50)
    for l in log_aktivitas[mulai:]:
        print("  " + l["username"].ljust(15),
              l["aksi"].ljust(15),
              l["detail"])

def tandai_berangkat_admin():
    """Admin menandai semua tiket satu jadwal layanan sebagai berangkat."""
    garis()
    print("  TANDAI KEBERANGKATAN")
    garis()
    for i in range(len(layanan)):
        print("  " + str(i + 1) + ".", layanan[i][0], layanan[i][2])
    print("  0. Batal")

    idx = input_angka_atau_batal("  Nomor layanan: ", len(layanan))
    if idx == -1:
        return
    idx = idx - 1

    jadwal_str = input("  Jadwal (mis. 08.00, 0=Batal): ").strip()
    if jadwal_str == "0" or jadwal_str == "":
        print("  Dibatalkan.")
        return

    hitungan = 0
    for p in riwayat:
        if (p["idx"] == idx and
                p["jadwal"] == jadwal_str and
                p["status"] == "Aktif"):
            p["sudah_berangkat"] = True
            hitungan = hitungan + 1

    print("  " + str(hitungan), "tiket ditandai berangkat untuk",
          layanan[idx][0], jadwal_str)

def laporan_waitlist():
    """Tampilkan semua antrian waitlist."""
    garis()
    print("  DAFTAR WAITLIST")
    garis()
    if len(waitlist) == 0:
        print("  Waitlist kosong.")
        return
    for w in waitlist:
        print("  " + w["username"].ljust(15),
              layanan[w["idx"]][0], layanan[w["idx"]][2],
              "| Jadwal:", w["jadwal"],
              "| Kelas:", w["kelas"],
              "| Jumlah:", w["jumlah"],
              "| Kuota sekarang:", kuota[w["idx"]])


# ================================================================
#  BAGIAN 11 - MENU ADMIN
# ================================================================

def menu_admin(akun_user):
    """Menu utama untuk admin."""
    while True:
        garis("=", 40)
        print("  MENU ADMIN")
        print("  " + akun_user["username"])
        garis("=", 40)
        print("   1. Laporan Pendapatan")
        print("   2. Statistik Layanan")
        print("   3. Semua Riwayat Pemesanan")
        print("   4. Rating Crew")
        print("   5. Ulasan Penumpang")
        print("   6. Kelola Promo")
        print("   7. Kelola Akun Pengguna")
        print("   8. Kelola Crew")
        print("   9. Log Aktivitas")
        print("  10. Tandai Keberangkatan")
        print("  11. Daftar Waitlist")
        print("  12. Lihat Daftar Layanan")
        print("  13. Logout")
        garis("-", 40)

        menu = input_angka("  Pilih menu: ", 13)

        if   menu ==  1: laporan_pendapatan()
        elif menu ==  2: statistik_layanan()
        elif menu ==  3: lihat_semua_riwayat()
        elif menu ==  4: laporan_crew()
        elif menu ==  5: lihat_ulasan()
        elif menu ==  6: kelola_promo()
        elif menu ==  7: kelola_akun()
        elif menu ==  8: kelola_crew()
        elif menu ==  9: lihat_log()
        elif menu == 10: tandai_berangkat_admin()
        elif menu == 11: laporan_waitlist()
        elif menu == 12: tampilkan_layanan()
        else:
            print("  Logout berhasil.")
            catat_log(akun_user["username"], "LOGOUT")
            break

# ================================================================
#  PROGRAM UTAMA
# ================================================================

garis("=", 55)
print("  SELAMAT DATANG".center(55))
print("  SISTEM LAYANAN TRANSPORTASI TERPADU".center(55))
print("  Bus  |  Travel  |  Kereta".center(55))
garis("=", 55)

while True:
    print()
    print("  1. Registrasi")
    print("  2. Login")
    print("  3. Lihat Jadwal & Layanan")
    print("  4. Keluar")
    garis("-", 30)

    menu = input_angka("  Pilih: ", 4)

    if menu == 1:
        registrasi()

    elif menu == 2:
        pengguna = login()
        # Cek apakah login berhasil (bukan None)
        if pengguna != None:
            if pengguna["role"] == "admin":
                menu_admin(pengguna)
            else:
                menu_user(pengguna)

    elif menu == 3:
        print("  1. Semua layanan")
        print("  2. Urut dari harga termurah")
        print("  3. Urut dari rating terbaik")
        print("  0. Kembali")
        p = input_angka_atau_batal("  Pilih: ", 3)
        if p == 2:
            tampilkan_layanan(urut_harga=True)
        elif p == 3:
            tampilkan_layanan(urut_rating=True)
        elif p == 1:
            tampilkan_layanan()
        # p == -1 artinya 0 = kembali, tidak perlu tindakan

    else:
        print("  Terima kasih! Semoga perjalanan menyenangkan.")
        break
