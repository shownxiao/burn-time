import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import config
import json
import xlrd
import cv2
import sys


# 首页
class MainWindows(QMainWindow):

    def __init__(self):
        super(MainWindows, self).__init__()

        self.mainWidget = QWidget(self)
        self.Label1 = QLabel("材料种类:")
        self.Label2 = QLabel("材料厚度:")
        self.Label3 = QLabel("材料制备工艺:")
        self.Label4 = QLabel("材料体系:")
        self.Label5 = QLabel("环境条件:")
        self.Label6 = QLabel("选择配置文件:")
        self.Label7 = QLabel("选择厚度数据:")
        self.Label8 = QLabel("选择温度数据:")

        self.Edit1 = QLineEdit(self)
        self.Edit2 = QLineEdit(self)
        self.Edit3 = QLineEdit(self)
        self.Edit4 = QLineEdit(self)
        self.Edit5 = QLineEdit(self)
        self.Edit6 = QLineEdit(self)
        self.Edit7 = QLineEdit(self)
        self.Edit8 = QLineEdit(self)

        self.mainLayout = QVBoxLayout()
        self.menuLayout = QVBoxLayout()

        self.initUI()
        self.show()

    def initUI(self):
        # 设置选择器属性
        self.setObjectName("MainWindow")

        # 设置窗口属性
        self.setWindowTitle("入库")
        self.resize(config.main_width, config.main_height)
        self.setFixedSize(config.main_width, config.main_height)
        self.move(config.main_left, config.main_top)

        # 设置样式

        # 设置布局
        self.menuLayout.addWidget(self.Label1, 1)
        self.menuLayout.addWidget(self.Edit1, 1)
        self.menuLayout.addStretch(1)
        self.menuLayout.addWidget(self.Label2, 1)
        self.menuLayout.addWidget(self.Edit2, 1)
        self.menuLayout.addStretch(1)
        self.menuLayout.addWidget(self.Label3, 1)
        self.menuLayout.addWidget(self.Edit3, 1)
        self.menuLayout.addStretch(1)
        self.menuLayout.addWidget(self.Label4, 1)
        self.menuLayout.addWidget(self.Edit4, 1)
        self.menuLayout.addStretch(1)
        self.menuLayout.addWidget(self.Label5, 1)
        self.menuLayout.addWidget(self.Edit5, 1)
        self.menuLayout.addStretch(1)
        self.menuLayout.addWidget(self.Label6, 1)
        self.menuLayout.addWidget(self.Edit6, 1)
        self.menuLayout.addStretch(1)
        self.menuLayout.addWidget(self.Label7, 1)
        self.menuLayout.addWidget(self.Edit7, 1)
        self.menuLayout.addStretch(1)
        self.menuLayout.addWidget(self.Label8, 1)
        self.menuLayout.addWidget(self.Edit8, 1)

        self.mainLayout.addLayout(self.menuLayout)
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)


# 系统入口
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 测试主页面
    ex = MainWindows()
    sys.exit(app.exec_())
