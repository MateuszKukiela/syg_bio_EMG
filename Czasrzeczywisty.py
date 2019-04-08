from obci_cpp_amplifiers.amplifiers import TmsiCppAmplifier
import numpy as np
from pynput.mouse import Button, Controller
import scipy.signal as ss
import numpy as np
import matplotlib.pyplot as plt
from  scipy.signal import butter, buttord     # funkcje do projektowania filtrów  
from  scipy.signal import lfilter, filtfilt # funkcje do aplikowania filtrów
import time
mouse = Controller()
 
def click():
	mouse.press(Button.left)
	mouse.release(Button.left)


amps = TmsiCppAmplifier.get_available_amplifiers('usb')
amp = TmsiCppAmplifier(amps[0])
 
amp.sampling_rate = 2048
 
amp.start_sampling()
gains = np.array(amp.current_description.channel_gains)
offsets = np.array(amp.current_description.channel_offsets)

Fs = 2048
def samples_to_microvolts(samples):  # z jednostek wzmacniacza do mikrowoltów
    return samples * gains + offsets
 
stopper =0
tablica = np.zeros(30000)
while True:
    # 30 próbek w pakiecie, nieodebrane próbki się bufurują i można odebrać je później
    if stopper > 0:
       stopper = stopper -1
    packet = amp.get_samples(30)
    tab = (samples_to_microvolts(packet.samples))
    syg = tab[:,3]-tab[:,4]
    tablica[0:-30]=tablica[30:]
    tablica[-30:]=syg
    [b,a] = butter(5, 20/(Fs/2), btype = 'highpass')
    tablica_filt = filtfilt(b,a,tablica)
    if np.abs(np.mean(tablica_filt[-30:])) > 200 and stopper == 0:
       click()
       stopper = 20
    print(stopper)
    print(np.mean(tablica_filt[-30:]))
    print(packet.ts[0])
    print(packet.samples.shape, amp.current_description.channel_names)
