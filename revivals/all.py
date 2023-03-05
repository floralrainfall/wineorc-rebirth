from revivals.revival import Revival, create_desktop_entry
from tqdm import tqdm
import os, requests, subprocess, tempfile

class Crapblox(Revival):
    def setup_vars(self):
        self.name = "Crapblox2016"

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
            create_desktop_entry("wine-" + self.name, "env WINEPREFIX=%s wine %s" % (self.path, self.launcher_path) + " %U", "crapblox2016")

class Itteblox(Revival):
    def setup_vars(self):
        print("WARNING: This doesn't really work for some reason. It errors about __sys_errlist and I don't quite know how to fix it")
        self.name = "Itteblox"

    def install(self):
        self.create_prefix()
        wineboot_proc = subprocess.Popen(['/usr/bin/winecfg', '-v', 'win10'], env=self.env_vars)
        wineboot_proc.wait()
        itteblox_version = requests.get("https://setup.ittblox.gay/version")        
        self.launcher_path = "%s/drive_c/users/%s/AppData/Local/ItteBlox/Versions/%s/ItteBloxPlayerLauncher.exe" % (self.path, os.getlogin(), str(itteblox_version.content,"utf-8"))
        temp_dir = tempfile.TemporaryDirectory()
        url = "https://setup.ittblox.gay/ItteBloxPlayerLauncher.exe"
        response = requests.get(url, stream=True)
        with open("%s/ItteBloxPlayerLauncher.exe" % temp_dir.name, "wb") as handle:
            for data in tqdm(response.iter_content()):
                handle.write(data)
            handle.close()
            launcher_proc = subprocess.Popen(['/usr/bin/wine', "%s/ItteBloxPlayerLauncher.exe" % temp_dir.name], env=self.env_vars)

            create_desktop_entry("wine-" + self.name, "env WINEPREFIX=%s wine %s" % (self.path, self.launcher_path) + " %U", "ittblx-player")
            