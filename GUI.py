import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MyGUI:

    def __init__(self):
        
        self.root = tk.Tk()

        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Close", command=self.on_closing)
        #self.filemenu.add_separator()
        self.filemenu.add_command(label="Save current model", command=self.save)

        self.actionmenu = tk.Menu(self.menubar, tearoff=0)
        self.actionmenu.add_command(label="Create new Agent", command= self.createObj("Agent"))
        self.actionmenu.add_command(label="Create new Component", command= self.createObj("Component"))
        self.actionmenu.add_command(label="Create new Environment", command= self.createObj("Environment"))
        
        self.menubar.add_cascade(menu=self.filemenu, label="File")
        self.menubar.add_cascade(menu=self.actionmenu, label="Create")
        #self.menubar.add_cascade(menu=self.filemenu , label="file")
        self.root.config(menu=self.menubar)

        self.buttonAddGraph = tk.Button(self.root, text="Click to generate graph", font=("Arial",18), command= self.addGraph)
        self.buttonAddGraph.pack(padx= 20, pady= 20)
        
        self.label = tk.Label(self.root, text="Your Message", font = ("Arial", 18))
        self.label.pack(padx= 20, pady= 20)

        self.textbox = tk.Text(self.root, height= 5, font= ("Arial", 18))
        self.textbox.bind("<KeyPress>",self.shortcut)
        self.textbox.pack(padx= 10, pady= 10)

        self.check_state = tk.IntVar() 

        self.check = tk.Checkbutton(self.root, text="Show messageBOX", font = ("Arial", 18) ,  variable= self.check_state)
        self.check.pack(padx= 10, pady=10)

        self.button = tk.Button(self.root, text= "Show message", font= ("Arial", 18), command= self.show_message)
        self.button.pack(padx= 10, pady= 10)

        self.clearbtn = tk.Button(self.root, text="Clear", font=("Arial", 18), command=self.clear)
        self.clearbtn.pack(padx= 10, pady= 10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def show_message(self):
        if self.check_state.get() == 0:
            print(self.textbox.get("1.0", tk.END))
        else:
            messagebox.showinfo(title="Messgae", message= self.textbox.get("1.0", tk.END))

    def shortcut(self, event):
        if event.state == 12 and event.keysym == "Return":
            self.show_message()

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you reall want to quit?"):
            self.root.destroy()
    def clear(self):
        self.textbox.delete("1.0", tk.END)
    
    def save(self):
        #Add saving feature here
        pass

    def createObj(self, value):
        #Add create function here
        pass

    def addGraph(self):
        
        data2 = {'Years': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
         'No. Population': [100, 200*1.6, 200*1.6*1.6, 200*1.6*1.6*1.6, 500, 600*1.6, 700*1.4, 800*1.3, 900*1.1, 1000*0.7]
         }  
        df2 = pd.DataFrame(data2)

        figure2 = plt.Figure(figsize=(5, 4), dpi=100)
        ax2 = figure2.add_subplot(111)
        line2 = FigureCanvasTkAgg(figure2, self.root)
        line2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)
        df2 = df2[['Years', 'No. Population']].groupby('Years').sum()
        df2.plot(kind='line', legend=True, ax=ax2, color='r', marker='o', fontsize=10)
        ax2.set_title('Year Vs. No. Population')

MyGUI()
