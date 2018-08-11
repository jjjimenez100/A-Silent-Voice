print("Initializing")

import Modules.UserInterface.loginController as login
from PyQt5.QtWidgets import QApplication as app

if __name__ == '__main__':
    import sys
    app = app(sys.argv)
    window = login.LogInForm()
    sys.exit(app.exec_())# program still runs even if you quit on login window
