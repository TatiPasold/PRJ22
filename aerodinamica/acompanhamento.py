# Importar os arquivos
import design_tools_pinguim as dt
import aux_tools as at
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Definir uma variavel chamada aircraft que recebe o output da funcao my_aircraft

aircraft = dt.my_aircraft()
pprint(aircraft)
new_dimensions = dt.geometry(aircraft)
aircraft['dimensions'].update(new_dimensions)

# Cruzeiro
Mach = 0.77
altitude = 11000
n_engines_failed = 0
flap_def = 0.0
slat_def = 0.0
lg_down = 0
h_ground = 0
W0_guess = 0
cruise_aerodynamic_data, CLmax_cruise = dt.aerodynamics(aircraft, Mach, altitude, n_engines_failed, flap_def, slat_def, lg_down, h_ground, W0_guess)

print('\n')
print("=========================================")
print("Cruzeiro Aerodinâmico")
print("=========================================")
for k, v in cruise_aerodynamic_data.items():
    print(f"{k}: {float(v):.4f}")
print(f"CLmax: {float(CLmax_cruise):.4f}")

# CD0 por enflechamento

# CL/CD por enflechamento

# Mach por enflechamento

# CD0 por Mach

CD0 = np.zeros((5, 22))
CLmax = np.zeros((5, 1))

sweeps = [20, 25, 30, 35, 40]
M = [0.6 , 0.7, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9]

for sweep in sweeps:
    for i in range(len(M)):
        aircraft['geo_param']['wing']['sweep'] = sweep*np.pi/180
        new_dimensions = dt.geometry(aircraft)
        aircraft['dimensions'].update(new_dimensions)
        aerodynamic_data, clmax = dt.aerodynamics(aircraft, M[i], altitude, n_engines_failed, flap_def, slat_def, lg_down, h_ground, W0_guess)
        CD0[sweeps.index(sweep), i] = aerodynamic_data['CD0']
        CLmax[sweeps.index(sweep), 0] = float(clmax)

# Plote de CD0 como função de M para cada sweep
plt.figure(figsize=(10, 6))
colors = sns.color_palette("viridis", len(sweeps))
for i in range(len(sweeps)):
    plt.plot(M, CD0[i], label=f'Sweep {sweeps[i]}°', color=colors[i])
plt.xlabel('Mach')
plt.ylabel('CD0')
plt.title('CD0 vs Mach para diferentes ângulos de enflechamento')
plt.legend()
plt.grid()
plt.savefig('CD0_vs_Mach.png')

# CLmax por enflechamento

plt.figure(figsize=(10, 6))
color = sns.color_palette("viridis", 1)
for i in range(len(sweeps)):
    plt.plot(sweeps, CLmax, color=color[0])
plt.xlabel('Sweep (graus)')
plt.ylabel('CLMAX')
plt.title('CLMAX vs Sweep')
plt.grid()
plt.savefig('CLmax_vs_sweep.png')

# Para Mach = 0.77, CD0 por sweep
sweeps = [20, 25, 30, 35, 40]
M = 0.77
CD0s = []
for sweep in sweeps:
    aircraft['geo_param']['wing']['sweep'] = sweep*np.pi/180
    new_dimensions = dt.geometry(aircraft)
    aircraft['dimensions'].update(new_dimensions)
    aerodynamic_data, clmax = dt.aerodynamics(aircraft, M, altitude, n_engines_failed, flap_def, slat_def, lg_down, h_ground, W0_guess)
    CD0= aerodynamic_data['CD0']
    CD0s.append(CD0)

plt.figure(figsize=(10, 6))
plt.plot(sweeps, CD0s)
plt.xlabel('Sweep (graus)')
plt.ylabel('CD0')
plt.title('CD0 vs Sweep')
plt.grid()
plt.savefig('CD0_vs_sweep.png')

# Dados de pouso

# Mach = 0.2
# altitude = 0
# n_engines_failed = 0
# flap_def = 40*np.pi/180
# slat_def = 0.0
# lg_down = 1
# h_ground = 10.67

# # Polares de arrastos
# CLmin = -0.5


# flap_types = ['plain', 'slotted', 'fowler', 'double slotted', 'triple slotted']

# aircraft['geo_param']['wing']['sweep'] = 17.45*np.pi/180
# new_dimensions = dt.geometry(aircraft)
# aircraft['dimensions'].update(new_dimensions)

# plt.figure(figsize=(10, 6))
# colors = sns.color_palette("viridis", 5)


# for flap_type in flap_types:
#     aircraft['data']['flap']['type'] = flap_type
#     new_dimensions = dt.geometry(aircraft)
#     aircraft['dimensions'].update(new_dimensions)

#     landing_aerodynamic_data, CLmax_landing = dt.aerodynamics(aircraft, Mach, altitude, n_engines_failed, flap_def, slat_def, lg_down, h_ground, W0_guess)

#     CD0_landing = landing_aerodynamic_data['CD0']
#     print(CD0_landing)
#     K_landing = landing_aerodynamic_data['K']

#     CL_landing = np.linspace(CLmin, CLmax_landing, 100)
#     CD= CD0_landing + K_landing * CL_landing**2

#     plt.plot(CL_landing, CD, label=f'Tipo do flap:{flap_type}', color= colors[flap_types.index(flap_type)])

# plt.xlabel('Coeficiente de Sustentação (CL)')
# plt.ylabel('Coeficiente de Arrasto (CD)')
# plt.title('Polares de Arrasto para Pouso variando o tipo de flap')
# plt.legend()
# plt.grid()
# plt.show()



    