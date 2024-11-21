from PyQt5 import QtCore, QtGui, QtWidgets
from Bar import MyBar
from PdModel import PandasModel
from ImageViewer import PhotoViewer
import sys, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense
from keras_visualizer import visualizer 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class ModelTrainingThread(QtCore.QThread):
    updateProgress = QtCore.pyqtSignal(int, float)
    finished = QtCore.pyqtSignal(list, list)

    def __init__(self, main):
        super().__init__()
        self.main = main
        self.is_cancelled = False

    def cancel(self):
        self.is_cancelled = True

    def run(self):
        full_history = []
        for epoch in range(self.main.nb_epoch_box.value()):
            if self.is_cancelled:
                break

            history = self.main.model.fit(self.main.X_train, self.main.y_train, epochs=1, batch_size=1, verbose=0)
            self.updateProgress.emit(epoch + 1, history.history['loss'][0])
            full_history.append(history.history['loss'][0])
        
        pred = self.main.model.predict(self.main.X_test, verbose = 0)

        y_pred = []
        for i in pred:
            y_pred.append(i[0])

        rmse_value = ((y_pred - self.main.y_test) ** 2).mean() ** 0.5

        self.main.rmse.setText('RMSE :' + str(round(rmse_value, 3)))
        mean = self.main.y_test.mean()

        if rmse_value >= mean * 0.15 :
            self.main.rmse.setStyleSheet("color : red;")

        elif rmse_value >= mean * 0.05 :
            self.main.rmse.setStyleSheet("color : yellow;")

        else:
            self.main.rmse.setStyleSheet("color : green;")

        self.finished.emit(full_history, y_pred)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.FramelessWindowHint)

        np.random.seed(42)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy_views = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.main_lay = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_lay.setObjectName("main_lay")

        self.main_lay.addWidget(MyBar(MainWindow))
        self.main_lay.setContentsMargins(0,0,0,0)

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")

######################################################################
############################# PARAMETRES #############################
######################################################################

        self.page_par = QtWidgets.QWidget()
        self.page_par.setObjectName("page_par")

        self.page_par_lay = QtWidgets.QVBoxLayout(self.page_par)
        self.page_par_lay.setObjectName("page_par_lay")

        self.par_lab = QtWidgets.QLabel(self.page_par)
        self.par_lab.setSizePolicy(sizePolicy)
        self.par_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.par_lab.setObjectName("par_lab")
        self.page_par_lay.addWidget(self.par_lab)

        self.line_par_t = QtWidgets.QFrame(self.page_par)
        self.line_par_t.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_par_t.setLineWidth(5)
        self.line_par_t.setStyleSheet("color : rgba(63, 59, 146, 255);")
        self.line_par_t.setObjectName("line_par_t")
        self.page_par_lay.addWidget(self.line_par_t)

        self.par_lay = QtWidgets.QHBoxLayout()
        self.par_lay.setObjectName("par_lay")

