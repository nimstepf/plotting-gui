"""


Inspired by:
https://pyshine.com/Make-GUI-With-Matplotlib-And-PyQt5/
https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_qt_sgskip.html#sphx-glr-gallery-user-interfaces-embedding-in-qt-sgskip-py
https://www.pythonguis.com/tutorials/plotting-matplotlib/
"""

import sys
import os

import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np

from PyQt5 import QtCore, QtWidgets, QtGui, sip
from PyQt5.Qt import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi

from pathlib import Path


__version__ = "0.0.1"
__author__ = "Nicolas Imstepf"


class ApplicationWindow(QtWidgets.QMainWindow):
    """
    Class to create the main window

    ___________________________________________________
    | Toolbar                       | Open Button     |
    |_______________________________|_________________|
    | Plot                          | File Explorer   |
    |                               |                 |
    |                               |                 |
    |_______________________________|_________________|

    """

    def __init__(self):
        super().__init__()

        # Debug Mode
        #   change function of Open Button
        self.DEBUG = True

        # Window Layout
        self.setWindowTitle("Harry Plotter and the Chromatography of Secrets") # TODO: find serious title
        self.setWindowIcon(QtGui.QIcon('logo.svg'))

        self.setWindowState(QtCore.Qt.WindowMaximized)

        self._centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self._centralWidget)

        self.generalLayout = QtWidgets.QGridLayout(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self.generalLayout.setColumnStretch(0, 4)
        self.generalLayout.setColumnStretch(1, 1)

        # Menubar
        self._createMenu()

        # Toolbar
        self._createToolbar()

        # Plot
        #   initialize values
        self.title = "Title"
        self.xlabel = "x-axis label"
        self.ylabel = "y-axis label"
        self.filelistoflist = []

        self._createPlot()

        # File Explorer
        #   initialize path
        self.folderpath = None

        self._createExplorer()


        # show window
        self.show()

    def _createMenu(self):
        """
        Menubar
            - open folder function
            - restart function
            - exit function
        """

        # open folder function
        self.openAct = QtWidgets.QAction("&Open", self)
        self.openAct.setShortcut("Ctrl+O")
        self.openAct.triggered.connect(self.openfolder)

        # restart function
        self.restartAct = QtWidgets.QAction("&Restart", self)
        self.restartAct.setShortcut("Ctrl+R")
        self.restartAct.triggered.connect(self.restart)

        # exit function
        self.exitAct = QtWidgets.QAction("&Exit", self)
        self.exitAct.setShortcut("Ctrl+Q")
        self.exitAct.triggered.connect(self.close)

        # add functions to menubar
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction(self.openAct)
        self.menu.addAction(self.restartAct)
        self.menu.addAction(self.exitAct)


    def restart(self):
        """
        Restart function for the Menubar
        """
        os.execl(sys.executable, sys.executable, *sys.argv)


    def _createToolbar(self):
        """
        ____________________________________________________
        | ThemeBox      |  NaviBox       | Open Button     |
        |_______________|________________|_________________|

        """
        self.ToolbarLayout = QtWidgets.QHBoxLayout()
        self.generalLayout.addLayout(self.ToolbarLayout, 0, 0)

        # create sublayouts
        self._createThemeBox()
        self._createNaviBox()
        self._createOpenFolder()


    def _createThemeBox(self):
        """
        Combobox to select theme for plotting
        sublayout of toolbar
        """
        self.themes = ['default', 'bmh', 'classic', 'dark_background', 'fast',
                       'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-bright',
                       'seaborn-colorblind', 'seaborn-dark-palette', 'seaborn-dark',
                       'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook',
                       'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk',
                       'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'seaborn',
                       'Solarize_Light2', 'tableau-colorblind10'] # TODO: minimize after discussion w/ users

        self.ThemeBox = QtWidgets.QComboBox()
        self.ThemeBox.addItems(self.themes)
        self.ToolbarLayout.addWidget(self.ThemeBox)


    def _createNaviBox(self):
        """
        Matplotlib navigation functions
        sublayout of toolbar
        """
        self.canv = MatplotlibCanvas(self)
        self.toolbar = Navi(self.canv, self._centralWidget)
        self.ToolbarLayout.addWidget(self.toolbar)


    def _createOpenFolder(self):
        """
        Create "Open Folder" button and add it next to the ToolbarLayout
        """
        self.OpenBtnLayout = QtWidgets.QHBoxLayout()
        openbtn = QtWidgets.QPushButton("Open Folder")
        openbtn.clicked.connect(self.openfolder)
        self.OpenBtnLayout.addWidget(openbtn)
        self.generalLayout.addLayout(self.OpenBtnLayout, 0, 1)


    def openfolder(self):
        """
        shows Windows Explorer Dialog to select directory
        saves directory to self.folderpath
        connected with "Open Folder" button
        """
        options = QtWidgets.QFileDialog.Options()

        # Debuggin mode -> set folderpath directly
        if self.DEBUG:
            self.folderpath = str(Path.cwd())

        else:
            self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder', options=options)

        if self.folderpath:
            self.UpdateTree()


    def _createPlot(self):
        """
        Layout/placeholder for plot
        """
        self.PlotLayout = QtWidgets.QVBoxLayout()
        self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.PlotLayout.addItem(self.spacerItem)
        self.generalLayout.addLayout(self.PlotLayout, 1, 0)
        self.ThemeBox.currentIndexChanged['QString'].connect(self.Update)


    def Update(self, value=None):
        if self.filelistoflist:

            plt.close()
            plt.clf()
            mpl.rcParams.update(mpl.rcParamsDefault)

            self.ToolbarLayout.removeWidget(self.toolbar)
            self.PlotLayout.removeWidget(self.canv)

            if self.Nsubplots == 42:
                self.xkcdPlot()
                return None

            if self.Nsubplots == 0:
                self.myPlot()
                return None

            if value is not None and value != "default":
                plt.style.use(value)


            sip.delete(self.toolbar)
            sip.delete(self.canv)

            self.toolbar = None
            self.canv = None
            self.PlotLayout.removeItem(self.spacerItem)

            self.canv = MatplotlibCanvas(self, nsubplots=self.Nsubplots)
            self.toolbar = Navi(self.canv, self._centralWidget)

            self.ToolbarLayout.addWidget(self.toolbar)
            self.PlotLayout.addWidget(self.canv)

            axs = self.canv.axs

            # Colorset according to Bang Wong nature methods | VOL.8 NO.6 | JUNE 2011 | 441
            COLORS = {0: (0, 114 / 255, 178 / 255), 1: (0, 158 / 255, 115 / 255), 2: (213 / 255, 94 / 255, 0),
                      3: (86 / 255, 180 / 255, 233 / 255), 4: (230 / 255, 159 / 255, 0 / 255),
                      5: (204 / 255, 121 / 255, 167 / 255)}
            COLORS.update({i: "black" for i in range(6, 100)})  # unrealistic, but if more than 10 plots are needed


            if self.Nsubplots == 1:
                if value is None or value == "default":
                    [axs.plot(self.Xlist[0][i]+i*0.1, self.Ylist[0][i]+i*max(self.Ylist[0][0])/5,
                              label=self.LEGENDS[0][i], color=COLORS[i]) for i in reversed(range(len(self.Xlist[0])))]
                else:
                    [axs.plot(self.Xlist[0][i] + i * 0.1, self.Ylist[0][i] + i * max(self.Ylist[0][0]) / 5,
                              label=self.LEGENDS[0][i]) for i in reversed(range(len(self.Xlist[0])))]

                # add legend (reversed order needed)
                # adapted from unutbu stackoverflow.com/questions/34576059/reverse-the-order-of-a-legend
                handles, labels = axs.get_legend_handles_labels()
                axs.legend(handles[::-1], labels[::-1], frameon=False).set_draggable(True)

            else:
                for j in range(self.Nsubplots):
                    if value is None or value == "default":
                        [axs[j].plot(self.Xlist[j][i]+i*0.1, self.Ylist[j][i]+i*max(self.Ylist[j][0])/5,
                                     label=self.LEGENDS[j][i], color=COLORS[i]) for i in reversed(range(len(self.Xlist[j])))]
                    else:
                        [axs[j].plot(self.Xlist[j][i] + i * 0.1, self.Ylist[j][i] + i * max(self.Ylist[j][0]) / 5,
                                     label=self.LEGENDS[j][i]) for i in reversed(range(len(self.Xlist[j])))]

                    # add legend
                    handles, labels = axs[j].get_legend_handles_labels()
                    axs[j].legend(handles[::-1], labels[::-1], frameon=False).set_draggable(True)

                    # add title (for navibar)
                    if j == 0:
                        axs[j].set_title(f"{j+1}    (Top)", visible=False)
                    elif j == self.Nsubplots-1:
                        axs[j].set_title(f"{j+1}    (Bottom)", visible=False)
                    else:
                        axs[j].set_title(j+1, visible=False)


            self.canv.fig.suptitle(self.title, fontsize=16)
            self.canv.fig.supxlabel(self.xlabel)
            self.canv.fig.supylabel(self.ylabel)


            self.canv.draw()


    def xkcdPlot(self):
        """
        creates plot with xkcd style
        """
        #plt.clf()
        #self.canv = None
        self.PlotLayout.removeItem(self.spacerItem)
        self.canv = xkcdPlot(self)
        self.PlotLayout.addWidget(self.canv)
        self.toolbar = Navi(self.canv, self._centralWidget)
        self.ToolbarLayout.addWidget(self.toolbar)
        self.canv.draw()


    def myPlot(self):
        """
        creates plot with my own style
        """
        #plt.clf()
        #self.canv = None
        self.PlotLayout.removeItem(self.spacerItem)
        self.canv = myPlot(self)
        self.PlotLayout.addWidget(self.canv)
        self.toolbar = Navi(self.canv, self._centralWidget)
        self.ToolbarLayout.addWidget(self.toolbar)
        self.canv.draw()


    def _createExplorer(self):
        """
        _________________
        | Tree          |
        |               |
        |               |
        |               |
        | DragDropList  |
        |               |
        |               |
        |               |
        |_______________|
        """
        self.ExplorerLayout = QtWidgets.QVBoxLayout()

        self._createSetLabels()
        self._createTree()
        self._createDragDropList()
        self._createSubplots()


        scrollwidget = QtWidgets.QWidget()
        scrollwidget.setLayout(self.ExplorerLayout)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(scrollwidget)
        scroll.setWidgetResizable(True)

        self.generalLayout.addWidget(scroll, 1, 1)




    def _createSetLabels(self):
        self.LabelGroupBox = QtWidgets.QGroupBox("Set Labels")
        self.LabelsLayout = QtWidgets.QVBoxLayout()


        self.titleEdit = QtWidgets.QLineEdit()
        self.titleEdit.setPlaceholderText("set title")
        self.titleEdit.editingFinished.connect(self.changedTitle)
        self.LabelsLayout.addWidget(self.titleEdit)

        self.xlabelEdit = QtWidgets.QLineEdit()
        self.xlabelEdit.setPlaceholderText("set x-axis label")
        self.xlabelEdit.editingFinished.connect(self.changedXlabel)
        self.LabelsLayout.addWidget(self.xlabelEdit)

        self.ylabelEdit = QtWidgets.QLineEdit()
        self.ylabelEdit.setPlaceholderText("set y-axis label")
        self.ylabelEdit.editingFinished.connect(self.changedYlabel)
        self.LabelsLayout.addWidget(self.ylabelEdit)

        self.updatebtn = QtWidgets.QPushButton("Update")
        self.updatebtn.clicked.connect(self.changedLabels)
        self.LabelsLayout.addWidget(self.updatebtn)

        self.LabelGroupBox.setLayout(self.LabelsLayout)
        self.ExplorerLayout.addWidget(self.LabelGroupBox)


    def changedTitle(self):
        self.title = self.titleEdit.text()
        self.Update()


    def changedXlabel(self):
        self.xlabel = self.xlabelEdit.text()
        self.Update()

    def changedYlabel(self):
        self.ylabel = self.ylabelEdit.text()
        self.Update()

    def changedLabels(self):
        self.Update()



    def _createTree(self):
        """
        Layout to show files from selected directory
        sublayout of Explorer
        """
        self.treeGroupBox = QtWidgets.QGroupBox("Raw Data")

        self.tree = QtWidgets.QTreeWidget()
        self.tree.itemClicked.connect(self.check_status)
        self.tree.setHeaderLabels([""])
        self.treeLayout = QtWidgets.QVBoxLayout()
        self.treeLayout.addWidget(self.tree)
        self.treeGroupBox.setLayout(self.treeLayout)
        self.ExplorerLayout.addWidget(self.treeGroupBox)


    def UpdateTree(self):
        """
        Creates tree from selected directory
        """
        self.tree.clear()
        self.tree.setHeaderLabels([self.folderpath])

        for folderName, subfolders, filenames in os.walk(self.folderpath):
            parent = QtWidgets.QTreeWidgetItem(self.tree)
            parent.setText(0, Path(folderName).name)
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)

            for filename in filenames:
                if filename[-4:].lower() == ".csv":
                    child = QtWidgets.QTreeWidgetItem(parent)
                    child.setText(0, Path(filename).name)
                    child.setData(0, Qt.UserRole, Path(self.folderpath, folderName, filename))
                    child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                    child.setCheckState(0, Qt.Unchecked)

            if parent.childCount() == 0:
                parent.setHidden(True)

        self.tree.setColumnWidth(0, 800) # TODO: if possible, find solution with relative values (feedback...)


    def check_status(self):
        """
        starts when item of tree is clicked
        call/create DragDropList
        creates Plot if > 1 item is selected -> readData()
        """
        self.filelst = []
        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            subroot = root.child(i)
            for j in range(subroot.childCount()):
                item = subroot.child(j)
                if item.checkState(0) == QtCore.Qt.Checked:
                    self.filelst.append(item.data(0, Qt.UserRole))

        self.DragDropList()


    def _createDragDropList(self):
        """
        Layout to show selected files
            functions
                - change order (drag & drop)
                - remove items with doubleclick
        sublayout of Explorer
        """
        self.ddlstGroupBox = QtWidgets.QGroupBox("Selected files")
        self.ddlstLayout = QtWidgets.QVBoxLayout()

        self.ddlst = QtWidgets.QListWidget()
        self.ddlst.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.ddlst.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.ddlst.doubleClicked.connect(lambda: self.ddlst.takeItem(self.ddlst.currentRow()))

        self.ddlstLayout = QtWidgets.QVBoxLayout()
        self.ddlstLayout.addWidget(self.ddlst)
        self.ddlstGroupBox.setLayout(self.ddlstLayout)
        self.ExplorerLayout.addWidget(self.ddlstGroupBox)


    def DragDropList(self):
        """
        Creates Drag and Drop List from selected files of tree
        """
        self.ddlst.clear()
        self.filedict = {}
        for file in self.filelst:
            item = QtWidgets.QListWidgetItem(file.stem)
            self.filedict[file.stem] = file
            self.ddlst.addItem(item)
        self.ddlst.repaint()


    def _createSubplots(self):
        self.SubplotLayout = QtWidgets.QVBoxLayout()
        self.subplotGroupBox = QtWidgets.QGroupBox("Subplots")
        self._createSpinBox()
        self._createSubplotList()
        self.subplotGroupBox.setLayout(self.SubplotLayout)
        self.ExplorerLayout.addWidget(self.subplotGroupBox)


    def _createSpinBox(self):
        self.spinBox = QtWidgets.QSpinBox()
        self.spinBox.setValue(1)
        self.spinBox.valueChanged.connect(self.getSpinBoxvalue)

        self.NsubplotsLayout = QtWidgets.QHBoxLayout()
        self.NsubplotsLabel = QtWidgets.QLabel("Number of subplots")
        self.Nsubplots = 1

        self.NsubplotsLayout.addWidget(self.NsubplotsLabel)
        self.NsubplotsLayout.addWidget(self.spinBox)
        self.SubplotLayout.addLayout(self.NsubplotsLayout)


    def getSpinBoxvalue(self):
        self.Nsubplots = self.spinBox.value()
        [self.SubplotLayout.removeWidget(i) for i in self.subplotList]
        self._createSubplotList()


    def _createSubplotList(self):
        self.SubplotListLayout = QtWidgets.QVBoxLayout()

        self.subplotList = []
        for i in range(self.Nsubplots):
            self.subplotList.append(QtWidgets.QListWidget())
            self.subplotList[i].setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
            self.subplotList[i].setDefaultDropAction(QtCore.Qt.MoveAction)

            self.subplotList[i].doubleClicked.connect(self.removeItem2)
            self.subplotList[i].model().rowsMoved.connect(self.updateSubplotOrder)
            self.subplotList[i].model().rowsMoved.connect(self.deselectItem)
            self.subplotList[i].model().rowsInserted.connect(self.updateSubplotOrder)
            self.subplotList[i].model().rowsRemoved.connect(self.updateSubplotOrder)
            self.subplotList[i].model().dataChanged.connect(self.updateSubplotOrder)
            self.subplotList[i].clicked.connect(lambda: [j.clearSelection() for j in self.subplotList])

            self.SubplotListLayout.addWidget(self.subplotList[i])

        self.SubplotLayout.addLayout(self.SubplotListLayout)


    def updateSubplotOrder(self):
        self.filelistoflist = []

        for j in self.subplotList:
            keylist = [j.item(i).text() for i in range(j.count())]
            self.filelistoflist.append([self.filedict[i] for i in keylist if i in self.filedict])

        self.readData()


    def removeItem2(self):
        """
        delete items by doubleclicking
        """
        for i in self.subplotList:
            i.takeItem(i.currentRow())
            i.setCurrentRow(-1)

        self.updateSubplotOrder()


    def deselectItem(self):
        for i in self.subplotList:
            i.setCurrentRow(-1)


    def readData(self):
        """
        read Data from selected files
        updates plot
        """
        if self.filelistoflist != []:
            self.datalst = []
            self.Xlist = []
            self.Ylist = []
            self.LEGENDS = []
            for j in range(self.Nsubplots):
                self.datalst.append({index: np.genfromtxt(i, delimiter=",", names=["x", "y"]) for index, i in enumerate(self.filelistoflist[:][j])})

                self.Xlist.append({i: self.datalst[j][i]["x"] for i in range(len(self.datalst[j]))})
                self.Ylist.append({i: self.datalst[j][i]["y"] for i in range(len(self.datalst[j]))})
                self.LEGENDS.append({i: file.stem for i, file in enumerate(self.filelistoflist[j])})

        self.Update()


