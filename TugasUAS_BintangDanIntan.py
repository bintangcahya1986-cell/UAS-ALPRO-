# =============================================
# Tugas UAS Algoritma dan Pemrograman
# Nama : Bintang dan Intan
# Program: Kalkulator Sederhana
# =============================================


def tambah(a, b):
    return a + b


def kurang(a, b):
    return a - b


def kali(a, b):
    return a * b


def bagi(a, b):
    if b == 0:
        return "Error: tidak bisa dibagi dengan nol"
    return a / b


def main():
    print("=== Kalkulator Sederhana ===")
    print("1. Tambah (+)")
    print("2. Kurang (-)")
    print("3. Kali (*)")
    print("4. Bagi (/)")

    pilihan = input("Pilih operasi (1/2/3/4): ")

    if pilihan not in ("1", "2", "3", "4"):
        print("Pilihan tidak valid!")
        return

    try:
        a = float(input("Masukkan angka pertama: "))
        b = float(input("Masukkan angka kedua: "))
    except ValueError:
        print("Input harus berupa angka!")
        return

    if pilihan == "1":
        print("Hasil:", a, "+", b, "=", tambah(a, b))
    elif pilihan == "2":
        print("Hasil:", a, "-", b, "=", kurang(a, b))
    elif pilihan == "3":
        print("Hasil:", a, "*", b, "=", kali(a, b))
    elif pilihan == "4":
        print("Hasil:", a, "/", b, "=", bagi(a, b))


if __name__ == "__main__":
    main()