############################# DATA #############################

        self.data_lay = QtWidgets.QVBoxLayout()
        self.data_lay.setObjectName("data_lay")

        self.data_lab = QtWidgets.QLabel(self.page_par)
        self.data_lab.setSizePolicy(sizePolicy)
        self.data_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.data_lab.setObjectName("data_lab")
        self.data_lay.addWidget(self.data_lab)

        self.data_lay.addSpacerItem(spacerItem2)

        self.nb_val_lab = QtWidgets.QLabel(self.page_par)
        self.nb_val_lab.setSizePolicy(sizePolicy)
        self.nb_val_lab.setObjectName("nb_val_lab")
        self.data_lay.addWidget(self.nb_val_lab)

        self.nb_val_box = QtWidgets.QSpinBox(self.page_par)
        self.nb_val_box.setObjectName("nb_val_box")
        self.nb_val_box.setAlignment(QtCore.Qt.AlignCenter)
        self.nb_val_box.setAccelerated(True)
        self.nb_val_box.setMinimum(10)
        self.nb_val_box.setMaximum(1000)
        self.nb_val_box.setValue(100)
        self.data_lay.addWidget(self.nb_val_box)

        self.data_lay.addSpacerItem(spacerItem2)

        self.min_lab = QtWidgets.QLabel(self.page_par)
        self.min_lab.setSizePolicy(sizePolicy)
        self.min_lab.setObjectName("min_lab")
        self.data_lay.addWidget(self.min_lab)

        self.min_box = QtWidgets.QSpinBox(self.page_par)
        self.min_box.setObjectName("min_box")
        self.min_box.setAlignment(QtCore.Qt.AlignCenter)
        self.min_box.setAccelerated(True)
        self.min_box.setMinimum(1)
        self.min_box.setMaximum(99)
        self.min_box.setValue(1)
        self.data_lay.addWidget(self.min_box)

        self.data_lay.addSpacerItem(spacerItem2)

        self.max_lab = QtWidgets.QLabel(self.page_par)
        self.max_lab.setSizePolicy(sizePolicy)
        self.max_lab.setObjectName("max_lab")
        self.data_lay.addWidget(self.max_lab)

        self.max_box = QtWidgets.QSpinBox(self.page_par)
        self.max_box.setObjectName("max_box")
        self.max_box.setAlignment(QtCore.Qt.AlignCenter)
        self.max_box.setAccelerated(True)
        self.max_box.setMinimum(2)
        self.max_box.setMaximum(100)
        self.max_box.setValue(100)
        self.data_lay.addWidget(self.max_box)

        self.data_lay.addSpacerItem(spacerItem2)

        self.par_lay.addLayout(self.data_lay)

        self.line_par_l = QtWidgets.QFrame(self.page_par)
        self.line_par_l.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_par_l.setLineWidth(5)
        self.line_par_l.setStyleSheet("color : rgba(63, 59, 146, 255);")
        self.line_par_l.setObjectName("line_par_l")
        self.par_lay.addWidget(self.line_par_l)

############################# EQUATION #############################

        self.eq_lay = QtWidgets.QVBoxLayout()
        self.eq_lay.setObjectName("eq_lay")

        self.eq_lab = QtWidgets.QLabel(self.page_par)
        self.eq_lab.setSizePolicy(sizePolicy)
        self.eq_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.eq_lab.setObjectName("eq_lab")
        self.eq_lay.addWidget(self.eq_lab)

        self.eq_box = QtWidgets.QLineEdit(self.page_par)
        self.eq_box.setObjectName("eq_box")
        self.eq_box.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.eq_box.setAlignment(QtCore.Qt.AlignCenter) 
        self.eq_box.setText("a + b + c")
        self.eq_lay.addWidget(self.eq_box)
        
        self.par_lay.addLayout(self.eq_lay)

        self.line_par_r = QtWidgets.QFrame(self.page_par)
        self.line_par_r.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_par_r.setLineWidth(5)
        self.line_par_r.setStyleSheet("color : rgba(63, 59, 146, 255);")
        self.line_par_r.setObjectName("line_par_r")
        self.par_lay.addWidget(self.line_par_r)

