# Importar os arquivos
import design_tools as dt
import aux_tools as at
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Configurações de estilo consistentes para todos os gráficos
plt.style.use('seaborn-v0_8-pastel')
sns.set_palette("viridis")
plt.rcParams.update({
    'figure.autolayout': True,
    'axes.titlesize': 22,
    'axes.labelsize': 20,
    'xtick.labelsize': 18,
    'ytick.labelsize': 18,
    'legend.fontsize': 18,
    'legend.title_fontsize': 18,
    'figure.figsize': (14, 10)
})

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

# Mostrar o valor da area de asa
print('\n')
print(f"A área da asa é S = {aircraft['geo_param']['wing']['S']}")

# Mostrar o valor de duas variaveis diferentes no mesmo print
taper_h = aircraft['geo_param']['EH']['taper']
ARw = aircraft['geo_param']['wing']['AR']

print(f"O afilamento da EH é: {taper_h} e o AR da asa é: {ARw}")

new_dimensions = dt.geometry(aircraft)
aircraft['dimensions'].update(new_dimensions)
# at.plot3d(aircraft)

# ------------------------------------------------------------------------------------------------------------
# Caso teste

Mach = 0.3
altitude = 10.668000000000001
n_engines_failed = 1
flap_def = 0.3490658503988659
slat_def = 0.0
lg_down = 1
h_ground = 10.668000000000001
W0_guess = 422712.9

aerodynamic_data, CLmax = dt.aerodynamics(
    aircraft, Mach, altitude, n_engines_failed, flap_def, slat_def, lg_down, h_ground, W0_guess)

print('\n')
print("=========================================")
print("Dados Aerodinâmicos")
print("=========================================")
for k, v in aerodynamic_data.items():
    print(f"{k}: {float(v):.4f}")
print(f"CLmax: {float(CLmax):.4f}")

# ------------------------------------------------------------------------------------------------------------

# Alterando o enflechamento da asa
aircraft['geo_param']['wing']['sweep'] = 20*np.pi/180
new_dimensions = dt.geometry(aircraft)
aircraft['dimensions'].update(new_dimensions)

aerodynamic_data, CLmax = dt.aerodynamics(
    aircraft, Mach, altitude, n_engines_failed, flap_def, slat_def, lg_down, h_ground, W0_guess)

print('\n')
print("=========================================")
print("Dados Aerodinâmicos com enflechamento")
print("=========================================")
for k, v in aerodynamic_data.items():
    print(f"{k}: {float(v):.4f}")
print(f"CLmax: {float(CLmax):.4f}")

# Gráfico de pizza com as contribuições de Swet

Swet_w = aerodynamic_data.get('Swet_w', 0)
Swet_h = aerodynamic_data.get('Swet_h', 0)
Swet_v = aerodynamic_data.get('Swet_v', 0)
Swet_f = aerodynamic_data.get('Swet_f', 0)
Swet_n = aerodynamic_data.get('Swet_n', 0)

Swet = Swet_w + Swet_h + Swet_v + Swet_f + Swet_n

# Dados
labels = ['Asa', 'EH', 'EV', 'Fuselagem', 'Nacele']
sizes = [Swet_w, Swet_h, Swet_v, Swet_f, Swet_n]
total = sum(sizes)

# Paleta de cores personalizada
colors = sns.color_palette("viridis")[0:5]
explode = (0.05, 0.05, 0.05, 0.05, 0.05)

wedges, texts, autotexts = plt.pie(
    sizes,
    colors=colors,
    explode=explode,
    autopct=lambda p: f'{p:.1f}%',
    startangle=140,
    wedgeprops={'edgecolor': 'black', 'linewidth': 0.4},
    textprops={'fontsize': 18, 'color': 'white'},
)

# Legenda
plt.legend(
    wedges,
    [f'{l} ({s:.1f} m²)' for l, s in zip(labels, sizes)],
    title="Componentes",
    title_fontsize=17,
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=18
)

