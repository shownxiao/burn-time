# coding=utf-8
import codecs
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import config
import json
import xlrd
import cv2
import sys


# 首页
class MainWindows(QMainWindow):

    def __init__(self):
        super(MainWindows, self).__init__()

        self.config_path = './'
        self.thickness_path = './'
        self.temperature_path = './'

        self.thickness_x = []
        self.thickness_y = []
        self.temperature_x = []
        self.temperature_y = []

        self.mainWidget = QWidget(self)
        self.Label1 = QLabel("材料种类:")
        self.Label2 = QLabel("材料厚度(mm):")
        self.Label3 = QLabel("材料制备工艺:")
        self.Label4 = QLabel("材料体系:")
        self.Label5 = QLabel("环境条件:")

        self.databaseButton = QPushButton('选择数据库文件')
        self.thicknessButton = QPushButton('选择厚度数据文件')
        self.temperatureButton = QPushButton('选择温度数据文件')
        self.confirmButton = QPushButton('确定')

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
        self.Edit6.setEnabled(False)
        self.Edit7.setEnabled(False)
        self.Edit8.setEnabled(False)
        # self.Edit2.setValidator(QRegExpValidator(QRegExp("[0-9]{12}.[0-9]{6}"), self))

        # 设置事件
        self.databaseButton.clicked.connect(self.databaseOpen)
        self.thicknessButton.clicked.connect(self.thicknessOpen)
        self.temperatureButton.clicked.connect(self.temperatureOpen)
        self.confirmButton.clicked.connect(self.upload)

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
        self.menuLayout.addWidget(self.databaseButton, 1)
        self.menuLayout.addWidget(self.Edit6, 1)
        self.menuLayout.addStretch(1)
        self.menuLayout.addWidget(self.thicknessButton, 1)
        self.menuLayout.addWidget(self.Edit7, 1)
        self.menuLayout.addStretch(1)
        self.menuLayout.addWidget(self.temperatureButton, 1)
        self.menuLayout.addWidget(self.Edit8, 1)
        self.menuLayout.addWidget(self.confirmButton, 1)

        self.mainLayout.addLayout(self.menuLayout)
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

    
    def upload(self):
        if self.Edit1.text() and self.Edit2.text() and self.Edit3.text() and self.Edit4.text() and self.Edit5.text() and self.Edit6.text():
            with open(self.Edit6.text(), 'a', encoding="utf-8") as f:
                data = {
                    "材料种类": self.Edit1.text(),
                    "材料厚度": self.Edit2.text(),
                    "材料制备工艺": self.Edit3.text(),
                    "材料体系": self.Edit4.text(),
                    "环境条件": self.Edit5.text(),
                    "厚度数据": {
                        "x": self.thickness_x,
                        "y": self.thickness_y
                    },
                    "温度数据": {
                        "x": self.temperature_x,
                        "y": self.temperature_y
                    }
                }
                json.dump(data, f, ensure_ascii=False)
                f.write('\n')
                QMessageBox.information(self, "成功", "上传成功！")
        else:
            QMessageBox.critical(self, "错误", "请输入完整信息！")
            
    
    def databaseOpen(self):
        try:
            databaseName, databaseType = QFileDialog.getOpenFileName(self, "打开数据库文件", self.config_path, "*.txt;;All Files(*)")
            self.config_path = '/'.join(databaseName.split('/')[:-1])
            self.Edit6.setText(databaseName)
        except FileNotFoundError:
            QMessageBox.critical(self, "错误", "请选择文件！")
    
    def thicknessOpen(self):
        try:
            begin_thickness = float(self.Edit2.text())
        except ValueError:
            QMessageBox.critical(self, "错误", "厚度请输入正确的数字！")
            return
        try:
            if not self.Edit2.text():
                QMessageBox.critical(self, "错误", "请先输入初始厚度！")
                return
            thicknessName, thicknessType = QFileDialog.getOpenFileName(self, "打开厚度数据文件", self.thickness_path, "*.xlsx;;*.xls;;All Files(*)")
            self.thickness_path = '/'.join(thicknessName.split('/')[:-1])
            self.Edit7.setText(thicknessName)
            data = xlrd.open_workbook(thicknessName)
            table = data.sheets()[0]
            self.thickness_x = [0]
            self.thickness_y = [begin_thickness]
            for rown in range(1, table.nrows):
                begin_x = int(self.thickness_x[-1])
                end_x = int(table.cell(rown, 0).value)
                begin_y = float(self.thickness_y[-1])
                end_y = begin_y - float(table.cell(rown, 1).value)
                for index in range(begin_x + 1, end_x + 1):
                    self.thickness_x.append(int(index))
                    self.thickness_y.append(float('%.3f' % (begin_y - (begin_y -  end_y) * (index - begin_x) / (end_x - begin_x))))
        except FileNotFoundError:
            QMessageBox.critical(self, "错误", "请选择文件！")
    
    def temperatureOpen(self):
        try:
            temperatureName, temperatureType = QFileDialog.getOpenFileName(self, "打开温度数据文件", self.temperature_path, "*.xlsx;;*.xls;;All Files(*)")
            self.temperature_path = '/'.join(temperatureName.split('/')[:-1])
            self.Edit8.setText(temperatureName)
            data = xlrd.open_workbook(temperatureName)
            table = data.sheets()[0]
            self.temperature_x = []
            self.temperature_y = []
            for rown in range(1, table.nrows):
                if(table.cell(rown, 0).value.is_integer()):
                    self.temperature_x.append(int(table.cell(rown, 0).value))
                    self.temperature_y.append(int(table.cell(rown, 1).value))
        except FileNotFoundError:
            QMessageBox.critical(self, "错误", "请选择文件！")


# 系统入口
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 测试主页面
    ex = MainWindows()
    sys.exit(app.exec_())