############################# MODEL #############################

        self.model_lay = QtWidgets.QVBoxLayout()
        self.model_lay.setObjectName("model_lay")

        self.model_lab = QtWidgets.QLabel(self.page_par)
        self.model_lab.setSizePolicy(sizePolicy)
        self.model_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.model_lab.setObjectName("model_lab")
        self.model_lay.addWidget(self.model_lab)

        self.model_lay.addSpacerItem(spacerItem2)

        self.nb_layer_lab = QtWidgets.QLabel(self.page_par)
        self.nb_layer_lab.setSizePolicy(sizePolicy)
        self.nb_layer_lab.setObjectName("nb_layer_lab")
        self.model_lay.addWidget(self.nb_layer_lab)

        self.nb_layer_box = QtWidgets.QSpinBox(self.page_par)
        self.nb_layer_box.setObjectName("nb_layer_box")
        self.nb_layer_box.setAlignment(QtCore.Qt.AlignCenter)
        self.nb_layer_box.setMinimum(1)
        self.nb_layer_box.setMaximum(3)
        self.nb_layer_box.setValue(1)
        self.model_lay.addWidget(self.nb_layer_box)

        self.model_lay.addSpacerItem(spacerItem2)
        self.model_lay.addSpacerItem(spacerItem2)

        self.nb_neur_lab = QtWidgets.QLabel(self.page_par)
        self.nb_neur_lab.setSizePolicy(sizePolicy)
        self.nb_neur_lab.setObjectName("nb_neur_lab")
        self.model_lay.addWidget(self.nb_neur_lab)

        self.model_lay.addSpacerItem(spacerItem2)

        self.layer1_lab = QtWidgets.QLabel(self.page_par)
        self.layer1_lab.setSizePolicy(sizePolicy)
        self.layer1_lab.setObjectName("layer1_lab")
        self.model_lay.addWidget(self.layer1_lab)

        self.layer1_box = QtWidgets.QSpinBox(self.page_par)
        self.layer1_box.setObjectName("layer1_box")
        self.layer1_box.setAlignment(QtCore.Qt.AlignCenter)
        self.layer1_box.setMinimum(1)
        self.layer1_box.setMaximum(500)
        self.layer1_box.setValue(12)
        self.layer1_box.setAccelerated(True)
        self.model_lay.addWidget(self.layer1_box)

        self.model_lay.addSpacerItem(spacerItem2)

        self.layer2_lab = QtWidgets.QLabel(self.page_par)
        self.layer2_lab.setSizePolicy(sizePolicy)
        self.layer2_lab.setObjectName("layer2_lab")
        self.model_lay.addWidget(self.layer2_lab)

        self.layer2_box = QtWidgets.QSpinBox(self.page_par)
        self.layer2_box.setObjectName("layer2_box")
        self.layer2_box.setAlignment(QtCore.Qt.AlignCenter)
        self.layer2_box.setMinimum(1)
        self.layer2_box.setMaximum(500)
        self.layer2_box.setValue(12)
        self.layer2_box.setAccelerated(True)
        self.model_lay.addWidget(self.layer2_box)

        self.model_lay.addSpacerItem(spacerItem2)

        self.layer3_lab = QtWidgets.QLabel(self.page_par)
        self.layer3_lab.setSizePolicy(sizePolicy)
        self.layer3_lab.setObjectName("layer3_lab")
        self.model_lay.addWidget(self.layer3_lab)

        self.layer3_box = QtWidgets.QSpinBox(self.page_par)
        self.layer3_box.setObjectName("layer3_box")
        self.layer3_box.setAlignment(QtCore.Qt.AlignCenter)
        self.layer3_box.setMinimum(1)
        self.layer3_box.setMaximum(500)
        self.layer3_box.setValue(12)
        self.layer3_box.setAccelerated(True)
        self.model_lay.addWidget(self.layer3_box)

        self.model_lay.addSpacerItem(spacerItem2)

        self.par_lay.addLayout(self.model_lay)

        self.par_lay.setStretch(0, 5)
        self.par_lay.setStretch(2, 8)
        self.par_lay.setStretch(4, 5)

##########################################################

        self.page_par_lay.addLayout(self.par_lay)

        self.page2_but = QtWidgets.QPushButton(self.page_par)
        self.page2_but.setObjectName("page2_but")
        self.page2_but.setIcon(QtGui.QIcon("Assets:right.png"))
        self.page2_but.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.page_par_lay.addWidget(self.page2_but)

        self.stackedWidget.addWidget(self.page_par)

