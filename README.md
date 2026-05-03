# 🎛️ P-Pico-LED-Audio-Control

Proyek berbasis **Raspberry Pi Pico** yang mengintegrasikan kontrol LED, audio buzzer, tampilan LCD, dan penerimaan sinyal inframerah menggunakan **MicroPython**. Sistem ini mendukung 5 mode operasi yang dapat diubah secara real-time melalui remote IR, dengan potensiometer sebagai pengatur parameter dan LCD 20×4 sebagai antarmuka pengguna.

> 🔗 Simulasi tersedia di [Wokwi](https://wokwi.com/projects/462884846948708353)

---

## 📋 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
- [Diagram Skematik](#-diagram-skematik)
- [Prasyarat Instalasi](#-prasyarat-instalasi)
- [Susunan Project](#-susunan-project)
- [Koneksi Pin](#-koneksi-pin)
- [Cara Penggunaan](#-cara-penggunaan)
- [Mode Operasi](#-mode-operasi)
---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|---|---|
| **5 Mode LED** | Running LED, Bar Graph, Buzzer, Kedip, dan Sirine Darurat |
| **Kontrol Remote IR** | Ganti mode operasi tanpa menyentuh perangkat |
| **Potensiometer** | Atur kecepatan, jumlah LED aktif, dan frekuensi suara secara real-time |
| **Audio Buzzer** | Output suara dengan frekuensi yang dapat dikonfigurasi via PWM |
| **Tampilan LCD I2C** | Status dan informasi mode ditampilkan di LCD 20×4 karakter |
| **Feedback Audio** | Nada konfirmasi saat program dimulai dan saat mode berubah |
| **Simulasi Wokwi** | Dapat langsung diuji di browser tanpa hardware fisik |

---

## 🛠️ Teknologi yang Digunakan

- **Platform:** Raspberry Pi Pico (RP2040)
- **Bahasa Pemrograman:** MicroPython v1.24.1
- **Simulator:** [Wokwi](https://wokwi.com)
- **Komunikasi:** I2C (LCD), ADC (Potensiometer), PWM (Buzzer), IRQ/Interrupt (IR Receiver)
- **Protokol IR:** NEC Protocol (32-bit decoding via interrupt)

### Komponen Hardware

| Komponen | Jumlah | Keterangan |
|---|---|---|
| Raspberry Pi Pico | 1 | Mikrokontroler utama |
| LED Merah | 6 | Output visual utama |
| Resistor 220Ω | 6 | Pembatas arus LED |
| Buzzer Pasif | 1 | Output audio via PWM |
| Potensiometer | 1 | Input analog pengatur parameter |
| IR Receiver | 1 | Penerima sinyal remote inframerah |
| LCD 2004 I2C | 1 | Layar tampilan 20×4 karakter |

---

## 📐 Diagram Skematik

Diagram rangkaian lengkap tersedia dalam file `diagram.json` (format Wokwi).  
Buka langsung di simulator:

👉 **[Buka di Wokwi Simulator](https://wokwi.com/projects/462884846948708353)**

---

## ⚙️ Prasyarat Instalasi

### Software

1. **MicroPython** — Firmware untuk Raspberry Pi Pico  
   Unduh dari: https://micropython.org/download/RPI_PICO/

2. **Thonny IDE** *(direkomendasikan)* — Editor dan flashing tool  
   Unduh dari: https://thonny.org/

3. **Git** — Untuk mengkloning repositori  
   ```bash
   sudo apt install git       # Linux/Debian
   brew install git           # macOS
   # Windows: https://git-scm.com
   ```

### Hardware

- Raspberry Pi Pico
- Kabel USB Micro-B
- Komponen sesuai tabel di atas
- Breadboard dan kabel jumper

---

## 📁 Susunan Project

```
P-Pico-LED-Audio-Control/
├── main.py          # Program utama MicroPython
├── diagram.json     # Skematik dan konfigurasi Wokwi simulator
├── project.txt      # Informasi asal proyek (Wokwi)
├── LICENSE          # Lisensi MIT
└── README.md        # Dokumentasi proyek
```

### Penjelasan File Utama

**`main.py`**  
Berisi seluruh logika program, meliputi:
- Kelas `LayarMini` — Driver LCD 2004 via I2C (tanpa library eksternal)
- Kelas `PenerimaSinyal` — Decoder NEC IR Protocol menggunakan hardware interrupt
- Loop utama — Manajemen 5 mode operasi secara real-time

**`diagram.json`**  
File konfigurasi Wokwi yang mendefinisikan semua komponen, posisi, dan koneksi pin secara visual.

---

## 🔌 Koneksi Pin

| Pin Pico | Komponen | Fungsi |
|---|---|---|
| GP16 | LED 6 | Output LED |
| GP17 | LED 5 | Output LED |
| GP18 | LED 4 | Output LED |
| GP19 | LED 3 | Output LED |
| GP20 | LED 2 | Output LED |
| GP21 | LED 1 | Output LED |
| GP1 | Buzzer | PWM Audio Output |
| GP2 | IR Receiver (DAT) | Input sinyal remote |
| GP26 (SDA) | LCD 2004 | I2C Data |
| GP27 (SCL) | LCD 2004 | I2C Clock |
| GP28 (ADC) | Potensiometer | Input analog |
| 3V3 | VCC komponen | Tegangan referensi |
| GND | GND komponen | Ground bersama |

---

## 🚀 Cara Penggunaan

### 1. Clone Repositori

```bash
git clone https://github.com/liwirya/P-Pico-LED-Audio-Control.git
cd P-Pico-LED-Audio-Control
```

### 2. Flash MicroPython ke Pico

1. Tekan dan tahan tombol **BOOTSEL** pada Pico, lalu hubungkan ke komputer via USB
2. Pico akan muncul sebagai USB drive (`RPI-RP2`)
3. Salin file firmware `.uf2` MicroPython ke dalam drive tersebut
4. Pico akan restart otomatis dengan MicroPython aktif

### 3. Upload Program

**Menggunakan Thonny IDE:**
1. Buka Thonny → pilih interpreter **MicroPython (Raspberry Pi Pico)**
2. Buka file `main.py`
3. Klik **Run** atau tekan `F5` untuk menjalankan langsung
4. Untuk menyimpan permanen: pilih **File → Save as... → Raspberry Pi Pico** → simpan sebagai `main.py`

**Menggunakan mpremote (CLI):**
```bash
pip install mpremote
mpremote connect auto cp main.py :main.py
mpremote connect auto run main.py
```

### 4. Simulasi Tanpa Hardware (Wokwi)

Buka tautan berikut di browser untuk langsung mensimulasikan proyek:

```
https://wokwi.com/projects/462884846948708353
```

---

## 🎮 Mode Operasi

Ganti mode menggunakan tombol remote IR. LCD akan menampilkan mode aktif secara real-time.

### Mode 1 — Running LED
LED menyala satu per satu secara berurutan (efek berjalan).  
**Potensiometer:** mengatur kecepatan dari *Sangat Cepat* hingga *Sangat Lambat*.

```
[■][ ][ ][ ][ ][ ] → [ ][■][ ][ ][ ][ ] → ...
```

### Mode 2 — Meteran Bar Graph
Sejumlah LED menyala sesuai posisi potensiometer (seperti VU meter).  
**Potensiometer:** mengatur jumlah LED yang menyala (0–6 LED).

```
Pot penuh → [■][■][■][■][■][■]
Pot setengah → [■][■][■][ ][ ][ ]
```

### Mode 3 — Pengatur Nada Buzzer
Semua LED mati. Buzzer menghasilkan suara dengan frekuensi yang dikontrol potensiometer.  
**Potensiometer:** mengatur frekuensi dari *100 Hz* hingga *~2600 Hz*. Putar ke minimum untuk mematikan suara.

### Mode 4 — Lampu Kedip
Semua LED menyala dan mati secara bersamaan (efek strobe/blinking).  
**Potensiometer:** mengatur tempo kedip dari *cepat* hingga *lambat*.

### Mode 5 — Sirine Darurat
LED bergantian antara 3 LED kiri dan 3 LED kanan dengan nada sirine dua frekuensi (800 Hz / 1200 Hz) secara otomatis.

---

<div align="center">

Dibuat menggunakan MicroPython & Wokwi

Beri ⭐ jika proyek ini bermanfaat!

</div>
