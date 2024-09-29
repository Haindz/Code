from PIL import Image

def encode_image(image_path, message, output_path):
    # Membuka gambar
    image = Image.open(image_path)
    encoded_image = image.copy()
    
    # Mengubah pesan menjadi biner
    message += '\0'  # Menandai akhir pesan
    binary_message = ''.join(format(ord(i), '08b') for i in message)
    
    data_index = 0
    pixels = encoded_image.load()
    
    # Mengubah piksel gambar untuk menyimpan pesan
    for i in range(encoded_image.size[0]):
        for j in range(encoded_image.size[1]):
            r, g, b = pixels[i, j]
            
            if data_index < len(binary_message):
                # Mengubah bit paling kanan dari channel merah
                r = (r & ~1) | int(binary_message[data_index])
                data_index += 1
            
            pixels[i, j] = (r, g, b)
            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    # Menyimpan gambar yang sudah terkode
    encoded_image.save(output_path)
    print(f'Message encoded and saved to {output_path}')

def decode_image(image_path):
    # Membuka gambar
    image = Image.open(image_path)
    binary_message = ''
    pixels = image.load()
    
    # Membaca piksel gambar untuk mengambil pesan
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r, g, b = pixels[i, j]
            binary_message += str(r & 1)  # Mengambil bit paling kanan dari channel merah
            
            # Jika menemukan akhir pesan
            if binary_message[-8:] == '00000000':
                break
        if binary_message[-8:] == '00000000':
            break
            
    # Mengubah biner kembali ke teks
    message = ''
    for i in range(0, len(binary_message) - 8, 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))
    
    return message

# Contoh penggunaan
image_path = "C:/Users/HAFIDZ/OneDrive/Documents/Kuliah/Aljabar Linier/coba.png"  # Gambar asli
output_path = "C:/Users/HAFIDZ/OneDrive/Documents/Kuliah/Aljabar Linier/encode_coba.png" # Gambar setelah encoding
message = 'cihuuyyy'

encode_image(image_path, message, output_path)
decoded_message = decode_image(output_path)
print(f'Decoded message: {decoded_message}')
