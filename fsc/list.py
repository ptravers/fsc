import sys
from PyQt4.QtGui import *

app = QApplication(sys.argv)
scroll = QScrollArea()
a = QWidget()
listWidget = QListWidget()
scroll.setWidget(a)
for i in range(30):
    item = QListWidgetItem("Item %i" % i)
    listWidget.addItem(item)

listWidget.show()
sys.exit(app.exec_())