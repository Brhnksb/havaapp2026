import customtkinter as ctk
import requests
from tkinter import messagebox


#API anahtarını buraya yapıştırın:
API_KEY = "30f7973aaadd83c3d9fadaf2e60a1b04" 
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


app = ctk.CTk()
app.geometry("400x450")
app.title("Modern Hava Durumu")
app.resizable(False, False)


def hava_durumu_getir():
    sehir = sehir_giris.get().strip()
    if not sehir:
        messagebox.showwarning("Uyarı", "Lütfen bir şehir adı girin!")
        return

    params = {
        "q": sehir,
        "appid": API_KEY,
        "units": "metric",
        "lang": "tr"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        veri = response.json()

        # API'den gelen kodu string (metin) olarak alıyoruz ki tam tespit edelim
        hata_kodu = str(veri.get("cod"))

        if hata_kodu == "200":
            sicaklik = round(veri["main"]["temp"])
            hissedilen = round(veri["main"]["feels_like"])
            durum = veri["weather"][0]["description"].title()
            nem = veri["main"]["humidity"]
            ruzgar = veri["wind"]["speed"]

            sonuc_metni = (
                f"📍 {sehir.upper()}\n\n"
                f"🌡️ Sıcaklık: {sicaklik} °C\n"
                f"🤔 Hissedilen: {hissedilen} °C\n"
                f"☁️ Durum: {durum}\n"
                f"💧 Nem: %{nem}\n"
                f"💨 Rüzgar: {ruzgar} m/s"
            )
            sonuc_etiket.configure(text=sonuc_metni, text_color="#1f6aa5" if ctk.get_appearance_mode() == "Light" else "#569cbd")

        elif hata_kodu == "401":
            sonuc_etiket.configure(text="HATA 401: API Anahtarın henüz aktif değil!\n(Yeni aldıysan 1-2 saat sürebilir, beklemelisin)", text_color="orange")
        elif hata_kodu == "404":
            sonuc_etiket.configure(text="Şehir bulunamadı!\nLütfen yazımı kontrol edin.", text_color="red")
        else:
            sonuc_etiket.configure(text=f"Bilinmeyen Hata Kodu: {hata_kodu}\nMesaj: {veri.get('message')}", text_color="red")

    except requests.exceptions.RequestException:
        sonuc_etiket.configure(text="Bağlantı hatası!\nİnternetinizi kontrol edin.", text_color="red")




baslik = ctk.CTkLabel(app, text="Hava Durumu", font=("Helvetica", 28, "bold"))
baslik.pack(pady=(30, 10))


alt_baslik = ctk.CTkLabel(app, text="Hava durumunu öğrenmek için şehir girin", font=("Helvetica", 14), text_color="gray")
alt_baslik.pack(pady=(0, 20))


sehir_giris = ctk.CTkEntry(app, placeholder_text="Örn: Istanbul, Ankara, Izmir", width=250, height=40, font=("Helvetica", 14))
sehir_giris.pack(pady=10)


app.bind('<Return>', lambda event: hava_durumu_getir())


sorgula_buton = ctk.CTkButton(app, text="Sorgula", command=hava_durumu_getir, width=200, height=40, font=("Helvetica", 15, "bold"), corner_radius=20)
sorgula_buton.pack(pady=15)


sonuc_etiket = ctk.CTkLabel(app, text="", font=("Helvetica", 18, "bold"), justify="left")
sonuc_etiket.pack(pady=20)


app.mainloop()