# Título
# plt.title(f'Contribuição de cada componente para a área molhada total\nÁrea molhada total: {total:.2f} m²', fontsize=22, pad=20, fontweight='bold')

plt.setp(autotexts, size=18)
plt.tight_layout()
plt.savefig('área molhada.jpg', dpi=500, bbox_inches='tight')
# plt.show()

# ------------------------------------------------------------------------------------------------------------

# Matriz de CD0
CD0 = np.zeros((5, 22))
CLmax = np.zeros((5, 1))

sweeps = [20, 25, 30, 35, 40]

M = [0.6, 0.7, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79,
     0.8, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.9]

for sweep in sweeps:
    for i in range(len(M)):
        aircraft['geo_param']['wing']['sweep'] = sweep*np.pi/180
        new_dimensions = dt.geometry(aircraft)
        aircraft['dimensions'].update(new_dimensions)
        aerodynamic_data, clmax = dt.aerodynamics(
            aircraft, M[i], altitude, n_engines_failed, flap_def, slat_def, lg_down, h_ground, W0_guess)
        CD0[sweeps.index(sweep), i] = aerodynamic_data['CD0']
        CLmax[sweeps.index(sweep), 0] = float(clmax)

plt.figure()
norm = plt.Normalize(min(sweeps), max(sweeps))
cmap = sns.color_palette("viridis", as_cmap=True)

for i, sweep in enumerate(sweeps):
    plt.plot(M, CD0[i], label=f'{sweep}°',
             color=cmap(norm(sweep)), linewidth=3)

