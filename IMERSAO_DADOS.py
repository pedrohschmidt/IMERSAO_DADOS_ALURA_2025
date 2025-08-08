import pandas as pd
import numpy as np
caminho_base = 'C:\\Users\\Pichau\\OneDrive\\CURSOS\\ALURA\\IMERSAO_DADOS\\SALARIES.txt'

palavra1 = 'PANDAS'
palavra2 = 'PRINT'
palavra3 = 'MATPLOTLIB'
palavra4 = ''



df = pd.read_csv(caminho_base)
#exibir os tipos de dados da tabela
#print("Exibir os tipos de dados da tabela:")
#df.info()

#traz as estatísticas da tabela, como mínimo, máximo, média, etc...
#print("Análise superficial dos dados da tabela:")
#print(df.describe())

#traz a quantidade de linhas e colunas
#print(f'Linhas: {df.shape[0]}')
#print(f'Colunas: {df.shape[1]}')

#coletar os nomes das colunas
#print(df.columns)


#renomeando as colunas
renomear_colunas = {
    'work_year':'ano', 
    'experience_level':'nivel_experiencia',
    'employment_type':'tipo_emprego', 
    'job_title':'cargo',
    'salary':'salario',
    'salary_currency':'moeda_salario',
    'salary_in_usd':'salario_usd',
    'employee_residence':'residencia_empregado',
    'remote_ratio':'taxa_remoto',
    'company_location':'localizacao_empresa',
    'company_size':'tamanho_empresa'
}

df.rename(columns=renomear_colunas, inplace=True)

#print(df.columns)


#renomeando a senioridade
renomear_senioridade = {
    'SE':'Senior',
    'MI':'Pleno',
    'EN':'Junior',
    'EX':'Executivo'
}

df['nivel_experiencia'] = df['nivel_experiencia'].replace(renomear_senioridade)
#SE = SENIOR, MI = MID, EN = ENTRY, EX = EXECUTIVO
#print('Frequência das categorias na tabela:')
#print(df['nivel_experiencia'].value_counts())

renomear_tipo_emprego = {
    'FT':'Full time',
    'CT':'Temporario',
    'PT':'Part-time',
    'FL':'Freelancer'
}
df['tipo_emprego'] = df['tipo_emprego'].replace(renomear_tipo_emprego)
#FT = FULL TIME, CT=TEMPORARIO, PT=PART TIME, FL=FREELANCER
#print('Frequência das categorias na tabela:')
#print(df['tipo_emprego'].value_counts())


#print('Frequência das categorias na tabela:')
#print(df['cargo'].value_counts())


renomear_tamanho_empresa = {
    'S':'Pequena',
    'M':'Media',
    'L':'Grande'
}

df['tamanho_empresa'] = df['tamanho_empresa'].replace(renomear_tamanho_empresa)
#print('Frequência das categorias na tabela:')
#print(df['tamanho_empresa'].value_counts())


renomear_taxa_remoto ={
    0:'Presencial',
    50:'Hibrido',
    100:'Remoto'
}

df['taxa_remoto'] = df['taxa_remoto'].replace(renomear_taxa_remoto)
#print('Frequência das categorias na tabela:')
#print(df['taxa_remoto'].value_counts())

#print('Informações por coluna:')
#print(df.describe(include="object"))

#print('Marcando os nulos como TRUE')
#print(df.isnull())

#print('Contando os nulos:')
#print(df.isnull().sum())

#print('Exibindo os anos da tabela:')
#print(df['ano'].unique())

#print('Filtrando o dataframe pra trazer as linhas que contém nulo:')
#print(df[df.isnull().any(axis=1)])

'''
print('Testando a substituição dos nulos pela média e mediana')
df_teste = pd.DataFrame({
    'nome':['Pedro','Joao','Kaue','Beatriz','Marcia','Jonas'],
    'salario':[1000.0,1500.0,np.nan,2100.0,np.nan,250000.0]
})
#substitui os nulos pelo salário médio
df_teste['salario_media'] = df_teste['salario'].fillna(df_teste['salario'].mean())

#substitui os nulos pela mediana. A mediana é mais recomendável pq ela retira os outliers
df_teste['salario_mediana'] = df_teste['salario'].fillna(df_teste['salario'].median())
print(df_teste)




print('Testando o preenchimento baseado no valor anterior (ffill), posterior (bfill) e valor fixo:')
df_temperaturas = pd.DataFrame({
    'Dia_semana':['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo'],
    'Temperatura':[30,np.nan,29, np.nan, 27, 29,29]
})
#Anterior
df_temperaturas['Temperatura_f_fill'] = df_temperaturas['Temperatura'].ffill()
#posterior
df_temperaturas['Temperatura_b_fill'] = df_temperaturas['Temperatura'].bfill()
#default
df_temperaturas['Temperatura_fillna'] = df_temperaturas['Temperatura'].fillna(25)
print(df_temperaturas)

'''

