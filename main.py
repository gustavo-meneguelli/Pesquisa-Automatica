import tkinter as tk
from tkinter import ttk
import tkinter.messagebox 
from tkinter.filedialog import asksaveasfile
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd 
from selenium.webdriver.chrome.service import Service as ChromeService
from subprocess import CREATE_NO_WINDOW
import tkinter as tk
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument('--log-level=1')
chrome_service = ChromeService('chromedriver')
chrome_service.creationflags = CREATE_NO_WINDOW
servico = Service(ChromeDriverManager().install())


def PesquisarProdutosGoogleShopping(produto, termos_banidos, preco_minimo, preco_maximo):

    #Entrando no site
    nav = webdriver.Chrome(options=options, service= chrome_service, service_log_path=servico)    
    nav.get('https://www.google.com/')

    #Pesquisando
    nav.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(produto)
    nav.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
    
    #Entrando na Aba Google Shopping
    opcoes_menu_google = nav.find_elements(By.CLASS_NAME, 'hdtb-mitem')
    
    for opcoes in opcoes_menu_google:
        if opcoes.text == 'Shopping':
            opcoes.click()
            break
    
    time.sleep(5)

    #Termos Banidos e Nome do Produto
    lista_termos_banidos = termos_banidos.split(' ')
    lista_termos_produto = produto.split(' ')
    
    #Tratando os dados do produto
    lista_info_produto = nav.find_elements(By.CLASS_NAME, 'i0X6df')
    lista_ofertas_final = []

    #Tratando os dados do produto
    for item in lista_info_produto:
        try:
            nome = item.find_element(By.CLASS_NAME, 'Xjkr3b').text.lower()
            preco = item.find_element(By.CLASS_NAME, 'a8Pemb ').text
            preco = preco.replace(' ', '').replace('R$', '').replace('.', '').replace(',', '.')
            preco = float(preco)
            link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')

            #verificação se o nome corresponde
            tem_palavra_do_produto = True
            for palavra in lista_termos_produto:
                if not palavra in nome:
                    tem_palavra_do_produto = False

            #verificação se o termo banido não está incluido
            tem_termo_banido = False
            for palavra in lista_termos_banidos:
                if palavra in nome:
                    tem_termo_banido = True

            #se o nome do produto corresponder e não tiver termo banido
            if tem_palavra_do_produto and tem_termo_banido == False:
                if preco_minimo <= preco <= preco_maximo:
                    lista_ofertas_final.append((nome.title(), preco, link, 'Google Shopping'))
        except:
            continue

    lista_ofertas_final = set(lista_ofertas_final)
    lista_ofertas_final = list(lista_ofertas_final)
    
    return lista_ofertas_final 


def PesquisarProdutosAmazon(produto, termos_banidos, preco_minimo, preco_maximo):
    #Entrar no site
    nav = webdriver.Chrome(options=options, service=chrome_service, service_log_path=servico)    
    nav.get('https://www.amazon.com.br/')
    
    #Pesquisar pelo produto na Amazon
    nav.find_element(By.ID, 'twotabsearchtextbox').send_keys(produto)
    nav.find_element(By.ID, 'twotabsearchtextbox').send_keys(Keys.ENTER)
    time.sleep(5)
    
    lista_ofertas_final = [] 
    #Obter as informações do produto
    lista_info_produto = nav.find_elements(By.CLASS_NAME, 'sg-col-inner')

    #Para cada informação do produto
    for item in lista_info_produto:
        try:
            lista_termos_produto = produto.split(' ')
            lista_termos_banidos = termos_banidos.split(' ')

            #Tratando os dados do nome, preco e link
            nome = item.find_element(By.CLASS_NAME, 'a-size-base-plus').text.lower()
            termos_nome = nome.split(' ')
            preco = item.find_element(By.CLASS_NAME, 'a-price-whole').text
            preco = preco.replace('.', '') + '.' + item.find_element(By.CLASS_NAME, 'a-price-fraction').text
            preco = float(preco)
            link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')

            #verificação se o nome corresponde
            tem_palavra_do_produto = True
            for palavra in lista_termos_produto:
                if not palavra in nome:
                    tem_palavra_do_produto = False

            #verificação se o termo banido não está incluido
            tem_termo_banido = False
            for palavra in lista_termos_banidos:
                if palavra in termos_nome:
                    tem_termo_banido = True

            #se o nome do produto corresponder e não tiver termo banido
            if tem_palavra_do_produto and tem_termo_banido == False: 
                if preco_minimo <= preco <= preco_maximo:
                    lista_ofertas_final.append((nome.title(), preco, link, 'Amazon'))

        except:
            continue
    lista_ofertas_final = set(lista_ofertas_final)
    return 
    

