import PySimpleGUI as sg
import psycopg2
from datetime import timedelta, date
data_hj = date.today()
data10 = data_hj + timedelta(days=10)
# print(f"Current date: {data_hj.strftime('%d/%m/%Y')}")
# print(f"Date 10 days from now (date only): {data10.strftime("%d/%m/%Y")}")

def limpar():
    try:
        window['-ID-'].update('')
        window['-NOME-'].update('')
        window['-FONE-'].update('')
        window['-EMAIL-'].update('')
        window['-WHATS-'].update('')
        window['-SEXO-'].update('')
        window['-CPFCNPJ-'].update('')
        window['-TIPO-'].update(False)
        window['-END-'].update('')
    except Exception as e: 
        sg.popup(f"Erro ao limpar campos de cliente: {e}")
        window.refresh()
    
def limparP():
    try:
        window['-IDPED-'].update('')
        window['-IDCLIENT-'].update('')
        window['-VALOR-'].update('')
        window['-QUANT-'].update('')
        window['-PRAZO-'].update('')
        window['-DATA-'].update('')
        window['-DESC-'].update('')
        window['-STATUS-'].update('')
    except Exception as e:
        sg.popup(f"Erro ao limpar campos de pedido: {e}")
        window.refresh()

def atualiza():
    if len(lista) == 0:
        limpar()
    else:
        try:
            window['-ID-'].update( lista[indice][0] )
            window['-NOME-'].update( lista[indice][1] )
            window['-FONE-'].update( lista[indice][2] )
            window['-EMAIL-'].update( lista[indice][3] )
            window['-WHATS-'].update(lista[indice][4])
            window['-SEXO-'].update(lista[indice][5])
            window['-CPFCNPJ-'].update(lista[indice][6])
            window['-TIPO-'].update(lista[indice][7] == 'Pessoa Jurídica')
            window['-END-'].update(lista[indice][8])
        except Exception as e:
            sg.popup(f"Erro ao atualizar campos de cliente: {e}")
            window.refresh()

def atualizaP():
    if len(lista) == 0:
        limparP()
    else:
        try:
            window['-IDPED-'].update(lista[indice][0])
            window['-IDCLIENT-'].update(lista[indice][1])
            window['-VALOR-'].update(lista[indice][2])
            window['-QUANT-'].update(lista[indice][3])
            window['-PRAZO-'].update(lista[indice][4])
            window['-DATA-'].update(lista[indice][5])
            window['-DESC-'].update(lista[indice][6])
            window['-STATUS-'].update(lista[indice][7])
        except Exception as e:
            sg.popup(f"Erro ao atualizar campos de pedido: {e}")
            window.refresh()

def todos_clientes():
    try:
        global indice
        global lista
        resposta = []
        with con:
            with con.cursor() as cursor:
                cursor.execute("SELECT * FROM cliente;")
                resposta = cursor.fetchall()
        lista.clear()
        for i in range(len(resposta)):
            lista.append( list(resposta[i]) )

        sg.popup('Quantidade de registros: ' + str(len(resposta)))
        indice = 0
        atualiza()
    except Exception as e:
        sg.popup(f"Erro ao procurar todos os clientes: {e}")
        window.refresh()

def todos_pedidos():
    try:
        global indice
        global lista
        respostap = []
        with con:
            with con.cursor() as cursor:
                cursor.execute("SELECT * FROM pedido;")
                respostap = cursor.fetchall()
        lista.clear()
        for i in range(len(respostap)):
            lista.append( list(respostap[i]) )

        sg.popup('Quantidade de registros: ' + str(len(respostap)))
        indice = 0
        atualizaP()
    except Exception as e:
        sg.popup(f"Erro ao procurar todos os pedidos: {e}")
        window.refresh()

