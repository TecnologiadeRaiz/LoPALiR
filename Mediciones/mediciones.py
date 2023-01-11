#! /usr/bin/python3
# Importamos librerías necesarias
import logging
import subprocess
import time
import datetime
import test_config as cfg

# seteamos la configuración de loggin para que muestre los datos que queremos ver
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

logging.info("Iniciando")

# buscamos los nombres de los nodos en el archivo local config.py
nodos = [cfg.nodo_rx, cfg.nodo_tx]

# configuramos radio, canal y potencia de transmisión en ambos nodos y esperamos los cambios
for canal in cfg.canales:

    logging.info("Configurando")
    for nodo in nodos:
        cmd = """ssh root@{} "uci set wireless.radio{}.channel={}; 
                 uci set wireless.radio{}.txpower={}; uci changes;
                 uci commit wireless; sleep 3 && wifi &" """.format(nodo, cfg.radio, canal, cfg.radio, cfg.txpower)
        logging.info("ejecutando comando: {}".format(cmd))
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
        print("salida: {}".format(proc)) #ex loggin.info

    time.sleep(25)

# configuramos modulación MCS0 en ambos nodos, para no tener niveles intermedios de potencia
    for nodo in nodos:
        cmd = """ssh root@{} "iw wlan{}-{} set bitrates ht-mcs-5 {}" """.format(nodo, cfg.radio, cfg.modo, cfg.mcs_bitrate)
        logging.info("ejecutando comando: {}".format(cmd))
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
        print("salida: {}".format(proc)) #ex loggin.info
 
    time.sleep(7)
   
# Tomamos n cantidad de mediciones según indique el archivo local config.py
    mediciones = []
    mediciones_file = open("{}_{}_{}--{}_ch{}_{}db.txt".format(cfg.antena, cfg.fecha, cfg.nodo_rx, cfg.nodo_tx, canal, cfg.txpower), "w+")

    logging.info("Midiendo")
    for n in range(cfg.cantidad_mediciones):
        cmd = """ssh root@{} "iw wlan{}-{} station dump | mac2bat | grep -i {} -A 11" """.format(cfg.nodo_rx, cfg.radio, cfg.modo, cfg.nodo_tx.replace("-","_"))
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, encoding="utf-8")
#        print("salida: {}".format(proc)) #exloggin.info
#        print(proc.stdout)
        mediciones.append(proc.stdout)
        time.sleep(1)

# se guarda un archivo por cada canal medido
    mediciones_str = "\n".join(mediciones)
    print(mediciones_str)
    mediciones_file.write(mediciones_str)
    mediciones_file.close()
    

