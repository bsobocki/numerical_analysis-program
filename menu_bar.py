from PyQt5.QtWidgets import QMenu, QMenuBar, QAction

class Menu_Bar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.menu_names = ["File", "Edit", "Tools", "Windows", "Settings", "Help"]
        self.menu = {}
        self.create_menu()


    def create_menu(self):
        # addMenu returns QMenu Object
        for name in self.menu_names: 
            self.menu[name] = self.addMenu(name) 
            
        self.create_file_menu()

    def create_file_menu(self):
        self.new = QMenu("New", self.menu["File"])
        self.spline = QAction("Spline Creator project", self)
        self.spline.setShortcut('Ctrl+N+S')
        self.new.addAction(self.spline)
        self.menu["File"].addMenu(self.new)

        exit = QAction('Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit application')
        exit.triggered.connect(self.parent().close)
        self.menu["File"].addAction(exit) 


    # Actions

    def set_spline_creator_action(self, action):
        self.spline.triggered.connect(action)