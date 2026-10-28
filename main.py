import numpy as np
import matplotlib.pyplot as plt
import sys

#Premenne
num_symbols = 1000
SNR = float(sys.argv[1]) #dB
M = 4 #pocet mod stavov
k = np.log2(M) #pocet bitov na symbol
#-------------------------------

#random bits QPSK
x_int = np.random.randint(0, M, num_symbols)

#Mod QPSK
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

#Noisy channel
r = x_symbols + n

#Plot
fig, (g1, g2) = plt.subplots(1, 2, figsize=(12, 6))
fig.text(0.02,0.98, f"SNR = {SNR}dB", ha="left", va="top", fontsize=12)

g1.grid()
g1.title.set_text("QPSK")
g1.set_xlabel("I")
g1.set_ylabel("Q")
g1.set_xlim(-2, 2)
g1.set_ylim(-2, 2)
g1.plot(np.real(x_symbols), np.imag(x_symbols), '.')

g2.grid()
g2.title.set_text("QPSK + AWGN")
g2.set_xlabel("I")
g2.set_ylabel("Q")
g2.set_xlim(-2, 2)
g2.set_ylim(-2, 2)
g2.plot(np.real(r), np.imag(r), '.')



plt.show()
