# Importar os arquivos
import design_tools as dt
import aux_tools as at
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

# Padronizando o tamanho da fontes

plt.rcParams.update({
    'font.size': 12,             # Tamanho da fonte global
    'axes.titlesize': 12,        # Título do gráfico
    'axes.labelsize': 12,        # Labels dos eixos
    'xtick.labelsize': 12,       # Labels do eixo x
    'ytick.labelsize': 12,       # Labels do eixo y
    'legend.fontsize': 12,       # Legenda
    'figure.titlesize': 12       # Título geral da figura
})

# Definir uma variavel chamada aircraft que recebe o output da funcao default_aircraft
aircraft = dt.default_aircraft()

# Mostrar o conteudo da variavel
print("=========================================")
print("Aeronave padrão")
print("=========================================")
pprint(aircraft)

new_dimensions = dt.geometry(aircraft)
aircraft['dimensions'].update(new_dimensions)

# Parametros de teste

gravity = 9.81
W0_guess = 43090 * gravity
T0_guess = 125600
Mach_cruise = 0.77
altitude_cruise = 11000
range_cruise = 2390000.00000000000000
Mach_altcruise = 0.4
range_altcruise = 370000
altitude_altcruise = 4572
loiter_time = 2700
altitude_takeoff = 0
distance_takeoff = 1520
TO_flap_def = 0.34906585039887
TO_slat_def = 0
altitude_landing = 0
distance_landing = 1520
LD_flap_def = 0.69813170079773
LD_slat_def = 0
MLW_frac = 0.84

W0, Wf, T0, deltaS_wlan, SM_fwd, SM_aft, b_tank_b_w, frac_nlg_fwd, frac_nlg_aft, alpha_tipback, alpha_tailstrike, phi_overturn = dt.analyze(aircraft , W0_guess , T0_guess ,
Mach_cruise , altitude_cruise , range_cruise ,
Mach_altcruise , range_altcruise , altitude_altcruise ,
loiter_time ,
altitude_takeoff , distance_takeoff , TO_flap_def , TO_slat_def ,
altitude_landing , distance_landing , LD_flap_def , LD_slat_def ,
MLW_frac)

print('\n')
print("=========================================")
print("Resultados do caso de teste")
print("=========================================")
print(f"Peso inicial: {W0:.2f} N")
print(f"Peso final: {Wf:.2f} N")
print(f"Empuxo inicial: {T0:.2f} N")
print(f"Delta S_wlan: {deltaS_wlan:.2f} m²")
print(f"SM_fwd: {SM_fwd:.2f}")
print(f"SM_aft: {SM_aft:.2f}")
print(f"b_tank_b_w: {b_tank_b_w:.2f} m")
print(f"Frac_nlg_fwd: {frac_nlg_fwd:.2f}")
print(f"Frac_nlg_aft: {frac_nlg_aft:.2f}")
print(f"Alpha_tipback: {alpha_tipback:.2f} rad")
print(f"Alpha_tailstrike: {alpha_tailstrike:.2f} rad")
print(f"Phi_overturn: {phi_overturn:.2f} rad")

# Primeiro vamos variar os enflechamentos

sweeps = np.arange(0, 45, 5)
sweeps = np.radians(sweeps)
sm_afts = []
sm_fwds = []

for sweep in sweeps:
    aircraft['geo_param']['wing']['sweep'] = sweep
    new_dimensions = dt.geometry(aircraft)
    aircraft['dimensions'].update(new_dimensions)

    W0, Wf, T0, deltaS_wlan, SM_fwd, SM_aft, b_tank_b_w, frac_nlg_fwd, frac_nlg_aft, alpha_tipback, alpha_tailstrike, phi_overturn = dt.analyze(
        aircraft, W0_guess, T0_guess,
        Mach_cruise, altitude_cruise, range_cruise,
        Mach_altcruise, range_altcruise, altitude_altcruise,
        loiter_time,
        altitude_takeoff, distance_takeoff, TO_flap_def, TO_slat_def,
        altitude_landing, distance_landing, LD_flap_def, LD_slat_def,
        MLW_frac
    )

    sm_fwds.append(SM_fwd)
    sm_afts.append(SM_aft)

# Plot de sm_fwd e sm_aft em funcao do sweep

colors = sns.color_palette("viridis", 2)

plt.figure(figsize=(10, 6))
plt.plot(sm_fwds, np.degrees(sweeps), label='SM Fwd', color =colors[0])
plt.plot(sm_afts, np.degrees(sweeps), label='SM Aft', color = colors[1])

# sm_fwd <= 0.30
plt.axvline(x=0.30, linestyle='--', label=r'SM Fwd Limite ($\leq 0.30$)', color = colors[0])

# sm_aft >= 0.05
plt.axvline(x=0.05, linestyle='--', label=r'SM Aft Limite ($\geq 0.05$)', color = colors[1])

plt.xlabel('Margem Estática (SM)')
plt.ylabel('Enflechamento (graus)')

plt.grid(linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('sm_vs_sweep.png', dpi=300)