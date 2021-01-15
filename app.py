import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QDesktopWidget
from PyQt5.QtWidgets import QPushButton, QFileDialog, QLineEdit, QCheckBox, QLabel

import cv2
import os
import glob
from tqdm import tqdm


class V2I:
    def createFolder(directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print('Error: Creating directory. ' + directory)

    def video_to_image(dir, fps, n):
        V2I.createFolder(str(dir) + '_shot')
        save_dir = str(dir) + '_shot\\'
        video = '*.mp4'
        flag = False

        for vid in tqdm(glob.glob(str(dir) + '\\' + video)):
            cap = cv2.VideoCapture(vid)
            img = save_dir + vid.split('.')[0].split('\\')[-1]
            V2I.createFolder(img)

            i = 0

            while (cap.isOpened()):
                ret, frame = cap.read()

                if ret:
                    if (i % fps) == 0:
                        cv2.imwrite(img + '\\img_' + str(i) + '.jpg', frame)
                        if n:
                            f = open(img + '\\img_' + str(i) + '.txt', 'wt')
                            f.close()
                    i += 1

                else:
                    flag = True
                    break

            if flag:
                print('Finished Video to Image : ' + vid)
            else:
                print('Not exist File : ' + vid)

            cap.release()
            cv2.destroyAllWindows()


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setdir(self):
        dname = QFileDialog.getExistingDirectory(self, "select folder", ".")
        self.statusBar().showMessage(dname)

    def process(self):
        dname = self.statusBar().currentMessage()
        fps = int(self.txt.text())
        V2I.video_to_image(dname, fps, self.n)
        self.statusBar().showMessage('Finished')

    def chkFunction(self):
        if self.n:
            self.n = False
        else:
            self.n = True

    def initUI(self):
        self.label = QLabel(self)
        self.label.resize(100,50)
        self.label.move(100, 100)
        self.n = False
        self.txt = QLineEdit(self)
        self.txt.move(500,300)
        btn1 = QPushButton("Open", self)
        btn1.move(400,350)
        btn1.clicked.connect(self.setdir)
        btn2 = QPushButton("Process", self)
        btn2.move(500, 350)
        btn2.clicked.connect(self.process)
        self.chk = QCheckBox(self)
        self.chk.stateChanged.connect(self.chkFunction)
        self.chk.move(500,250)

        self.statusBar()

        openDir = QAction('Open', self)
        openDir.setShortcut('Ctrl+O')
        openDir.setStatusTip('Open Directory')
        openDir.triggered.connect(self.setdir)

        processAction = QAction('Process', self)
        processAction.setShortcut('Ctrl+P')
        processAction.setStatusTip('Processing Video to Img')
        processAction.triggered.connect(self.process)

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(openDir)
        filemenu.addAction(processAction)
        filemenu.addAction(exitAction)

        self.setWindowTitle('video to image')
        self.center()
        self.resize(640, 400)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
