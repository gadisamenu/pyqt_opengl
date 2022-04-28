from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL import *
from PyQt5.QtOpenGL import *
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtWidgets import *
import sys,time
import numpy as np
import importlib.util
import subprocess


if importlib.util.find_spec("PyQt5"):
    print(f"Package already installed")
else:
    try:
        permission = input("Do you what to install PyQt5(y/n)?")
        if permission.lower() == "y":
            subprocess.check_call([sys.executable, '-m', 'pip', 'install',
            'PyQt5'])
            print("Installed PyQt5 successfully")
        else:
            sys.exit(0)
    except Exception(e):
        print("Failed installing PyQt5")

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setAcceptDrops(True)
        mainLayout = QHBoxLayout()
        self.setLayout(mainLayout)

        self.widget = glWidget(self)
        mainLayout.addWidget(self.widget,8)

        self.side = qtWidget(self)
        mainLayout.addWidget(self.side,2)
        
        self.setWindowTitle("Graphs")
        self.setGeometry(150, 150, 900, 600)


class qtWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.selected = set()
        self.vLayout = QVBoxLayout() 
        self.vLayout.setSpacing(15)
        self.vLayout.addStretch(1)
        self.vLayout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.vLayout)

        self.text = QLabel("Select the checkboxs to draw")
        self.text.setFont(QtGui.QFont("Times",15,10))
        self.text.setWordWrap(True)
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.vLayout.addWidget(self.text)

        self.checkbox_1 = QCheckBox('y = xsin(1/x)')
        self.checkbox_2 = QCheckBox('r = sin(44θ) - 2cosθ')
        self.checkbox_3 = QCheckBox('x = sin2t, y = sin3t')
        self.checkbox_4 = QCheckBox('x = tsin5t , y = tcos5t')
        self.checkbox_5 = QCheckBox('y = sqrt(x^2 - (x^4)/4)')
        self.checkbox_6 = QCheckBox('y = cosx')


        self.checkboxs  = [self.checkbox_1,self.checkbox_2,self.checkbox_3,self.checkbox_4,self.checkbox_5,self.checkbox_6]
        
        self.actions = [self.action_1, self.action_2, self.action_3, self.action_4, self.action_5, self.action_6]

        for ch,act in zip(self.checkboxs,self.actions):
            ch.stateChanged.connect(act)
        
        for checkbox in self.checkboxs:
            self.vLayout.addWidget(checkbox)
        self.vLayout.addStretch(4)

    
    def control(self):
        if len(self.selected) >= 2:
            for check in self.checkboxs:
                if check not in self.selected:
                    check.setDisabled(True)
        else:
            for check in self.checkboxs:
                check.setEnabled(True)


    def action_1(self, checked):
        if QtCore.Qt.Checked == checked:
            self.selected.add(self.checkbox_1)
            x = np.linspace(-3.5,3.5, 1000)
            y = np.multiply(x, np.sin(1/x))
            glWidget.graphs[1] = (x,y)
        else:
            self.selected.remove(self.checkbox_1)
            glWidget.graphs.pop(1)
        self.control()
   
    def action_2(self, checked):
        if QtCore.Qt.Checked == checked:
            self.selected.add(self.checkbox_2)
            teta = np.linspace(0,10,360)
            x = np.multiply(np.subtract(np.sin(44*teta),2*np.cos(teta)),np.cos(teta))
            y = np.multiply(np.subtract(np.sin(44*teta),2*np.cos(teta)),np.sin(teta))
            glWidget.graphs[2] = (x,y)
        else:
            self.selected.remove(self.checkbox_2)
            glWidget.graphs.pop(2)
        self.control()

    def action_3(self, checked):
        if QtCore.Qt.Checked == checked:
            self.selected.add(self.checkbox_3)
            t = np.linspace(0, 8,360)
            x = np.sin(2*t)
            y =  np.sin(3*t)
            glWidget.graphs[3] = (x,y)
        else:
            self.selected.remove(self.checkbox_3)
            glWidget.graphs.pop(3)
        self.control()

    def action_4(self, checked):
        if QtCore.Qt.Checked == checked:
            self.selected.add(self.checkbox_4)
            t = np.linspace(0,4,200)
            x = t* np.sin(5*t)
            y = t* np.cos(5*t)
            glWidget.graphs[4] = (x,y)
        else:
            self.selected.remove(self.checkbox_4)
            glWidget.graphs.pop(4)
        self.control()

    def action_5(self, checked):
        if QtCore.Qt.Checked == checked:
            self.selected.add(self.checkbox_5)
            x = np.linspace(-2,2,100)
            y = np.sqrt(np.subtract(np.power(x,2),np.divide(np.power(x,4),4)))
            y = np.append(y, np.flip(-y))
            x = np.append(x, np.flip(x))
            glWidget.graphs[5] = (x,y)
        else:
            self.selected.remove(self.checkbox_5)
            glWidget.graphs.pop(5)
        self.control()

    def action_6(self, checked):
        if QtCore.Qt.Checked == checked:
            self.selected.add(self.checkbox_6)
            x = np.linspace(-3.5,3.5,100)
            y = np.cos(x)
            glWidget.graphs[6] = (x,y)
        else:
            self.selected.remove(self.checkbox_6)
            glWidget.graphs.pop(6)
        self.control()



class glWidget(QGLWidget):
    graphs = {}
    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.x_cor = np.linspace(-3.5, 3.5, 9)
        self.y_cor = np.linspace(-3.5, 3.4, 9)
        self.colors = [[0.3,0.7,0.5],[0.3, 0.2, 0.8]]

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(1.0, 0.0, 0.0)        

        # drawing the coordinate plane
        glLineWidth(1)
        glBegin(GL_LINE_STRIP)
        for a in self.x_cor:
            glVertex2f(a, 0)
        glEnd()

        glBegin(GL_LINE_STRIP)
        for b in self.y_cor:
            glVertex2f(0, b)
        glEnd()

        # drawing the graphs
        glLineWidth(2)
        for idx , pairs in enumerate(glWidget.graphs.values()):
            glBegin(GL_LINE_STRIP)
            glColor(self.colors[idx])
            for a,b in zip(pairs[0],pairs[1]):
                glVertex2f(a,b)
            glEnd()
    
        glFlush()
        time.sleep(1)
        self.update()      

    def resizeGL(self, w, h):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-1.5, 1.5, -1.75, 1.75 )
        glViewport(0, 0, w, h)

    def initializeGL(self):
        glClearColor(0.2, 0.2, 0.2, 1.0)
        gluPerspective(45,800/600,0.1,50.0)
        glTranslatef(0.0,0.0,-5)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit((app.exec_()))