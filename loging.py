# Cripto App logging system

from customtkinter import (CTk, CTkFrame, CTkEntry, CTkButton, CTkLabel, CTkCheckBox,
                           set_appearance_mode, CTkToplevel, CTkImage)
from tkinter import PhotoImage
from PIL import Image, ImageTk

# Colors
COLOR_BLACK = ("#010101")
COLOR_PURPLE = ("#7f5af0")
COLOR_GREEN = ("#2cb67d")
COLOR_GOLDEN = ("#CDA434")

color_black = ("#010101")
color_golden = ("#CDA434")

 

class Frame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure([0,1], weight = 1)
        self.rowconfigure([0,1,2,3], weight = 1)
        
        # Images
        self.image = Image.open("./Images/logo_full.png")
        self.img = self.image.resize((386, 195), )
        self.logo = ImageTk.PhotoImage(self.img)


        ### Add widgets onto the frame ##

        #Logos central picture
        self.label = CTkLabel(master=self, image = self.logo, text="").grid(columnspan = 2, row = 0)

        #Entry user:
        self.user = CTkEntry(self, placeholder_text = 'User', border_color = color_golden,
                            fg_color = color_black, width = 220, 
                            height = 40)
        self.user.grid(columnspan = 2, row = 2, padx = 4, pady = 0)

        # Entry Password:
        self.password = CTkEntry(self, placeholder_text = 'Password', border_color = color_golden, 
                                fg_color = color_black, width = 220, 
                                height = 40)
        self.password.grid(columnspan = 2, row = 3, padx = 4, pady = 4)

        

        



class Loging(CTkToplevel):
    def __init__(self):
        # Configuate window
        super().__init__()
        set_appearance_mode("Dark")
        self.geometry("450x600+720+150")
        self.resizable(False, False)
        self.title("Wellcome to CriptoAPP ")
        self.config(bg = color_black)
        self.iconbitmap("./Images/logo_s.ico")

        # Configurate column and row
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)

        # Create frame
        self.frame = Frame(master=self, fg_color = color_black)
        self.frame.grid(column = 0, row = 0, sticky = 'nsew', padx = 40, pady = 90)


if __name__ == "__main__":
    loging = Loging()
    loging.mainloop()