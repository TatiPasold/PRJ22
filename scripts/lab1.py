import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from adjustText import adjust_text

### Importação dos Dados
df = pd.read_csv(
    'https://docs.google.com/spreadsheets/d/e/2PACX-1vSr7tU5tK8cvvR32yypE1PArgXhmNbFJ9bw8w6Sm2zQhyaMs27csoo-77vgFedHw9z25Ez3Qm-geKyU/pub?gid=43084471&single=true&output=csv',
    skiprows=1
)

df.drop(columns='Unnamed: 0', inplace=True)
df.reset_index(drop=True, inplace=True)

### Análise de Correlação
# Achamos interessante investigar antes a correlação das variáveis e verificar os melhores plots
cols = df.columns
string_columns = df.select_dtypes(include=['object']).columns
ft_columns = [col for col in cols if 'ft' in col]
lb_columns = [col for col in cols if 'lb' in col]

colunas_para_remover = list(set(string_columns) | set(ft_columns) | set(lb_columns))
colunas_para_remover = [col for col in colunas_para_remover if col in df.columns]

correlation_matrix = df.drop(columns=colunas_para_remover).corr()

plt.figure(figsize=(20, 10))

sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')

# Filtrar pares com correlação superior a 0.8
correlation_matrix = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool))
high_corr_pairs = [
    (col1, col2, correlation_matrix[col1][col2])
    for col1 in correlation_matrix.columns
    for col2 in correlation_matrix.columns
    if col1 != col2 and abs(correlation_matrix[col1][col2]) > 0.8
]

# Exibir os pares de colunas com correlação alta
print("\n Pares de colunas com correlação > 0.8")
for pair in high_corr_pairs:
    print(f"{pair[0]} e {pair[1]}: {pair[2]:.2f}")

### Função para plotar os gráficos que escolhemos
def plotar(coluna1, coluna2):
    """ Plota a relação entre duas variáveis, destacando outliers e ajustando uma regressão linear(sem outliers). """

    df[coluna1] = pd.to_numeric(df[coluna1].astype(str).str.replace(',', '').str.strip(), errors='coerce')
    df[coluna2] = pd.to_numeric(df[coluna2].astype(str).str.replace(',', '').str.strip(), errors='coerce')

    df_valid = df.dropna(subset=[coluna1, coluna2])

    X = df_valid[coluna1].values
    Y = df_valid[coluna2].values

    # Regressão linear inicial para ver outliers
    Z1 = np.polyfit(X, Y, 1)
    p1 = np.poly1d(Z1)
    Y_pred1 = p1(X)

    # Cálculo do erro e desvio padrão para ver os outl
    erros = Y - Y_pred1
    desvio_padrao = np.std(erros)

    # Vamos usar com 1.5
    limite_inferior = Y_pred1 - 1.5 * desvio_padrao
    limite_superior = Y_pred1 + 1.5 * desvio_padrao
    mascara = (Y >= limite_inferior) & (Y <= limite_superior)

    # Separação dos dados filtrados e outliers
    X_filtrado, Y_filtrado = X[mascara], Y[mascara]
    X_outliers, Y_outliers = X[~mascara], Y[~mascara]

    # Regressão linear final com dados filtrados(essa que vamos plotar)
    Z2 = np.polyfit(X_filtrado, Y_filtrado, 1)
    p2 = np.poly1d(Z2)

    plt.figure(figsize=(12, 8))
    # pontos normais e outliers
    plt.scatter(X_filtrado, Y_filtrado, label='Dados Filtrados', color='black')
    plt.scatter(X_outliers, Y_outliers, label='Outliers', color='blue')

    # Regressão linear
    sns.lineplot(x=np.sort(X), y=p2(np.sort(X)), color='gray', linestyle='dotted',
                 label=f'Regressão Linear: f(x) = {p2[0].round(3)} + {p2[1].round(6)} x')

    # Esses deltas são para as labels
    delta_x = (X_filtrado.max() - X_filtrado.min()) / 50
    delta_y = (Y_filtrado.max() - Y_filtrado.min()) / 20

    df_aviao = df_valid[['Parameter', coluna1, coluna2]].copy()
    df_aviao['Y_pred'] = p2(df_aviao[coluna1])
    df_aviao.set_index('Parameter', inplace=True)

    posicoes_rotulos = []
    # se estiver abaixo da reta, a label vai em cima, se estiver em baixo, vai em baixo
    for index, aviao in df_aviao.iterrows():
        x, y, y_pred = aviao[coluna1], aviao[coluna2], aviao['Y_pred']
        label_x, label_y = x - delta_x, y + delta_y * 0.5 if y > y_pred else y - delta_y

        # Isso é para evitar sobreposição de labels
        for px, py in posicoes_rotulos:
            if abs(label_x - px) < delta_x * 1.5 and abs(label_y - py) < delta_y * 1.5:
                label_y += delta_y

        posicoes_rotulos.append((label_x, label_y))
        plt.text(label_x, label_y, str(index), fontsize=10)


    plt.xlabel(coluna1, fontsize=16)
    plt.ylabel(coluna2, fontsize=16)
    plt.legend(fontsize=14)

    ax = plt.gca()
    ax.tick_params(axis='x', top=False)
    ax.tick_params(axis='y', right=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.grid(False)
    plt.show()

### Execução dos Plots
plotar("MTOW (kg)", "Empty_Weight (kg)")
plotar("Number_of_passengers", "MTOW (kg)")
plotar("Number_of_passengers", "Fuselage_length (m)")
plotar("Number_of_passengers", "Fuselage_diameter (m)")
plotar("Cruise_Mach", "Wing_sweep(deg)")
plotar("MTOW (kg)", "Wing_area (m²)")
plotar("MTOW (kg)", "Range (NM)")
plotar('Engine_TSFC', 'Cruise_Mach')