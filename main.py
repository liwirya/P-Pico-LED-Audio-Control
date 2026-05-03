import machine
from time import sleep, ticks_us, ticks_diff

class LayarMini:
    def __init__(self, jalur, alamat=0x27):
        self.i2c = jalur
        self.addr = alamat
        self.nyala = 0x08
        for p in [0x33, 0x32, 0x28, 0x0C, 0x01]:
            self.krm_cmd(p)
            sleep(0.005)

    def tls_byte(self, isi):
        self.i2c.writeto(self.addr, bytearray([isi | self.nyala | 0x04]))
        self.i2c.writeto(self.addr, bytearray([isi | self.nyala & ~0x04]))

    def krm_cmd(self, cmd):
        self.tls_byte(cmd & 0xF0)
        self.tls_byte((cmd << 4) & 0xF0)

    def krm_huruf(self, data):
        self.tls_byte((data & 0xF0) | 0x01)
        self.tls_byte(((data << 4) & 0xF0) | 0x01)

    def hapus(self):
        self.krm_cmd(0x01)
        sleep(0.002)

    def geser(self, x, y):
        offset = [0x00, 0x40, 0x14, 0x54]
        self.krm_cmd(0x80 | (x + offset[y]))

    def cetak(self, kalimat):
        for hrf in kalimat:
            self.krm_huruf(ord(hrf))


pin_output = [21, 20, 19, 18, 17, 16]
kumpulan_led = [machine.Pin(p, machine.Pin.OUT) for p in pin_output]

speaker = machine.PWM(machine.Pin(1))
speaker.duty_u16(0)

sensor_putar = machine.ADC(28) 
sensor_remote = machine.Pin(2, machine.Pin.IN)

i2c_bus = machine.I2C(1, sda=machine.Pin(26), scl=machine.Pin(27), freq=400000)
layar_lcd = LayarMini(i2c_bus)

status_program = 1
mode_sebelumnya = 0 
teks_keterangan_sebelumnya = ""

def proses_tombol(perintah):
    global status_program
    if perintah in [1, 2, 3, 4, 5]:
        status_program = perintah

class PenerimaSinyal:
    def __init__(self, pin, fungsi_panggil):
        self.pin = pin
        self.aksi = fungsi_panggil
        self.waktu_lalu = ticks_us()
        self.tahap = 0
        self.data_sinyal = 0
        self.jumlah_bit = 0
        self.pin.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=self.interupsi_baca)

    def interupsi_baca(self, pin_ir):
        waktu_skrg = ticks_us()
        selisih = ticks_diff(waktu_skrg, self.waktu_lalu)
        self.waktu_lalu = waktu_skrg
        nilai = pin_ir.value()

        if self.tahap == 0:
            if nilai == 0: self.tahap = 1
        elif self.tahap == 1:
            if nilai == 1 and 8000 < selisih < 10000: self.tahap = 2
            else: self.tahap = 0
        elif self.tahap == 2:
            if nilai == 0 and 4000 < selisih < 5000:
                self.tahap = 3; self.data_sinyal = 0; self.jumlah_bit = 0
            else: self.tahap = 0
        elif self.tahap == 3:
            if nilai == 1: pass
            elif nilai == 0:
                if 1500 < selisih < 2000:
                    self.data_sinyal |= (1 << self.jumlah_bit)
                    self.jumlah_bit += 1
                elif 400 < selisih < 700:
                    self.jumlah_bit += 1
                else:
                    self.tahap = 0; return

                if self.jumlah_bit == 32:
                    tombol = (self.data_sinyal >> 16) & 0xFF
                    self.aksi(tombol)
                    self.tahap = 0

remote_kontrol = PenerimaSinyal(sensor_remote, proses_tombol)

layar_lcd.hapus()
layar_lcd.geser(3, 1)
layar_lcd.cetak("MULAI PROGRAM")

nada_nyala = [800, 1100, 1500]
for n in nada_nyala:
    speaker.freq(n)
    speaker.duty_u16(30000) 
    sleep(0.15) 
