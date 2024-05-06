import flet as ft
import numpy as np

def main(page: ft.Page):
    def KSA(key):
        key_length = len(key)
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % key_length]) % 256
            S[i], S[j] = S[j], S[i] #swap
        return S

    def PRGA(S, n):
        i = 0
        j = 0
        key = []

        while n>0:
            n=n-1
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            K = S[(S[i] + S[j]) % 256]
            key.append(K)
        return key

    def exit_(e):
        page.window_destroy()     

    def opendialog():
        page.dialog = dialog    
        dialog.open = True
        page.update()

    def closedialog(e):
        dialog.open = False
        page.update()
    
    def openinf(e):
        page.dialog = inf    
        inf.open = True
        page.update()
    def closeinf(e):
        inf.open = False
        page.update()

    def openhelp(e):
        page.dialog = help    
        help.open = True
        page.update()
    def closehelp(e):
        help.open = False
        page.update()
    
    def HapusText(e):
        if not (plaintext.value) and not (key.value) and (hasil.value) == "Hasil Teks":    
            opendialog()
            page.update()
        else:
            plaintext.value=""
            hasil.value="Hasil Teks"
            key.value =""
            page.update()
   
    def RC4_encrypt(e):
        t = plaintext.value
        k = key.value
        if not (plaintext.value) or not (key.value):    
            opendialog()
            page.update()
        else:
            page.update()
            k = [ord(c) for c in k]
            S = KSA(k)
            keystream = np.array(PRGA(S, len(t)))
            t = np.array([ord(i) for i in t])
            cipher = keystream ^ t
            hasil.value = cipher.astype(np.uint8).data.hex()
            page.update()
            return cipher.astype(np.uint8).data.hex()

    def RC4_decrypt(e):
        t = plaintext.value
        k = key.value
        if not (plaintext.value) or not (key.value):    
            opendialog()
            page.update()
        else:
            try:
                k = [ord(c) for c in k]
                S = KSA(k)
                keystream = np.array(PRGA(S, len(t) // 2))
                t = bytes.fromhex(t)
                p = keystream ^ np.array([c for c in t])
                hasil.value = ''.join([chr(c) for c in p])
                page.update()
                return ''.join([chr(c) for c in p])
            except:
                opendialog()              

    dialog = ft.AlertDialog(modal=True,
            title=ft.Text("Kesalahan"),
            content=ft.Text("Teks yang dimasukan kosong atau tidak sesuai"),actions=[
                ft.TextButton("OK",on_click=closedialog)
            ])
    
    inf = ft.AlertDialog(modal=True,
            title=ft.Text("Informasi Aplikasi"),
            content=ft.Text(" Aplikasi ini dibuat untuk memenuhi tugas mata kuliah Keamanan Informasi \n Dibuat Oleh :\n\n Naufal\n https://github.com/thatsatouguy \n"),
            actions=[ft.TextButton("OK",on_click=closeinf)])

    help = ft.AlertDialog(modal=True,
            title=ft.Text("Cara Penggunaan"),
            content=ft.Text("- Masukkan teks yang ingin Anda enkripsi atau dekripsi pada kolom text, Teks yang dimasukkan akan dienkripsi atau didekripsi menggunakan algoritma RC4 \n- Masukkan kunci yang sesuai pada kolom key \n- Tekan tombol Enkripsi untuk mengenkripsi teks, sedangkan tekan tombol Dekripsi untuk mengdekripsi teks \n- Hasil enkripsi atau dekripsi akan ditampilkan di kolom Hasil Teks \n- Tekan tombol Hapus untuk menghapus teks yang sudah diisi di plaintext, key, dan Hasil Teks \n"),
            actions=[ft.TextButton("OK",on_click=closehelp)])
    
    page.title = "EncryptRC4"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.bgcolor = ft.colors.BLACK26
    page.window_height = 400
    page.window_width = 700
    page.window_resizable = False
    page.window_maximizable = False

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.KEY),
        leading_width=40,
        title=ft.Text("EncryptRC4", font_family="Open Sans",size=16),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=
        [
            ft.PopupMenuButton(tooltip="Tampilkan Menu",
                items=
                [
                    ft.PopupMenuItem(text="Info", on_click=openinf ),
                    ft.PopupMenuItem(text="Cara Penggunaan", on_click=openhelp ),
                    ft.PopupMenuItem(text="Close", on_click=exit_ ),
                ]
            ),
        ],
    )
    
    plaintext = ft.TextField(label="text", border_radius=15,border_width=2,expand=True, height=60, tooltip= "Masukkan teks yang ingin Anda enkripsi atau dekripsi pada kolom tersebut, Teks yang dimasukkan akan dienkripsi atau didekripsi menggunakan algoritma RC4")
    key = ft.TextField(label="key", border_radius=15,border_width=2,expand=True, height=60, tooltip= "Masukkan kunci yang sesuai pada kolom tersebut") 
    hasil = ft.TextField(value="Hasil Teks", read_only=True,expand=True,border_radius=15, border_width=2, height=60, tooltip= "Hasil enkripsi atau dekripsi akan ditampilkan di kolom tersebut")
    
    textboxplain = ft.Container(
        content=ft.Row(controls=[
            plaintext]))
    textboxplain.padding = ft.padding.only(top=5)
    textboxkey = ft.Container(
        content=ft.Row(controls=[
            key]))
    textboxkey.padding = ft.padding.only(top=5)
    textboxhasil = ft.Container(
        content=ft.Row(controls=[
            hasil]))
    textboxhasil.padding = ft.padding.only(top=5)
    Tombol = ft.Container(content=ft.Row(controls=[
        ft.ElevatedButton("Hapus",on_click=HapusText, width=150, height=50,expand=True,tooltip=""),
        ft.ElevatedButton("Enkripsi",on_click=RC4_encrypt, width=150, height=50, expand=True, tooltip=""),
        ft.ElevatedButton("Dekripsi",on_click=RC4_decrypt ,width=150, height=50,expand=True, tooltip="")
    ]))
    Tombol.padding = ft.padding.only(top=10)

    page.add(textboxplain,textboxkey,textboxhasil,Tombol)

ft.app(target=main)