from PyQt4 import QtCore
from PyQt4 import QtGui

class mygraphicsview(QtGui.QGraphicsView):

    def __init__(self, parent = None):
        super(QtGui.QGraphicsView, self).__init__(parent)

    def resizeEvent(self, event):
        scene = self.scene()

        if hasattr(scene, "update") == False:
            return

        scene.update(self.size())
        self.resetCachedContent()
