import os, subprocess, shutil, tempfile, requests, tarfile
from tqdm import tqdm

class Revival:
    def setup_vars(self):
        self.path = "%s/.wineorc/%s" % (self.home_dir, self.name)
        self.env_vars = dict(os.environ) 
        self.env_vars['WINEPREFIX'] = self.path
        self.desktop_entry_path = "%s/.local/share/applications/wine-%s.desktop" % (self.home_dir, self.name)
        pass

    def create_entry():
        pass

    def install_dxvk(self):
        temp_dir = tempfile.TemporaryDirectory()
        if not os.path.exists('dxvk.tar.gz'):
            dxvk_url = "https://github.com/doitsujin/dxvk/releases/download/v2.0/dxvk-2.0.tar.gz"        
            response = requests.get(dxvk_url, stream=True)
            with open("dxvk.tar.gz", "wb") as handle:
                for data in tqdm(response.iter_content()):
                    handle.write(data)
                handle.close()
        tar = tarfile.open("dxvk.tar.gz")
        tar.extractall(temp_dir.name)
        tar.close()
        dxvk_install_script = subprocess.Popen(["sh", "-c", "%s/dxvk-2.0/setup_dxvk.sh install" % (temp_dir.name),], env=self.env_vars)
        dxvk_install_script.wait()
        input()

    def install(self):
        pass

    def uninstall(self):
        if os.path.exists(self.path):
            shutil.rmtree(self.path)
        #if os.path.exists("%s/drive_c/%s" % (self.path, self.launcher_path)):
        #
        if os.path.exists(self.desktop_entry_path):
            os.remove(self.desktop_entry_path)
        os.system("update-desktop-database ~/.local/share/applications")

    def create_prefix(self):
        if not self.wine_installed():
            os.mkdir("%s/.wineorc" % self.home_dir)
        if not self.installed():
            os.mkdir(self.path)
        if not os.path.exists("%s/drive_c" % self.path):
            wineboot_proc = subprocess.Popen(['/usr/bin/wineboot', '-u'], env=self.env_vars)
            wineboot_proc.wait()
            print("created prefix at %s" % self.path)

    def installed(self):
        return os.path.exists(self.path)

    def wine_installed(self):
        return os.path.exists("%s/.wineorc" % self.home_dir)

    def __init__(self) -> None:
        self.name = "Hello"
        self.home_dir = os.path.expanduser('~')
        self.launcher_path = "."
        self.desktop_entry_path = ""
        self.env_vars = dict()
        self.path = "/"
        pass