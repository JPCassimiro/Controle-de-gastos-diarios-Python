
import customtkinter as ctk
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import functools
import operator
from PIL import ImageGrab
import pygetwindow as gw
from tkinter import Listbox


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Tracker")
root.geometry("875x525")

class TrackerApp:
    def __init__(self, root):
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        frameFather = ctk.CTkFrame(root, corner_radius=10)
        frameFather.pack(padx=20,pady=20,fill="both",expand=True)

        self.listRows = []

        #campos
        self.categoriesVar = ctk.StringVar()
        self.categories = [
        "Aluguel", "Animais", "Assinaturas", "Comida", "Educação", 
        "Energia", "Entretenimento", "Gás", "Higiene Pessoal", "Lazer", 
        "Limpeza", "Manutenção", "Outros", "Investimentos", 
        "Saúde", "Seguros", "Internet", "Transporte", "Utensílios", "Vestuário"]
        self.nameField = ctk.CTkEntry(frameFather,width=110)
        self.nameField.grid(row=2,column=0,sticky="N")
        self.amountField = ctk.CTkEntry(frameFather,width=80)
        self.amountField.grid(row=2,column=1,sticky="N")
        self.catCombobox = ctk.CTkComboBox(frameFather,width=125,variable=self.categoriesVar, values=self.categories, state='readonly')
        self.catCombobox.grid(row=2,column=2,sticky="N")
        ctk.CTkLabel(frameFather,text="Nome").grid(row=1,column=0,sticky="N")
        ctk.CTkLabel(frameFather,text="Custo(Usar ponto)").grid(row=1,column=1,sticky="N")
        ctk.CTkLabel(frameFather,text="Categoria").grid(row=1,column=2,sticky="N")

        #botao entrar
        ctk.CTkButton(frameFather, text="Adicionar",command=self.addList).grid(row=2,column=3,sticky="N")
        
        #remover
        ctk.CTkButton(frameFather,text="Remover",command=self.removeList).grid(row=2,column=4,sticky="N")

        #lista
        self.listBoxAmount = Listbox(frameFather,justify='center',bg='#1d1e1e',fg='white',selectbackground="#106a43",relief="flat",borderwidth=0,highlightthickness=0)
        self.listBoxAmount.grid(row=3,column=0,columnspan=3,sticky='NSEW')
        
        #data
        self.date = DateEntry(frameFather, width=9)
        self.date.grid(row=1,column=4,sticky="N")
        self.dateVariable = self.date.get_date()
            
        #chart
        self.frameChart = ctk.CTkFrame(frameFather,border_width=2,corner_radius=1)
        self.frameChart.grid(row=3,column=3,columnspan=3,sticky='NSEW')
        self.plot()
        
        #total
        self.totalValue = ctk.DoubleVar()
        self.totalLabel = ctk.CTkLabel(frameFather,text='Total:')
        self.totalLabel.grid(row=4,column=0,sticky="w")
        
        self.totalEntry = ctk.CTkEntry(frameFather,state='readonly',textvariable=self.totalValue)
        self.totalEntry.grid(row=4,column=1,sticky="w")
        
        #salvar
        ctk.CTkButton(frameFather,text="Salvar como imagem",command=self.printScreen).grid(row=4,column=4,sticky="S")
        
        for child in frameFather.winfo_children(): 
            child.grid_configure(padx=10, pady=10)

        
    #funçoes
    def addList(self):
        try:
            name = self.nameField.get()
            cost = float(self.amountField.get())
            category = self.categoriesVar.get()

            if name and category:
                self.listRows.append({"name": name, "amount": cost, "category": category})
                self.listBoxAmount.insert("end", f"{name} - R$ {cost:.2f} - {category}")
                self.plot()
            else:
                messagebox.showwarning("Entrada inválida", "Por favor, preencha todos os campos corretamente.")
        except ValueError:
            messagebox.showwarning("Entrada inválida", "O custo deve ser um número válido.")

    def removeList(self):
        selectedRow = self.listBoxAmount.curselection()
        self.listRows.pop(selectedRow[0])
        self.listBoxAmount.delete(selectedRow)
        self.plot()
        
    def plot(self):
        for elements in self.frameChart.winfo_children():
            elements.destroy()

        subtotal = {}
        for itens in self.listRows:
            category = itens['category']
            subtotal[category] = subtotal.get(category,0) + itens['amount']
            
        labels = subtotal.keys()
        sizes = subtotal.values()
        
        fig, ax = plt.subplots()
        ax.pie(sizes, autopct="%1.1f%%", startangle=90,textprops={'size': 'smaller'})
        ax.axis("equal")
        ax.legend(labels=labels,loc='upper right',fontsize=7,bbox_to_anchor=(1.605,1.15))
        fig.set_size_inches(3,3)
        fig.subplots_adjust(right=0.66)
        
        chart = FigureCanvasTkAgg(fig,self.frameChart)
        chart.get_tk_widget().pack()
        
        totalArray = list(subtotal.values())
        if totalArray:
            self.totalValue.set(functools.reduce(operator.add,totalArray))
            
    def printScreen(self):
        self.getWindow()
        left,top = self.window.topleft
        right, bottom = self.window.bottomright
        self.dateVariable = self.date.get_date()
        shot = ImageGrab.grab(bbox=(left,top,right,bottom))
        shot.save(f"Gastos_{self.dateVariable}.PNG")
        shot.close()

    def getWindow(self):
        self.window = gw.getWindowsWithTitle("Tracker")[0]

TrackerApp(root)
root.mainloop()