import json
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import config
import xlrd
import cv2
import sys


# 首页
class MainWindows(QMainWindow):

    def __init__(self):
        super(MainWindows, self).__init__()

        self.config_path = './'
        self.data = []
        self.dataIndex = 0

        self.mainWidget = QWidget(self)
        self.LeftLabel1 = QLabel("材料种类:")
        self.LeftLabel2 = QLabel("材料厚度:")
        self.LeftLabel3 = QLabel("烧烛速度:")
        self.LeftLabel4 = QLabel("烧烛时间:")
        self.RightLabel1 = QLabel("材料制备工艺:")
        self.RightLabel2 = QLabel("材料体系:")
        self.RightLabel3 = QLabel("环境条件:")
        self.RightLabel4 = QLabel("推进加速:")

        self.materialChoose = QComboBox(self)
        self.materialChoose.addItem('请选择数据库文件')
        self.databaseButton = QPushButton('选择数据库文件')
        self.speedChoose = QComboBox(self)
        self.speedChoose.addItem('1')
        self.speedChoose.addItem('0.5')
        self.speedChoose.addItem('2')
        self.speedChoose.addItem('5')
        self.speedChoose.addItem('10')
        self.playtButton = QPushButton('播放')

        self.LeftEdit1 = QLineEdit(self)
        self.LeftEdit2 = QLineEdit(self)
        self.LeftEdit3 = QLineEdit(self)
        self.LeftEdit4 = QLineEdit(self)
        
        self.RightEdit1 = QLineEdit(self)
        self.RightEdit2 = QLineEdit(self)
        self.RightEdit3 = QLineEdit(self)

        self.mainLayout = QHBoxLayout()
        self.menuLayout = QVBoxLayout()
        self.menuTopLayout = QHBoxLayout()
        self.menuTopLeftLayout = QVBoxLayout()
        self.menuTopRightLayout = QVBoxLayout()
        self.menuBottomLayout = QVBoxLayout()
        self.graphLayout = QVBoxLayout()

        self.initUI()
        self.show()

    def initUI(self):
        # 设置选择器属性
        self.setObjectName("MainWindow")

        # 设置窗口属性
        self.setWindowTitle("材料库")
        self.resize(config.main_width, config.main_height)
        self.setFixedSize(config.main_width, config.main_height)
        self.move(config.main_left, config.main_top)

        # 设置样式
        self.LeftEdit1.setEnabled(False)
        self.LeftEdit2.setEnabled(False)
        self.LeftEdit3.setEnabled(False)
        self.RightEdit1.setEnabled(False)
        self.RightEdit2.setEnabled(False)
        self.RightEdit3.setEnabled(False)
        self.LeftEdit4.setValidator(QRegExpValidator(QRegExp("[0-9]{12}"), self))

        # 设置事件
        self.materialChoose.activated.connect(self.selectionchange)
        self.databaseButton.clicked.connect(self.databaseOpen)
        self.playtButton.clicked.connect(self.dataPlay)

        # 设置布局
        self.menuTopLeftLayout.addWidget(self.LeftLabel1, 1)
        self.menuTopLeftLayout.addWidget(self.LeftEdit1, 1)
        self.menuTopLeftLayout.addStretch(1)
        self.menuTopLeftLayout.addWidget(self.LeftLabel2, 1)
        self.menuTopLeftLayout.addWidget(self.LeftEdit2, 1)
        self.menuTopLeftLayout.addStretch(1)
        self.menuTopLeftLayout.addWidget(self.LeftLabel3, 1)
        self.menuTopLeftLayout.addWidget(self.LeftEdit3, 1)
        self.menuTopLeftLayout.addStretch(1)
        self.menuTopLeftLayout.addWidget(self.LeftLabel4, 1)
        self.menuTopLeftLayout.addWidget(self.LeftEdit4, 1)
        self.menuTopLeftLayout.addStretch(2)
        self.menuTopLeftLayout.addWidget(self.databaseButton, 1)

        self.menuTopRightLayout.addWidget(self.RightLabel1, 1)
        self.menuTopRightLayout.addWidget(self.RightEdit1, 1)
        self.menuTopRightLayout.addStretch(1)
        self.menuTopRightLayout.addWidget(self.RightLabel2, 1)
        self.menuTopRightLayout.addWidget(self.RightEdit2, 1)
        self.menuTopRightLayout.addStretch(1)
        self.menuTopRightLayout.addWidget(self.RightLabel3, 1)
        self.menuTopRightLayout.addWidget(self.RightEdit3, 1)
        self.menuTopRightLayout.addStretch(1)
        self.menuTopRightLayout.addWidget(self.RightLabel4, 1)
        self.menuTopRightLayout.addWidget(self.speedChoose, 1)
        self.menuTopRightLayout.addStretch(2)
        self.menuTopRightLayout.addWidget(self.playtButton, 1)

        self.menuBottomLayout.addWidget(self.materialChoose)

        self.menuTopLayout.addLayout(self.menuTopLeftLayout, 1)
        self.menuTopLayout.addLayout(self.menuTopRightLayout, 1)

        self.menuLayout.addLayout(self.menuTopLayout)
        self.menuLayout.addLayout(self.menuBottomLayout)

        self.mainLayout.addLayout(self.menuLayout, 1)
        self.mainLayout.addLayout(self.graphLayout, 2)
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
    
    def dataPlay(self):
        if not self.LeftEdit1.text():
            QMessageBox.critical(self, "错误", "请选择材料！")
            return
        if not self.LeftEdit4.text():
            QMessageBox.critical(self, "错误", "请输入时间！")
            return
        playTime = int(self.LeftEdit4.text())
        speed = float(self.speedChoose.currentText())
        print(self.data[self.dataIndex], self.dataIndex, playTime, speed)
        
    
    def selectionchange(self, index):
        if self.materialChoose.currentText() == "请选择数据库文件":
            QMessageBox.critical(self, "错误", "请选择数据库文件！")
            return
        if self.materialChoose.currentText() == "请选择材料":
            QMessageBox.critical(self, "错误", "请选择材料！")
            return
        self.dataIndex = index - 1
        self.LeftEdit1.setText(self.data[self.dataIndex]['材料种类'])
        self.LeftEdit2.setText(self.data[self.dataIndex]['材料厚度'])
        self.RightEdit1.setText(self.data[self.dataIndex]['材料制备工艺'])
        self.RightEdit2.setText(self.data[self.dataIndex]['材料体系'])
        self.RightEdit3.setText(self.data[self.dataIndex]['环境条件'])

    def databaseOpen(self):
        try:
            databaseName, databaseType = QFileDialog.getOpenFileName(self, "打开数据库文件", self.config_path, "*.txt;;All Files(*)")
            if databaseName:
                self.config_path = '/'.join(databaseName.split('/')[:-1])
                self.setWindowTitle("材料库({})".format(databaseName))
                self.materialChoose.clear()
                self.materialChoose.addItem('请选择材料')
                with open(databaseName, 'r', encoding='utf-8') as f:
                    line = f.readline()
                    while line:
                        data = json.loads(line)
                        self.data.append(data)
                        self.materialChoose.addItem("{}/{}/{}/{}/{}".format(data['材料种类'], data['材料厚度'], data['材料制备工艺'], data['材料体系'], data['环境条件']))
                        line = f.readline()
                    
        except FileNotFoundError:
            self.materialChoose.clear()
            self.materialChoose.addItem('请选择配置文件')
            QMessageBox.critical(self, "错误", "请选择文件！")

# 系统入口
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 测试主页面
    ex = MainWindows()
    sys.exit(app.exec_())
