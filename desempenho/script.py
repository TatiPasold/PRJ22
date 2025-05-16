# Importar os arquivos
import design_tools as dt
import aux_tools as at
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

# Definir uma variavel chamada aircraft que recebe o output da funcao default_aircraft
aircraft = dt.default_aircraft()

# Mostrar o conteudo da variavel
print("=========================================")
print("Aeronave padrão")
print("=========================================")
pprint(aircraft)

# Acessar apenas o sub-dicionario dos parametros geometricos da asa:
print('\n')
print("=========================================")
print("Parâmetros geométricos da asa")
print("=========================================")
pprint(aircraft['geo_param']['wing'])

new_dimensions = dt.geometry(aircraft)
aircraft['dimensions'].update(new_dimensions)

W0_guess = 422712.90000000002328
T0_guess = 125600
TO_flap_def = 0.34906585039887
LD_flap_def = 0.69813170079773
TO_slat_def = 0.0
LD_slat_def = 0.0
h_ground = 10.668
altitude_cruise = 11000
Mach_cruise = 0.77
range_cruise = 2390000
loiter_time = 2700
altitude_altcruise = 4572
Mach_altcruise = 0.4
range_altcruise = 370000
altitude_takeoff = 0.0
distance_takeoff = 1520.0
altitude_landing = 0.0
distance_landing = 1520.0
MLW_frac = 0.84

W0 , We , Wf , xcg_e , T0 , T0vec , S_wlan = dt.thrust_matching(
    aircraft, W0_guess, T0_guess, TO_flap_def, LD_flap_def, TO_slat_def, LD_slat_def,
    h_ground, altitude_cruise, Mach_cruise, range_cruise, loiter_time,
    altitude_altcruise, Mach_altcruise, range_altcruise,
    altitude_takeoff, distance_takeoff,
    altitude_landing, distance_landing,
    MLW_frac
)

print('\n')
print("=========================================")
print("Resultados do caso de teste")
print("=========================================")
print("Peso inicial: ", W0)
print("Peso de decolagem: ", We)
print("Peso de combustível: ", Wf)
print("Centro de gravidade: ", xcg_e)
print("Thrust: ", T0)
print("Thrust vector: ", T0vec)
print("S_wlan: ", S_wlan)

Sw = np.arange(80, 140, 5)

T01 = []
T02 = []
T03 = []
T04 = []
T05 = []
T06 = []
T07 = []
T08 = []
T0vecs = []

plt.figure(figsize=(10, 6))
colors = sns.color_palette("pastel", 8)

for S in Sw:
    aircraft['geo_param']['wing']['S'] = S
    new_dimensions = dt.geometry(aircraft)
    aircraft['dimensions'].update(new_dimensions)

    W0 , We , Wf , xcg_e , T0 , T0vec , S_wlan = dt.thrust_matching(
        aircraft, W0_guess, T0_guess, TO_flap_def, LD_flap_def, TO_slat_def, LD_slat_def,
        h_ground, altitude_cruise, Mach_cruise, range_cruise, loiter_time,
        altitude_altcruise, Mach_altcruise, range_altcruise,
        altitude_takeoff, distance_takeoff,
        altitude_landing, distance_landing,
        MLW_frac
    )

    T01.append(T0vec[0])
    T02.append(T0vec[1])
    T03.append(T0vec[2])
    T04.append(T0vec[3])
    T05.append(T0vec[4])
    T06.append(T0vec[5])
    T07.append(T0vec[6])
    T08.append(T0vec[7])
    T0vecs.append(T0vec)

plt.plot(Sw, T01, label=r'$T_{0, TO}$', color=colors[0])
plt.plot(Sw, T02, label=r'$T_{0, cruise}$', color=colors[1])
plt.plot(Sw, T03, label=r'$T_{0, FAR 25.111}$', color=colors[2])
plt.plot(Sw, T04, label=r'$T_{0, FAR 25.121a}$', color=colors[3])
plt.plot(Sw, T05, label=r'$T_{0, FAR 25.121b}$', color=colors[4])
plt.plot(Sw, T06, label=r'$T_{0, FAR 25.121c}$', color=colors[5])
plt.plot(Sw, T07, label=r'$T_{0, FAR 25.119}$', color=colors[6])
plt.plot(Sw, T08, label=r'$T_{0, FAR 25.121d}$', color=colors[7])
plt.legend()
plt.xlabel('Wing area (m²)')
plt.ylabel('Thrust vector (N)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('thrust_vector_vs_wing_area.png')

aircraft = dt.default_aircraft()
new_dimensions = dt.geometry(aircraft)
aircraft['dimensions'].update(new_dimensions)

sweeps = np.arange(20, 40, 5)
sweeps = sweeps*np.pi/180

T0s = []
S_wlans = []

for sweep in sweeps:
    aircraft['geo_param']['wing']['sweep'] = sweep
    new_dimensions = dt.geometry(aircraft)
    aircraft['dimensions'].update(new_dimensions)

    W0 , We , Wf , xcg_e , T0 , T0vec , S_wlan = dt.thrust_matching(
        aircraft, W0_guess, T0_guess, TO_flap_def, LD_flap_def, TO_slat_def, LD_slat_def,
        h_ground, altitude_cruise, Mach_cruise, range_cruise, loiter_time,
        altitude_altcruise, Mach_altcruise, range_altcruise,
        altitude_takeoff, distance_takeoff,
        altitude_landing, distance_landing,
        MLW_frac
    )

    T0s.append(T0)
    S_wlans.append(S_wlan)

plt.figure(figsize=(10, 6))
plt.plot(sweeps*180/np.pi, T0s, label=r'$T_{0}$', color=colors[0])
plt.xlabel('Sweep (degrees)')
plt.ylabel('Thrust (N)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('thrust_vs_aspect_ratio.png')

plt.figure(figsize=(10, 6))
plt.plot(sweeps*180/np.pi, S_wlans, label=r'$S_{wlan}$', color=colors[1])
plt.xlabel('Sweep (degrees)')
plt.ylabel('Wing area (m²)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('wing_area_vs_aspect_ratio.png')