def PesquisarProdutosMercadoLivre(produto, termos_banidos, preco_minimo, preco_maximo):
    #Entrando no site
    nav = webdriver.Chrome(options=options, service=chrome_service, service_log_path=servico)    
    nav.get('https://www.mercadolivre.com.br/')
    #Escrevendo o nome do produto
    nav.find_element(By.CLASS_NAME, 'nav-search-input').send_keys(produto)
    nav.find_element(By.CLASS_NAME, 'nav-search-input').send_keys(Keys.ENTER)
    time.sleep(5)
    
    lista_info_produto = nav.find_elements(By.CLASS_NAME, 'ui-search-result__wrapper') 
    lista_ofertas_final = []
    
    # Para cada informação do produto
    for item in lista_info_produto:
        try:

            lista_termos_produto = produto.split(' ')
            lista_termos_banidos = termos_banidos.split(' ')

            #Tratando os dados do nome, preco e link
            nome = item.find_element(By.CLASS_NAME, 'ui-search-item__title').text.lower()
            preco = item.find_element(By.CLASS_NAME, 'price-tag-fraction').text
            preco = preco.replace('.', '') + '.' + item.find_element(By.CLASS_NAME, 'price-tag-cents').text 
            preco = float(preco)
            link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')

            #verificação se o nome corresponde
            tem_palavra_do_produto = True
            for palavra in lista_termos_produto:
                if not palavra in nome:
                    tem_palavra_do_produto = False

            #verificação se o termo banido não está incluido
            tem_termo_banido = False
            for palavra in lista_termos_banidos:
                if palavra in nome:
                    tem_termo_banido = True

            #se o nome do produto corresponder e não tiver termo banido
            if tem_palavra_do_produto and tem_termo_banido == False:
                if preco_minimo <= preco <= preco_maximo:
                    lista_ofertas_final.append((nome.title(), preco, link, 'Mercado Livre'))
                    
        except:
            continue
    lista_ofertas_final = set(lista_ofertas_final)
    return lista_ofertas_final


def PesquisarProdutosMagazineLuiza(produto, termos_banidos, preco_minimo, preco_maximo):
    #Entrando no navegador e pesquisando
    nav = webdriver.Chrome(options=options, service=chrome_service, service_log_path=servico)    
    nav.get('https://www.magazineluiza.com.br/')

    nav.find_element(By.CLASS_NAME, 'hMjGCJ').send_keys(produto)
    nav.find_element(By.CLASS_NAME, 'hMjGCJ').send_keys(Keys.ENTER)
    time.sleep(5)

    lista_info_produto = nav.find_elements(By.CLASS_NAME, 'sc-gpcHMt')
    lista_ofertas_final = []

    for item in lista_info_produto:

        lista_termos_produto = produto.split(' ')
        lista_termos_banidos = termos_banidos.split(' ')
        try:

            #Tratando os dados do nome, preco e link
            nome  = item.find_element(By.TAG_NAME, 'h2').text.lower()
            preco = item.find_element(By.CLASS_NAME, 'bvdLco').text
            preco = preco.replace('R$', '').replace('.', '').replace(',', '.')
            preco = float(preco)
            link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')

            #verificação se o nome corresponde
            tem_palavra_do_produto = True
            for palavra in lista_termos_produto:
                if not palavra in nome:
                    tem_palavra_do_produto = False

            #verificação se o termo banido não está incluido
            tem_termo_banido = False
            for palavra in lista_termos_banidos:
                if palavra in nome:
                    tem_termo_banido = True

            #se o nome do produto corresponder e não tiver termo banido
            if tem_palavra_do_produto and tem_termo_banido == False:
                if preco_minimo <= preco <= preco_maximo:
                    lista_ofertas_final.append((nome.title(), preco, link, 'Magalu'))     
        except:
            continue
    lista_ofertas_final = set(lista_ofertas_final)
    return lista_ofertas_final 


