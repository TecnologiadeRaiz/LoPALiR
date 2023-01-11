import datetime
import os
import sys

sys.path.append(os.getcwd())

#antena = os.path.split(os.getcwd())[-1]
antena = "esoterica-vs-doblebiquadmimo"

nodo_tx = "testantena"
nodo_rx = "ql-graciela-bbone"
radio = 1
modo = "adhoc"
mcs_bitrate = 0

fecha = datetime.date.today().isoformat()

# borramos 140 y 165 porque no generan resultados, al menos en ql-graciela-bbone -- testantena
canales = [36,40,44,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161]
txpower = 21

netperf_duration = 30
cantidad_mediciones = 100

try:
    from local_config import *
except:
    exit("Falta local_test_config.py en la carpeta local para configurar el experimento.")
