import requests
from time import sleep

def converte_nomemes_para_nummes(data):
    relacao_mes = {
        " de janeiro": "01",
        " de fevereiro": "02",
        " de março": "03",
        " de abril": "04",
        " de maio": "05",
        " de junho": "06",
        " de julho": "07",
        " de agosto": "08",
        " de setembro": "09",
        " de outubro": "10",
        " de novembro": "11",
        " de dezembro": "12",
    }

    for mes_txt, mes_num in relacao_mes.items():
        if mes_txt in data:
            data = data.replace(mes_txt, "/" + mes_num)

    return data

def converte_abrevmes_para_nummes(data):
    relacao_mes = {
        " jan ": "01",
        " fev ": "02",
        " mar ": "03",
        " abr ": "04",
        " mai ": "05",
        " jun ": "06",
        " jul ": "07",
        " ago ": "08",
        " set ": "09",
        " out ": "10",
        " nov ": "11",
        " dez ": "12",
    }

    for mes_txt, mes_num in relacao_mes.items():
        if mes_txt in data:
            data = data.replace(mes_txt, ("/" + mes_num + "/"))

    return data

def dia_da_semana_para_data(dia_escolhido):
    from datetime import date, datetime, timedelta

    dias = {
        "Hoje": None,
        "Ontem": 1,
        "Segunda-feira": 0,
        "Terça-feira": 1,
        "Quarta-feira": 2,
        "Quinta-feira": 3,
        "Sexta-feira": 4,
        "Sábado": 5,
        "Domingo": 6
    }
    dia_de_hoje = date.today().weekday()

    if dia_escolhido == "Hoje":
        diff_dias = None
    else:
        diff_dias = dia_de_hoje - dias[dia_escolhido]

    if diff_dias is None:
        return (date.today()).strftime("%d/%m/%Y")
    elif diff_dias > 0:
        return (date.today() - timedelta(days=diff_dias)).strftime("%d/%m/%Y")
    elif diff_dias <= 0:
        return (date.today() - timedelta(days=7 + diff_dias)).strftime("%d/%m/%Y")

def cadastrar_conta_pagar(dataEmissao, vencimentoOriginal, competencia, nroDocumento, valor, historico, categoria):
    url = "https://bling.com.br/b/Api/v2/contapagar/json/"

    payload= 'apikey=a46ebb16b15e9fdfade2817a3b346942fabe8320811de301aa81b5cbde6feb6d864c1d19&xml=%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%0A%3Ccontapagar%3E%0A%20%20%20%20%3CdataEmissao%3E{}%3C%2FdataEmissao%3E%0A%20%20%20%20%3CvencimentoOriginal%3E{}%3C%2FvencimentoOriginal%3E%0A%20%20%20%20%3Ccompetencia%3E{}%3C%2Fcompetencia%3E%0A%20%20%20%20%3CnroDocumento%3E{}%3C%2FnroDocumento%3E%20%0A%20%20%20%20%3Cvalor%3E{}%3C%2Fvalor%3E%0A%20%20%20%20%3Chistorico%3E{}%3C%2Fhistorico%3E%0A%20%20%20%20%3Ccategoria%3E{}%3C%2Fcategoria%3E%0A%20%20%20%20%3Cportador%3EMercado%20Pago%3C%2Fportador%3E%20%0A%20%20%20%20%3CidFormaPagamento%3E1608994%3C%2FidFormaPagamento%3E%0A%20%20%20%20%3Cocorrencia%3E%0A%20%20%20%20%20%20%20%3CocorrenciaTipo%3EU%3C%2FocorrenciaTipo%3E%0A%20%20%20%20%3C%2Focorrencia%3E%0A%20%20%20%20%3Cfornecedor%3E%0A%20%20%20%20%3Cnome%3EMERCADOLIVRE%20COM%20ATIVIDADES%20INTERNET%20LT%3C%2Fnome%3E%0A%20%20%20%20%20%20%20%3Ccpf_cnpj%3E03361252000134%3C%2Fcpf_cnpj%3E%0A%20%20%20%20%20%20%20%3CtipoPessoa%3EJ%3C%2FtipoPessoa%3E%0A%20%20%20%20%20%20%20%3Cie_rg%3E115562960119%3C%2Fie_rg%3E%0A%20%20%20%20%20%20%20%3Cendereco%3ERUA%20ARANDU%3C%2Fendereco%3E%0A%20%20%20%20%20%20%20%3Cnumero%3E281%3C%2Fnumero%3E%0A%20%20%20%20%20%20%20%3Ccomplemento%3E8%20AND%3C%2Fcomplemento%3E%0A%20%20%20%20%20%20%20%3Ccidade%3ESAO%20PAULO%3C%2Fcidade%3E%0A%20%20%20%20%20%20%20%3Cbairro%3EC%20MONCOES%3C%2Fbairro%3E%0A%20%20%20%20%20%20%20%3Ccep%3E04562030%3C%2Fcep%3E%0A%20%20%20%20%20%20%20%3Cuf%3ESP%3C%2Fuf%3E%0A%20%20%20%20%3C%2Ffornecedor%3E%20%0A%3C%2Fcontapagar%3E'.format(dataEmissao, vencimentoOriginal, competencia, nroDocumento, valor, historico, categoria)
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    sleep(0.5)
    return response.text

