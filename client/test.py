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

        self.mainLayout = QHBoxLayout()
        self.menuLayout = QHBoxLayout()
        self.menuLeftLayout = QVBoxLayout()
        self.menuRightLayout = QVBoxLayout()
        self.graphLayout = QVBoxLayout()

        self.aValue = 0
        self.bValue = 0
        self.dsValue = 0
        self.dcValue = 0

        self.imgPath = "./static/images"

        self.mainWidget = QWidget(self)
        self.font = QFont("方正粗圆简体", 24)
        self.fileButton = QPushButton('选择图片文件')
        self.aLabel1 = QLabel("a像素点:")
        self.aLabel2 = QLabel("真实值:")
        self.bLabel = QLabel("b像素点:")
        self.dsLabel = QLabel("ds像素点:")
        self.dcLabel = QLabel("dc像素点:")
        self.aValueEdit = QLineEdit(self)
        self.bValueLabel = QLabel("b值:0")
        self.dsValueLabel = QLabel("ds值:0")
        self.dcValueLabel = QLabel("dc值:0")
        self.pValueLabel = QLabel("密度差:")
        self.gValueLabel = QLabel("重力加速度:")
        self.sValueLabel = QLabel("S值:0")
        self.HValueLabel = QLabel("1/H值:")
        self.resultValueLabel = QLabel("结果:0")
        self.aPixelsEdit = QLineEdit(self)
        self.bPixelsEdit = QLineEdit(self)
        self.dsPixelsEdit = QLineEdit(self)
        self.dcPixelsEdit = QLineEdit(self)
        self.pPixelsEdit = QLineEdit(self)
        self.gPixelsEdit = QLineEdit(self)
        self.HPixelsEdit = QLineEdit(self)
        self.pictureLabel = QLabel()
        self.pictureLabel.setFixedSize(config.pictureWidth, config.pictureHeight)
        self.textCopyButton = QPushButton("一键复制")

        self.mainLayout = QVBoxLayout()
        self.pictureLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()
        self.bottomLeftLayout = QVBoxLayout()
        self.bottomMidLayout = QVBoxLayout()
        self.bottomRightLayout = QVBoxLayout()
        self.aLayout = QHBoxLayout()
        self.bLayout = QHBoxLayout()
        self.dsLayout = QHBoxLayout()
        self.dcLayout = QHBoxLayout()
        self.pLayout = QHBoxLayout()
        self.SHLayout = QHBoxLayout()
        self.resultLayout = QHBoxLayout()

        self.initUI()
        self.show()

    def initUI(self):
        # 设置选择器属性
        self.setObjectName("MainWindow")

        # 设置窗口属性
        self.resize(config.main_width, config.main_height)
        self.setFixedSize(config.main_width, config.main_height)
        self.move(config.main_left, config.main_top)
        # self.setWindowFlags(Qt.Qt.FramelessWindowHint)

        # 设置样式
        # self.titleLabel.setFont(self.font)
        #
        self.fileButton.clicked.connect(self.open)
        self.aValueEdit.editingFinished.connect(self.setLabel)
        self.aPixelsEdit.editingFinished.connect(self.setLabel)
        self.bPixelsEdit.editingFinished.connect(self.setLabel)
        self.dsPixelsEdit.editingFinished.connect(self.setLabel)
        self.dcPixelsEdit.editingFinished.connect(self.setLabel)
        self.pPixelsEdit.editingFinished.connect(self.setResult)
        self.gPixelsEdit.editingFinished.connect(self.setResult)
        self.HPixelsEdit.editingFinished.connect(self.setResult)
        self.textCopyButton.clicked.connect(self.copyText)

        # 设置布局
        self.pictureLayout.addStretch(1)
        self.pictureLayout.addWidget(self.pictureLabel)
        self.pictureLayout.addStretch(1)

        self.aLayout.addWidget(self.aLabel1)
        self.aLayout.addWidget(self.aPixelsEdit)
        self.aLayout.addWidget(self.aLabel2)
        self.aLayout.addWidget(self.aValueEdit)

        self.bottomLeftLayout.addWidget(self.fileButton)
        self.bottomLeftLayout.addLayout(self.aLayout)

        self.bLayout.addWidget(self.bLabel)
        self.bLayout.addWidget(self.bPixelsEdit)
        self.bLayout.addWidget(self.bValueLabel)

        self.dsLayout.addWidget(self.dsLabel)
        self.dsLayout.addWidget(self.dsPixelsEdit)
        self.dsLayout.addWidget(self.dsValueLabel)

        self.dcLayout.addWidget(self.dcLabel)
        self.dcLayout.addWidget(self.dcPixelsEdit)
        self.dcLayout.addWidget(self.dcValueLabel)

        self.bottomMidLayout.addLayout(self.bLayout)
        self.bottomMidLayout.addLayout(self.dsLayout)
        self.bottomMidLayout.addLayout(self.dcLayout)

        self.pLayout.addWidget(self.pValueLabel)
        self.pLayout.addWidget(self.pPixelsEdit)
        self.pLayout.addWidget(self.gValueLabel)
        self.pLayout.addWidget(self.gPixelsEdit)

        self.SHLayout.addWidget(self.sValueLabel)
        self.SHLayout.addWidget(self.HValueLabel)
        self.SHLayout.addWidget(self.HPixelsEdit)

        self.resultLayout.addWidget(self.resultValueLabel)
        self.resultLayout.addWidget(self.textCopyButton)

        self.bottomRightLayout.addLayout(self.pLayout)
        self.bottomRightLayout.addLayout(self.SHLayout)
        self.bottomRightLayout.addLayout(self.resultLayout)

        self.bottomLayout.addLayout(self.bottomLeftLayout, 1)
        self.bottomLayout.addLayout(self.bottomMidLayout, 1)
        self.bottomLayout.addLayout(self.bottomRightLayout, 1)

        self.mainLayout.addLayout(self.pictureLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

    def open(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", self.imgPath, "*.jpg;;*.png;;All Files(*)")
        jpg = QPixmap(imgName).scaled(self.pictureLabel.width(), self.pictureLabel.height())
        self.pictureLabel.setPixmap(jpg)
        # print(imgName, imgType)
        self.imgPath = '/'.join(imgName.split('/')[:-1])
        self.aValueEdit.setText("")
        self.compute(imgName, 2)

    def setLabel(self):
        if self.aValueEdit.text():
            self.bValueLabel.setText("b值:{:.2f}".format(float(self.aValueEdit.text()) * float(self.bPixelsEdit.text())
                                                        / float(self.aPixelsEdit.text())))
            self.dsValueLabel.setText("ds值:{:.2f}".format(float(self.aValueEdit.text()) * float(self.dsPixelsEdit.text())
                                                          / float(self.aPixelsEdit.text())))
            self.dcValueLabel.setText("dc值:{:.2f}".format(float(self.aValueEdit.text()) * float(self.dcPixelsEdit.text())
                                                          / float(self.aPixelsEdit.text())))
            self.sValueLabel.setText("S值:{:.3f}".format(float(self.dsValueLabel.text().replace('ds值:', ''))
                                                        / float(self.dcValueLabel.text().replace('dc值:', ''))))
            bok = xlrd.open_workbook(r'static/data/SH.xlsx')
            sht = bok.sheets()[0]
            index = int(float(self.sValueLabel.text().replace('S值:', ''))*1000 - 300) + 1
            if index > 704:
                index = 704
            cell_d4 = sht.cell(index, 1).value
            self.HPixelsEdit.setText(str(cell_d4))

        if self.pPixelsEdit.text() and self.gPixelsEdit.text():
            self.setResult()

    def setResult(self):
        if self.pPixelsEdit.text() and self.gPixelsEdit.text():
            result = float(self.gPixelsEdit.text()) \
                     * float(self.pPixelsEdit.text())\
                     * float(self.dcValueLabel.text().replace('dc值:', ''))\
                     * float(self.dcValueLabel.text().replace('dc值:', ''))\
                     * float(self.HPixelsEdit.text())
            self.resultValueLabel.setText("结果:" + str(result))

    def copyText(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.resultValueLabel.text().replace("结果:", ""))

    def compute(self, imgName, area):
        result = []
        img = cv2.imdecode(np.fromfile(imgName, dtype=np.uint8), -1)
        # img = cv2.imread(imgName)

        # print(img.shape)
        height, width, channels = img.shape

        for i in range(height):
            for j in range(width-1):
                if img[i][j-1][0] >= 245 and img[i][j-1][1] >= 245 and img[i][j-1][2] >= 245 and img[i][j+1][0] >= 245 and img[i][j+1][1] >= 245 and img[i][j+1][2] >= 245:
                    img[i][j][0] = 255
                    img[i][j][1] = 255
                    img[i][j][2] = 255
        for i in range(height):
            result.append(0)
        # print("height:%s,width:%s,channels:%s" % (height, width, channels))
        for row in range(height):
            mid = int(width / 2)
            if img[row][mid][0] >= 245 and img[row][mid][1] >= 245 and img[row][mid][2] >= 245:
                for dis in range(mid):
                    col = mid - dis - 1
                    if img[row][col][0] >= 245 and img[row][col][1] >= 245 and img[row][col][2] >= 245:
                        result[row] = result[row] + 1
                    else:
                        break

                for dis in range(mid):
                    col = mid + dis
                    if img[row][col][0] >= 245 and img[row][col][1] >= 245 and img[row][col][2] >= 245:
                        result[row] = result[row] + 1
                    else:
                        break
        # print(result)

        aRow = 0
        bRow = 0
        dsRow = 0
        dcRow = 0
        maxLength = 0
        minLength = 640

        for index, value in enumerate(result):
            if value > maxLength:
                maxLength = value
                aRow = index
        # print(aRow, result[aRow])

        for index, value in enumerate(result):
            if index < 10 or index >= height - 10:
                pass
            else:
                flag = True
                for i in range(20):
                    if result[index - 10 + i] == 0 or result[index - 10 + i] < result[index]:
                        flag = False
                if value < minLength and value != 0 and flag:
                    minLength = value
                    bRow = index
        # print(bRow, result[bRow])

        maxLength = 0
        for index, value in enumerate(result):
            if index > bRow:
                if value > maxLength:
                    maxLength = value
                    dcRow = index
        # print(dcRow, result[dcRow])

        for index, value in enumerate(result):
            if index < 20:
                pass
            else:
                flag = True
                count = 0
                for i in range(20):
                    if index + i - 20 < len(result) and result[index - 20 + i] == 0:
                        count = count + 1
                        if count > 2:
                            flag = False
                count = 0
                for i in range(10):
                    if index + i + 1 < len(result) and result[index + i + 1] != 0:
                        count = count + 1
                        if count > 2:
                            flag = False
                if result[index] > 0 and flag and index > dcRow:
                    dsRow = index - result[dcRow]
        # print(dsRow, result[dsRow])

        for col in range(width):
            for i in [aRow, bRow, dsRow, dcRow]:
                if img[i][col][0] >= 245 and img[i][col][1] >= 245 and img[i][col][2] >= 245:
                    img[i][col][0] = 232
                    img[i][col][1] = 80
                    img[i][col][2] = 78
        cv2.imwrite("./static/result/" + imgName.split('/')[-1], img)
        jpg = QPixmap("./static/result/" + imgName.split('/')[-1]).scaled(self.pictureLabel.width(), self.pictureLabel.height())
        self.pictureLabel.setPixmap(jpg)

        self.aPixelsEdit.setText(str(result[aRow]))
        self.bPixelsEdit.setText(str(result[bRow]))
        self.dsPixelsEdit.setText(str(result[dsRow]))
        self.dcPixelsEdit.setText(str(result[dcRow]))


# 系统入口
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 测试主页面
    ex = MainWindows()
    sys.exit(app.exec_())
