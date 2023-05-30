import json
import tkinter as tk

def save_file(classement,reponse_formations):
    with open("parcoursup.json","w",encoding="utf-8") as file:
        json.dump({"classement":classement,"reponse_formations": reponse_formations}, file, ensure_ascii=False, indent=4)
        file.close()

def read_file():
    with open("parcoursup.json","r",encoding="utf-8") as file:
        data = json.load(file)
        file.close()
    return data


class StrikethroughLabel:
    def __init__(self, master=None, text=""):
        self.canvas = tk.Canvas(master)
        self.text_item = self.canvas.create_text(2, 0, text=text, anchor="nw")
        self.update_strikethrough()

    def grid(self, **kwargs):
        self.canvas.grid(**kwargs)

    def update_strikethrough(self):
        bbox = self.canvas.bbox(self.text_item)
        if bbox:
            x1, y1, x2, y2 = bbox
            y = (y1 + y2) / 2
            self.strikethrough = self.canvas.create_line(x1, y, x2, y)
            self.canvas.tag_lower(self.strikethrough, self.text_item)
            # Set the size of the canvas to the size of the text
            self.canvas.config(width=x2-x1, height=y2-y1)


class GaleShapleyEleve:
    def __init__(self, classement, rep_forma):
        self.classement = list(classement)
        self.rep_forma = list(rep_forma)
        self.formation_definitive = False
        self.formation_accept = None 

    def process_formation(self):
        """Méthode permettant de trouver l'ensemble des formations qu'il est nécessaire de garder ainsi que la formation qu'il faut accepter (provisoirement/définitivement)"""
        if not self.formation_definitive:
            i = 0
            while i < len(self.classement):
                if self.rep_forma[i] == "non":
                    if self.formation_accept == self.rep_forma[i]:
                        self.formation_accept = None
                    self.classement.pop(i)
                    self.rep_forma.pop(i)
                    if self.process_formation():  
                        return True
                elif self.rep_forma[i] == "oui":
                    if i == 0:
                        self.formation_accept = self.classement[i]
                        self.formation_definitive = True
                        self.classement = self.classement[:1]
                        self.rep_forma=self.rep_forma[:1]
                        return True
                    else:
                        self.formation_accept = self.classement[i]
                        self.classement = self.classement[:i+1]
                        self.rep_forma = self.rep_forma[:i+1]
                        return True
                else:
                    i += 1 
        return False

    def retour_gui(self):
        """Méthode renvoyant un tuple qui sera lu par l'application"""
        return (self.classement,self.formation_accept,self.formation_definitive)
