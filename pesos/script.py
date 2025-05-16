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

# Casos de teste

T0_guess = 125600
W0_guess = 422712.9
altitude_cruise = 11000.0000
Mach_cruise = 0.7700000
range_cruise = 2390000.00000
loiter_time = 2700.00000
altitude_altcruise = 4572.00000
Mach_altcruise = 0.40000000
range_altcruise = 370000.00000

W0, We, Wf, Wf_cruise, xcg_e, weightsvec = dt.weight(
    aircraft, W0_guess, T0_guess, altitude_cruise, Mach_cruise, range_cruise, loiter_time, altitude_altcruise, Mach_altcruise, range_altcruise)

print('\n')
print("=========================================")
print("Resultados do caso de teste")
print("=========================================")
print("Peso inicial: ", W0)
print("Peso de decolagem: ", We)
print("Peso de combustível: ", Wf)
print("Peso de combustível para cruzeiro: ", Wf_cruise)
print("Centro de gravidade: ", xcg_e)
print("Vetor de pesos: ", weightsvec)

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

# Gráfico de pizza considerando  carga-paga, tripulação, combustível e peso vazio

# Dados

W_payload = aircraft['weights']['W_payload']
W_crew = aircraft['weights']['W_crew']

labels = ['Carga-paga', 'Tripulação', 'Combustível', 'Peso vazio']
sizes = [W_payload, W_crew, Wf, We]
total = sum(sizes)

# Paleta de cores personalizada
colors = sns.color_palette("viridis")[0:4]
explode = (0.05, 0.05, 0.05, 0.05)

wedges, texts, autotexts = plt.pie(
    sizes,
    colors=colors,
    explode=explode,
    autopct=lambda p: f'{p:.1f}%',
    startangle=140,
    wedgeprops={'edgecolor': 'black', 'linewidth': 0.4},
    textprops={'fontsize': 20, 'color': 'black'},
    pctdistance=1.1,
)

# Legenda
plt.legend(
    wedges,
    [f'{l} ({s:.1f} lb)' for l, s in zip(labels, sizes)],
    title="Pesos",
    title_fontsize=17,
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=18
)

plt.setp(autotexts, size=18)
plt.tight_layout()
plt.savefig('pesos.jpg', dpi=500, bbox_inches='tight')
# plt.show()

# Breakdown do peso vazio

plt.figure(figsize=(14, 10))

W_w, W_h, W_v, W_f, W_nlg, W_mlg, W_eng_installed, W_allelse = weightsvec

labels2 = ['Asa', 'Empenagem horizontal', 'Empenagem vertical', 'Fuselagem',
           'Trem de pouso principal', 'Trem de pouso dianteiro', 'Motores instalados', 'Outros componentes']
sizes2 = [W_w, W_h, W_v, W_f, W_mlg, W_nlg, W_eng_installed, W_allelse]
total2 = sum(sizes2)

# Paleta de cores personalizada
colors2 = sns.color_palette("viridis", 8)
explode2 = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)

wedges2, texts2, autotexts2 = plt.pie(
    sizes2,
    colors=colors2,
    explode=explode2,
    autopct=lambda p: f'{p:.1f}%',
    startangle=140,
    wedgeprops={'edgecolor': 'black', 'linewidth': 0.4},
    textprops={'fontsize': 20, 'color': 'black'},
    pctdistance=1.1,
)

# Legenda
plt.legend(
    wedges2,
    [f'{l} ({s:.1f} lb)' for l, s in zip(labels2, sizes2)],
    title="Pesos dos componentes",
    title_fontsize=17,
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=18
)

plt.setp(autotexts2, size=18)
plt.tight_layout()
plt.savefig('pesos dos componentes.jpg', dpi=500, bbox_inches='tight')
# plt.show()

# Agora vamos variar o alongamento da asa

W0_list = []

AR = np.arange(7, 14, 0.1)

for AR_w in AR:
    aircraft['geo_param']['wing']['AR'] = AR_w
    aircraft.update(dt.geometry(aircraft))
    W0, We, Wf, Wf_cruise, xcg_e, weightsvec = dt.weight(
        aircraft, W0_guess, T0_guess, altitude_cruise, Mach_cruise, range_cruise, loiter_time, altitude_altcruise, Mach_altcruise, range_altcruise)
    W0_list.append(W0)

plt.figure(figsize=(14, 10))

plt.plot(AR, W0_list, color='#440154', linewidth=3)

plt.ylabel('MTOW (lb)', fontweight='bold')
plt.xlabel(
    'Alongamento da asa (m)', fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('w0 x arw.jpg', dpi=500, bbox_inches='tight')
# plt.show()

# Retornando para a aeronave padrão

aircraft = dt.default_aircraft()
aircraft['dimensions'].update(dt.geometry(aircraft))

range_cruise_list = np.arange(1000000, 5000000, 100)

W0_list = []

for range_cruise in range_cruise_list:
    W0, We, Wf, Wf_cruise, xcg_e, weightsvec = dt.weight(
        aircraft, W0_guess, T0_guess, altitude_cruise, Mach_cruise, range_cruise, loiter_time, altitude_altcruise, Mach_altcruise, range_altcruise)
    W0_list.append(W0)

plt.figure(figsize=(14, 10))

plt.plot(range_cruise_list, W0_list, color='#440154',
         linewidth=3)

plt.ylabel('MTOW (lb)', fontweight='bold')
plt.xlabel(
    'Alcance de cruzeiro (m)', fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
# plt.show()

# Dados do Lab01
df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSr7tU5tK8cvvR32yypE1PArgXhmNbFJ9bw8w6Sm2zQhyaMs27csoo-77vgFedHw9z25Ez3Qm-geKyU/pub?gid=43084471&single=true&output=csv', skiprows=1)
df.drop(columns='Unnamed: 0', inplace=True)
df.reset_index(drop=True)

coluna1 = 'Range (NM)'
coluna2 = 'MTOW (lb)'

df[coluna1] = pd.to_numeric(df[coluna1].astype(
    str).str.replace(',', '').str.strip(), errors='coerce')
df[coluna2] = pd.to_numeric(df[coluna2].astype(
    str).str.replace(',', '').str.strip(), errors='coerce')

df_valid = df.dropna(subset=[coluna1, coluna2])

X = df_valid[coluna1].values*1852  # Convertendo de NM para m
Y = df_valid[coluna2].values
L = df_valid["Parameter"].values
# colors = sns.color_palette("viridis", len(L))
colors = plt.cm.tab20(np.linspace(0, 1, len(L)))

for i, (x, y, label) in enumerate(zip(X, Y, L)):
    plt.scatter(x, y, color=colors[i], label=label, s=80)

# Regressão linear
Z2 = np.polyfit(X, Y, 1)
p2 = np.poly1d(Z2)

plt.plot(np.sort(X), p2(np.sort(X)), color='gray',
         linestyle='dotted', linewidth=3)

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,
           fontsize=14, title="Aeronaves do Lab01", title_fontsize=18)

plt.savefig('w0 x range.jpg', dpi=500, bbox_inches='tight')
