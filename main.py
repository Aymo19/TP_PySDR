import numpy as np
import matplotlib.pyplot as plt
import sys

SIZE_X = 18
SIZE_Y = 6

#Premenne
num_symbols = 1000

SNR = float(sys.argv[1]) #dB
M = float(sys.argv[2]) #pocet mod stavov
k = np.log2(M) #pocet bitov na symbol

fc = 200e6 #200MHz
Fs = 100e3 #100kHz
N = 100
duration = 1.0
v_mph = 60 #mph
c = 3e8 #m/s
#-------------------------------

#random bits QPSK
x_int = np.random.randint(0, M, num_symbols)

#Mod
if M == 2: #BPSK
    x_degrees = x_int*180 + 180
    x_radians = x_degrees*np.pi/180.0
    x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians)
elif M == 4: #QPSK
    x_degrees = x_int*360/4.0 + 45
    x_radians = x_degrees*np.pi/180.0
    x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians)

#AWGN
SNR_lin = 10.0 ** ((SNR+k) / 10.0)

Es = 0
for i in x_symbols:
    Es += np.abs(i)**2
Es /= num_symbols #ocakava sa 1

odchylka = np.sqrt(Es / (SNR_lin * 2.0))

n = np.random.normal(0,1, num_symbols) * odchylka + 1j*np.random.normal(0,1, num_symbols) *odchylka

#Rayleigh
v = v_mph * 0.44704 # mph -> m/s
fd = v * fc / c  

t = np.arange(num_symbols) / Fs

x = np.zeros(num_symbols)
y = np.zeros(num_symbols)

for i in range(N):
    alpha = np.random.uniform(-np.pi, np.pi)
    phi = np.random.uniform(-np.pi, np.pi)

    amplitude_x = np.random.randn()
    amplitude_y = np.random.randn()

    phase = 2 * np.pi * fd * t * np.cos(alpha) + phi

    x += amplitude_x * np.cos(phase)
    y += amplitude_y * np.sin(phase)

h = (x + 1j * y) / np.sqrt(N)

h = h / np.sqrt(np.mean(np.abs(h)**2))

#Noisy channel
sn = x_symbols + n
r = (h * x_symbols) + n 

#Plot
fig, (g1, g2, g3) = plt.subplots(1, 3, figsize=(SIZE_X, SIZE_Y))
fig.text(0.02,0.98, f"EbN0 = {SNR}dB", ha="left", va="top", fontsize=20)

def konstalacia(okno, nazov):
    okno.title.set_text(nazov)
    okno.grid()
    okno.set_xlabel("I")
    okno.set_ylabel("Q")
    okno.set_xlim(-2, 2)
    okno.set_ylim(-2, 2)
    okno.axhline(y=0, lw=1, color='k')
    okno.axvline(x=0, lw=1, color='k')

konstalacia(g1, "QPSK")
konstalacia(g2, "QPSK + AWGN")
konstalacia(g3, "QPSK + AWGN + Rayleigh")

g1.plot(np.real(x_symbols), np.imag(x_symbols), '.')

g2.plot(np.real(sn), np.imag(sn), 'r.')
g2.plot(np.real(x_symbols), np.imag(x_symbols), '.')

g3.plot(np.real(r), np.imag(r), "g.")
g3.plot(np.real(x_symbols), np.imag(x_symbols), '.')

plt.show()
