from tkinter import *

window = Tk()

class Application():
    def __init__(self):
        #Função principal da aplicação
        self.window = window
        self.screen()
        self.screen_frames()
        self.buttons()
        window.mainloop()

    def screen(self):
        # Criando a janela da aplicação
        self.window.title("R.I.M.S")
        self.window.configure(background='#1e3743')
        self.window.geometry('700x500')
        self.window.resizable(True, True)
        self.window.maxsize(width= 900, height= 700)
        self.window.minsize(width= 400, height= 300)

    def screen_frames(self):
        # Criando frame da área de busca
        self.search_frame = Frame(self.window, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness= 3)
        self.search_frame.place(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.46)
        #Criando frame da área das informações em formato de tabela
        self.table_frame = Frame(self.window, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness= 3)
        self.table_frame.place(relx= 0.02, rely= 0.5, relwidth= 0.96, relheight= 0.46)

    def buttons(self):
        # Criando botão Limpar
        self.bt_clean = Button(self.search_frame, text= 'Limpar')
        self.bt_clean.place(relx= 0.2, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        # Criando botão Buscar
        self.bt_search = Button(self.search_frame, text= 'Buscar')
        self.bt_search.place(relx= 0.3, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        # Criando botão Novo
        self.bt_new = Button(self.search_frame, text= 'Novo')
        self.bt_new.place(relx= 0.6, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        # Criando botão Alterar
        self.bt_change = Button(self.search_frame, text= 'Alterar')
        self.bt_change.place(relx= 0.7, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        # Criando botão Apagar
        self.bt_delete = Button(self.search_frame, text= 'Apagar')
        self.bt_delete.place(relx= 0.8, rely= 0.1, relwidth= 0.1, relheight= 0.15)

Application()