def PesquisarProdutosAliExpress(produto, termos_banidos, preco_minimo, preco_maximo):
    tabela_ali_express = pd.DataFrame()
    
    nav = webdriver.Chrome(options=options, service=chrome_service, service_log_path=servico)    
    #Entrando no site do Ali Express
    nav.get('https://best.aliexpress.com/')

    #Buscando o nome do produto
    nav.find_element(By.CLASS_NAME, 'search-key').send_keys(produto)
    nav.find_element(By.ID, 'search-key').send_keys(Keys.ENTER)
    time.sleep(5)

    lista_info_produto = nav.find_elements(By.CLASS_NAME, '_3t7zg')

    #Tratando os termos banidos e o nome do produto
    lista_termos_banidos = termos_banidos.split(' ')
    lista_termos_produto = produto.split(' ') 

    lista_ofertas_final = []
    #Trantando os dados do produto
    for item in lista_info_produto:
        try:
            nome = item.find_element(By.CLASS_NAME, '_18_85').text.lower()
            lista_preco = item.find_elements(By.CLASS_NAME, 'mGXnE')
            preco = ''
            #Obtando o preço, pois o Ali Express separa cada fração
            for p in lista_preco:
                preco = preco + p.text
            preco = preco.replace(' ', '').replace('R$', '').replace('.', '').replace(',', '.')
            preco = float(preco)
            link = item.get_attribute('href')

            tem_nome_produto = True
            for palavra in lista_termos_produto:
                if not palavra in nome:
                    tem_nome_produto = False

            tem_termo_banido = False
            for palavra in lista_termos_banidos:
                if palavra in nome:
                    tem_termo_banido = True

            if tem_nome_produto and tem_termo_banido == False:
                if preco_minimo <= preco <= preco_maximo:
                    lista_ofertas_final.append((nome.title(), preco, link, 'Ali Express'))
        except:
            continue
    lista_ofertas_final = set(lista_ofertas_final)
    return lista_ofertas_final 


def PesquisarProdutosBuscape(produto, termos_banidos, preco_minimo, preco_maximo):
    #Entrando no site e pesquisando o produto
    nav = webdriver.Chrome(options=options, service=chrome_service, service_log_path=servico)    
    nav.get('https://www.buscape.com.br/')

    nav.find_element(By.XPATH, '//*[@id="new-header"]/div[1]/div/div/div[3]/div/div/div/div/div[1]/input').send_keys(produto)
    nav.find_element(By.XPATH, '//*[@id="new-header"]/div[1]/div/div/div[3]/div/div/div/div/div[1]/input').send_keys(Keys.ENTER)
    time.sleep(5)
    
    lista_info_produto = nav.find_elements(By.CLASS_NAME, 'Cell_CellBody__YODBS')

    #Tratando os termos banidos e o nome do produto
    lista_termos_banidos = termos_banidos.split(' ')
    lista_termos_produto = produto.split(' ') 
    lista_ofertas_final = []
    for item in lista_info_produto:
        try:
            nome = item.find_element(By.CLASS_NAME, 'Text_LabelSmRegular__qvxsr').text.lower()
            preco = item.find_element(By.CLASS_NAME, 'CellPrice_MainValue__JXsj_').text
            preco = preco.replace('R$', '').replace('.', '').replace(',', '.').replace(' ', '')
            preco = float(preco)
            link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')

            tem_nome_produto = True
            for palavra in lista_termos_produto:
                if not palavra in nome:
                    tem_nome_produto = False

            tem_termo_banido = False
            for palavra in lista_termos_banidos:
                if palavra in nome:
                    tem_termo_banido = True

            if tem_nome_produto and tem_termo_banido == False:
                if preco_minimo <= preco <= preco_maximo:
                    lista_ofertas_final.append((nome.title(), preco, link, 'Buscape'))
        except:
            continue
    lista_ofertas_final = set(lista_ofertas_final)
    return lista_ofertas_final


def TratarDados(produto, termos_banidos, preco_minimo, preco_maximo):
    
    validacao_produto = True
    validacao_termos_banidos = True 
    
    #Verificação do Produto digitado
    produto_info = tk.Label()
    if len(produto) > 0 and produto.isspace() == False and produto.isnumeric() == False:
        pass
    else:
        validacao_produto = False
    
    #Verificação dos termos banidos
    termosBan_info = tk.Label()
    if len(termos_banidos) > 0 and termos_banidos.isspace() == False:
        pass
    else:
        validacao_termos_banidos = False
        
    #Verificação do preço minimo
    validacao_precoMin = True
    if preco_minimo.isnumeric() == False or preco_minimo.isspace():
        validacao_precoMin = False
    
    #Verificação preço maximo
    validacao_precoMax = True
    if preco_maximo.isnumeric() == False or preco_maximo.isspace():
        validacao_precoMax = False
    
    if validacao_produto and validacao_termos_banidos and validacao_precoMin and validacao_precoMax:
        return True
    else:
        return False


