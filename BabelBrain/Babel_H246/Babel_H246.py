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

import platform
_IS_MAC = platform.system() == 'Darwin'

def resource_path():  # needed for bundling
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if not _IS_MAC:
        return os.path.split(Path(__file__))[0]

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = Path(sys._MEIPASS) / 'Babel_H246'
    else:
        bundle_dir = Path(__file__).parent

    return bundle_dir

class H246(QWidget):
    def __init__(self,parent=None,MainApp=None):
        super(H246, self).__init__(parent)
        self.static_canvas=None
        self._MainApp=MainApp
        self.DefaultConfig()
        self.load_ui()


    def load_ui(self):
        loader = QUiLoader()
        #path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        path = os.path.join(resource_path(), "form.ui")
        
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.Widget =loader.load(ui_file, self)
        ui_file.close()

        self.Widget.TPODistanceSpinBox.setMinimum(self.Config['MinimalTPODistance']*1e3)
        self.Widget.TPODistanceSpinBox.setMaximum(self.Config['MaximalTPODistance']*1e3)
        self.Widget.TPODistanceSpinBox.valueChanged.connect(self.TPODistanceUpdate)
        self.Widget.TPORangeLabel.setText('[%3.1f - %3.1f]' % (self.Config['MinimalTPODistance']*1e3,self.Config['MaximalTPODistance']*1e3))
        self.Widget.CalculatePlanningMask.clicked.connect(self.RunSimulation)

    @Slot()
    def TPODistanceUpdate(self,value):
        self._ZSteering =self.Widget.TPODistanceSpinBox.value()/1e3
        print('ZSteering',self._ZSteering*1e3)

    def DefaultConfig(self):
        #Specific parameters for the H246 - to be configured later via a yaml

        #with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'default.yaml'), 'r') as file:
        with open(os.path.join(resource_path(),'default.yaml'), 'r') as file:
            config = yaml.safe_load(file)
        print("H246 configuration:")
        print(config)

        self.Config=config

    def NotifyGeneratedMask(self):
        VoxelSize=self._MainApp._DataMask.header.get_zooms()[0]
        TargetLocation =np.array(np.where(self._MainApp._FinalMask==5.0)).flatten()
        LineOfSight=self._MainApp._FinalMask[TargetLocation[0],TargetLocation[1],:]
        StartSkin=np.where(LineOfSight>0)[0].min()
        DistanceFromSkin = (TargetLocation[2]-StartSkin)*VoxelSize

        self.Widget.TPODistanceSpinBox.setValue(np.round(DistanceFromSkin,1))
        self.Widget.DistanceSkinLabel.setText('%3.2f'%(DistanceFromSkin))
        self.Widget.DistanceSkinLabel.setProperty('UserData',DistanceFromSkin)

        self.TPODistanceUpdate(0)

    @Slot()
    def RunSimulation(self):
        self._FullSolName=self._MainApp._prefix_path+'DataForSim.h5'
        self._WaterSolName=self._MainApp._prefix_path+'Water_DataForSim.h5'

        print('FullSolName',self._FullSolName)
        print('WaterSolName',self._WaterSolName)
        bCalcFields=False
        if os.path.isfile(self._FullSolName) and os.path.isfile(self._WaterSolName):
            Skull=ReadFromH5py(self._FullSolName)
            TPO=Skull['ZSteering']

            ret = QMessageBox.question(self,'', "Acoustic sim files already exist with:.\n"+
                                    "ZSteering=%3.2f\n" %(TPO*1e3)+
                                    "TxMechanicalAdjustmentX=%3.2f\n" %(Skull['TxMechanicalAdjustmentX']*1e3)+
                                    "TxMechanicalAdjustmentY=%3.2f\n" %(Skull['TxMechanicalAdjustmentY']*1e3)+
                                    "Do you want to recalculate?\nSelect No to reload",
                QMessageBox.Yes | QMessageBox.No)

            if ret == QMessageBox.Yes:
                bCalcFields=True
            else:
                self.Widget.TPODistanceSpinBox.setValue(TPO*1e3)
                self.Widget.XMechanicSpinBox.setValue(Skull['TxMechanicalAdjustmentX']*1e3)
                self.Widget.YMechanicSpinBox.setValue(Skull['TxMechanicalAdjustmentY']*1e3)
        else:
            bCalcFields = True
        if bCalcFields:
            self._MainApp.Widget.tabWidget.setEnabled(False)
            self.thread = QThread()
            self.worker = RunAcousticSim(self._MainApp,self.thread)
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

    def NotifyError(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText("There was an error in execution -\nconsult log window for details")
        msgBox.exec()

    @Slot()
    def UpdateAcResults(self):
        #this will generate a modified trajectory file
        self._MainApp.Widget.tabWidget.setEnabled(True)
        self._MainApp.ThermalSim.setEnabled(True)
        Water=ReadFromH5py(self._WaterSolName)
        Skull=ReadFromH5py(self._FullSolName)
        if self._MainApp._bInUseWithBrainsight:
            with open(self._MainApp._BrainsightSyncPath+os.sep+'Output.txt','w') as f:
                f.write(self._MainApp._BrainsightInput)    
        self._MainApp.ExportTrajectory(CorX=Skull['AdjustmentInRAS'][0],
                                    CorY=Skull['AdjustmentInRAS'][1],
                                    CorZ=Skull['AdjustmentInRAS'][2])

        LocTarget=Skull['TargetLocation']
        print(LocTarget)

        for d in [Water,Skull]:
            for t in ['p_amp','MaterialMap']:
                d[t]=np.ascontiguousarray(np.flip(d[t],axis=2))

        DistanceToTarget=self.Widget.DistanceSkinLabel.property('UserData')
        dx=  np.mean(np.diff(Skull['x_vec']))

        Water['z_vec']*=1e3
        Skull['z_vec']*=1e3
        Skull['x_vec']*=1e3
        Skull['y_vec']*=1e3
        Skull['MaterialMap'][Skull['MaterialMap']==3]=2
        Skull['MaterialMap'][Skull['MaterialMap']==4]=3

        IWater=Water['p_amp']**2/2/Water['Material'][0,0]/Water['Material'][0,1]

        DensityMap=Skull['Material'][:,0][Skull['MaterialMap']]
        SoSMap=    Skull['Material'][:,1][Skull['MaterialMap']]

        ISkull=Skull['p_amp']**2/2/Skull['Material'][4,0]/Skull['Material'][4,1]

        IntWaterLocation=IWater[LocTarget[0],LocTarget[1],LocTarget[2]]
        IntSkullLocation=ISkull[LocTarget[0],LocTarget[1],LocTarget[2]]
        
        ISkull[Skull['MaterialMap']!=3]=0
        cxr,cyr,czr=np.where(ISkull==ISkull.max())
        cxr=cxr[0]
        cyr=cyr[0]
        czr=czr[0]

        EnergyAtFocusSkull=ISkull[:,:,czr].sum()*dx**2

        cxr,cyr,czr=np.where(IWater==IWater.max())
        cxr=cxr[0]
        cyr=cyr[0]
        czr=czr[0]

        EnergyAtFocusWater=IWater[:,:,czr].sum()*dx**2

        print('EnergyAtFocusWater',EnergyAtFocusWater,'EnergyAtFocusSkull',EnergyAtFocusSkull)
        
        Factor=EnergyAtFocusWater/EnergyAtFocusSkull
        print('*'*40+'\n'+'*'*40+'\n'+'Correction Factor for Isppa',Factor,'\n'+'*'*40+'\n'+'*'*40+'\n')
        
        ISkull/=ISkull.max()
        IWater/=IWater.max()
        
        self._figAcField=Figure(figsize=(14, 12))

        if self.static_canvas is not None:
            self._layout.removeItem(self._layout.itemAt(0))
            self._layout.removeItem(self._layout.itemAt(0))
        else:
            self._layout = QVBoxLayout(self.Widget.AcField_plot1)

        self.static_canvas = FigureCanvas(self._figAcField)
        toolbar=NavigationToolbar2QT(self.static_canvas,self)
        self._layout.addWidget(toolbar)
        self._layout.addWidget(self.static_canvas)
        static_ax1,static_ax2 = self.static_canvas.figure.subplots(1,2)

        dz=np.diff(Skull['z_vec']).mean()
        Zvec=Skull['z_vec'].copy()
        Zvec-=Zvec[LocTarget[2]]
        Zvec+=DistanceToTarget
        XX,ZZ=np.meshgrid(Skull['x_vec'],Zvec)
        self._imContourf1=static_ax1.contourf(XX,ZZ,ISkull[:,LocTarget[1],:].T,np.arange(2,22,2)/20,cmap=plt.cm.jet)
        h=plt.colorbar(self._imContourf1,ax=static_ax1)
        h.set_label('$I_{\mathrm{SPPA}}$ (normalized)')
        static_ax1.contour(XX,ZZ,Skull['MaterialMap'][:,LocTarget[1],:].T,[0,1,2,3], cmap=plt.cm.gray)
        static_ax1.set_aspect('equal')
        static_ax1.set_xlabel('X mm')
        static_ax1.set_ylabel('Z mm')
        static_ax1.invert_yaxis()
        static_ax1.plot(0,DistanceToTarget,'+y',markersize=18)

        YY,ZZ=np.meshgrid(Skull['y_vec'],Zvec)

        self._imContourf2=static_ax2.contourf(YY,ZZ,ISkull[LocTarget[0],:,:].T,np.arange(2,22,2)/20,cmap=plt.cm.jet)
        h=plt.colorbar(self._imContourf1,ax=static_ax2)
        h.set_label('$I_{\mathrm{SPPA}}$ (normalized)')
        static_ax2.contour(YY,ZZ,Skull['MaterialMap'][LocTarget[0],:,:].T,[0,1,2,3], cmap=plt.cm.gray)
        static_ax2.set_aspect('equal')
        static_ax2.set_xlabel('Y mm')
        static_ax2.set_ylabel('Z mm')
        static_ax2.invert_yaxis()
        static_ax2.plot(0,DistanceToTarget,'+y',markersize=18)
        self._figAcField.set_facecolor(np.array(self.Widget.palette().color(QPalette.Window).getRgb())/255)
        self._figAcField.set_tight_layout(True)

        #f.set_title('MAIN SIMULATION RESULTS')
   
    def GetExport(self):
        Export={}
        for k in ['TPODistance','XMechanic','YMechanic']:
            Export[k]=getattr(self.Widget,k+'SpinBox').value()
        return Export

class RunAcousticSim(QObject):

    finished = Signal()
    endError = Signal()

    def __init__(self,mainApp,thread):
        super(RunAcousticSim, self).__init__()
        self._mainApp=mainApp
        self._thread=thread

    def run(self):

        deviceName=self._mainApp.Config['ComputingDevice']
        COMPUTING_BACKEND=self._mainApp.Config['ComputingBackend']
        basedir,ID=os.path.split(os.path.split(self._mainApp.Config['T1W'])[0])
        basedir+=os.sep
        Target=[self._mainApp.Config['ID']+'_'+self._mainApp.Config['TxSystem']]

        InputSim=self._mainApp._outnameMask

        #we can use mechanical adjustments in other directions for final tuning
        TxMechanicalAdjustmentX= self._mainApp.AcSim.Widget.XMechanicSpinBox.value()/1e3 #in m
        TxMechanicalAdjustmentY= self._mainApp.AcSim.Widget.YMechanicSpinBox.value()/1e3  #in m
        TxMechanicalAdjustmentZ= self._mainApp.AcSim.Widget.ZMechanicSpinBox.value()/1e3  #in m

        ###############
        TPODistance=self._mainApp.AcSim.Widget.TPODistanceSpinBox.value()/1e3  #Add here the final adjustment)
        ##############

        print('Ideal Distance to program in TPO : ', TPODistance*1e3)


        ZSteering=TPODistance
        print('ZSteering',ZSteering*1e3)

        Frequencies = [self._mainApp.Widget.USMaskkHzDropDown.property('UserData')]
        basePPW=[self._mainApp.Widget.USPPWSpinBox.property('UserData')]
        T0=time.time()
        kargs={}
        kargs['ID']=ID
        kargs['deviceName']=deviceName
        kargs['COMPUTING_BACKEND']=COMPUTING_BACKEND
        kargs['basePPW']=basePPW
        kargs['basedir']=basedir
        kargs['TxMechanicalAdjustmentZ']=TxMechanicalAdjustmentZ
        kargs['TxMechanicalAdjustmentX']=TxMechanicalAdjustmentX
        kargs['TxMechanicalAdjustmentY']=TxMechanicalAdjustmentY
        kargs['ZSteering']=ZSteering
        kargs['Frequencies']=Frequencies

        # Start mask generation as separate process.
        queue=Queue()
        fieldWorkerProcess = Process(target=CalculateFieldProcess, 
                                    args=(queue,Target),
                                    kwargs=kargs)
        fieldWorkerProcess.start()      
        # progress.
        T0=time.time()
        bNoError=True
        while fieldWorkerProcess.is_alive():
            time.sleep(0.1)
            while queue.empty() == False:
                cMsg=queue.get()
                print(cMsg,end='')
                if '--Babel-Brain-Low-Error' in cMsg:
                    bNoError=False  
        fieldWorkerProcess.join()
        while queue.empty() == False:
            cMsg=queue.get()
            print(cMsg,end='')
            if '--Babel-Brain-Low-Error' in cMsg:
                bNoError=False
        if bNoError:
            TEnd=time.time()
            print('Total time',TEnd-T0)
            print("*"*40)
            print("*"*5+" DONE ultrasound simulation.")
            print("*"*40)
            self.finished.emit()
        else:
            print("*"*40)
            print("*"*5+" Error in execution.")
            print("*"*40)
            self.endError.emit()




if __name__ == "__main__":
    app = QApplication([])
    widget = H246()
    widget.show()
    sys.exit(app.exec_())