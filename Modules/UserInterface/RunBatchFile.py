import os
from subprocess import Popen, PIPE

def install():
    wd = os.path.dirname(os.path.realpath(__file__))

    wd = "\\".join(wd.split("\\")[:-2])

    wd += "\\wininstall.bat"

    p = Popen(wd, shell=True, stdout= PIPE)
    stdout, stderr = p.communicate()
    print(p.returncode)