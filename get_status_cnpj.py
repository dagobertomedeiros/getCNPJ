import requests
import json
import time
import pandas as pd
import re

url = 'https://www.receitaws.com.br/v1/cnpj/'

#Carregando CNPJ das empresas em dataframe
arq = pd.read_excel("agentes_ativos_17-10-19.xlsx")
dt = pd.DataFrame(arq)

#Consultando através do CNPJ a atividade principal da empresa
#utilizando api do receitaws, como a versão pública e gratuita desta api permite no máximo 3 
#consultas por minuto foi introduzido no código um delay de 22s por consulta assim retornando 
#todos os valores sem erros
i = 0
ativPrincipal = []
situacao = []
motivoSituacao = []
dataSituacao = []
while(i < dt['CNPJ/CPF'].size):
    cnpj = str(dt['CNPJ/CPF'][i])
    cnpj = cnpj.replace('-', '')
    cnpj = cnpj.replace('/', '')
    cnpj = cnpj.replace('.', '')
    if(len(cnpj) < 14):
        while(len(cnpj) < 14):
            cnpj = '0' + cnpj
    page = requests.get(url + cnpj)
    if(page):
        jsonAll = json.loads(page.text)
        jsonAtiv = jsonAll['atividade_principal']
        codAtiv = str(jsonAtiv[0].get('code'))
        codAtiv = codAtiv.replace('.', '')
        codAtiv = codAtiv.replace('-', '')
        ativPrincipal.append(codAtiv)
        jsonSituacao = jsonAll['situacao']
        jsonMotivoSituacao = jsonAll['motivo_situacao']
        jsonDataSituacao = jsonAll['data_situacao']
        situacao.append(jsonSituacao)
        motivoSituacao.append(jsonMotivoSituacao)
        dataSituacao.append(jsonDataSituacao)
        time.sleep(22)
    i+=1

#adicionando os novos dados conseguidos ao dt
dt['cod_atividade'] = ativPrincipal
dt['situacao'] = situacao
dt['motivo_situacao'] = motivoSituacao
dt['data_situacao'] = dataSituacao

#salvando tudo em um novo arquivo
dt.to_excel('EMP_CNPJS_ATIVIDADES.xlsx')

