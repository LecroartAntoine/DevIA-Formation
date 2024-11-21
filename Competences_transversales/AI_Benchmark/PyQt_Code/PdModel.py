from PyQt5 import QtCore, QtGui
import pandas as pd

class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, dataframe: pd.DataFrame, result = False, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe
        self.result = result

    def rowCount(self, parent=QtCore.QModelIndex()) -> int:
        if parent == QtCore.QModelIndex():
            return len(self._dataframe)

        return 0

    def columnCount(self, parent=QtCore.QModelIndex()) -> int:
        if parent == QtCore.QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QtCore.QModelIndex, role=QtCore.Qt.ItemDataRole):
        if not index.isValid():
            return None

        elif role == QtCore.Qt.DisplayRole:
            try :
                x = round(self._dataframe.iloc[index.row()][index.column()], 4)
                return str(x)
            except :
                return str(self._dataframe.iloc[index.row()][index.column()])
            
        elif role == QtCore.Qt.TextColorRole and index.column() == 3 :
                return QtGui.QColor('blue')
        
        elif role == QtCore.Qt.TextColorRole and index.column() == 4 :
                return QtGui.QColor('red')
        
        elif role == QtCore.Qt.TextColorRole and index.column() < 3 :
                return QtGui.QColor('green')

        return None

    def headerData(
        self, section: int, orientation: QtCore.Qt.Orientation, role: QtCore.Qt.ItemDataRole
    ):

        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self._dataframe.columns[section])
        return None