######################################################################
############################## OVERVIEW ##############################
######################################################################

        self.page_over = QtWidgets.QWidget()
        self.page_over.setObjectName("page_over")

        self.page_over_lay = QtWidgets.QVBoxLayout(self.page_over)
        self.page_over_lay.setObjectName("page_over_lay")

        self.over_lab = QtWidgets.QLabel(self.page_over)
        self.over_lab.setSizePolicy(sizePolicy)
        self.over_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.over_lab.setObjectName("over_lab")
        self.page_over_lay.addWidget(self.over_lab)

        self.over_line_t = QtWidgets.QFrame(self.page_over)
        self.over_line_t.setFrameShape(QtWidgets.QFrame.HLine)
        self.over_line_t.setLineWidth(5)
        self.over_line_t.setStyleSheet("color : rgba(63, 59, 146, 255);")
        self.over_line_t.setObjectName("over_line_t")
        self.page_over_lay.addWidget(self.over_line_t)

        self.over_lay = QtWidgets.QHBoxLayout()
        self.over_lay.setObjectName("over_lay")

############################# DATA OVERVIEW #############################

        self.over_data_lay = QtWidgets.QVBoxLayout()
        self.over_data_lay.setObjectName("over_data_lay")

        self.over_data_lab = QtWidgets.QLabel(self.page_over)
        self.over_data_lab.setSizePolicy(sizePolicy)
        self.over_data_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.over_data_lab.setObjectName("over_data_lab")
        self.over_data_lay.addWidget(self.over_data_lab)

        self.over_data_view = QtWidgets.QTableView(self.page_over)
        self.over_data_view.setSizePolicy(sizePolicy_views)
        self.over_data_view.setObjectName("over_data_view")
        self.over_data_lay.addWidget(self.over_data_view)
        self.over_lay.addLayout(self.over_data_lay)

        self.line_over_c = QtWidgets.QFrame(self.page_over)
        self.line_over_c.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_over_c.setLineWidth(5)
        self.line_over_c.setStyleSheet("color : rgba(63, 59, 146, 255);")
        self.line_over_c.setObjectName("line_over_c")
        self.over_lay.addWidget(self.line_over_c)

############################# MODEL OVERVIEW #############################

        self.over_model_lay = QtWidgets.QVBoxLayout()
        self.over_model_lay.setObjectName("over_model_lay")

        self.over_model_lab = QtWidgets.QLabel(self.page_over)
        self.over_model_lab.setSizePolicy(sizePolicy)
        self.over_model_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.over_model_lab.setObjectName("over_model_lab")
        self.over_model_lay.addWidget(self.over_model_lab)

        self.over_model_img = PhotoViewer(MainWindow)
        self.over_model_img.setObjectName("over_model_img")
        self.over_model_lay.addWidget(self.over_model_img)

        self.over_lay.addLayout(self.over_model_lay)

        self.over_lay.setStretch(0, 3)
        self.over_lay.setStretch(2, 7)

######################################################################

        self.page_over_lay.addLayout(self.over_lay)

        self.page2_but_lay = QtWidgets.QHBoxLayout()
        self.page2_but_lay.setObjectName("page2_but_lay")

        self.page1_but = QtWidgets.QPushButton(self.page_over)
        self.page1_but.setObjectName("page1_but")
        self.page1_but.setIcon(QtGui.QIcon("Assets:left.png"))
        self.page2_but_lay.addWidget(self.page1_but)

        self.page3_but = QtWidgets.QPushButton(self.page_over)
        self.page3_but.setObjectName("page3_but")
        self.page3_but.setIcon(QtGui.QIcon("Assets:right.png"))
        self.page3_but.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.page2_but_lay.addWidget(self.page3_but)

        self.page_over_lay.addLayout(self.page2_but_lay)

        self.stackedWidget.addWidget(self.page_over)

