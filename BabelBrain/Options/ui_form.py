# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QDoubleSpinBox, QGroupBox, QLabel, QPushButton,
    QSizePolicy, QTabWidget, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(664, 261)
        self.CancelpushButton = QPushButton(Dialog)
        self.CancelpushButton.setObjectName(u"CancelpushButton")
        self.CancelpushButton.setGeometry(QRect(579, 232, 74, 32))
        self.ContinuepushButton = QPushButton(Dialog)
        self.ContinuepushButton.setObjectName(u"ContinuepushButton")
        self.ContinuepushButton.setGeometry(QRect(275, 234, 136, 32))
        self.ResetpushButton = QPushButton(Dialog)
        self.ResetpushButton.setObjectName(u"ResetpushButton")
        self.ResetpushButton.setGeometry(QRect(5, 232, 136, 32))
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(5, 4, 644, 224))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.label_5 = QLabel(self.tab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(136, 11, 201, 16))
        self.ElastixOptimizercomboBox = QComboBox(self.tab)
        self.ElastixOptimizercomboBox.addItem("")
        self.ElastixOptimizercomboBox.addItem("")
        self.ElastixOptimizercomboBox.addItem("")
        self.ElastixOptimizercomboBox.setObjectName(u"ElastixOptimizercomboBox")
        self.ElastixOptimizercomboBox.setGeometry(QRect(328, 5, 281, 30))
        self.ElastixOptimizercomboBox.setLayoutDirection(Qt.LeftToRight)
        self.ElastixOptimizercomboBox.setStyleSheet(u"")
        self.ForceBlendercheckBox = QCheckBox(self.tab)
        self.ForceBlendercheckBox.setObjectName(u"ForceBlendercheckBox")
        self.ForceBlendercheckBox.setGeometry(QRect(3, 65, 349, 20))
        self.ForceBlendercheckBox.setLayoutDirection(Qt.RightToLeft)
        self.TrabecularProportionSpinBox = QDoubleSpinBox(self.tab)
        self.TrabecularProportionSpinBox.setObjectName(u"TrabecularProportionSpinBox")
        self.TrabecularProportionSpinBox.setGeometry(QRect(334, 37, 61, 22))
        self.TrabecularProportionSpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.TrabecularProportionSpinBox.setDecimals(1)
        self.TrabecularProportionSpinBox.setMinimum(0.000000000000000)
        self.TrabecularProportionSpinBox.setMaximum(1.000000000000000)
        self.TrabecularProportionSpinBox.setSingleStep(0.100000000000000)
        self.TrabecularProportionSpinBox.setValue(1.000000000000000)
        self.FocalLengthLabel_3 = QLabel(self.tab)
        self.FocalLengthLabel_3.setObjectName(u"FocalLengthLabel_3")
        self.FocalLengthLabel_3.setGeometry(QRect(401, 38, 251, 20))
        self.grpManualFOV = QGroupBox(self.tab)
        self.grpManualFOV.setObjectName(u"grpManualFOV")
        self.grpManualFOV.setEnabled(False)
        self.grpManualFOV.setGeometry(QRect(233, 117, 206, 72))
        self.FOVDiameterSpinBox = QDoubleSpinBox(self.grpManualFOV)
        self.FOVDiameterSpinBox.setObjectName(u"FOVDiameterSpinBox")
        self.FOVDiameterSpinBox.setGeometry(QRect(105, 7, 90, 22))
        self.FOVDiameterSpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.FOVDiameterSpinBox.setDecimals(1)
        self.FOVDiameterSpinBox.setMinimum(10.000000000000000)
        self.FOVDiameterSpinBox.setMaximum(400.000000000000000)
        self.FOVDiameterSpinBox.setSingleStep(0.100000000000000)
        self.FOVDiameterSpinBox.setValue(200.000000000000000)
        self.DiameterLabel = QLabel(self.grpManualFOV)
        self.DiameterLabel.setObjectName(u"DiameterLabel")
        self.DiameterLabel.setGeometry(QRect(9, 40, 82, 20))
        self.FOVLengthSpinBox = QDoubleSpinBox(self.grpManualFOV)
        self.FOVLengthSpinBox.setObjectName(u"FOVLengthSpinBox")
        self.FOVLengthSpinBox.setGeometry(QRect(105, 40, 90, 22))
        self.FOVLengthSpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.FOVLengthSpinBox.setDecimals(1)
        self.FOVLengthSpinBox.setMinimum(200.000000000000000)
        self.FOVLengthSpinBox.setMaximum(600.000000000000000)
        self.FOVLengthSpinBox.setSingleStep(0.100000000000000)
        self.FOVLengthSpinBox.setValue(400.000000000000000)
        self.FocalLengthLabel = QLabel(self.grpManualFOV)
        self.FocalLengthLabel.setObjectName(u"FocalLengthLabel")
        self.FocalLengthLabel.setGeometry(QRect(9, 7, 94, 20))
        self.ManualFOVcheckBox = QCheckBox(self.tab)
        self.ManualFOVcheckBox.setObjectName(u"ManualFOVcheckBox")
        self.ManualFOVcheckBox.setGeometry(QRect(203, 93, 150, 20))
        self.ManualFOVcheckBox.setLayoutDirection(Qt.RightToLeft)
        self.FocalLengthLabel_2 = QLabel(self.tab)
        self.FocalLengthLabel_2.setObjectName(u"FocalLengthLabel_2")
        self.FocalLengthLabel_2.setGeometry(QRect(151, 37, 181, 20))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.label_6 = QLabel(self.tab_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(179, 16, 137, 16))
        self.CTX500CorrectioncomboBox = QComboBox(self.tab_2)
        self.CTX500CorrectioncomboBox.addItem("")
        self.CTX500CorrectioncomboBox.addItem("")
        self.CTX500CorrectioncomboBox.setObjectName(u"CTX500CorrectioncomboBox")
        self.CTX500CorrectioncomboBox.setGeometry(QRect(316, 11, 99, 30))
        self.CTX500CorrectioncomboBox.setLayoutDirection(Qt.LeftToRight)
        self.CTX500CorrectioncomboBox.setStyleSheet(u"")
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.CancelpushButton.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.ContinuepushButton.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.ResetpushButton.setText(QCoreApplication.translate("Dialog", u"Reset to defaults", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Elastix co-registration Optimizer", None))
        self.ElastixOptimizercomboBox.setItemText(0, QCoreApplication.translate("Dialog", u"AdaptiveStochasticGradientDescent", None))
        self.ElastixOptimizercomboBox.setItemText(1, QCoreApplication.translate("Dialog", u"FiniteDifferenceGradientDescent", None))
        self.ElastixOptimizercomboBox.setItemText(2, QCoreApplication.translate("Dialog", u"QuasiNewtonLBFGS", None))

        self.ForceBlendercheckBox.setText(QCoreApplication.translate("Dialog", u"Force using Blender for Constructive Solid Geometry   ", None))
        self.FocalLengthLabel_3.setText(QCoreApplication.translate("Dialog", u" (applicable using only MRI input)", None))
        self.grpManualFOV.setTitle("")
        self.DiameterLabel.setText(QCoreApplication.translate("Dialog", u"Length (mm)", None))
        self.FocalLengthLabel.setText(QCoreApplication.translate("Dialog", u"Diameter (mm)", None))
        self.ManualFOVcheckBox.setText(QCoreApplication.translate("Dialog", u"Manual Subvolume  ", None))
        self.FocalLengthLabel_2.setText(QCoreApplication.translate("Dialog", u"Proportion of trabecular bone", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Domain Generation", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"CTX-500 Correction", None))
        self.CTX500CorrectioncomboBox.setItemText(0, QCoreApplication.translate("Dialog", u"Original", None))
        self.CTX500CorrectioncomboBox.setItemText(1, QCoreApplication.translate("Dialog", u"July2024", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"Transcranial Ultrasound", None))
    # retranslateUi

