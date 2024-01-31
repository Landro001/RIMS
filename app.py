from tkinter import *
from tkinter import ttk
import sqlite3

window = Tk()

class Functions():
    def clean_entrys(self):
        # Limpar o conteúdo escrito nos inputs
        self.code_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.department_entry.delete(0, END)
        self.note_entry.delete(0, END)

    def bd_connect(self):
        # Faz a conexão ao banco de dados
        self.conn = sqlite3.connect('radios.bd')
        self.cursor = self.conn.cursor()
        print("Conectando ao banco de dados")

    def bd_disconnect(self):
        # Desconecta do bando de dados
        self.conn.close()
        print("Desconectando do banco de dados")

    def assemble_tables(self):
        # Monta as tabelas no bando de dados
        self.bd_connect()
        # Cria a tabela
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS radios (
                code INTEGER PRIMARY KEY,
                customer_name CHAR(40) NOT NULL,
                phone INTEGER(20),
                department CHAR(30),
                observations TEXT
            )
        ''')
        self.conn.commit()
        print('Banco de dados criado')
        self.bd_disconnect()

    def entry_vars(self):
        # Variáveis para os inputs
        self.code = self.code_entry.get()
        self.name = self.name_entry.get()
        self.phone = self.phone_entry.get()
        self.department = self.department_entry.get()
        self.notes = self.note_entry.get()

    def on_double_click(self, event):
        # Ao clicar duas vezes em um item da tabela, os dados são inseridos nos inputs
        self.clean_entrys()
        self.radio_list.selection()

        for n in self.radio_list.selection():
            col1, col2, col3, col4, col5 = self.radio_list.item(n, 'values')
            self.code_entry.insert(END, col1)
            self.name_entry.insert(END, col2)
            self.phone_entry.insert(END, col3)
            self.department_entry.insert(END, col4)
            self.note_entry.insert(END, col5)
    
    def add_customer(self):
        # Adiciona a partir dos inputs requeridos ao usuário um novo cliente no banco de dados
        self.entry_vars()
        self.bd_connect()

        self.cursor.execute(''' INSERT INTO radios (customer_name, phone, department, observations) 
                            VALUES (?, ?, ?, ?)''', (self.name, self.phone, self.department, self.notes))
        self.conn.commit()
        self.bd_disconnect()
        self.select_list()
        self.clean_entrys()

    def delete_customer(self):
        # Deleta um cliente do banco de dados
        self.entry_vars()
        self.bd_connect()
        self.cursor.execute('''DELETE FROM radios WHERE code = ?''', (self.code))
        self.conn.commit()
        self.bd_disconnect()
        self.clean_entrys()
        self.select_list()

    def change_customer(self):
        # Altera as informações de um cliente no banco de dados
        self.entry_vars()
        self.bd_connect()
        self.cursor.execute('''UPDATE radios SET customer_name = ?, phone = ?, department = ?, observations = ? WHERE code = ?''', (self.name, self.phone, self.department, self.notes, self.code))
        self.conn.commit()
        self.bd_disconnect()
        self.select_list()
        self.clean_entrys()

    def select_list(self):
        # Lista as informações salvas no bando de dados na tabela de apresentação
        self.radio_list.delete(*self.radio_list.get_children())
        self.bd_connect()
        list = self.cursor.execute(''' SELECT code, customer_name, phone, department, observations FROM radios 
                                   ORDER BY code ASC; ''')
        for i in list:
            self.radio_list.insert('', END, values=i)
        self.bd_disconnect()

    def search_customer(self):
        self.bd_connect()
        self.radio_list.delete(*self.radio_list.get_children())

        self.name_entry.insert(END, '%')
        nome = self.name_entry.get()
        self.cursor.execute(
            '''SELECT code, customer_name, phone, department, observations FROM radios WHERE customer_name LIKE "%s" ORDER BY code ASC''' % nome)
        search_name_customer = self.cursor.fetchall()
        for i in search_name_customer:
            self.radio_list.insert('', END, values=i)
        self.clean_entrys()
        self.bd_disconnect()

class Application(Functions):
    def __init__(self):
        #Função principal da aplicação
        self.window = window
        self.screen()
        self.screen_frames()
        self.widgets_search_frame()
        self.list_table_frame()
        self.assemble_tables()
        self.select_list()
        self.menus()
        window.mainloop()

    def screen(self):
        # Criando a janela da aplicação
        self.window.title("R.I.M.S")
        self.window.configure(background='#1e3743')
        self.window.geometry('700x500')
        self.window.resizable(True, True)
        self.window.maxsize(width= 900, height= 700)
        self.window.minsize(width= 500, height= 400)

    def screen_frames(self):
        # Criando frame da área de busca
        self.search_frame = Frame(self.window, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness= 3)
        self.search_frame.place(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.46)
        #Criando frame da área das informações em formato de tabela
        self.table_frame = Frame(self.window, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness= 3)
        self.table_frame.place(relx= 0.02, rely= 0.5, relwidth= 0.96, relheight= 0.46)

    def widgets_search_frame(self):
        # Criando botão Limpar
        self.bt_clean = Button(self.search_frame, text= 'Limpar', 
                               bd= 2, bg= '#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command= self.clean_entrys)
        self.bt_clean.place(relx= 0.3, rely= 0.1, relwidth= 0.1, relheight= 0.15)

        # Criando botão Buscar
        self.bt_search = Button(self.search_frame, text= 'Buscar',
                                bd= 2, bg= '#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command= self.search_customer)
        self.bt_search.place(relx= 0.4, rely= 0.1, relwidth= 0.1, relheight= 0.15)

        # Criando botão Novo
        self.bt_new = Button(self.search_frame, text= 'Novo',
                             bd= 2, bg= '#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command= self.add_customer)
        self.bt_new.place(relx= 0.6, rely= 0.1, relwidth= 0.1, relheight= 0.15)

        # Criando botão Alterar
        self.bt_change = Button(self.search_frame, text= 'Alterar',
                                bd= 2, bg= '#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command= self.change_customer)
        self.bt_change.place(relx= 0.7, rely= 0.1, relwidth= 0.1, relheight= 0.15)

        # Criando botão Apagar
        self.bt_delete = Button(self.search_frame, text= 'Apagar',
                                bd= 2, bg= '#107db2', fg= 'white', font= ('verdana', 8, 'bold'), command= self.delete_customer)
        self.bt_delete.place(relx= 0.8, rely= 0.1, relwidth= 0.1, relheight= 0.15)

        # Criando label e input do código do rádio
        self.lb_code = Label(self.search_frame, text='Código do rádio', bg= '#dfe3ee', fg='#107db2')
        self.lb_code.place(relx= 0.05, rely= 0.05)

        self.code_entry = Entry(self.search_frame, relief= 'groove')
        self.code_entry.place(relx= 0.05, rely= 0.15, relwidth= 0.2)

        # Criando label e input do nome
        self.lb_name = Label(self.search_frame, text='Nome', bg= '#dfe3ee', fg='#107db2')
        self.lb_name.place(relx= 0.05, rely= 0.35)

        self.name_entry = Entry(self.search_frame, relief= 'groove')
        self.name_entry.place(relx= 0.05, rely= 0.45, relwidth= 0.4)

        # Criando label e input do telefone
        self.lb_phone = Label(self.search_frame, text='Telefone', bg= '#dfe3ee', fg='#107db2')
        self.lb_phone.place(relx= 0.5, rely= 0.35)

        self.phone_entry = Entry(self.search_frame, relief= 'groove')
        self.phone_entry.place(relx= 0.5, rely= 0.45, relwidth= 0.4)

        # Criando label e input do setor
        self.lb_department = Label(self.search_frame, text='Setor', bg= '#dfe3ee', fg='#107db2')
        self.lb_department.place(relx= 0.05, rely= 0.6)

        self.department_entry = Entry(self.search_frame, relief= 'groove')
        self.department_entry.place(relx= 0.05, rely= 0.7, relwidth= 0.4)

        # Criando label e input do observação
        self.lb_note = Label(self.search_frame, text='Observações', bg= '#dfe3ee', fg='#107db2')
        self.lb_note.place(relx= 0.5, rely= 0.6)

        self.note_entry = Entry(self.search_frame, relief= 'groove')
        self.note_entry.place(relx= 0.5, rely= 0.7, relwidth= 0.4, relheight= 0.2)

    def list_table_frame(self):
        # Criando a listagem das informações em formato de tabela
        self.radio_list = ttk.Treeview(self.table_frame, height= 3, columns=("col1", "col2", "col3", "col4", "col5"))
        self.radio_list.heading('#0', text='')
        self.radio_list.heading('#1', text='Código')
        self.radio_list.heading('#2', text='Nome')
        self.radio_list.heading('#3', text='Telefone')
        self.radio_list.heading('#4', text='Setor')
        self.radio_list.heading('#5', text='Observações')

        self.radio_list.column('#0', width= 1)
        self.radio_list.column('#1', width= 50)
        self.radio_list.column('#2', width= 135)
        self.radio_list.column('#3', width= 125)
        self.radio_list.column('#4', width= 100)
        self.radio_list.column('#5', width= 150)

        self.radio_list.place(relx= 0.01, rely= 0.1, relwidth= 0.95, relheight= 0.85)
        
        #Criando a scrool bar da tabela
        self.scrool_list = Scrollbar(self.table_frame, orient='vertical')
        self.radio_list.configure(yscroll= self.scrool_list.set)
        self.scrool_list.place(relx= 0.96, rely= 0.1, relwidth= 0.03, relheight= 0.85)
        self.radio_list.bind('<Double-1>', self.on_double_click)

    def menus(self):
        # Criando o menu da aplicação
        menu_bar = Menu(self.window)
        self.window.config(menu=menu_bar)
        options_menu = Menu(menu_bar)
        about_menu = Menu(menu_bar)

        # Função para sair da aplicação
        def Quit(): self.window.destroy()

        # Criando as opções do menu
        menu_bar.add_cascade(label='Opções', menu=options_menu)
        menu_bar.add_cascade(label='Sobre', menu=about_menu)

        options_menu.add_command(label= 'Sair', command= Quit)
        about_menu.add_command(label='Limpa Entradas', command= self.clean_entrys)
        

        





Application()