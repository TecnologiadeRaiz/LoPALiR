#! /usr/bin/python3

# SPDX-FileCopyrightText: 2023 Tecnología de Raíz <tecnologiaderaiz@disroot.org>
#
# SPDX-License-Identifier: CC-BY-NC-4.0

import glob
import test_config as cfg
import matplotlib.pyplot as plt
import subprocess
import pickle

promedios = {}
canales_con_mediciones = []
promedios_signal = []
promedios_chain1 = []
promedios_chain2  = []

print(cfg.antena)
for canal in cfg.canales:
    archivos = glob.glob("./{}*ch{}_{}db.txt".format(cfg.antena, canal, cfg.txpower))
    signal = []
    chain1 = []
    chain2  = []

    if len(archivos) != 1:
        exit("El script espera que haya un archivo por cada canal y potencia.")

    cmd = """cat {} | grep "Station {}_wlan{}_{}" -A 11 | grep "signal:"  """.format(archivos[0], cfg.nodo_tx.replace('-', '_'), cfg.radio, cfg.modo)
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, encoding="utf-8")

    if proc.stdout.strip() == '':
        print("No hay  mediciones para el canal {}. Descartando el canal.".format(canal))
        continue

    data = proc.stdout.strip().split("\n")
    if len(data)!= cfg.cantidad_mediciones:
        print("No hay {} mediciones para el canal {}. Hay sólo {}.".format(cfg.cantidad_mediciones, canal, len(data)))

    for line in data:
        if line:
            # recortamos de forma muy brutal los datos
            signal.append(float(line.split()[1].strip()))
            chain1.append(float(line.split()[2][1:][:-1]))
            chain2.append(float(line.split()[3][:-1]))
            
#    promedios[str(canal)] = (sum(signal)/len(signal), sum(chain1)/len(chain1), sum(chain2)/len(chain2))
    canales_con_mediciones.append(str(canal))
    promedios_signal.append(sum(signal)/len(signal))
    promedios_chain1.append(sum(chain1)/len(chain1))
    promedios_chain2.append(sum(chain2)/len(chain2))

plt.plot(canales_con_mediciones, promedios_signal, label=("señal"))
plt.plot(canales_con_mediciones, promedios_chain1, label=("chain 1"))
plt.plot(canales_con_mediciones, promedios_chain2, label=("chain 2"))

plt.title("{}\n txpower: {}db".format(cfg.antena, cfg.txpower))
plt.xlabel("Canal")
plt.ylabel("Señal")
plt.grid()
plt.legend()
plt.savefig("{}_{}.pdf".format(cfg.antena, cfg.fecha))
plt.show()

pickle_file = open("{}_{}.pkl".format(cfg.antena, cfg.fecha), "wb")
pickle.dump(promedios_signal, pickle_file)
pickle_file.close()