def GuardarInfoProduto():
    global produto
    global preco_minimo
    global preco_maximo
    global termos_banidos
    
    
    produto = caixa_nome.get().strip()
    preco_minimo = caixa_preco_min.get()
    preco_maximo = caixa_preco_max.get()
    termos_banidos = caixa_termosBan.get().strip()
    
    tratar_dados = TratarDados(produto, termos_banidos, preco_minimo, preco_maximo )
    
    if tratar_dados:
        produto = caixa_nome.get().strip().lower()
        preco_minimo = int(caixa_preco_min.get())
        preco_maximo = int(caixa_preco_max.get())
        termos_banidos = caixa_termosBan.get().strip().lower()
        return True
    else:
        return False


def SalvarPlanilha():
    
    salvar_produto = GuardarInfoProduto()
    
    pesquisar = tkinter.messagebox.askokcancel(title='Pesquisar Produto', message='Deseja Pesquisar {}'.format(produto.title()))
    
    if salvar_produto and pesquisar:
        
        tabela_produtos_final = pd.DataFrame()
        lista_produtos_selecionados = [(escolha_amazon.get(), PesquisarProdutosAmazon, 'Amazon'),
                                       (escolha_google.get(), PesquisarProdutosGoogleShopping, 'Google'),
                                      (escolha_mercado_livre.get(), PesquisarProdutosMercadoLivre, 'Mercado Livre'),
                                       (escolha_magalu.get(), PesquisarProdutosMagazineLuiza, 'Magazine Luiza'),
                                      (escolha_ali_express.get(), PesquisarProdutosAliExpress, 'Ali Express'),
                                      (escolha_buscape.get(), PesquisarProdutosBuscape, 'Buscape')]
        
        qtde_selecionada = 0
        
        barra_progresso['value'] = 0 

        for escolha, funcao, site in lista_produtos_selecionados:
            if escolha == 1:
                qtde_selecionada += 1
        qtde_selecionada = 100 / qtde_selecionada
        
        for escolha_selecionada, busca_automatica, nome_site in lista_produtos_selecionados:
            try:
                if escolha_selecionada == 1:

                    barra_progresso['value'] += qtde_selecionada / 2

                    produtos_salvo = tk.Label(text='Pesquisando em {}'.format(nome_site), font=("Cambria", 11), fg= 'blue')
                    produtos_salvo.grid(row=14, column=0, columnspan=4, sticky='NWSE')

                    janela.update()

                    lista_temporaria = busca_automatica(produto, termos_banidos, preco_minimo, preco_maximo)

                    barra_progresso['value'] += qtde_selecionada / 2
                    janela.update()

                    tabela_temporaria = pd.DataFrame(lista_temporaria, columns=['Produto', 'Preço', 'Link', 'Site'])
                    tabela_produtos_final = pd.concat([tabela_produtos_final, tabela_temporaria])
            except:
                msg_erro = tkinter.messagebox.showerror(title='ERRO ENCONTRADO', message='Ops, aconteceu algum erro.')
                
        tabela_produtos_final = tabela_produtos_final.sort_values(by=['Preço'], ascending=True)
        tabela_produtos_final = tabela_produtos_final.reset_index(drop=True)
        tabela_produtos_final = tabela_produtos_final.sort_values(['Preço'], ascending=True)

        tipos_arquivos = [('Arquivo em Excel', '*.xlsx*')]  
        local_do_arquivo = asksaveasfile(filetypes = tipos_arquivos, defaultextension = '.xlsx')
        
        try:
            tabela_produtos_final.to_excel(local_do_arquivo.name, index=False)
            
            msg_final = tkinter.messagebox.showinfo(title='Pesquisar Concluida', message='Arquivo salvo em {}'.format(local_do_arquivo.name))
            
        except:
            
            mensagem_erro = tk.Label(text='Erro. Não foi escolhido um local para salvar.', font=("Cambria", 11), fg= 'red') 
            mensagem_erro.grid(row=14, column=0, columnspan=4, sticky='NWSE')
    else:
        
        produtos_salvo = tk.Label(text='Prencha os campos corretamente para prosseguir', font=("Cambria", 11), fg= 'red')
        produtos_salvo.grid(row=14, column=0, columnspan=4, sticky='NWSE')