class MatplotlibCanvas(FigureCanvasQTAgg):
    """
    Class to create canvas for matplotlib subplots
    """

    def __init__(self, parent=None, dpi=120, nsubplots=2):
        self.nsubplots = nsubplots

        if nsubplots == 1:
            self.fig, self.axs = plt.subplots(1, 1)
            self.axs.spines["top"].set_visible(False)
            self.axs.spines["right"].set_visible(False)

        else:
            self.fig, self.axs = plt.subplots(self.nsubplots, 1, sharex=True)
            # self.fig.tight_layout()
            self.fig.subplots_adjust(hspace=0.2)
            for i in range(nsubplots):
                self.axs[i].spines["top"].set_visible(False)
                self.axs[i].spines["right"].set_visible(False)


                if i != nsubplots-1:
                    self.axs[i].get_xaxis().set_visible(False)
                    self.axs[i].spines['bottom'].set_visible(False)

        super(MatplotlibCanvas, self).__init__(self.fig)


class xkcdPlot(FigureCanvasQTAgg):
    """
    Class to create canvas for matplotlib with xkcd style
    https://matplotlib.org/stable/gallery/showcase/xkcd.html#sphx-glr-gallery-showcase-xkcd-py

    Based on "Stove Ownership" from XKCD by Randall Munroe    https://xkcd.com/418/
    """

    def __init__(self, parent=None, dpi=120):
        with plt.xkcd():

            self.fig = plt.figure()
            self.ax = self.fig.add_axes((0.1, 0.2, 0.8, 0.7))
            self.ax.spines.right.set_color('none')
            self.ax.spines.top.set_color('none')
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.ax.set_ylim([-30, 10])

            self.data = np.ones(100)
            self.data[70:] -= np.arange(30)

            self.ax.annotate(
                'THE DAY I REALIZED\nI COULD COOK BACON\nWHENEVER I WANTED',
                xy=(70, 1), arrowprops=dict(arrowstyle='->'), xytext=(15, -10))

            self.ax.plot(self.data)

            self.ax.set_xlabel('time')
            self.ax.set_ylabel('my overall health')

            # self.fig.tight_layout()
            super(xkcdPlot, self).__init__(self.fig)