#como nosso df tem dez registros nulos, e o campo é o do ano (que não se usa média), o mais indicado seria remover da base

#removendo os nulos do df original
df_limpo = df.dropna()
#verificando se ele removeu os nulos
#print(df_limpo.isnull().sum())

#convertendo o ano de float para int

df_limpo = df_limpo.assign(ano = df_limpo['ano'].astype('int64'))
#print(df_limpo.info())

#plotando as quantidades em um gráfico usando pandas


import matplotlib.pyplot as plt


def plotar_experiencia():
    df_limpo['nivel_experiencia'].value_counts().plot(kind='bar', title='Distribuição de senioridade')
    plt.show()

#plotar_experiencia()

import seaborn as sns

def plotar_salario_medio():
    plt.figure(figsize=(8,5))
    plt.title('Salário por senioridade')
    plt.xlabel('Senioridade')
    plt.ylabel('Salário médio anual - USD')
    df_salario_medio = pd.DataFrame(df_limpo.groupby('nivel_experiencia')['salario_usd'].mean().sort_values(ascending=True))
    ordenado = df_limpo.groupby('nivel_experiencia')['salario_usd'].mean().sort_values(ascending=False).index
    sns.barplot(data = df_salario_medio, x = 'nivel_experiencia', y='salario_usd', order=ordenado)
    #o seaborn não dispensa o uso do matplot lib, por isso usamos o plt.show, aqui
    plt.show()

#plotar_salario_medio()


#plotando histograma

def histograma_salarios():
    plt.figure(figsize=(8,4))
    plt.title('Distribuição de salários anuais')
    plt.xlabel('Salário em USD')
    plt.ylabel('Frequência')
    #bins é a quantidade de barras
    #kde é a linha 
    sns.histplot(df_limpo['salario_usd'], bins=50, kde=True)
    plt.show()
#histograma_salarios()


#plotando boxplot

def boxplot():
    plt.figure(figsize=(8,5))
    plt.title('Distribuição de salários anuais')
    plt.xlabel('Salário em USD')
    plt.ylabel('Frequência')
    sns.boxplot(x=df_limpo['salario_usd'])
    plt.show()


#boxplot()


def ordem_senioridade():
    ordem_senioridade = ['Junior','Pleno','Senior','Executivo']
    plt.figure(figsize=(8,5))
    plt.title('Distribuição de salários por senioridade')
    plt.xlabel('Salário em USD')
    plt.ylabel('Frequência')
    sns.boxplot(data = df_limpo, x = df_limpo['nivel_experiencia'], y = df_limpo['salario_usd'], order = ordem_senioridade, palette='Set2', hue='nivel_experiencia')
    plt.show()
#ordem_senioridade()


import plotly.express as px
def plotando_interativo():
    df_salario_medio = (
    df_limpo
    .groupby('nivel_experiencia')['salario_usd']
    .mean()
    .sort_values(ascending=True)
    .reset_index()
)
    fig = px.bar(df_salario_medio, 
                x='nivel_experiencia', 
                y='salario_usd', 
                title = 'Salário médio USD', 
                labels = {'nivel_experiencia':'Senioridade','salario_usd':'Salário em dólar'})
    fig.show()

#plotando_interativo()


def plotando_pizza():
    contagem_remoto = df_limpo['taxa_remoto'].value_counts().reset_index()
    contagem_remoto.columns = ['Tipo_trabalho','Quantidade']

    fig = px.pie(contagem_remoto, 
            names='Tipo_trabalho',
            values='Quantidade',
            title = 'Proporção tipos de trabalho',
            hole = 0.5,
            )
    fig.update_traces(textinfo='percent+label')
    fig.show()
#plotando_pizza()


#DESAFIO: FAZER UM GRÁFICO DE SALÁRIO MÉDIO POR PAÍS