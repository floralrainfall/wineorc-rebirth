from revivals.revival import Revival
import revivals.all
import os

def install_ui(revival_id):
    revival_sel = Revival.__subclasses__()[revival_id]
    revival_ent = revival_sel.__new__(revival_sel)
    revival_ent.__init__()
    revival_ent.setup_vars()
    Revival.setup_vars(revival_ent) # so the super can setup all the other vars we need
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

if __name__ == "__main__":
    print("WineORC v2.0 by Ryelow")
    print("Select a revival")
    print("NOTICE: Make sure you have xdg and wine before installing with this utility.")
    while True:
        cur_id = 0
        for cls in Revival.__subclasses__():
            cur_id += 1
            print("%i: %s" % (cur_id, cls.__name__))
        print("%i: Exit" % (cur_id + 1))
        revival_id = int(input())-1
        if revival_id + 1 == cur_id + 1:
            exit()
        install_ui(revival_id)
        print("Returning to menu.")