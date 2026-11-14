import socket
import threading

# 1. Alamat dan Port tempat Server ini membuka pintu
HOST = '127.0.0.1'
PORT = 9999

# 2. Inisialisasi Socket TCP dan Bind ke alamat sendiri
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))

# 3. Buku Tamu (Menyimpan semua client yang sedang aktif)
daftar_client = []

server_socket.listen()
print(f"[*] SERVER CHAT AKTIF!")
print(f"[*] Sedang menunggu di IP: {HOST} pada Port: {PORT}...")


# 4. Fungsi Broadcast: Mengoper pesan ke SEMUA client, kecuali si pengirim
def broadcast(pesan, pengirim):
    for client in daftar_client:
        if client != pengirim:
            try:
                client.send(pesan.encode('utf-8'))
            except:
                # Jika koneksi client error/putus, bersihkan dari daftar tamu
                if client in daftar_client:
                    daftar_client.remove(client)


# 5. Fungsi Pelayan Khusus (Dijalankan per Client oleh Thread terpisah)
def terima_pesan(koneksi, alamat_client):
    while True:
        try:
            pesan = koneksi.recv(1024).decode('utf-8')
            
            # Jika client menutup koneksi (pesan kosong atau 'exit')
            if not pesan or pesan == 'exit':
                print(f"[-] Client {alamat_client} keluar dari chat.")
                break
            
            format_pesan = f"[{alamat_client[1]}]: {pesan}"
            print(f"[PESAN DITERIMA] {format_pesan}")
            
            # Teruskan pesan ke teman-teman lain di grup
            broadcast(format_pesan, koneksi)
            
        except ConnectionResetError:
            print(f"[-] Client {alamat_client} terputus tiba-tiba.")
            break

    # Bersihkan saat client pamit/selesai
    if koneksi in daftar_client:
        daftar_client.remove(koneksi)
    koneksi.close()


# 6. Loop Utama (Satpam Pintu): Selalu siaga menerima tamu baru
while True:
    koneksi, alamat_client = server_socket.accept()
    print(f"[+] Ada koneksi masuk dari client dengan alamat: {alamat_client}")
    
    # Masukkan tamu baru ke buku tamu
    daftar_client.append(koneksi)
    
    # Rekrut 1 thread baru untuk melayani obrolan tamu ini di latar belakang
    thread = threading.Thread(target=terima_pesan, args=(koneksi, alamat_client))
    thread.daemon = True  # Supaya thread otomatis mati jika server ditutup
    thread.start()