speaker.duty_u16(0)
sleep(0.2)

titik_led = 0

while True:
    baca_pot = sensor_putar.read_u16() 
    
    teks_keterangan = ""
    if status_program == 1 or status_program == 4:
        level = int((baca_pot * 4.99) / 65536) 
        list_cepat = ["-> Sngt Cepat", "-> Cepat", "-> Sedang", "-> Lambat", "-> Sngt Lambat"]
        teks_keterangan = list_cepat[level]
    elif status_program == 2:
        batas = (baca_pot * 7) // 65536 
        teks_keterangan = f"-> {batas} LED Nyala"
    elif status_program == 3:
        if baca_pot < 500:
            teks_keterangan = "-> Suara Mati"
        else:
            level = int((baca_pot * 4.99) / 65536)
            list_suara = ["-> Sngt Rendah", "-> Nada Rendah", "-> Nada Sedang", "-> Nada Tinggi", "-> Sngt Tinggi"]
            teks_keterangan = list_suara[level]
    elif status_program == 5:
        teks_keterangan = "-> Mode Otomatis"

    if status_program != mode_sebelumnya:
        speaker.freq(2500)
        speaker.duty_u16(30000)
        sleep(0.1)
        speaker.duty_u16(0)
        
        layar_lcd.hapus()
        layar_lcd.geser(0, 0)
        layar_lcd.cetak(f"== STATUS: MODE {status_program} ==")
        layar_lcd.geser(0, 1)
        
        if status_program == 1:
            layar_lcd.cetak("Running LED")
        elif status_program == 2:
            layar_lcd.cetak("Meteran Bar Graph")
        elif status_program == 3:
            layar_lcd.cetak("Pengatur Nada Buzzer")
        elif status_program == 4:
            layar_lcd.cetak("Lampu Kedip")
        elif status_program == 5:
            layar_lcd.cetak("Sirine Darurat")
            
        mode_sebelumnya = status_program
        teks_keterangan_sebelumnya = "" 

    if teks_keterangan != teks_keterangan_sebelumnya:
        layar_lcd.geser(0, 3) 
        layar_lcd.cetak(teks_keterangan + " " * (20 - len(teks_keterangan)))
        teks_keterangan_sebelumnya = teks_keterangan

    if status_program == 1:
        speaker.duty_u16(0)
        tunda = 0.02 + (baca_pot * 0.48 / 65535) 
        
        for idx, l in enumerate(kumpulan_led):
            l.value(1 if idx == titik_led else 0)
            
        titik_led = 0 if titik_led >= 5 else titik_led + 1
        sleep(tunda)
            
    elif status_program == 2:
        speaker.duty_u16(0)
        batas = (baca_pot * 7) // 65536 
        for idx, l in enumerate(kumpulan_led):
            l.value(1 if idx < batas else 0)
        sleep(0.05)
        
    elif status_program == 3:
        for l in kumpulan_led: l.value(0) 
        
        if baca_pot < 500:
            speaker.duty_u16(0)
        else:
            frek = 100 + int((baca_pot / 65535) * 2500)
            speaker.freq(frek)
            speaker.duty_u16(32768)
        sleep(0.05)

    elif status_program == 4:
        speaker.duty_u16(0)
        tempo = 0.05 + (baca_pot * 0.8 / 65535)
        
        for l in kumpulan_led: l.value(1)
        sleep(tempo)
        
        if status_program == 4:
            for l in kumpulan_led: l.value(0)
            sleep(tempo)

    elif status_program == 5:
        for i in range(3): kumpulan_led[i].value(1)
        for i in range(3, 6): kumpulan_led[i].value(0)
        speaker.freq(800)
        speaker.duty_u16(32768)
        sleep(0.25)
        
        if status_program == 5:
            for i in range(3): kumpulan_led[i].value(0)
            for i in range(3, 6): kumpulan_led[i].value(1)
            speaker.freq(1200)
            speaker.duty_u16(32768)
            sleep(0.25)