#####################################################################
############################### TRAIN ###############################
#####################################################################

        self.page_train = QtWidgets.QWidget()
        self.page_train.setObjectName("page_train")

        self.page_train_lay = QtWidgets.QVBoxLayout(self.page_train)
        self.page_train_lay.setObjectName("page_train_lay")

        self.train_lab = QtWidgets.QLabel(self.page_train)
        self.train_lab.setSizePolicy(sizePolicy)
        self.train_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.train_lab.setObjectName("train_lab")
        self.page_train_lay.addWidget(self.train_lab)

        self.line_train_t = QtWidgets.QFrame(self.page_train)
        self.line_train_t.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_train_t.setLineWidth(5)
        self.line_train_t.setStyleSheet("color : rgba(63, 59, 146, 255);")
        self.line_train_t.setObjectName("line_train_t")
        self.page_train_lay.addWidget(self.line_train_t)

############################# TRAIN PARAMS #############################

        self.train_set_lay = QtWidgets.QHBoxLayout()
        self.train_set_lay.setObjectName("train_set_lay")

        self.nb_epoch_lab = QtWidgets.QLabel(self.page_train)
        self.nb_epoch_lab.setSizePolicy(sizePolicy)
        self.nb_epoch_lab.setObjectName("nb_epoch_lab")
        self.train_set_lay.addWidget(self.nb_epoch_lab)

        self.nb_epoch_box = QtWidgets.QSpinBox(self.page_train)
        self.nb_epoch_box.setObjectName("nb_epoch_box")
        self.nb_epoch_box.setAlignment(QtCore.Qt.AlignCenter)
        self.nb_epoch_box.setMinimum(1)
        self.nb_epoch_box.setMaximum(10000)
        self.nb_epoch_box.setValue(50)
        self.nb_epoch_box.setAccelerated(True)
        self.train_set_lay.addWidget(self.nb_epoch_box)

        self.train_set_lay.addItem(spacerItem)

        self.start_train_but = QtWidgets.QPushButton(self.page_train)
        self.start_train_but.setObjectName("start_train_but")
        self.start_train_but.setIcon(QtGui.QIcon("Assets:start.png"))
        self.train_set_lay.addWidget(self.start_train_but)

        self.resume_train_but = QtWidgets.QPushButton(self.page_train)
        self.resume_train_but.setObjectName("resume_train_but")
        self.resume_train_but.setIcon(QtGui.QIcon("Assets:resume.png"))
        self.train_set_lay.addWidget(self.resume_train_but)

        self.page_train_lay.addLayout(self.train_set_lay)

        self.line_train_t_2 = QtWidgets.QFrame(self.page_train)
        self.line_train_t_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_train_t_2.setLineWidth(5)
        self.line_train_t_2.setStyleSheet("color : rgba(63, 59, 146, 255);")
        self.line_train_t_2.setObjectName("line_train_t_2")
        self.page_train_lay.addWidget(self.line_train_t_2)

        self.train_res_lay = QtWidgets.QHBoxLayout()
        self.train_res_lay.setObjectName("train_res_lay")

############################# TRAIN DATA RESULTS #############################

        self.val_res_lay = QtWidgets.QVBoxLayout()
        self.val_res_lay.setObjectName("val_res_lay")

        self.val_res_lab = QtWidgets.QLabel(self.page_train)
        self.val_res_lab.setSizePolicy(sizePolicy)
        self.val_res_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.val_res_lab.setObjectName("val_res_lab")
        self.val_res_lay.addWidget(self.val_res_lab)

        self.val_res_view = QtWidgets.QTableView(self.page_train)
        self.val_res_view.setSizePolicy(sizePolicy_views)
        self.val_res_view.setObjectName("val_res_view")
        self.val_res_lay.addWidget(self.val_res_view)

        self.train_res_lay.addLayout(self.val_res_lay)

