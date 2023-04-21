# This Python file uses the following encoding: utf-8

from multiprocessing import Process,Queue
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import (QApplication, QWidget,QGridLayout,
                QHBoxLayout,QVBoxLayout,QLineEdit,QDialog,
                QGridLayout, QSpacerItem, QInputDialog, QFileDialog,
                QErrorMessage, QMessageBox)
from PySide6.QtCore import QFile,Slot,QObject,Signal,QThread
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPalette, QTextCursor

import numpy as np

from scipy.io import loadmat
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import (
    FigureCanvas,NavigationToolbar2QT)
import os
import sys
import shutil
from datetime import datetime
import time
import yaml
from BabelViscoFDTD.H5pySimple import ReadFromH5py, SaveToH5py
from .CalculateFieldProcess import CalculateFieldProcess

from .Babel_SingleTx import SingleTx,RunAcousticSim

import platform
_IS_MAC = platform.system() == 'Darwin'

def resource_path():  # needed for bundling
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if not _IS_MAC:
        return os.path.split(Path(__file__))[0]

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = Path(sys._MEIPASS) / 'Babel_SingleTx'
    else:
        bundle_dir = Path(__file__).parent

    return bundle_dir

def DistanceOutPlaneToFocus(FocalLength,Diameter):
    return np.sqrt(FocalLength**2-(Diameter/2)**2)

class BSonix(SingleTx):
    def __init__(self,parent=None,MainApp=None,formfile='formBx.ui'):
        super(BSonix, self).__init__(parent,MainApp,formfile)

    def load_ui(self,formfile):
        loader = QUiLoader()
        path = os.path.join(resource_path(), formfile)
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.Widget =loader.load(ui_file, self)
        ui_file.close()
        self.Widget.CalculatePlanningMask.clicked.connect(self.RunSimulation)
        self.Widget.ZMechanicSpinBox.valueChanged.connect(self.UpdateTxInfo)
        self.Widget.ShowWaterResultscheckBox.stateChanged.connect(self.UpdateAcResults)
        self.Widget.TransducerModelcomboBox.currentIndexChanged.connect(self.UpdateTxInfo)
        
        
    def DefaultConfig(self,cfile='defaultBSonix.yaml'):
        super(BSonix,self).DefaultConfig(cfile)

    def NotifyGeneratedMask(self):
        super(BSonix, self).NotifyGeneratedMask()
        self.Widget.ZMechanicSpinBox.setValue(self.Widget.ZMechanicSpinBox.maximum())

    def GetTxModel(self):
        return "BSonix"+self.Widget.TransducerModelcomboBox.currentText()

    def UpdateLimits(self):
        model=self.GetTxModel()
        FocalLength = self.Config[model]['TxFoc']*1e3
        Diameter = self.Config[model]['TxDiam']*1e3
        DOut=DistanceOutPlaneToFocus(FocalLength,Diameter)-self.Config[model]['AdjustDistanceSkin']*1e3
        ZMax=DOut-self.Widget.DistanceSkinLabel.property('UserData')
        self.Widget.ZMechanicSpinBox.setMaximum(np.round(ZMax,1))

    @Slot()
    def UpdateTxInfo(self):
        if self._bIgnoreUpdate:
            return
        self._bIgnoreUpdate=True
        self.UpdateLimits()
        ZMax=self.Widget.ZMechanicSpinBox.maximum()
        ZMec=self.Widget.ZMechanicSpinBox.value()
        if ZMec > ZMax:
            self.ZMechanicSpinBox.setValue(ZMax)
            ZMec=ZMax
        
        CurDistance=ZMax-ZMec
        self.Widget.DistanceTxToSkinLabel.setText('%3.1f' %(CurDistance))
        self._bIgnoreUpdate=False       

    @Slot()
    def RunSimulation(self):
        model=self.GetTxModel()
        FocalLength = self.Config[model]['TxFoc']*1e3
        Diameter = self.Config[model]['TxDiam']*1e3
        self._FullSolName=self._MainApp._prefix_path+model+'_DataForSim.h5' 
        self._WaterSolName=self._MainApp._prefix_path+model+'_Water_DataForSim.h5' 
        extrasuffix=model+'_'
        print('FullSolName',self._FullSolName)
        print('WaterSolName',self._WaterSolName)
        bCalcFields=False
        if os.path.isfile(self._FullSolName) and os.path.isfile(self._WaterSolName):
            Skull=ReadFromH5py(self._FullSolName)

            ret = QMessageBox.question(self,'', "Acoustic sim files already exist with:.\n"+
                                    "TxMechanicalAdjustmentX=%3.2f\n" %(Skull['TxMechanicalAdjustmentX']*1e3)+
                                    "TxMechanicalAdjustmentY=%3.2f\n" %(Skull['TxMechanicalAdjustmentY']*1e3)+
                                    "TxMechanicalAdjustmentZ=%3.2f\n" %(Skull['TxMechanicalAdjustmentZ']*1e3)+
                                    "Do you want to recalculate?\nSelect No to reload",
                QMessageBox.Yes | QMessageBox.No)

            if ret == QMessageBox.Yes:
                bCalcFields=True
            else:
                self.Widget.XMechanicSpinBox.setValue(Skull['TxMechanicalAdjustmentX']*1e3)
                self.Widget.YMechanicSpinBox.setValue(Skull['TxMechanicalAdjustmentY']*1e3)
                self.Widget.ZMechanicSpinBox.setValue(Skull['TxMechanicalAdjustmentZ']*1e3)
        else:
            bCalcFields = True
        if bCalcFields:
            self._MainApp.Widget.tabWidget.setEnabled(False)
            self.thread = QThread()
            self.worker = RunAcousticSim(self._MainApp,self.thread,
                                        extrasuffix,Diameter/1e3,FocalLength/1e3)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.UpdateAcResults)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.worker.endError.connect(self.NotifyError)
            self.worker.endError.connect(self.thread.quit)
            self.worker.endError.connect(self.worker.deleteLater)
 
            self.thread.start()
        else:
            self.UpdateAcResults()

