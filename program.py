import sys
from PyQt5.QtWidgets import QApplication
from image_interpolation import Image_Interpolation

app = QApplication(sys.argv)
widdget = Image_Interpolation()
sys.exit(app.exec_())