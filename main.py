import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
from fonctions import save_file, read_file, GaleShapleyEleve, StrikethroughLabel
import webbrowser

class MainApp:
    def __init__(self, root, voeux=[], reponses=[]):
        self.root = root
        self.voeux = voeux
        self.reponses = reponses
        img_up = Image.open("./assets/arrow_up_icon.png").resize((20,20))
        self.img_up = ImageTk.PhotoImage(img_up)
        img_down = Image.open("./assets/arrow_down_icon.png").resize((20,20))
        self.img_down = ImageTk.PhotoImage(img_down)
        img_trash = Image.open("./assets/trash_icon.png").resize((20,20))
        self.img_trash = ImageTk.PhotoImage(img_trash)
        img_github = Image.open("./assets/github_icon.png").resize((20,20))
        self.img_github = ImageTk.PhotoImage(img_github)

    def create_voeux(self):

        self.root.bind('<Return>',lambda e: self.nouveau_voeu()) # quand on appuie sur enter valide le texte mis dans la combo box

        self.frame_main = tk.Frame(self.root)
        self.frame_main.pack(expand=True, fill="both")

        self.title = tk.Label(self.frame_main,text="Classement", font=("MS Sans Serif", 20))
        self.title.pack(side="top")

        self.frame_top = tk.Frame(self.frame_main,borderwidth=1, relief="groove")
        self.frame_top.pack(side="top", fill="x")

        self.frame_bottom = tk.Frame(self.frame_main)
        self.frame_bottom.pack(side="top", fill="both", expand=True, pady=(10,0))

        self.canvas_voeux = tk.Canvas(self.frame_bottom, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.frame_bottom, orient="vertical", command=self.canvas_voeux.yview)
        self.scrollbar.pack(side="right", fill='y')

        self.canvas_voeux.pack(side="left", fill='both', expand=True)
        self.canvas_voeux.configure(yscrollcommand=self.scrollbar.set)

        self.frame_voeux = tk.Frame(self.canvas_voeux)
        self.canvas_voeux.create_window((0,0), window=self.frame_voeux, anchor="nw")
        self.frame_voeux.bind('<Configure>', lambda e: self.canvas_voeux.configure(scrollregion=self.canvas_voeux.bbox("all")))

        self.user_input = tk.StringVar()
        self.entry = tk.Entry(self.frame_top, textvariable=self.user_input)
        self.entry.grid(row=0, column=0, padx=(50, 10), pady=20, sticky='ew')

        self.frame_top.grid_columnconfigure(0, weight=1)

        self.entry_button = tk.Button(self.frame_top, text='Créer voeu', command=self.nouveau_voeu)
        self.entry_button.grid(row=0, column=1, padx=(20,50), pady=20)

        self.solution_button = tk.Button(self.frame_top, text='Afficher solution', bg='green', command=lambda:[self.frame_main.destroy(),self.create_solution()])
        self.solution_button.grid(row=1,column=0, padx=(130,0), pady=(0,20))

        self.frame_buttons = tk.Frame(self.frame_bottom) # frame en bas de la fenêtre pour mettre des boutons
        self.frame_buttons.pack(side="bottom", fill="x")

        self.reset_button = tk.Button(self.frame_buttons, text='RESET', bg='red', command=self.reset)
        self.reset_button.pack(side="right")

        self.github_button = tk.Button(self.frame_buttons, image=self.img_github, command=lambda: webbrowser.open('https://github.com/Ikseno')) # ouvre mon github :)
        self.github_button.pack(side="left")

        if self.voeux == []:
            vide_label = tk.Label(self.frame_voeux,text="Vous n'avez pas encore enregistré vos voeux")
            vide_label.grid(row=0,column=0,sticky="n",padx=50,pady=50)
        else:
            for i, (voeux, reponse) in enumerate(zip(self.voeux, self.reponses), start=1):
                label_voeux = tk.Label(self.frame_voeux, text=str(i) + ". " + voeux)
                
                # combobox
                combo_reponse = ttk.Combobox(self.frame_voeux, state="readonly", values=["oui", "en attente", "non", "none"])
                combo_reponse.set(reponse)
                combo_reponse.bind('<<ComboboxSelected>>', lambda e, voeux=i-1, combo=combo_reponse: self.combobox_change(voeux, combo.get()))
 
                # arrow up
                arrow_up = tk.Button(self.frame_voeux, image=self.img_up, command=lambda voeux=i-1: self.decaler_voeux("up", voeux))

                # arrow down 
                arrow_down = tk.Button(self.frame_voeux, image=self.img_down, command=lambda voeux=i-1: self.decaler_voeux("down", voeux))

                # trash
                trash = tk.Button(self.frame_voeux, image=self.img_trash, command=lambda voeux=i-1: self.delete_voeu(voeux))

                label_voeux.grid(row=i, column=0, sticky='w', pady=(10,0))
                combo_reponse.grid(row=i, column=1, sticky='e',padx=(10,0), pady=(10,0))
                arrow_up.grid(row=i, column=2, sticky='e', padx=(10,0), pady=(10,0))
                arrow_down.grid(row=i,column=3,sticky='e', pady=(10,0))
                trash.grid(row=i,column=4, sticky='e',padx=(10,0), pady=(10,0))
                
    def create_solution(self):
        self.frame_main2 = tk.Frame(self.root)
        self.frame_main2.pack(expand=True, fill="both")

        self.title = tk.Label(self.frame_main2,text="Solution", font=("MS Sans Serif", 20))
        self.title.pack(side="top")

        self.frame_top = tk.Frame(self.frame_main2,borderwidth=1, relief="groove")
        self.frame_top.pack(side="top", fill="x")

        self.frame_bottom = tk.Frame(self.frame_main2)
        self.frame_bottom.pack(side="top", fill="both", expand=True, pady=(10,0))

        self.canvas_voeux = tk.Canvas(self.frame_bottom, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.frame_bottom, orient="vertical", command=self.canvas_voeux.yview)
        self.scrollbar.pack(side="right", fill='y')

        self.canvas_voeux.pack(side="left", fill='both', expand=True)
        self.canvas_voeux.configure(yscrollcommand=self.scrollbar.set)

        self.frame_voeux = tk.Frame(self.canvas_voeux)
        self.canvas_voeux.create_window((0,0), window=self.frame_voeux, anchor="nw")
        self.frame_voeux.bind('<Configure>', lambda e: self.canvas_voeux.configure(scrollregion=self.canvas_voeux.bbox("all")))

        self.frame_top.columnconfigure(0, weight=1)
        self.frame_top.rowconfigure(0, weight=1)

        self.retour_button = tk.Button(self.frame_top, text='Retour au classement', bg='blue', command=lambda:[self.frame_main2.destroy(),self.create_voeux()])
        self.retour_button.grid(row=0, column=0, pady=20)

        self.github_button = tk.Button(self.frame_bottom, image=self.img_github, command=lambda: webbrowser.open('https://github.com/Ikseno')) # ouvre mon github :)
        self.github_button.pack(side="bottom")

        if self.voeux == []:
            vide_label = tk.Label(self.frame_voeux,text="Vous n'avez pas encore enregistré vos voeux")
            vide_label.grid(row=0,column=0,sticky="n",padx=50,pady=50)
        else:
            algo = GaleShapleyEleve(self.voeux,self.reponses)
            algo.process_formation()

            algo_voeux, formation_accept, definitive = algo.retour_gui()
            
            for i, (voeu, reponse) in enumerate(zip(self.voeux, self.reponses), start=1):
                if voeu == formation_accept:
                    label_voeu = tk.Label(self.frame_voeux, text=str(i) + ". " + voeu)
                    if definitive:
                        label_action = tk.Label(self.frame_voeux,text="Accepter définitivement ce voeu", fg="green")
                    else:
                        label_action = tk.Label(self.frame_voeux,text="Accepter provisoirement ce voeu", fg="green")
                    label_voeu.grid(row=i, column=0, sticky='w', pady=(10,0))
                    label_action.grid(row=i, column=1, sticky='w', pady=(10,0))

                elif voeu not in algo_voeux or reponse == "oui":
                    label_voeu = StrikethroughLabel(self.frame_voeux, text=str(i) + ". " + voeu)
                    label_voeu.grid(row=i, column=0, sticky='w', pady=(10,0), padx=(0,10))
                    if reponse == "en attente" or reponse == "oui" or reponse == "none":
                        label_action = tk.Label(self.frame_voeux,text="Renoncer à ce voeu", fg="red")
                        label_action.grid(row=i, column=1, sticky='w', pady=(10,0))
                    else:
                        label_action = tk.Label(self.frame_voeux,text="La formation ne vous veut pas", fg="red")
                        label_action.grid(row=i, column=1, sticky='w', pady=(10,0))
                elif reponse == "en attente":
                    label_voeu = tk.Label(self.frame_voeux, text=str(i) + ". " + voeu)
                    label_action = tk.Label(self.frame_voeux,text="Maintenir ce voeu en attente", fg="blue")
         
                    label_voeu.grid(row=i, column=0, sticky='w', pady=(10,0))
                    label_action.grid(row=i, column=1, sticky='w', pady=(10,0))
                elif reponse=="non":     # si reponse formation est non et qu'on a accepté un voeu
                    label_voeu = StrikethroughLabel(self.frame_voeux, text=str(i) + ". " + voeu)
                    label_voeu.grid(row=i, column=0, sticky='w', pady=(10,0), padx=(0,10))
                    label_action = tk.Label(self.frame_voeux,text="La formation ne vous veut pas", fg="red")
                    label_action.grid(row=i, column=1, sticky='w', pady=(10,0))
                else: # si reponse == None
                    label_voeu = tk.Label(self.frame_voeux, text=str(i) + ". " + voeu)
                    label_action = tk.Label(self.frame_voeux,text="La formation ne vous a pas encore répondu", fg="grey")
         
                    label_voeu.grid(row=i, column=0, sticky='w', pady=(10,0))
                    label_action.grid(row=i, column=1, sticky='w', pady=(10,0))

    def nouveau_voeu(self):
        text = self.user_input.get()
        if text:  # pour éviter d'avoir des voeux vides
            self.voeux.append(text)
            self.reponses.append('none')
            save_file(self.voeux,self.reponses) # sauvegarde sur fichier .json
            self.frame_main.destroy()
            self.create_voeux()
        self.entry.focus_set()
    
    def delete_voeu(self,voeux):
        self.voeux.pop(voeux)
        self.reponses.pop(voeux)
        save_file(self.voeux,self.reponses) # sauvegarde sur fichier .json
        self.frame_main.destroy()
        self.create_voeux()

    def decaler_voeux(self,direction,voeux):
        if direction == "up":
            if voeux == 0:
                self.voeux.append(self.voeux.pop(voeux))
                self.reponses.append(self.reponses.pop(voeux))
            else:
                self.voeux.insert(voeux-1, self.voeux.pop(voeux))
                self.reponses.insert(voeux-1, self.reponses.pop(voeux))
        else:
            if voeux == len(self.voeux)-1:
                self.voeux.insert(0,self.voeux.pop(-1))
                self.reponses.insert(0,self.reponses.pop(-1))
            else:
                self.voeux.insert(voeux+1, self.voeux.pop(voeux))
                self.reponses.insert(voeux+1, self.reponses.pop(voeux))
        save_file(self.voeux,self.reponses) # sauvegarde sur fichier .json
        self.frame_main.destroy()
        self.create_voeux()
    
    def combobox_change(self,voeux,reponse):
        self.reponses[voeux]=reponse
        self.frame_voeux.focus_set() # retire le surlignage bleu 
        save_file(self.voeux,self.reponses) # sauvegarde sur fichier .json

    def reset(self):
        reponse_alerte = messagebox.askyesno("Reset", "Etes-vous sûr de vouloir supprimer toutes vos entrées ?")
        if reponse_alerte:
            self.voeux = []
            self.reponses = []
            save_file([],[])
            self.frame_main.destroy()
            self.create_voeux()

    

def main():
    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # simule la taille de la taskbar
    taskbar_height = 100

    window_width = min(1024, screen_width)
    window_height = min(768, screen_height - taskbar_height)

    root.geometry("%dx%d" % (window_width, window_height))
    root.title("Parcoursup Helper")
    root.iconbitmap("./assets/favicon.ico")
    
    # lis le fichier .json pour récupérer la liste des voeux et des réponses
    dico = read_file() 
    classement = dico["classement"]
    reponse_formations = dico["reponse_formations"]

    app = MainApp(root,classement,reponse_formations)
    app.create_voeux()

    root.mainloop()

if __name__ == '__main__':
    main()