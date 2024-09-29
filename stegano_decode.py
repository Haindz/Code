from PIL import Image

# Fungsi XOR untuk enkripsi dan dekripsi
def xor_encrypt_decrypt(message, password):
    print("Pesan sebelum XOR:", message)
    encrypted_message = ''.join(chr(ord(c) ^ ord(password[i % len(password)])) for i, c in enumerate(message))
    print("Pesan setelah XOR:", encrypted_message)
    return encrypted_message

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
output_image = "C:/Users/HAFIDZ/OneDrive/Documents/Kuliah/Aljabar Linier/hasil.png"  # Path ke gambar hasil encode

# Ambil pesan dari gambar
decoded_message = decode_message(output_image)
print("Pesan tersembunyi:", decoded_message)