def cadastrar_conta_receber(dataEmissao, vencimentoOriginal, competencia, nroDocumento, valor, historico, categoria):
    url = "https://bling.com.br/b/Api/v2/contareceber/json/"

    payload='apikey=a46ebb16b15e9fdfade2817a3b346942fabe8320811de301aa81b5cbde6feb6d864c1d19&xml=%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%0A%3Ccontareceber%3E%0A%20%20%20%20%3CdataEmissao%3E{}%3C%2FdataEmissao%3E%0A%20%20%20%20%3CvencimentoOriginal%3E{}%3C%2FvencimentoOriginal%3E%0A%20%20%20%20%3Ccompetencia%3E{}%3C%2Fcompetencia%3E%0A%20%20%20%20%3CnroDocumento%3E{}%3C%2FnroDocumento%3E%0A%20%20%20%20%3Cvalor%3E{}%3C%2Fvalor%3E%0A%20%20%20%20%3Chistorico%3E{}%3C%2Fhistorico%3E%0A%20%20%20%20%3Ccategoria%3E{}%3C%2Fcategoria%3E%0A%20%20%20%20%3CidFormaPagamento%3E1608994%3C%2FidFormaPagamento%3E%0A%20%20%20%20%3Cportador%3EMercado%20Pago%3C%2Fportador%3E%0A%20%20%20%20%3Cocorrencia%3E%0A%20%20%20%20%20%20%20%3CocorrenciaTipo%3EU%3C%2FocorrenciaTipo%3E%0A%20%20%20%20%3C%2Focorrencia%3E%0A%20%20%20%20%3Ccliente%3E%0A%20%20%20%20%3Cnome%3EMERCADOLIVRE%20COM%20ATIVIDADES%20INTERNET%20LT%3C%2Fnome%3E%0A%20%20%20%20%20%20%20%3Ccpf_cnpj%3E03361252000134%3C%2Fcpf_cnpj%3E%0A%20%20%20%20%20%20%20%3CtipoPessoa%3EJ%3C%2FtipoPessoa%3E%0A%20%20%20%20%20%20%20%3Cie_rg%3E115562960119%3C%2Fie_rg%3E%0A%20%20%20%20%20%20%20%3Cendereco%3ERUA%20ARANDU%3C%2Fendereco%3E%0A%20%20%20%20%20%20%20%3Cnumero%3E281%3C%2Fnumero%3E%0A%20%20%20%20%20%20%20%3Ccomplemento%3E8%20AND%3C%2Fcomplemento%3E%0A%20%20%20%20%20%20%20%3Ccidade%3ESAO%20PAULO%3C%2Fcidade%3E%0A%20%20%20%20%20%20%20%3Cbairro%3EC%20MONCOES%3C%2Fbairro%3E%0A%20%20%20%20%20%20%20%3Ccep%3E04562030%3C%2Fcep%3E%0A%20%20%20%20%20%20%20%3Cuf%3ESP%3C%2Fuf%3E%0A%20%20%20%20%3C%2Fcliente%3E%0A%20%3C%2Fcontareceber%3E'.format(dataEmissao, vencimentoOriginal, competencia, nroDocumento, valor, historico, categoria)
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    sleep(0.5)
    return response.text