# CriptoApp

from customtkinter import (CTk, set_appearance_mode, CTkButton, CTkFrame, CTkLabel, CTkTextbox, CTkEntry, CTkToplevel)
import _tkinter as tk
import tkinter
from tkinter import filedialog
from tkinter import messagebox as MessageBox
from loging import Loging
import funtion as fn
from tkinter import PhotoImage
from PIL import Image, ImageTk


COLOR_BLACK = ("#010101")
COLOR_PURPLE = ("#7f5af0")
COLOR_GREEN = ("#2cb67d")
COLOR_GOLDEN = ("#CDA434")

# Colors
color_black = ("#010101")
color_golden = ("#CDA434")
color_gray = ("#696969")

# Global variables
mode = None
new_file_name = None
file_name = None
barcode = None
password = None


# Frame where the user can deside the mode to use (encrypt or decrypt)
class Frame_menu(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure([0,1,], weight = 1)
        self.rowconfigure([0,1,2,3], weight = 1)

        ### Frame widgets ###
        self.encrypt_btn = CTkButton(master=self, border_color=color_golden, fg_color=color_black, text="Encrypt",
                            hover_color= color_golden, corner_radius= 12, border_width=2, width= 500, height= 100,
                            command=self.encrypt_btn_click)
        self.encrypt_btn.grid(columnspan = 4, row = 1, padx = 0, pady = 0)

        self.decrypt_btn = CTkButton(master=self, border_color=color_golden, fg_color= color_black, text="Decrypt",
                            hover_color=color_golden, corner_radius= 12, border_width=2, width= 500, height= 100,
                            command=self.decrypt_btn_click)
        self.decrypt_btn.grid(columnspan = 4, row = 2, padx = 0, pady = 0)

    # Methods
    def decrypt_btn_click(self):
        global mode
        mode = "decrypt"
        process_frame()

    def encrypt_btn_click(self):
        global mode
        mode = "encrypt"
        process_frame()

class Frame_mode(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)

        self.frame_doc = CTkFrame(master=self, fg_color = color_black, width=500, height= 200)
        self.frame_doc.grid(column = 0, row = 0, sticky = 'nsew', padx = 30, pady = 0)

        self.frame_widgets = CTkFrame(master=self, fg_color = color_black, width=500, height= 200)
        self.frame_widgets.grid(column = 0, row = 1, sticky = 'nsew', padx = 30, pady = 30)


        self.document_text_box = CTkTextbox(master=self.frame_doc, width=900, height= 372, corner_radius=12,)
        self.document_text_box.grid(column=0, row=0, sticky = 'nsew', padx = 0, pady = 0)
        self.document_text_box.insert("0.0",f"{mode.capitalize()}:\n\n")

        self.document_file_btn = CTkButton(master=self.frame_widgets, border_color=color_golden, fg_color=color_black,
                            text=f"Select the file you want to {mode}", hover_color= color_golden, corner_radius= 12,
                            border_width=2, width= 240, height= 30, command=self.document_name)
        self.document_file_btn.grid(column = 0, row = 0, padx = 0, pady = 2.5)

        self.new_file_btn = CTkButton(master=self.frame_widgets, border_color=color_golden, fg_color=color_black,
                            text=f"Select how to save the {mode}ed file", hover_color= color_golden, corner_radius= 12,
                            border_width=2,  width= 240, height= 30,
                            command=self.new_document_name)
        self.new_file_btn.grid(column = 0, row = 1, padx = 0, pady = 2.5)

        self.start_process_btn = CTkButton(master=self.frame_widgets, border_color=color_golden, fg_color=color_golden,
                            text=f"{mode.capitalize()}", hover_color= color_golden, corner_radius= 12,
                            border_width=3, width= 165, height= 75, 
                            command=validation)
        self.start_process_btn.grid(column = 0, row = 3, padx = 0, pady = 0)
        self.start_process_btn.place(relx=0.815, rely=0.695, anchor=tkinter.SW)

        self.barcode_btn = CTkButton(master=self.frame_widgets, border_color=color_golden, fg_color=color_black,
                            text=f"Scan barcode", hover_color= color_golden, corner_radius= 12,
                            border_width=2, width= 240, height= 30, command=self.take_barcode)
        self.barcode_btn.grid(column = 0, row = 2, padx = 0, pady = 2.5)

        self.barcode_entry = CTkEntry(self.frame_widgets, placeholder_text = "Barcode", border_color = color_golden,
                            fg_color = color_black, width = 240, height = 30, corner_radius= 12)
        self.barcode_entry.grid(column = 1, row = 2, padx = 2, pady = 2.5)
        barcode = self.barcode_entry

        self.password_entry = CTkEntry(self.frame_widgets, placeholder_text = f"Password", border_color = color_golden,
                            fg_color = color_black, width = 240, height = 30, corner_radius= 12, show = "•" )
        self.password_entry.grid(column = 2, row = 2, padx = 2, pady = 2.5)
        


        self.come_back_btn = CTkButton(master=self.frame_widgets, border_color=color_gray, fg_color=color_black,
                            text=f"Come Back", hover_color= color_gray, corner_radius= 10,
                            border_width=2, width= 165, height= 25,
                            command=menu_frame)
        self.come_back_btn.place(relx=0.815, rely=0.95, anchor=tkinter.SW)

    #METHODS
    def document_name(self):
        global file_name
        # Ask the user for a file
        file_name = filedialog.askopenfilename(title="Selec the file", filetypes=(("Text files", "*.txt"), ("All file", "*")))
        try: # If file is not found, raise an error.
            with open(file_name, "r", encoding="utf-8") as file:
                file.close()
        except FileNotFoundError:
            MessageBox.showerror("Error", "File not found.")

        else: # If the file name is too long, just print SELECTED.
            if len(file_name) > 70:
                self.label_doc_name = CTkLabel(master=self.frame_widgets, text="Selected")
                self.label_doc_name.place(relx=0.2760, rely=0.16, anchor=tkinter.W)
            else:
                self.label_doc_name = CTkLabel(master=self.frame_widgets, text=file_name)
                self.label_doc_name.place(relx=0.2760, rely=0.16, anchor=tkinter.W)

            # Show the file content in screen.
            show_doc_text(file_name, self)

    def new_document_name(self):
        global new_file_name
        new_file_name = filedialog.asksaveasfilename(title="Selec the directory and write the name", defaultextension=("*.txt"))
        if len(new_file_name) > 70:
            self.label_doc_name = CTkLabel(master=self.frame_widgets, text="Selected")
            self.label_doc_name.place(relx=0.2760, rely=0.50, anchor=tkinter.W)
        else:
            self.label_doc_name = CTkLabel(master=self.frame_widgets, text=new_file_name)
            self.label_doc_name.place(relx=0.2760, rely=0.50, anchor=tkinter.W)

    def take_barcode(self):
        global barcode
        try:
            barcode = fn.scan_barcode()
        except ValueError:
            MessageBox.showerror("Error", "Cannot open camera.")
        except IndexError:
            MessageBox.showerror("Error", "Can't receive frames")
        else:
            self.barcode_entry.insert(0, barcode)

    
class Wait_window(CTkToplevel):
    def __init__(self):
        # Configuate window
        super().__init__()
        set_appearance_mode("Dark")
        self.geometry("300x150+720+150")
        self.resizable(False, False)
        self.title("In process")
        self.config(bg = color_black)
        self.iconbitmap("./Images/logo_s.ico")

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)

        self.label_txt = CTkLabel(master=self, text="This may take several minutes", fg_color=color_black)
        self.label_txt.place(relx=0.2460, rely=0.16, anchor=tkinter.W)





