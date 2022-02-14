""""
    Arquivo responsável por cadastrar contas no Bling (a pagar e a receber),
    a partir das vendas feitas pelo Mercado Livre, 
    e abrir conversa no Whatsapp com o cliente, com mensagem pré-definida.
    Como:
        - Usuário executa o programa e copia o <body> do html da página da venda
        - Função faz_scrapping_e_cadastro faz web scrapping da página com BeautifulSoup para obter os dados da venda
        - Com os dados da venda, função faz_cadastro_das_contas cadastra as contas no sistema por requisição POST
"""

import pyperclip
import utils
import logging
from time import sleep

logging.basicConfig(
            filename='ml_bling_wpp.log', encoding='utf-8', level=logging.INFO,
            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

### LOGGING ###
# Nível  |  Quando é usando
# DEBUG -> Informação detalhada, tipicamente de interesse apenas quando diagnosticando problemas.
# INFO -> Confirmação de que as coisas estão funcionando como esperado.
# WARNING -> Uma indicação que algo inesperado aconteceu, ou um indicativo que algum problema 
#            em um futuro próximo (ex.: ‘pouco espaço em disco’). 
#            O software está ainda funcionando como esperado.
# ERROR -> Por conta de um problema mais grave, o software não conseguiu executar alguma função.
# CRITICAL -> Um erro grave, indicando que o programa pode não conseguir continuar rodando.

def faz_scrapping_e_cadastro(html):
    """
    html: body da página da venda
    """
    from bs4 import BeautifulSoup
    import re

    soup = BeautifulSoup(html, 'html.parser')

    nome_cliente = soup.find(class_="sc-buyer__content")
    nome_cliente = nome_cliente.find('b').text
    nome_cliente = nome_cliente.encode('utf-8').decode('unicode_escape')
    primeiro_nome_cliente = nome_cliente.split(" ")[0]
    nome_venda = soup.find(class_="sc-detail-title__text").text
    nome_venda = nome_venda.encode('utf-8').decode('unicode_escape')
    codigo_venda = soup.find(class_="sc-detail-title__subtitle").text.split(' ')[1].strip('#')
    data_hora_venda = soup.find(class_="sc-detail-title__subtitle").text.strip('.').split(' ')
    data_hora_venda = ' '.join([str(i) for i in data_hora_venda[2:]])
    data = data_hora_venda.split(' ')
    # tratamento pra quando for um dia com um numeral (1 a 9): acrescentar zero antes
    if len(data[0]) == 1:
        data[0] = '0' + data[0]
    data = ' '.join([str(i) for i in data[:3]])
    data_venda = utils.converte_abrevmes_para_nummes(data)
    print("===================================")
    print(nome_venda)
    print('---------------------')
    print(data_venda)

    sku_produto = soup.find(class_="sc-title-subtitle-action__sublabel").text.strip("SKU ")

    valores = soup.find_all(class_="sc-account-rows false")

    valores_cliente = valores[0].find_all('li')
    valores_custos = valores[1].find_all('li')

    if soup.find(text=re.compile("Tel.: ")):
        tel_cliente = soup.find(text=re.compile("Tel.: ")).split("Tel.: ")[1]
    else:
        tel_cliente = 00000000000

    if soup.find(text=re.compile('pacote')):
        l = []
        tarifas = soup.find_all(text=re.compile('Tarifa'))
        if tarifas:
                for i in range(len(tarifas)-1):
                    l.append(float("-" + valores_custos[i].text.split()[-1].replace(",",".")))
        valor_tarifa_custo = sum(l)

        # codigo_mercado_pago = soup.find(text=re.compile('Ver mais'))
        codigo_mercado_pago = ""
    else:
        valor_tarifa_custo = float("-" + valores_custos[0].text.split()[-1].replace(",","."))
        codigo_mercado_pago = soup.find(class_="sc-account-title__subtext").text.split(' ')[0].strip('#')

    valor_produto_cliente = float(valores_cliente[0].text.split()[-1].replace(".", "").replace(",","."))

    if len(valores_cliente) < 2:
        valor_frete_cliente = 0.00
    else:
        valor_frete_cliente = float(valores_cliente[1].text.split()[-1].replace(",","."))

    for v in valores_custos:
        if len(valores_custos) < 2 or not v.find(text=re.compile('Envio')):
            valor_frete_custo = 0.00
        else:
            valor_frete_custo = float("-" + valores_custos[-1].text.split()[-1].replace(",","."))

    total_recebido = float(list(valores[2].text.split())[-1].replace(".", "").replace(",","."))
    total_conta_receber = valor_produto_cliente + valor_frete_cliente
    total_conta_pagar = valor_tarifa_custo + valor_frete_custo

    print(f'##### CLIENTE {nome_cliente} #####\n---------------------\nProduto: {valor_produto_cliente}\nFrete: {valor_frete_cliente}')
    print('---------------------')
    print(f'Total Conta a Receber: {total_conta_receber:.2f}\n')
    print(f'##### CUSTOS #####\nTarifa: {valor_tarifa_custo}\nFrete: {valor_frete_custo}')
    print('---------------------')
    print(f'Total Conta a Pagar: {total_conta_pagar:.2f}\n')
    print('='*56)

    def faz_cadastro_das_contas():
        # VALOR PRODUTO
        conta_receber_produto = utils.cadastrar_conta_receber(
                                    dataEmissao=data_venda, vencimentoOriginal=data_venda, 
                                    competencia=data_venda, nroDocumento=f'{codigo_venda}VND', valor=valor_produto_cliente, 
                                    historico=f"Venda online {nome_venda} por {valor_produto_cliente} via Mercado Livre. Cliente: {nome_cliente}. Codigo Mercado Pago: {codigo_mercado_pago}",
                                    categoria="Vendas Mercado Livre")
        if '"cod":80' in conta_receber_produto:
            logging.warning(f"A conta a receber {codigo_venda}VND já foi cadastrada anteriormente")
            print(f"A conta a receber {codigo_venda}VND já foi cadastrada anteriormente")
        elif "erro" in conta_receber_produto:
            logging.error("ERRO ao cadastrar conta a receber")
            logging.error(conta_receber_produto)
            print("ERRO ao cadastrar conta a receber")
        else:
            print(f"Conta a receber de {valor_produto_cliente} cadastrada com sucesso!")
            logging.info(f"Conta a receber de {valor_produto_cliente} cadastrada com sucesso!")
        if valor_frete_cliente != 0.00:
            # FRETE CLIENTE
            conta_receber_frete = utils.cadastrar_conta_receber(
                                        dataEmissao=data_venda, vencimentoOriginal=data_venda, 
                                        competencia=data_venda, nroDocumento=f'{codigo_venda}FRT', valor=valor_frete_cliente, 
                                        historico=f"Venda online {nome_venda} por {valor_produto_cliente} via Mercado Livre. Cliente: {nome_cliente}. Codigo Mercado Pago: {codigo_mercado_pago}",
                                        categoria="Fretes Recebidos")
            if '"cod":80' in conta_receber_frete:
                logging.warning(f"A conta a receber {codigo_venda}FRT já foi cadastrada anteriormente")
                print(f"A conta a receber de {valor_frete_cliente} já foi cadastrada anteriormente")
            elif "erro" in conta_receber_frete:
                logging.error("ERRO ao cadastrar conta a receber")
                logging.info(f"Bling: {conta_receber_frete}")
                print("ERRO ao cadastrar conta a receber")
            else:
                logging.info(f"Conta a receber de {valor_frete_cliente} cadastrada com sucesso!")
                print(f"Conta a receber de {valor_frete_cliente} cadastrada com sucesso!")

        # condição para que a conta a pagar não seja recriada, 
        # pois só a requisição da conta a receber possui retorno do erro de repetição (cod: 80)
        if not '"cod":80' in (conta_receber_produto or conta_receber_frete):
            # TARIFA
            conta_pagar_tarifa = utils.cadastrar_conta_pagar(
                                    dataEmissao=data_venda, vencimentoOriginal=data_venda, 
                                    competencia=data_venda, nroDocumento=f'{codigo_venda}TRF', valor=((valor_tarifa_custo)*(-1)), 
                                    historico=f"Tarifa Venda de {nome_venda} por {valor_produto_cliente}. Cliente: {nome_cliente}. Codigo Mercado Pago: {codigo_mercado_pago}",
                                    categoria="Tarifa Mercado Livre")
            if "erro" in conta_pagar_tarifa:
                print("ERRO ao cadastrar conta a pagar")
            else:
                print(f"Conta a pagar de {valor_tarifa_custo} cadastrada com sucesso!")
            if valor_frete_custo != 0.00:
                # CUSTO FRETE
                conta_pagar_frete = utils.cadastrar_conta_pagar(
                                        dataEmissao=data_venda, vencimentoOriginal=data_venda, 
                                        competencia=data_venda, nroDocumento=f'{codigo_venda}FRT', valor=((valor_frete_custo)*(-1)), 
                                        historico=f"Frete Venda de {nome_venda} por {valor_produto_cliente}. Cliente: {nome_cliente}. Codigo Mercado Pago: {codigo_mercado_pago}",
                                        categoria="Frete Mercado Livre/Envios")
                if "erro" in conta_pagar_frete:
                    logging.error("ERRO ao cadastrar conta a pagar")
                    logging.info(f"Bling: {conta_pagar_frete}")
                    print("ERRO ao cadastrar conta a pagar")
                else:
                    logging.info(f"Conta a pagar de {valor_frete_custo} cadastrada com sucesso!")
                    print(f"Conta a pagar de {valor_frete_custo} cadastrada com sucesso!")
        print('='*56)
        def abre_link_zap():
            if tel_cliente:
                link_zap = f"https://api.whatsapp.com/send?phone=55{tel_cliente}&text=Boa%20tarde%2C%20{primeiro_nome_cliente}!%20Tudo%20bem%3F%20Eu%20sou%20a%20Larissa%2C%20da%20Don%20Adega. Estou%20entrando%20em%20contato%20para%20informar%20que%20seu%20pedido%20j%C3%A1%20est%C3%A1%20sendo%20despachado%20e%20que%20a%20entrega%20%C3%A9%20feita%20exclusivamente%20pelo%20Mercado%20Livre.%20Estarei%20h%C3%A1%20disposi%C3%A7%C3%A3o%20para%20qualquer%20d%C3%BAvida%20ou%20problema.%20Parab%C3%A9ns%20pela%20escolha!"      
                # print("\n")
                # print(link_zap)
                print("\nAbrindo link do zap...")
                import webbrowser
                webbrowser.open_new_tab(link_zap)
            else:
                link_zap = ""
                print("\nTelefone do cliente não encontrado")      
            return link_zap
        abre_link_zap()
    faz_cadastro_das_contas()

def main():
    len_texto_copiado_antes = {"mercado": [], "ultimo_copy": ""}
    def imp():
        return "\nCopie o elemento <body da página da venda do Mercado Livre"

    while True:
        sleep(0.3)
        texto_copiado = pyperclip.paste()

        # Salva variavel com a quandidade de caracteres na memoria
        len_texto_copiado = len(str(texto_copiado))

        # Verifica se a quantidade de caracteres na memoria mudou
        if len_texto_copiado != len_texto_copiado_antes["ultimo_copy"]:
            # Verifica se existe a tag mercado, se existe o numero do cartão e se existe alguma pesquisa no mercado com os mesmo caracteres
            if (
                ("</div>" and "Mercado Livre Brasil") in texto_copiado
                and len_texto_copiado not in len_texto_copiado_antes["mercado"]
            ):
                print("\nPágina da venda encontrada!")
                pyperclip.copy(faz_scrapping_e_cadastro(texto_copiado))

                # Armazena a quantidade de caracter na lista de pesquisados no mercado
                len_texto_copiado_antes["mercado"].append(len_texto_copiado)

                # Armazena a quantidade de carecteres do copy antigo na memoria
                len_texto_copiado_antes["ultimo_copy"] = len_texto_copiado

                print(imp())
            else:
                # Armazena a quantidade de caracter na lista de pesquisados no bradesco
                len_texto_copiado_antes["mercado"].append(len_texto_copiado)

                # Armazena a quantidade de carecteres do copy antigo na memoria
                len_texto_copiado_antes["ultimo_copy"] = len_texto_copiado

                print("\n\nPágina de venda não encontrada")
                print(imp())
main()