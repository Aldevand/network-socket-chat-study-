import socket
import threading

HOST_TUJUAN = '127.0.0.1'
PORT_TUJUAN = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"[*] Mencoba mengetuk pintu server di {HOST_TUJUAN}:{PORT_TUJUAN}...")
client_socket.connect((HOST_TUJUAN, PORT_TUJUAN))
print("[+] Berhasil terhubung ke Group Chat Server!")
print("[*] Ketik pesan lalu tekan Enter. Ketik 'exit' untuk keluar.\n")


# 1. Thread Pendengar: Tugasnya HANYA mendengarkan kiriman dari server
def dengar_pesan_masuk():
    while True:
        try:
            pesan = client_socket.recv(1024).decode('utf-8')
            if not pesan:
                break
            # Cetak pesan dari teman yang diteruskan oleh server
            print(f"\n{pesan}")
            print("Masukan Pesan: ", end="", flush=True)
        except:
            break


# Jalankan thread pendengar di latar belakang
thread_pendengar = threading.Thread(target=dengar_pesan_masuk)
thread_pendengar.daemon = True
thread_pendengar.start()


# 2. Loop Utama: Tugasnya HANYA membaca ketikan keyboard dan mengirimkannya
while True:
    pesan = input("Masukan Pesan: ")
    if pesan.strip() == "":
        continue
        
    client_socket.send(pesan.encode('utf-8'))
    
    if pesan == 'exit':
        break

client_socket.close()
print("[*] Kamu telah keluar dari chat.")