plt.xlabel('Número de Mach', fontweight='bold')
plt.ylabel(r'Coeficiente de arrasto ($C_{D_0}$)', fontweight='bold')
# plt.title('Variação do arrasto parasita com o número de Mach\npara diferentes ângulos de enflechamento', pad=20, fontweight='bold')
plt.legend(title='Ângulo de\nEnflechamento',
           loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('arrasto parasita.jpg', dpi=500, bbox_inches='tight')
# plt.show()

# ------------------------------------------------------------------------------------------------------------

print('\n')
print("=========================================")
print("CLmax para os diferentes ângulos de enflechamento")
print("=========================================")
for i, sweep in enumerate(sweeps):
    print(f"Ângulo de enflechamento: {sweep}° -> CLmax: {CLmax[i][0]:.4f}")

# CLmax vs Sweep
plt.figure()
plt.plot(sweeps, CLmax, color='#440154', linewidth=3, marker='o', markersize=8)

plt.xlabel('Ângulo de Enflechamento (graus)', fontweight='bold')
plt.ylabel(
    r'Coeficiente de Sustentação Máximo ($CL_{max}$)', fontweight='bold')
# plt.title('Efeito do ângulo de enflechamento no coeficiente\nde sustentação máximo', pad=20, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('clmax.jpg', dpi=500, bbox_inches='tight')
# plt.show()

# ------------------------------------------------------------------------------------------------------------

# Retornando a aeronave padrão
aircraft = dt.default_aircraft()
aircraft['geo_param']['wing']['sweep'] = 20*np.pi/180
# Atualizando as dimensões
new_dimensions = dt.geometry(aircraft)
aircraft['dimensions'].update(new_dimensions)

# Cruzeiro
Mach = 0.75
altitude = 11000
n_engines_failed = 0
flap_def = 0.0
slat_def = 0.0
lg_down = 0
h_ground = 0
cruise_aerodynamic_data, CLmax_cruise = dt.aerodynamics(
    aircraft, Mach, altitude, n_engines_failed, flap_def, slat_def, lg_down, h_ground, W0_guess)

print('\n')
print("=========================================")
print("Cruzeiro Aerodinâmico")
print("=========================================")
for k, v in cruise_aerodynamic_data.items():
    print(f"{k}: {float(v):.4f}")
print(f"CLmax: {float(CLmax_cruise):.4f}")

# Decolagem
Mach = 0.2
altitude = 0
n_engines_failed = 0
flap_def = 20*np.pi/180
slat_def = 0.0
lg_down = 1
h_ground = 10.67
takeoff_aerodynamic_data, CLmax_takeoff = dt.aerodynamics(
    aircraft, Mach, altitude, n_engines_failed, flap_def, slat_def, lg_down, h_ground, W0_guess)

print('\n')
print("=========================================")
print("Decolagem Aerodinâmica")
print("=========================================")
for k, v in takeoff_aerodynamic_data.items():
    print(f"{k}: {float(v):.4f}")
print(f"CLmax: {float(CLmax_takeoff):.4f}")

# Pouso
Mach = 0.2
altitude = 0
n_engines_failed = 0
flap_def = 40*np.pi/180
slat_def = 0.0
lg_down = 1
h_ground = 10.67
landing_aerodynamic_data, CLmax_landing = dt.aerodynamics(
    aircraft, Mach, altitude, n_engines_failed, flap_def, slat_def, lg_down, h_ground, W0_guess)

print('\n')
print("=========================================")
print("Pouso Aerodinâmico")
print("=========================================")
for k, v in landing_aerodynamic_data.items():
    print(f"{k}: {float(v):.4f}")
print(f"CLmax: {float(CLmax_landing):.4f}")

# Polares de arrastos
CLmin = -0.5

# Cruzeiro
CD0_cruise = cruise_aerodynamic_data['CD0']
K_cruise = cruise_aerodynamic_data['K']
CL_cruise = np.linspace(CLmin, CLmax_cruise, 100)
CD_cruise = CD0_cruise + K_cruise * CL_cruise**2
L_D_cruise = CL_cruise / CD_cruise
L_D_cruise_max = np.max(L_D_cruise)

# Decolagem
CD0_takeoff = takeoff_aerodynamic_data['CD0']
K_takeoff = takeoff_aerodynamic_data['K']
CL_takeoff = np.linspace(CLmin, CLmax_takeoff, 100)
CD_takeoff = CD0_takeoff + K_takeoff * CL_takeoff**2
L_D_takeoff = CL_takeoff / CD_takeoff
L_D_takeoff_max = np.max(L_D_takeoff)

# Pouso
CD0_landing = landing_aerodynamic_data['CD0']
K_landing = landing_aerodynamic_data['K']
CL_landing = np.linspace(CLmin, CLmax_landing, 100)
CD_landing = CD0_landing + K_landing * CL_landing**2
L_D_landing = CL_landing / CD_landing
L_D_landing_max = np.max(L_D_landing)

plt.figure()
colors = sns.color_palette("viridis", 3)

plt.plot(CD_cruise, CL_cruise,
         label=f'Cruzeiro', linewidth=3, color=colors[0])
plt.plot(CD_takeoff, CL_takeoff,
         label=f'Decolagem', linewidth=3, color=colors[1])
plt.plot(CD_landing, CL_landing,
         label=f'Pouso', linewidth=3, color=colors[2])

plt.ylabel(r'Coeficiente de Sustentação ($C_L$)', fontweight='bold')
plt.xlabel(r'Coeficiente de Arrasto ($C_D$)', fontweight='bold')
# plt.title('Polares de Arrasto para Diferentes Configurações de Voo', pad=20, fontweight='bold')
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('polares de arrasto.jpg', dpi=500, bbox_inches='tight')
# plt.show()

# ------------------------------------------------------------------------------------------------------------

# Valores máximos de L/D
print('\n')
print("=========================================")
print("Valores máximos de L/D")
print("=========================================")
print(f"Cruzeiro: {L_D_cruise_max:.4f}")
print(f"Decolagem: {L_D_takeoff_max:.4f}")
print(f"Pouso: {L_D_landing_max:.4f}")
