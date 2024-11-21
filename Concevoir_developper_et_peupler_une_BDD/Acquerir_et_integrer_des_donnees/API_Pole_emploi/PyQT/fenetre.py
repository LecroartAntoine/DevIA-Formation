from PyQt5 import QtCore, QtGui, QtWidgets

import API_content as api
from popup import Ui_Dialog
import os

class MyDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        self.liste_contrats, self.liste_domaines, self.liste_formations = [], [], []

        try:
            self.header = api.connect()
            self.liste_domaines = api.get_domaines(self.header)
            self.liste_contrats = api.get_types_contrats(self.header)
            self.liste_formations = api.get_niveaux_formations(self.header)

            self.no_connexion = False

        except:
            self.no_connexion = True

        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(0, 0, 81, 81))
        self.label_1.setPixmap(QtGui.QPixmap(os.path.dirname(os.path.abspath(__file__)) + "\Image.png"))
        self.label_1.setScaledContents(True)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(5, 100, 200, 30))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(5, 140, 170, 30))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(5, 180, 170, 30))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(5, 220, 170, 30))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(5, 300, 170, 30))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(5, 260, 170, 30))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(5, 380, 170, 30))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")

        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(5, 340, 170, 30))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")

        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(5, 420, 170, 30))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")

        self.salaire_min_box = QtWidgets.QSpinBox(self.centralwidget)
        self.salaire_min_box.setGeometry(QtCore.QRect(200, 100, 150, 30))
        self.salaire_min_box.setObjectName("salaire_min_box")
        self.salaire_min_box.setMaximum(999999999)
        self.salaire_min_box.setAccelerated(True)
        self.salaire_min_box.setSingleStep(10)

        self.domaine_box = QtWidgets.QComboBox(self.centralwidget)
        self.domaine_box.setGeometry(QtCore.QRect(200, 140, 300, 30))
        self.domaine_box.setObjectName("domaine_box")
        for _ in range(len(self.liste_domaines) + 1):
            self.domaine_box.addItem("")

        self.experience_box = QtWidgets.QComboBox(self.centralwidget)
        self.experience_box.setGeometry(QtCore.QRect(200, 180, 150, 30))
        self.experience_box.setObjectName("experience_box")
        self.experience_box.addItem("")
        self.experience_box.addItem("")
        self.experience_box.addItem("")
        self.experience_box.addItem("")

        self.contrat_box = QtWidgets.QComboBox(self.centralwidget)
        self.contrat_box.setGeometry(QtCore.QRect(200, 220, 300, 30))
        self.contrat_box.setObjectName("contrat_box")
        for _ in range(len(self.liste_contrats) + 1):
            self.contrat_box.addItem("")

        self.qualification_box = QtWidgets.QComboBox(self.centralwidget)
        self.qualification_box.setGeometry(QtCore.QRect(200, 260, 150, 30))
        self.qualification_box.setCurrentText("Non cadre")
        self.qualification_box.setObjectName("qualification_box")
        self.qualification_box.addItem("")
        self.qualification_box.addItem("")
        self.qualification_box.addItem("")

        self.departement_box = QtWidgets.QLineEdit(self.centralwidget)
        self.departement_box.setGeometry(QtCore.QRect(200, 300, 150, 30))
        self.departement_box.setObjectName("departement_box")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(510, 100, 280, 460))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setOpenExternalLinks(True)

        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(610, 20, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(20)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")

        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(205, 20, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(20)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")

        self.formation_box = QtWidgets.QComboBox(self.centralwidget)
        self.formation_box.setGeometry(QtCore.QRect(200, 340, 300, 30))
        self.formation_box.setObjectName("formation_box")
        for _ in range(len(self.liste_formations) + 1):
            self.formation_box.addItem("")

        self.mots_cles_box = QtWidgets.QLineEdit(self.centralwidget)
        self.mots_cles_box.setGeometry(QtCore.QRect(200, 380, 300, 30))
        self.mots_cles_box.setObjectName("mots_cles_box")

        self.handicap_box = QtWidgets.QComboBox(self.centralwidget)
        self.handicap_box.setGeometry(QtCore.QRect(200, 420, 150, 30))
        self.handicap_box.setCurrentText("Non")
        self.handicap_box.setObjectName("handicap_box")
        self.handicap_box.addItem("")
        self.handicap_box.addItem("")
        self.handicap_box.addItem("")

        self.recherche_but = QtWidgets.QPushButton(self.centralwidget)
        self.recherche_but.setGeometry(QtCore.QRect(15, 500, 150, 60))
        self.recherche_but.setObjectName("recherche_but")

        self.annuler_but = QtWidgets.QPushButton(self.centralwidget)
        self.annuler_but.setGeometry(QtCore.QRect(345, 500, 150, 60))
        self.annuler_but.setObjectName("annuler_but")

        self.commentaire_but = QtWidgets.QPushButton(self.centralwidget)
        self.commentaire_but.setGeometry(QtCore.QRect(180, 500, 150, 60))
        self.commentaire_but.setObjectName("commentaire_but")
        self.commentaire_but.setEnabled(False)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Recherche Pôle Emploi"))
        self.label_2.setText(_translate("MainWindow", "Salaire Minimum Mensuel"))
        self.label_3.setText(_translate("MainWindow", "Domaine"))
        self.label_4.setText(_translate("MainWindow", "Expérience"))
        self.label_5.setText(_translate("MainWindow", "Type de contrat"))
        self.label_6.setText(_translate("MainWindow", "Département"))
        self.label_7.setText(_translate("MainWindow", "Qualification"))
        self.label_8.setText(_translate("MainWindow", "Mots clés"))
        self.label_9.setText(_translate("MainWindow", "Niveau de formation"))
        self.label_10.setText(_translate("MainWindow", "Adaptée Handicap"))

        for i, domaine in enumerate(self.liste_domaines):
            self.domaine_box.setItemText(i + 1, _translate("MainWindow", domaine[1]))

        for i, contrat in enumerate(self.liste_contrats):
            self.contrat_box.setItemText(i + 1, _translate("MainWindow", contrat[1]))

        for i, niveau in enumerate(self.liste_formations):
            self.formation_box.setItemText(i + 1, _translate("MainWindow", niveau[1]))

        self.experience_box.setItemText(1, _translate("MainWindow", "Moins d'un an d'expérience"))
        self.experience_box.setItemText(2, _translate("MainWindow", "De 1 à 3 ans d'expérience"))
        self.experience_box.setItemText(3, _translate("MainWindow", "Plus de 3 ans d'expérience"))

        self.qualification_box.setItemText(1, _translate("MainWindow", "Non cadre"))
        self.qualification_box.setItemText(2, _translate("MainWindow", "Cadre"))

        self.label_11.setText(_translate("MainWindow", "Résultat"))
        self.label_12.setText(_translate("MainWindow", "Entrées"))

        self.handicap_box.setItemText(1, _translate("MainWindow", "Non"))
        self.handicap_box.setItemText(2, _translate("MainWindow", "Oui"))

        self.recherche_but.setText(_translate("MainWindow", "Rechercher"))

        self.annuler_but.setText(_translate("MainWindow", "Annuler"))

        self.commentaire_but.setText(_translate("MainWindow", "Commentaire"))

        self.recherche_but.clicked.connect(self.recherche_clicked)
        self.annuler_but.clicked.connect(self.annuler_clicked)
        self.commentaire_but.clicked.connect(self.commentaire_clicked)


        if self.no_connexion:
            
            text = """
                <!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">
                <p style=\" margin-top:0px; margin-bottom:0px; \"><span style="font-family:Arial,Helvetica,sans-serif">Pas de connexion Internet, recherche impossible.</span></p>
            """
            self.annuler_but.setEnabled(False)
            self.recherche_but.setEnabled(False)
            self.textBrowser.setHtml(_translate("MainWindow", text))


    
    def recherche_clicked(self):
        _translate = QtCore.QCoreApplication.translate

        self.header = api.connect()

        self.salaire = self.salaire_min_box.value()

        if self.domaine_box.currentIndex() == 0:
            self.domaine = 0
        else:
            for domaine_name in self.liste_domaines:
                if domaine_name[1] == self.domaine_box.currentText():
                    self.domaine = domaine_name[0]

        if self.experience_box.currentIndex() == 0:
            self.exp = 0
        else:
            if self.experience_box.currentIndex() == 1:
                self.exp = 1
            elif self.experience_box.currentIndex() == 2:
                self.exp = 2
            else:
                self.exp = 3

        if self.contrat_box.currentIndex() == 0:
            self.type = 0
        else:
            for contrat in self.liste_contrats:
                if contrat[1] == self.contrat_box.currentText():
                    self.type = contrat[0]
        
        if self.qualification_box.currentIndex() == 0:
            self.qualif = 0
        elif self.qualification_box.currentIndex() == 1:
            self.qualif = 0
        else:
            self.qualif = 9

        if self.formation_box.currentIndex() == 0:
            self.lvl = 0
        else:
            for formation in self.liste_formations:
                if formation[1] == self.formation_box.currentText():
                    self.lvl = formation[0]

        if self.handicap_box.currentIndex() == 0:
            self.handicap = 0
        else:
            self.handicap = False if self.handicap_box.currentText() == 'Non' else True
        
        self.dep = self.departement_box.text().replace(" ", "")

        self.mots_cles = self.mots_cles_box.text().replace(" ", ",")

        results = api.recherche(self.header, salaire = self.salaire, domaine = self.domaine, exp = self.exp, type = self.type, qualif = self.qualif, dep = self.dep, lvl = self.lvl, mots_cles = self.mots_cles, handicap = self.handicap)

        text = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">"

        if results[0] != 'Aucun résultat':
            for result in results:
                text += f"""
                    <p style=\" margin-top:0px; margin-bottom:0px; \"><span style="font-family:Arial,Helvetica,sans-serif">Lieu : {result[0]}</span></p>
                    <p style=\" margin-top:0px; margin-bottom:0px; \"><span style="font-family:Arial,Helvetica,sans-serif">Intitulé: {result[1]}</span></p>
                    <p style=\" margin-top:0px; margin-bottom:0px; \"><span style="font-family:Arial,Helvetica,sans-serif"><a href={result[2]}>Voir sur pole-emploi.fr</a><br></span></p>
                """
        else:
            text += f"""<p style=\" margin-top:0px; margin-bottom:0px; \"><span style="font-family:Arial,Helvetica,sans-serif">{results[0]}</span></p>"""

        self.textBrowser.setHtml(_translate("MainWindow", text))

        self.commentaire_but.setEnabled(True)

    def annuler_clicked(self):
        self.salaire_min_box.setValue(0)
        self.domaine_box.setCurrentIndex(0)
        self.experience_box.setCurrentIndex(0)
        self.contrat_box.setCurrentIndex(0)
        self.qualification_box.setCurrentIndex(0)
        self.departement_box.setText("")
        self.formation_box.setCurrentIndex(0)
        self.mots_cles_box.setText("")
        self.handicap_box.setCurrentIndex(0)

        self.commentaire_but.setEnabled(False)

    def commentaire_clicked(self):
        self.myDialog = MyDialog()
        self.myDialog.show()
        self.myDialog.exec_()
        data = {
            'nom' : self.myDialog.ui.lineEdit.text(),
            'prenom' : self.myDialog.ui.lineEdit_2.text(),
            'sentiment' : self.myDialog.ui.textEdit.toPlainText(),
            'parametres' : {
                'salaire' : self.salaire,
                'domaine' : self.domaine,
                'experience' : self.exp,
                'typeContrat' : self.type,
                'qualification' : self.qualif,
                'departement' : self.dep,
                'niveauFormation' : self.lvl,
                'mots_cles' : self.mots_cles,
                'handicap' : self.handicap
            } 
        }

        api.insert_BDD(data)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    app.setStyle('Fusion')

    app.setWindowIcon(QtGui.QIcon(os.path.dirname(os.path.abspath(__file__)) + "\Image.png"))

    app.setStyleSheet("""
                        QMainWindow {
                            background-color: #0e2f44;
                        }
                        QDialog {
                            background-color: #0e2f44;
                        }
                        QLabel {
                            color: #afeeee;
                            font-family: "Bahnschrift";
                        }
                        QPushButton {
                            color : #afeeee;
                            background-color: #8b0000;
                            border-style: outset;
                            border-width: 2px;
                            border-radius: 10px;
                            border-color: #6897bb;
                            font: bold 16px;
                            min-width: 5em;
                            padding: 6px;
                        }
                        QPushButton:disabled {
                            color : #101010;
                            background-color : #101010;
                        }
                        QPushButton:pressed {
                            background-color: #800000;
                            border-style: inset;
                        }
                        QSpinBox {
                            background-color: #6897bb;
                        }
                        QComboBox {
                            background-color: #6897bb;
                        }
                        QTextBrowser{
                            background-color: #6897bb;
                        }
                        QTextEdit {
                            background-color: #6897bb;
                        }
                        QLineEdit {
                            background-color: #6897bb;
                        }

                    """)


    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())