##########################################################

        self.train_line_m = QtWidgets.QFrame(self.page_train)
        self.train_line_m.setFrameShape(QtWidgets.QFrame.VLine)
        self.train_line_m.setLineWidth(5)
        self.train_line_m.setStyleSheet("color : rgba(63, 59, 146, 255);")
        self.train_line_m.setObjectName("train_line_m")
        self.train_res_lay.addWidget(self.train_line_m)

############################# TRAIN LOSS RESULTS #############################

        self.loss_res_lay = QtWidgets.QVBoxLayout()
        self.loss_res_lay.setObjectName("loss_res_lay")

        self.loss_lab = QtWidgets.QLabel(self.page_train)
        self.loss_lab.setSizePolicy(sizePolicy)
        self.loss_lab.setAlignment(QtCore.Qt.AlignCenter)
        self.loss_lab.setObjectName("loss_lab")
        self.loss_res_lay.addWidget(self.loss_lab)

        self.loss_res_img = PhotoViewer(MainWindow)
        self.loss_res_img.setObjectName("loss_res_img")
        self.loss_res_lay.addWidget(self.loss_res_img)

        self.train_res_lay.addLayout(self.loss_res_lay)

        self.train_res_lay.setStretch(0, 6)
        self.train_res_lay.setStretch(2, 6)

        self.page_train_lay.addLayout(self.train_res_lay)

        self.rmse = QtWidgets.QLabel(self.page_train)
        self.rmse.setObjectName("rmse")
        self.rmse.setAlignment(QtCore.Qt.AlignCenter)
        self.rmse.setText("RMSE : ?")
        self.page_train_lay.addWidget(self.rmse)

############################# PAGE TRAIN BUT #####################################

        self.page_3_but_lay = QtWidgets.QHBoxLayout()
        self.page_3_but_lay.setObjectName("page_3_but_lay")

        self.page2_back_but = QtWidgets.QPushButton(self.page_train)
        self.page2_back_but.setObjectName("page2_back_but")
        self.page2_back_but.setIcon(QtGui.QIcon("Assets:left.png"))
        self.page_3_but_lay.addWidget(self.page2_back_but)

        self.page1_back_but = QtWidgets.QPushButton(self.page_train)
        self.page1_back_but.setObjectName("page1_back_but")
        self.page1_back_but.setIcon(QtGui.QIcon("Assets:reset.png"))
        self.page1_back_but.setLayoutDirection(QtCore.Qt.RightToLeft) 
        self.page_3_but_lay.addWidget(self.page1_back_but)

        self.page_train_lay.addLayout(self.page_3_but_lay)

##################################################################

        self.stackedWidget.addWidget(self.page_train)

        self.main_lay.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        MainWindow.showFullScreen()

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)


############################# CONNEXION #############################
        self.page1_but.clicked.connect(self.page_1)
        self.page2_but.clicked.connect(self.page_2)
        self.page3_but.clicked.connect(self.page_3)
        self.page2_back_but.clicked.connect(self.page_2)
        self.page1_back_but.clicked.connect(self.page_1)

        self.start_train_but.clicked.connect(self.start_training)
        self.resume_train_but.clicked.connect(self.resume_training)

        self.nb_layer_box.valueChanged.connect(self.hide_layers)

        self.min_box.valueChanged.connect(self.min_max_check)
        self.max_box.valueChanged.connect(self.min_max_check)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

