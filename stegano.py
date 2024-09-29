from PIL import Image

# Fungsi XOR untuk enkripsi dan dekripsi
def xor_encrypt_decrypt(message, password):
    print("Pesan sebelum XOR:", message)
    encrypted_message = ''.join(chr(ord(c) ^ ord(password[i % len(password)])) for i, c in enumerate(message))
    print("Pesan setelah XOR:", encrypted_message)
    return encrypted_message

# Fungsi untuk menyembunyikan pesan ke dalam gambar
def encode_message(image_path, message, password, output_path):
    # Enkripsi pesan dengan password
    encrypted_message = xor_encrypt_decrypt(message, password)
    
    # Buka gambar
    img = Image.open(image_path)
    encoded_img = img.copy()
    width, height = img.size
    pixels = encoded_img.load()

    # Konversi pesan terenkripsi ke biner
    encrypted_message += chr(0)  # Menambahkan karakter akhir pesan (Null terminator)
    binary_message = ''.join([format(ord(i), "08b") for i in encrypted_message])

    # Pastikan pesan tidak terlalu panjang
    if len(binary_message) > width * height * 3:
        raise ValueError("Pesan terlalu panjang untuk disembunyikan dalam gambar ini.")

    # Menyembunyikan pesan dalam pixel
    idx = 0
    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])

            # Jika gambar memiliki channel alpha (RGBA), abaikan channel alpha
            for i in range(3):  # Hanya edit channel RGB (bukan alpha)
                if idx < len(binary_message):
                    pixel[i] = (pixel[i] & ~1) | int(binary_message[idx])
                    idx += 1
            pixels[x, y] = tuple(pixel)

    # Simpan gambar hasil encode
    encoded_img.save(output_path)
    print("Pesan berhasil disembunyikan ke dalam gambar.")

# Fungsi untuk mengambil pesan dari gambar
def decode_message(image_path):
    # Buka gambar
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    # Ambil biner dari gambar
    binary_message = ""
    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])
            for i in range(3):  # Hanya ambil channel RGB (bukan alpha)
                binary_message += str(pixel[i] & 1)

    # Konversi biner menjadi string
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    encrypted_message = ''.join([chr(int(char, 2)) for char in chars])

    # Berhenti saat bertemu Null terminator
    encrypted_message = encrypted_message.split(chr(0))[0]

    # Minta password dari pengguna
    password = input("Masukkan password untuk melihat pesan tersembunyi: ")

    # Dekripsi pesan menggunakan password
    decrypted_message = xor_encrypt_decrypt(encrypted_message, password)
    
    return decrypted_message

# Contoh penggunaan
input_image = 'C:/Users/HAFIDZ/OneDrive/Documents/Kuliah/Aljabar Linier/coba.png'  # Path ke gambar input
output_image = 'C:/Users/HAFIDZ/OneDrive/Documents/Kuliah/Aljabar Linier/anayycoba.png'  # Path ke gambar hasil encode
pesan = "cihuyyyyyyy anjayyyyy"  # Pesan yang akan disembunyikan
password = "gokil123"  # Password untuk enkripsi

# Sembunyikan pesan
encode_message(input_image, pesan, password, output_image)

# Ambil pesan dari gambar
decoded_message = decode_message(output_image)
print("Pesan tersembunyi:", decoded_message)