class myPlot(FigureCanvasQTAgg):
    """
    Nicolas favored plotting style
    """
    def __init__(self, parent=None, dpi=120):
        self.fig = plt.figure()
        self.ax = self.fig.add_axes((0.1, 0.1, 0.8, 0.8))
        self.ax.axis('off')
        self.fig.suptitle("my charts and graphs are:", size=20)

        self.ax.arrow(0, 1, 0, -2, color='black', head_length = 0.07, head_width = 0.05, length_includes_head = True)
        self.ax.arrow(0, -1, 0, 2, color='black', head_length = 0.07, head_width = 0.05, length_includes_head = True)
        self.ax.arrow(1, 0, -2, 0, color='black', head_length = 0.07, head_width = 0.05, length_includes_head = True)
        self.ax.arrow(-1, 0, 2, 0, color='black', head_length = 0.07, head_width = 0.05, length_includes_head = True)

        self.ax.text(0.5, 1, 'Easy to comprehend', horizontalalignment='center', size=16,
                 verticalalignment='center', transform=self.ax.transAxes)
        self.ax.text(0.5, 0, 'Hard to comprehend', horizontalalignment='center', size=16,
                 verticalalignment='center', transform=self.ax.transAxes)
        self.ax.text(0, 0.5, 'Boring', horizontalalignment='center', size=16,
                 verticalalignment='center', transform=self.ax.transAxes, rotation='vertical')
        self.ax.text(1, 0.5, 'Fascinating', horizontalalignment='center', size=16,
                 verticalalignment='center', transform=self.ax.transAxes, rotation=270)

        self.ax.plot(0.7,0.7,'co', markersize=20)
        self.ax.text(0.62,0.76,'My perception', size=12)
        self.ax.plot(-0.7,-0.7,'mo', markersize=20)
        self.ax.text(-0.78,-0.78,'Everyone else', size=12)

        super(myPlot, self).__init__(self.fig)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    view = ApplicationWindow()
    sys.exit(app.exec_())
