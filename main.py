import pandas as pd
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

def calcular_venda_total(dias_para_colher, valor_venda):
    """Calcula a venda total baseada nos dias para colher e no valor de venda."""
    colheitas_mensais = 28 // dias_para_colher
    return colheitas_mensais * valor_venda

def classificar_rentabilidade(df):
    """Classifica a rentabilidade em cinco grupos com base nos percentis."""
    # Calcula os percentis
    percentil_20 = np.percentile(df['Venda Total'], 20)
    percentil_40 = np.percentile(df['Venda Total'], 40)
    percentil_60 = np.percentile(df['Venda Total'], 60)
    percentil_80 = np.percentile(df['Venda Total'], 80)
    
    # Classificação fuzzy baseada nos percentis
    categorias = []
    for valor in df['Venda Total']:
        if valor <= percentil_20:
            categorias.append("Muito Baixa Rentabilidade")
        elif valor <= percentil_40:
            categorias.append("Baixa Rentabilidade")
        elif valor <= percentil_60:
            categorias.append("Média Rentabilidade")
        elif valor <= percentil_80:
            categorias.append("Alta Rentabilidade")
        else:
            categorias.append("Muito Alta Rentabilidade")
    
    df['Categoria Rentabilidade'] = categorias

def gerar_graficos(df):
    """Gera gráficos de pertinência e outros gráficos relacionados."""
    # Definir o universo para a variável de Venda Total
    x_venda_total = np.linspace(df['Venda Total'].min(), df['Venda Total'].max(), 500)
    
    # Funções de pertinência para os grupos fuzzy
    venda_muito_baixa = fuzz.trimf(x_venda_total, [df['Venda Total'].min() - 1, df['Venda Total'].min(), np.percentile(df['Venda Total'], 20)])
    venda_baixa = fuzz.trimf(x_venda_total, [df['Venda Total'].min(), np.percentile(df['Venda Total'], 20), np.percentile(df['Venda Total'], 40)])
    venda_media = fuzz.trimf(x_venda_total, [np.percentile(df['Venda Total'], 20), np.percentile(df['Venda Total'], 40), np.percentile(df['Venda Total'], 60)])
    venda_alta = fuzz.trimf(x_venda_total, [np.percentile(df['Venda Total'], 40), np.percentile(df['Venda Total'], 60), np.percentile(df['Venda Total'], 80)])
    venda_muito_alta = fuzz.trimf(x_venda_total, [np.percentile(df['Venda Total'], 60), np.percentile(df['Venda Total'], 80), df['Venda Total'].max() + 1])
    
    # Plotar as funções de pertinência
    plt.figure(figsize=(10, 8))
    plt.plot(x_venda_total, venda_muito_baixa, 'b', label='Muito Baixa')
    plt.plot(x_venda_total, venda_baixa, 'g', label='Baixa')
    plt.plot(x_venda_total, venda_media, 'r', label='Média')
    plt.plot(x_venda_total, venda_alta, 'c', label='Alta')
    plt.plot(x_venda_total, venda_muito_alta, 'm', label='Muito Alta')
    plt.title('Funções de Pertinência para a Rentabilidade')
    plt.xlabel('Venda Total')
    plt.ylabel('Grau de Pertinência')
    plt.legend()
    plt.show()
    
    # Gerar histograma da Venda Total
    plt.figure(figsize=(8, 6))
    plt.hist(df['Venda Total'], bins=15, color='skyblue', edgecolor='black')
    plt.title('Distribuição da Venda Total')
    plt.xlabel('Venda Total')
    plt.ylabel('Frequência')
    plt.show()

def main():
    # Carregar dados do arquivo Excel
    arquivo = 'lista-de-produtos.xlsx'
    df = pd.read_excel(arquivo)
    
    # Calcular a venda total e adicionar a coluna ao DataFrame
    df['Venda Total'] = df.apply(lambda row: calcular_venda_total(row['Dias'], row['Venda']), axis=1)
    
    # Classificar rentabilidade
    classificar_rentabilidade(df)
    
    # Gerar gráficos
    gerar_graficos(df)
    
    # Salvar o DataFrame atualizado
    df.to_excel('plantas_classificadas.xlsx', index=False)
    print("Arquivo 'plantas_classificadas.xlsx' salvo com sucesso.")

# Executar o programa
if __name__ == "__main__":
    main()