def LimparDados():
    caixa_nome.delete(0, 1000)
    caixa_preco_min.delete(0, 1000)
    caixa_preco_max.delete(0, 1000)
    caixa_termosBan.delete(0, 1000)


#Titulo
janela = tk.Tk()
janela.resizable(width=0, height=0)
janela.title('Pesquisa de Produtos')
janela.rowconfigure(0, weight=1)
janela.columnconfigure(0, weight=1)

#Variaveis de armazenamento da checkbox
escolha_amazon = tk.IntVar()
escolha_google = tk.IntVar()
escolha_mercado_livre = tk.IntVar()
escolha_buscape = tk.IntVar()
escolha_americanas = tk.IntVar()
escolha_ali_express = tk.IntVar()
escolha_magalu = tk.IntVar()

#Iniciando o programa com todas os sites selecionados
escolha_amazon.set(1)
escolha_google.set(1)
escolha_mercado_livre.set(1)
escolha_buscape.set(1)
escolha_ali_express .set(1)
escolha_magalu.set(1)

#Nome do produto
texto_nome = tk.Label(text='Nome do Produto', font=("Cambria", 11))
texto_nome.grid(row=0, column=0, sticky='W')
caixa_nome = tk.Entry(width=30, font=("Cambria", 11))
caixa_nome.grid(row=0, column=1, sticky='NWSE')

#Preço Minimo
preco_min_texto = tk.Label(text='Preço Mínimo', font=("Cambria", 11))
preco_min_texto.grid(row=1, column=0, sticky='W')
caixa_preco_min = tk.Entry(font=("Cambria", 11))
caixa_preco_min.grid(row=1, column=1, sticky='NWSE')

#Preço Máximo
preco_max_texto = tk.Label(text='Preço Máximo', font=("Cambria", 11))
preco_max_texto.grid(row=2, column=0, sticky='W')
caixa_preco_max = tk.Entry(font=("Cambria", 11))
caixa_preco_max.grid(row=2, column=1, sticky='NWSE')

#Termos Banidos
termosBan_texto = tk.Label(text='Termos Banidos', font=("Cambria", 11))
termosBan_texto.grid(row=3, column=0, sticky='W')
caixa_termosBan = tk.Entry(font=("Cambria", 11))
caixa_termosBan.grid(row=3, column=1, sticky='NWSE')

#Botão Limpar dados digitados
limpar_dados_digitados = tk.Button(text='Limpar Dados', command= LimparDados, font=("Cambria", 11) )
limpar_dados_digitados.grid(row=4, column=0, sticky='NWSE', columnspan=4)

#Label dos sites disponiveis
titulo_site = tk.Label(text= 'Escolha os sites que deseja pesquisar', font=("Cambria", 11))
titulo_site.grid(row=5, column=0, sticky='NWSE', columnspan=2)

checkbox_amazon = tk.Checkbutton(text='Amazon', variable=escolha_amazon, font=("Cambria", 11))
checkbox_amazon.grid(row=6, column=0, sticky='W')

checkbox_google = tk.Checkbutton(text='Google Shopping', variable=escolha_google, font=("Cambria", 11))
checkbox_google.grid(row=7, column=0, sticky='W')

checkbox_mercado_livre = tk.Checkbutton(text='Mercado Livre', variable=escolha_mercado_livre, font=("Cambria", 11))
checkbox_mercado_livre.grid(row=8, column=0, sticky='W')

checkbox_buscape = tk.Checkbutton(text='Buscape', variable=escolha_buscape, font=("Cambria", 11))
checkbox_buscape.grid(row=9, column=0, sticky='W')

checkbox_ali_express = tk.Checkbutton(text='Ali Express', variable=escolha_ali_express, font=("Cambria", 11))
checkbox_ali_express.grid(row=11, column=0, sticky='W')

checkbox_magalu = tk.Checkbutton(text='Magazine Luiza', variable=escolha_magalu, font=("Cambria", 11))
checkbox_magalu.grid(row=12, column=0, sticky='W')
    
pesquisar_produtos = tk.Button(text='Pesquisar', command=SalvarPlanilha, width=20, height=1, font=("Cambria", 11))
pesquisar_produtos.grid(row=13, column=0, sticky='NSWE', columnspan=4)

barra_progresso = ttk.Progressbar(janela, mode='determinate', length= 100)
barra_progresso.grid(row=15, columnspan=4, column=0, sticky='NSWE')


janela.mainloop()