from revivals.revival import Revival
import revivals.all
import os 
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox

def install_ui(revival_id):
    revival_ent = init_revival(revival_id)
    print("You have selected '%s'" % revival_ent.name)
    print("1) Install")
    print("2) Uninstall")
    print("3) Install DXVK")
    option_id = int(input())
    if option_id == 1:
        revival_ent.install()
        os.system("update-desktop-database ~/.local/share/applications")
    elif option_id == 2:
        revival_ent.uninstall()
    elif option_id == 3:
        revival_ent.install_dxvk()

def init_revival(revival_id):
    revival_sel = Revival.__subclasses__()[revival_id]
    revival_ent = revival_sel.__new__(revival_sel)
    revival_ent.__init__()
    revival_ent.setup_vars()
    Revival.setup_vars(revival_ent) # so the super can setup all the other vars we need
    return revival_ent

def tk_install_revival_callback(list : tk.Listbox, panel : tk.Frame):
    revival = init_revival(list.curselection()[0])
    revival.install()
    list.selection_set(list.curselection()[0])
    os.system("update-desktop-database ~/.local/share/applications")

def tk_uninstall_revival_callback(list : tk.Listbox, panel : tk.Frame):
    revival = init_revival(list.curselection()[0])
    revival.uninstall()
    list.selection_set(list.curselection()[0])

def tk_install_dxvk_callback(list : tk.Listbox, panel : tk.Frame):
    revival = init_revival(list.curselection()[0])   
    if not os.path.exists("dxvk.tar.gz"):
        messagebox.showwarning("WineORC v2: DXVK Warning", "WineORC will download DXVK from https://github.com/doitsujin/dxvk/releases/download/v2.0/dxvk-2.0.tar.gz. This is a ~7MB file.")
    revival.install_dxvk()    
    list.selection_set(list.curselection()[0])


def tk_list_onselect(x, list : tk.Listbox, panel : tk.Frame):
    revival = init_revival(list.curselection()[0])
    if revival:
        panel.pack(side=tk.TOP)
        inst_label = panel.children['install_label']
        inst_button = panel.children['install_button']
        uninst_button = panel.children['uninstall_button']
        instdxvk_button = panel.children['install_dxvk_button']
        if revival.installed():
            inst_label.config(text="This revival is installed.")
            inst_button["state"] = "disabled"
            uninst_button["state"] = "normal"
            instdxvk_button["state"] = "normal"
        else:
            inst_label.config(text="This revival is uninstalled.")
            inst_button["state"] = "normal"
            uninst_button["state"] = "disabled"
            instdxvk_button["state"] = "disabled"

if __name__ == "__main__":
    window = tk.Tk()
    window.wm_title("WineORC v2")

    revival_panel = tk.PanedWindow()
    revival_panel.pack(fill=tk.BOTH,expand=1)

    options_panel = tk.Frame(revival_panel)
    options_panel.pack_forget()

    revivals_list = tk.Listbox(revival_panel)
    cur_id = 0
    for cls in Revival.__subclasses__():
        revivals_list.insert(cur_id, cls.__name__)
        cur_id += 1
    revivals_list.bind("<<ListboxSelect>>", lambda x, revivals_list=revivals_list, options_panel=options_panel: tk_list_onselect(x, revivals_list, options_panel))
    revivals_list.pack(side=tk.LEFT)

    install_label = tk.Label(options_panel, name="install_label", text="This revival is uninstalled.")
    install_label.pack()
    install_button = tk.Button(options_panel, name="install_button", text="Install", command=lambda: tk_install_revival_callback(revivals_list, options_panel))
    install_button.pack()
    uninstall_button = tk.Button(options_panel, name="uninstall_button", text="Uninstall", command=lambda: tk_uninstall_revival_callback(revivals_list, options_panel))
    uninstall_button.pack()
    install_dxvk_button = tk.Button(options_panel, name="install_dxvk_button", text="Install DXVK", command=lambda: tk_install_dxvk_callback(revivals_list, options_panel))
    install_dxvk_button.pack()

    desc = tk.Label(text="WineORC v2, written by Ryelow (https://github.com/floralrainfall/wineorc-rebirth)")
    desc.pack()

    window.mainloop()
#    print("WineORC v2.0 by Ryelow")
#    print("Select a revival")
#    print("NOTICE: Make sure you have xdg and wine before installing with this utility.")
#    while True:
#        cur_id = 0
#        for cls in Revival.__subclasses__():
#            cur_id += 1
#            print("%i: %s" % (cur_id, cls.__name__))
#        print("%i: Exit" % (cur_id + 1))
#        revival_id = int(input())-1
#        if revival_id + 1 == cur_id + 1:
#            exit()
#        install_ui(revival_id)
#        print("Returning to menu.")