class CriptoApp(CTk):
    def __init__(self):
        # Configuate window
        super().__init__()
        set_appearance_mode("Dark")
        self.geometry("960x540+500+150")
        self.resizable(False, False)
        self.title("CriptoAPP")
        self.config(bg = color_black)
        self.iconbitmap("./Images/logo_s.ico")
        self.withdraw()

        # Configurate column and row
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)



    ####### Configuration used in loging window:
        self.toplevel_window = Loging()
        self.bt_start = CTkButton(master=self.toplevel_window.frame, border_color= color_golden, fg_color= color_black, 
                                  text="Sign up", hover_color= color_golden, corner_radius= 12, border_width=2, 
                                  command=self.logging_button_click)
        self.bt_start.grid(columnspan = 2, row = 4, padx = 4, pady = 10)

    # Methods used in loging window (used to close the window)
    def logging_button_click(self):
        self.toplevel_window.destroy()
        self.frame = Frame_menu(master=self, fg_color = color_black, width= 1000, height = 200)
        self.frame.grid(column = 0, row = 0, sticky = 'nsew', padx = 40, pady = 90)
        self.deiconify()
    ########



# Funtion that validates 
def validation():
    global barcode, password
    try: # Validate is the barcode is a int and is higher than 1
        barcode = int(app.frame.barcode_entry.get())
        if barcode < 1:
            raise ValueError
    except ValueError:
        MessageBox.showerror("Error", "Invalid barcode.")
        return ("Error", "Invalid barcode.")

    else: # Validate if there is a password
        password = app.frame.password_entry.get()
        if password == None or password == "" or len(password) < 5:
            MessageBox.showerror("Error", "Invalid password.")
            return ("Error", "Invalid password.")
        else:
            star_process(barcode, password)