# Inicialização BD
con = psycopg2.connect(host="localhost", database="tapecaria", user="postgres", password="78540307", port="5433")
with con:
    with con.cursor() as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS cliente (
            id_cliente SERIAL PRIMARY KEY,
            nome_cliente VARCHAR(60) NOT NULL,
            fone_cliente NUMERIC(13) NOT NULL,
            email_cliente VARCHAR(50),
            whats_cliente NUMERIC(13),
            sexo_cliente CHAR(2) CHECK(sexo_cliente IN ('M', 'F', 'NA')),  -- Masc; Fem; Não Atribuído
            cpfcnpj_cliente VARCHAR(14) UNIQUE, -- Evita muitas linhas vazias
            tipo_cliente VARCHAR(15) CHECK(tipo_cliente IN ('Pessoa Física', 'Pessoa Jurídica')),
            end_cliente VARCHAR(225)
            );
            CREATE TABLE IF NOT EXISTS pedido (
                id_pedido SERIAL PRIMARY KEY,
                id_cliente INTEGER NOT NULL,
                valor_pedido NUMERIC(7,2) NOT NULL,
                quant_pedido NUMERIC(7) NOT NULL DEFAULT(1),
                prazo_entrega DATE,
                data_pedido DATE NOT NULL DEFAULT(current_date),
                descricao_pedido VARCHAR(350) NOT NULL,
                status_pedido VARCHAR(50) DEFAULT 'Em andamento',
                FOREIGN KEY(id_cliente) REFERENCES cliente(id_cliente)
            );""")

lista=[]
indice = 0

tab1_layout = [
    [
        sg.Text("ID:", size=(8, 1)),
        sg.Input(size=(6, 1), key="-ID-", focus=False, disabled=True)
    ],
    [
        sg.Text("Nome*:", size=(8, 1)),
        sg.InputText(size=(40, 1), key="-NOME-", focus=True)
    ],
    [
        sg.Text("Celular* (apenas números):", size=(19, 1)),
        sg.Input(size=(27, 1), enable_events=True, key="-FONE-")

    ],
    [
        sg.Text("E-mail:", size=(8, 1)),
        sg.InputText(size=(40, 1), key="-EMAIL-")
    ],
    [
        sg.Text("WhatsApp (apenas números):", size=(22, 1)),
        sg.Input(size=(24, 1), key="-WHATS-")
    ],
    [
        sg.Text("Sexo:", size=(22, 1)),
        # sg.InputText(size=(33, 1), key="-SEXO-"),
        sg.Combo(['Masculino', 'Feminino', 'Não Atribuído'], default_value='Não Atribuído', key='-SEXO-', readonly=True)
    ],
    [
        sg.Text("CPF/CNPJ (apenas números):", size=(22, 1)),
        sg.Input(size=(24, 1), key="-CPFCNPJ-")
    ],
    [
        sg.Checkbox('Pessoa Jurídica', default=False, key="-TIPO-")
    ],
    [
        sg.Text("Endereço:", size=(8, 1)),
        sg.InputText(size=(40, 1), key="-END-")
    ],
    [
        sg.Text("* Campos obrigatórios", size=(20, 1))
    ],
    [
        sg.Button('Limpar', size=(8, 1), key="-LIMPAR-"),
        sg.Button('Inserir', size=(8, 1), key="-INSERIR-"),
        sg.Button('Atualizar', size=(8, 1), key="-ATUALIZAR-"),
        sg.Button('Remover', size=(8, 1), key="-REMOVER-")
    ],
    [
        sg.Button('<<', size=(8, 1), key="-<<-"),
        sg.Button('Procurar nome', size=(8, 2), key="-PROCURAR-"),
        sg.Button('Todos', size=(8, 1), key="-TODOS-"),
        sg.Button('>>', size=(8, 1), key="->>-")
    ]
]

# window = sg.Window("Cadastro de clientes", layout, use_default_focus=False)   
tab2_layout = [
    [
        sg.Text("ID do Pedido:", size=(12, 1)),
        sg.Input(size=(10, 1), key="-IDPED-", focus=False, disabled=True)
    ],
    [
        sg.Text("ID do Cliente*:", size=(12, 1)),
        sg.Input(size=(10, 1), key="-IDCLIENT-", focus=True)
    ],
    [
        sg.Text("Valor do Pedido*:", size=(12, 1)),
        sg.Input(size=(15, 1), key="-VALOR-")
    ],
    [
        sg.Text("Quantidade:", size=(12, 1)),
        sg.Input(size=(10, 1), default_text='1', key="-QUANT-")
    ],
    [
        sg.Text("Prazo de Entrega (DD-MM-AAAA):", size=(25, 1)),
        sg.Input(size=(15, 1), key="-PRAZO-")
    ],
    [
        sg.Text("Data do Pedido (DD-MM-AAAA):", size=(25, 1)),
        sg.Input(size=(15, 1), key="-DATA-", default_text=data_hj)
    ],
    [
        sg.Text("Descrição do Pedido*:", size=(15, 1)),
        sg.InputText(size=(40, 1), key="-DESC-")
    ],
    [
        sg.Text("Status do Pedido:", size=(15, 1)),
        # sg.InputText(size=(30, 1), key="-STATUS-")
        sg.Combo(['Em andamento', 'Finalizado', 'Cancelado'], default_value='Em andamento', key='-STATUS-', readonly=True)
    ],
    [
        sg.Text("* Campos obrigatórios", size=(20, 1))
    ],
    [
        sg.Button('Limpar', size=(8, 1), key="-LIMPARP-"),
        sg.Button('Inserir', size=(8, 1), key="-INSERIRP-"),
        sg.Button('Atualizar', size=(8, 1), key="-ATUALIZARP-"),
        sg.Button('Remover', size=(8, 1), key="-REMOVERP-")
    ],
    [
        sg.Button('<<', size=(8, 1), key="-<<P-"),
        sg.Button('Procurar descrição', size=(8, 2), key="-PROCURARP-"),
        sg.Button('Todos', size=(8, 1), key="-TODOSP-"),
        sg.Button('>>', size=(8, 1), key="->>P-")
    ]
]
layout = [[sg.TabGroup([[sg.Tab('Cadastro de clientes', tab1_layout), sg.Tab('Cadastro de pedidos', tab2_layout)]])]]    

window = sg.Window("Cadastros", layout, use_default_focus=False) 
# , default_element_size=(12,1))

# Run the Event Loop
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    elif event == "-LIMPAR-":
        limpar()
    elif event == "-LIMPARP-":
        limparP()
    elif event == "-INSERIR-":
        with con:
            with con.cursor() as cursor:
                try:
                    fone = values['-FONE-'] if values['-FONE-'] else None
                    whats = values['-WHATS-'] if values['-WHATS-'] else None
                    cpfcnpj = values['-CPFCNPJ-'] if values['-CPFCNPJ-'] else None
                    sexo = values['-SEXO-'] if values['-SEXO-'] else 'Não Atribuído'
                    tipo = 'Pessoa Jurídica' if values['-TIPO-'] else 'Pessoa Física'
                    cursor.execute("INSERT INTO cliente (nome_cliente, fone_cliente, email_cliente, whats_cliente, sexo_cliente, cpfcnpj_cliente, tipo_cliente, end_cliente) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_cliente;",
                        (values['-NOME-'], fone, values['-EMAIL-'], whats, sexo, values['-CPFCNPJ-'], tipo, values['-END-']))
                except Exception as e:
                    sg.popup(f"Erro ao inserir cliente: {e}")
                    window.refresh()
            con.commit()
        limpar()
    elif event == "-INSERIRP-":
        with con:
            with con.cursor() as cursor:
                try:
                    id_cliente = values['-IDCLIENT-'] if values['-IDCLIENT-'] else None
                    valor= float(values['-VALOR-'].replace(',', '.')) if values['-VALOR-'] else 0.0
                    quant= values['-QUANT-'] if values['-QUANT-'] else 1
                    prazo = values['-PRAZO-'] if values['-PRAZO-'] else data10
                    data = values['-DATA-'] if values['-DATA-'] else data_hj
                    status = values['-STATUS-'] if values['-STATUS-'] else 'Em andamento'
                    cursor.execute("INSERT INTO pedido (id_cliente, valor_pedido, quant_pedido, prazo_entrega, data_pedido, descricao_pedido, status_pedido) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_pedido;",
                        (id_cliente, valor, quant, prazo, data, values['-DESC-'], status))
                except Exception as e:
                    sg.popup(f"Erro ao inserir pedido: {e}")
                    window.refresh()
            con.commit()
        limparP()
    elif event == "-ATUALIZAR-":
        with con:
            with con.cursor() as cursor:
                try:
                    fone = values['-FONE-'] if values['-FONE-'] else None
                    whats = values['-WHATS-'] if values['-WHATS-'] else None
                    cpfcnpj = values['-CPFCNPJ-'] if values['-CPFCNPJ-'] else None
                    sexo = values['-SEXO-'] if values['-SEXO-'] else 'Não Atribuído'
                    tipo = 'Pessoa Jurídica' if values['-TIPO-'] else 'Pessoa Física'
                    cursor.execute("UPDATE cliente SET nome_cliente = %s, fone_cliente = %s, email_cliente = %s, whats_cliente = %s, sexo_cliente = %s, cpfcnpj_cliente = %s, tipo_cliente = %s, end_cliente = %s WHERE id_cliente = %s",
                        (values['-NOME-'], fone, values['-EMAIL-'], whats, sexo, cpfcnpj, tipo, values['-END-'], values['-ID-']))
                except Exception as e:
                    sg.popup(f"Erro ao atualizar cliente: {e}")
                    window.refresh()
        lista[indice] = [values['-ID-'], values['-NOME-'], values['-FONE-'], values['-EMAIL-'], values['-WHATS-'], values['-SEXO-'], values['-CPFCNPJ-'], tipo, values['-END-']]
    elif event == "-ATUALIZARP-":
        with con:
            with con.cursor() as cursor:
                try:
                    id_cliente = values['-IDCLIENT-'] if values['-IDCLIENT-'] else None
                    valor= float(values['-VALOR-'].replace(',', '.')) if values['-VALOR-'] else 0.0
                    quant= values['-QUANT-'] if values['-QUANT-'] else 1
                    prazo = values['-PRAZO-'] if values['-PRAZO-'] else data10
                    data = values['-DATA-'] if values['-DATA-'] else data_hj
                    status = values['-STATUS-'] if values['-STATUS-'] else 'Em andamento'
                    cursor.execute("UPDATE pedido SET id_cliente = %s, valor_pedido = %s, quant_pedido = %s, prazo_entrega = %s, data_pedido = %s, descricao_pedido = %s, status_pedido = %s WHERE id_pedido = %s",
                        (id_cliente, valor, quant, prazo, data, values['-DESC-'], status, values['-IDPED-']))
                except Exception as e:
                    sg.popup(f"Erro ao atualizar pedido: {e}")
                    window.refresh()
        lista[indice] = [values['-IDPED-'], values['-IDCLIENT-'], values['-VALOR-'], values['-QUANT-'], values['-PRAZO-'], values['-DATA-'], values['-DESC-'], values['-STATUS-']]
    elif event == "-REMOVER-":
        with con:
            with con.cursor() as cursor:
                try:
                    cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (values['-ID-'],))
                except Exception as e:
                    sg.popup(f"Erro ao remover cliente: {e}")
                    window.refresh()
        lista.pop(indice)
        indice -= 1

        atualiza()
    elif event == "-REMOVERP-":
        with con:
            with con.cursor() as cursor:
                try:
                    cursor.execute("DELETE FROM pedido WHERE id_pedido = %s", (values['-IDPED-'],))
                except Exception as e:
                    sg.popup(f"Erro ao remover pedido: {e}")
                    window.refresh()
        lista.pop(indice)
        indice -= 1
        atualizaP()
    elif event == "-PROCURAR-":
        with con:
            with con.cursor() as cursor:
                try:
                    cursor.execute("SELECT * FROM cliente WHERE nome_cliente LIKE %s;",
                        ('%'+values['-NOME-']+'%',))
                    resposta = cursor.fetchall()
                    lista.clear()
                    for i in range(len(resposta)):
                        lista.append( list(resposta[i]) )
                    sg.popup('Quantidade de registros: ' + str(len(resposta)))
                    indice = 0
                    atualiza()
                except Exception as e:
                    sg.popup(f"Erro ao procurar cliente: {e}")
                    window.refresh()
    elif event == "-PROCURARP-":
        with con:
            with con.cursor() as cursor:
                try:
                    cursor.execute("SELECT * FROM pedido WHERE descricao_pedido LIKE %s;",
                        ('%'+values['-DESC-']+'%',))
                    resposta = cursor.fetchall()
                    lista.clear()
                    for i in range(len(resposta)):
                        lista.append( list(resposta[i]) )
                    sg.popup('Quantidade de registros: ' + str(len(resposta)))
                    indice = 0
                    atualizaP()
                except Exception as e:
                    sg.popup(f"Erro ao procurar pedido: {e}")
                    window.refresh()
    elif event == "-TODOS-":
        todos_clientes()
    elif event == "-TODOSP-":
        todos_pedidos()
    elif event == "->>-":
        indice += 1
        if indice >= len(lista): indice = len(lista)-1
        atualiza()
    elif event == "->>P-":
        indice += 1
        if indice >= len(lista): indice = len(lista)-1
        atualizaP()
    elif event == "-<<-":
        indice -= 1
        if indice <= 0: indice = 0
        atualiza()
    elif event == "-<<P-":
        indice -= 1
        if indice <= 0: indice = 0
        atualizaP()

window.close()

while True:    
    event, values = window.read()    
    print(event,values)    
    if event == sg.WIN_CLOSED:           # always,  always give a way out!    
        break  

# Fazer as mudanças para a base persistente
con.commit()

# Fechar a comunicação com o servidor
cursor.close()
con.close()