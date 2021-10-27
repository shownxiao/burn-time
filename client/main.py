import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import config
import xlrd
import cv2
import sys


# 首页
class MainWindows(QMainWindow):

    def __init__(self):
        super(MainWindows, self).__init__()

        self.mainWidget = QWidget(self)
        self.LeftLabel1 = QLabel("材料种类:")
        self.LeftLabel2 = QLabel("材料厚度:")
        self.LeftLabel3 = QLabel("烧烛速度:")
        self.LeftLabel4 = QLabel("烧烛时间:")
        self.LeftLabel5 = QLabel("推进加速:")
        self.RightLabel1 = QLabel("材料制备工艺:")
        self.RightLabel2 = QLabel("材料体系:")
        self.RightLabel3 = QLabel("材料选择:")
        self.RightLabel4 = QLabel("环境条件:")
        self.RightLabel5 = QLabel("配置文件:")

        self.LeftEdit1 = QLineEdit(self)
        self.LeftEdit2 = QLineEdit(self)
        self.LeftEdit3 = QLineEdit(self)
        self.LeftEdit4 = QLineEdit(self)
        self.LeftEdit5 = QLineEdit(self)
        self.RightEdit1 = QLineEdit(self)
        self.RightEdit2 = QLineEdit(self)
        self.RightEdit3 = QLineEdit(self)
        self.RightEdit4 = QLineEdit(self)
        self.RightEdit5 = QLineEdit(self)

        self.mainLayout = QHBoxLayout()
        self.menuLayout = QHBoxLayout()
        self.menuLeftLayout = QVBoxLayout()
        self.menuRightLayout = QVBoxLayout()
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

        # 设置布局
        self.menuLeftLayout.addWidget(self.LeftLabel1, 1)
        self.menuLeftLayout.addWidget(self.LeftEdit1, 1)
        self.menuLeftLayout.addStretch(1)
        self.menuLeftLayout.addWidget(self.LeftLabel2, 1)
        self.menuLeftLayout.addWidget(self.LeftEdit2, 1)
        self.menuLeftLayout.addStretch(1)
        self.menuLeftLayout.addWidget(self.LeftLabel3, 1)
        self.menuLeftLayout.addWidget(self.LeftEdit3, 1)
        self.menuLeftLayout.addStretch(1)
        self.menuLeftLayout.addWidget(self.LeftLabel4, 1)
        self.menuLeftLayout.addWidget(self.LeftEdit4, 1)
        self.menuLeftLayout.addStretch(1)
        self.menuLeftLayout.addWidget(self.LeftLabel5, 1)
        self.menuLeftLayout.addWidget(self.LeftEdit5, 1)

        self.menuRightLayout.addWidget(self.RightLabel1, 1)
        self.menuRightLayout.addWidget(self.RightEdit1, 1)
        self.menuRightLayout.addStretch(1)
        self.menuRightLayout.addWidget(self.RightLabel2, 1)
        self.menuRightLayout.addWidget(self.RightEdit2, 1)
        self.menuRightLayout.addStretch(1)
        self.menuRightLayout.addWidget(self.RightLabel3, 1)
        self.menuRightLayout.addWidget(self.RightEdit3, 1)
        self.menuRightLayout.addStretch(1)
        self.menuRightLayout.addWidget(self.RightLabel4, 1)
        self.menuRightLayout.addWidget(self.RightEdit4, 1)
        self.menuRightLayout.addStretch(1)
        self.menuRightLayout.addWidget(self.RightLabel5, 1)
        self.menuRightLayout.addWidget(self.RightEdit5, 1)

        self.menuLayout.addLayout(self.menuLeftLayout, 1)
        self.menuLayout.addLayout(self.menuRightLayout, 1)

        self.mainLayout.addLayout(self.menuLayout, 1)
        self.mainLayout.addLayout(self.graphLayout, 2)
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)


# 系统入口
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 测试主页面
    ex = MainWindows()
    sys.exit(app.exec_())
