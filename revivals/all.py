from revivals.revival import Revival
from tqdm import tqdm
import os, requests, subprocess, tempfile

class Crapblox(Revival):
    def setup_vars(self):
        self.name = "Crapblox"

    def install(self):
        self.create_prefix()
        self.launcher_path = "%s/drive_c/users/%s/AppData/Local/CrapbloxLauncher.exe" % (self.path, os.getlogin())
        url = "https://cdn.discordapp.com/attachments/1061141208421896232/1066969740871995462/CrapbloxLauncher.exe" # pls update accordingly
        response = requests.get(url, stream=True)
        print("If it enters a web browser, just close it.")
        with open(self.launcher_path, "wb") as handle:
            for data in tqdm(response.iter_content()):
                handle.write(data)
            handle.close()
            launcher_proc = subprocess.Popen(['/usr/bin/wine', self.launcher_path], env=self.env_vars)
            with open(self.desktop_entry_path, "w") as desktop_handle:
                desktop_handle.write("[Desktop Entry]\n")
                desktop_handle.write("Name=%s Player\n" % (self.name))
                desktop_handle.write("Comment=Managed by WineORC2\n")
                desktop_handle.write("Type=Application\n")
                desktop_handle.write("Exec=env WINEPREFIX=%s wine %s" % (self.path, self.launcher_path) + " %U\n")
                desktop_handle.write("MimeType=x-scheme-handler/crapblox2\n")
                desktop_handle.close()
            launcher_proc.wait()