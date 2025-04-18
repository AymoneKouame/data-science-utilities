import os
import subprocess
import pkg_resources
def install_if_not_installed(modules):  
    uninstalled_packages = [p for p in modules if p not in sorted(["%s==%s" % (i.key, i.version) for i in pkg_resources.working_set])]
    uninstalled_packages_f = " ".join(uninstalled_packages)
    subprocess.run(['pip', 'install', '--upgrade', uninstalled_packages_f])

#intall_if_not_installed(modules = ['openpyxl', 'seaborn'])