############################# DISABLE #############################
        self.layer2_box.setEnabled(False)
        self.layer3_box.setEnabled(False)
        self.resume_train_but.setEnabled(False)

        self.bad_eq = False
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AI Benchmark"))
        self.par_lab.setText(_translate("MainWindow", "Paramètres"))
        self.data_lab.setText(_translate("MainWindow", "Données"))
        self.nb_val_lab.setText(_translate("MainWindow", "Nombre de valeurs"))
        self.min_lab.setText(_translate("MainWindow", "Valeur minimale"))
        self.max_lab.setText(_translate("MainWindow", "Valeur maximale"))
        self.eq_lab.setText(_translate("MainWindow", "Équation"))
        self.model_lab.setText(_translate("MainWindow", "Modèle"))
        self.nb_layer_lab.setText(_translate("MainWindow", "Nombre de couches"))
        self.nb_neur_lab.setText(_translate("MainWindow", "Nombre de neurones"))
        self.layer1_lab.setText(_translate("MainWindow", "Couche 1 :"))
        self.layer2_lab.setText(_translate("MainWindow", "Couche 2 :"))
        self.layer3_lab.setText(_translate("MainWindow", "Couche 3 :"))
        self.page2_but.setText(_translate("MainWindow", "Étape suivante   "))
        self.page1_but.setText(_translate("MainWindow", "   Revenir à la configuration"))
        self.over_lab.setText(_translate("MainWindow", "Résumé"))
        self.over_data_lab.setText(_translate("MainWindow", "Données"))
        self.over_model_lab.setText(_translate("MainWindow", "Modèle"))
        self.page3_but.setText(_translate("MainWindow", "Étape suivante   "))
        self.train_lab.setText(_translate("MainWindow", "Entrainement"))
        self.nb_epoch_lab.setText(_translate("MainWindow", "Nombre d\'entrainement"))
        self.start_train_but.setText(_translate("MainWindow", "   Lancer l'entrainement"))
        self.resume_train_but.setText(_translate("MainWindow", "   Reprendre l'entrainement"))
        self.val_res_lab.setText(_translate("MainWindow", "Résultat"))
        self.loss_lab.setText(_translate("MainWindow", "Loss"))
        self.page2_back_but.setText(_translate("MainWindow", "   Revenir au Schémas"))
        self.page1_back_but.setText(_translate("MainWindow", "Recommencer   "))

    def min_max_check(self):
        self.min_box.setMaximum(self.max_box.value() - 1)
        self.max_box.setMinimum(self.min_box.value() + 1)

    def hide_layers(self):
        if self.nb_layer_box.value() == 1:
            self.layer2_box.setEnabled(False)
            self.layer3_box.setEnabled(False)
        
        elif self.nb_layer_box.value() == 2:
            self.layer2_box.setEnabled(True)
            self.layer3_box.setEnabled(False)

        elif self.nb_layer_box.value() == 3:
            self.layer2_box.setEnabled(True)
            self.layer3_box.setEnabled(True)

    def page_1(self):
        self.stackedWidget.setCurrentIndex(0)

    def page_2(self):
        if self.stackedWidget.currentIndex() == 0:
            self.create_data()
            self.set_model()
        if not self.bad_eq:
            self.stackedWidget.setCurrentIndex(1)
            self.bad_eq = False
    
    def page_3(self):
        self.stackedWidget.setCurrentIndex(2)

    def create_data(self):
        self.resume_train_but.setEnabled(False)
        
        nb_val = self.nb_val_box.value()
        min = self.min_box.value()
        max = self.max_box.value()

        self.data = pd.DataFrame(
            {
            'a': np.random.randint(min, max + 1, nb_val),
            'b': np.random.randint(min, max + 1, nb_val),
            'c': np.random.randint(min, max + 1, nb_val)
            }
        )

        self.compute_y()

        if not self.bad_eq:
            X = self.data[['a', 'b', 'c']]
            y = self.data['y']

            self.X_train_b, self.X_test_b, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            self.x_scaler = StandardScaler()

            self.X_train = self.x_scaler.fit_transform(self.X_train_b)
            self.X_test = self.x_scaler.transform(self.X_test_b)

    def compute_y(self):

        eval_equation = lambda row: eval(self.eq_box.text(), dict(row))

        try:
            self.data['y'] = self.data.apply(eval_equation, axis=1)
            
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText(f"Équation non accepté")
            msg.setWindowTitle("Erreur")
            msg.exec_()
            self.bad_eq = True
        
        self.set_data()

    def set_data(self):
        self.over_data_view.setModel(PandasModel(self.data))
        self.over_data_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.over_data_view.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
    
    def create_model(self):

        self.model = Sequential()
        self.model.add(Dense(units=self.layer1_box.value(), activation='relu', input_dim=3))

        if self.nb_layer_box.value() > 1 :
            self.model.add(Dense(units=self.layer2_box.value(), activation='relu', input_dim=3))

        if self.nb_layer_box.value() > 2 :
            self.model.add(Dense(units=self.layer3_box.value(), activation='relu', input_dim=3))
        self.model.add(Dense(units=1))

        self.model.compile(optimizer='adamax', loss='mse')

    def set_model(self):

        self.create_model()

        os.environ['Path'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Assets/Graphviz/bin")
        os.environ.setdefault('Path', True)

        visualizer(self.model, file_name="model", file_format='png')
        self.over_model_img.setPhoto(QtGui.QPixmap("model.png"))
        os.remove("model.png")
        os.remove("model")

    def start_training(self):
        self.progress_dialog = QtWidgets.QProgressDialog("Entrainement du modèle...", "Stop", 0, self.nb_epoch_box.value())
        self.progress_dialog.setWindowModality(2) 
        self.progress_dialog.setWindowTitle("Entrainement en cours...")
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.setAutoReset(False)
        self.progress_dialog.setValue(0)
        self.progress_dialog.show()

        self.create_model()

        self.training_thread = ModelTrainingThread(self)
        self.training_thread.updateProgress.connect(self.update_progress)
        self.training_thread.finished.connect(self.training_finished)
        self.progress_dialog.canceled.connect(self.cancel_training)
        self.training_thread.start()

        self.resume_train_but.setEnabled(True)

    def resume_training(self):
        self.progress_dialog = QtWidgets.QProgressDialog("Entrainement du modèle...", "Stop", 0, self.nb_epoch_box.value())
        self.progress_dialog.setWindowModality(2) 
        self.progress_dialog.setWindowTitle("Entrainement en cours...")
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.setAutoReset(False)
        self.progress_dialog.setValue(0)
        self.progress_dialog.show()

        self.training_thread = ModelTrainingThread(self)
        self.training_thread.updateProgress.connect(self.update_progress)
        self.training_thread.finished.connect(self.training_finished)
        self.progress_dialog.canceled.connect(self.cancel_training)
        self.training_thread.start()
    
    def update_progress(self, epoch, loss):
        self.progress_dialog.setValue(epoch)
        self.progress_dialog.setLabelText(f"Epoch : {epoch}/{self.progress_dialog.maximum()}\nLoss : {round(loss, 4)}")

    def cancel_training(self):
        self.progress_dialog.hide()
        self.training_thread.cancel()

    def training_finished(self, history, y_pred):
        self.progress_dialog.reset()
        self.progress_dialog.hide()

        plt.plot(history)
        plt.savefig('history.png')
        plt.clf()
        self.loss_res_img.setPhoto(QtGui.QPixmap("history.png"))
        os.remove("history.png")

        result = pd.DataFrame(
            {'a' : self.do_round(self.X_test_b['a'], 0), 
             'b' : self.do_round(self.X_test_b['b'], 0), 
             'c' : self.do_round(self.X_test_b['c'], 0),
             'vrai' : self.do_round(self.y_test, 2), 
             'prediction' : self.do_round(y_pred, 2) 
            }
        )
        self.val_res_view.setModel(PandasModel(result))
        self.val_res_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.val_res_view.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def do_round (_, liste, rounding):
        rounded = []
        for nb in liste:
            rounded.append(round(nb, rounding))
        return(rounded)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    QtCore.QDir.addSearchPath('Assets', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Assets'))
    app.setWindowIcon(QtGui.QIcon("Assets:Logo.png"))
    file = QtCore.QFile('Assets:Style.qss')
    file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    app.setStyleSheet(str(file.readAll(), 'utf-8'))

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())