# Funtion that call the encrypt or decrypt funtion in funtion.py
def star_process(barcode, passWord):
    app.toplevel_window = Wait_window()
    try:
        if mode == "encrypt":
            fn.mode_encrypt(password=passWord, bar_code= barcode, document_file=file_name, new_file=new_file_name)
            app.toplevel_window.destroy()
        if mode == "decrypt":
            fn.mode_decrypt(password=passWord, bar_code= barcode, document_file=file_name, new_file=new_file_name)
            app.toplevel_window.destroy()
    except TypeError: # Check if the files selected excist.
        MessageBox.showerror("Error", "No files selected.")
        app.toplevel_window.destroy()
    else:
        show_doc_text(doc=new_file_name, app= app.frame, condition="done")

# Change the frame to the process frame
def process_frame():
    app.frame = Frame_mode(master=app,fg_color = color_black, width= 1000, height = 200)
    app.frame.grid(column = 0, row = 0, sticky = 'nsew', padx = 0, pady = 0)

# Change the frame to menu
def menu_frame():
    app.frame = Frame_menu(master=app, fg_color = color_black, width= 1000, height = 200)
    app.frame.grid(column = 0, row = 0, sticky = 'nsew', padx = 0, pady = 0)

    global mode, new_file_name, file_name, barcode
    mode = None
    new_file_name = None
    file_name = None
    barcode = None

    return "Done"

# Funtion that writes the file content in the text box
def show_doc_text(doc, app, condition = "first"):
    # Reset the text box.
    app.document_text_box = CTkTextbox(master=app.frame_doc, width=900, height= 305, corner_radius=12,)
    app.document_text_box.grid(column=0, row=0, sticky = 'nsew', padx = 0, pady = 0)

    with open(doc, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines[::-1]:
            app.document_text_box.insert(f"0.0",f"{line}\n")
        if condition == "first":
            app.document_text_box.insert(f"0.0", f"{mode.capitalize()}:\n\n")
        elif condition == "done":
            app.document_text_box.insert(f"0.0", f"{mode.capitalize()} done:\n\n")

# Connections to the funtion file to be accepted by CS50
def create_key_C(password, bar_code, doc_name = "document.txt"):
    return fn.create_keys(password, bar_code, doc_name)

# Optional and non-essential funtions if you want to add a register option
def cap_user(user):
    user = str(user)
    return user

def cap_password(password):
    password = str(password)
    return password


if __name__ == "__main__":
    # Start loging window
    app = CriptoApp()
    app.mainloop()




