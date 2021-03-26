import wx
import wx.grid as gridlib
import csv

class MyApp(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)

        # init frame
        self.InitFrame()

    def InitFrame(self):
        frame = MyFrame(parent=None, title="Basic Frame")
        frame.Show(True)


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent=parent, title=title)
        self.OnInit()

    def OnInit(self):
        # first creat some dummy panel to hold some text
        titlePanel = MyPanel(parent=self)

        # create sizers to control layout
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        gridSizer = wx.BoxSizer(wx.HORIZONTAL)

        titleSizer.Add(titlePanel, 0, wx.ALL, 5)
        mainSizer.Add(titleSizer, 0, wx.CENTER)
        mainSizer.Add(wx.StaticLine(self,), 0, wx.ALL|wx.EXPAND, 5)

        # data viewer
        grid = GridTable(self)
        grid.LoadFile()
        grid.SetColReadOnly(0)
        gridSizer.Add(grid, 1, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(gridSizer, 0, wx.ALL|wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        mainSizer.Fit(self)


class MyPanel(wx.Panel):
    def __init__(self,parent):
        super().__init__(parent=parent)
        welcomeText = wx.StaticText(self, label="Data Grid Display", pos=(20,20))



class GridTableSource(gridlib.GridTableBase):
    def __init__(self):
        super().__init__()
        self._data = None
        self._header = None
        self._readOnly = list()

    def LoadFile(self, fileName='./sample_data.csv'):
        fileName = './sample_data.csv'
        reader = csv.reader(open(fileName, 'r'))
        self._data = [row for row in reader]
        self._header = self._data.pop(0)
        self._readOnly = list()

    def Sort(self, col, ascending):
        #self._data.sort(key=lambda data: data[col], reverse=True)
        pass

    def SetColReadOnly(self, col):
        self._readOnly.append(col)

    def GetNumberRows(self):
        return len(self._data) if self._data else 0

    def GetNumberCols(self):
        return len(self._header) if self._header else 0

    def GetValue(self, row, col):
        if not self._data:
            return ""
        else:
            return self._data[row][col]

    def SetValue(self, row, col, value):
        if self._data:
            self._data[row][col] = value

    def GetColLabelValue(self, col):
        return self._header[col] if self._header else None



class GridTable(gridlib.Grid):
    def __init__(self, parent):
        super().__init__(parent)

        self._data = GridTableSource()
        self.SetTable(self._data)

        # need to implement a sorting event; else sementation fault error
        self.Bind(gridlib.EVT_GRID_COL_SORT, self.OnSort)

    def OnSort(self, event):
        self._data.Sort(event.Col,
                        self.IsSortOrderAscending())

    def LoadFile(self, fileName='./sample_data.csv'):
        self._data.LoadFile(fileName)
        self.SetTable(self._data)
        self.AutoSizeColumns()


    def SetColReadOnly(self, col):
        self._data.SetColReadOnly(col)


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()










import csv
from io import StringIO
import wx
import wx.grid as gridlib

class CSVDataSource(gridlib.GridTableBase):
    def __init__(self):
        super().__init__()
        self._data = None
        self._header = None
        self._readOnly = list()

        self._roAttr = gridlib.GridCellAttr()
        self._roAttr.SetReadOnly()
        c = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)
        self._roAttr.TextColour = c

    def LoadFile(self, fileName='./sample_data.csv'):
        fileName = './sample_data.csv'
        reader = csv.reader(open(fileName, 'r'))
        self._data = [row for row in reader]
        self._header = self._data.pop(0)
        self._readOnly = list()

    def GetData(self):
        if not self._data:
            return ""

        buff = StringIO()
        writer = csv.writer(buff)
        writer.writerow(self._header)
        writer.writerows(self._data)
        print(buff.getvalue())
        return buff.getvalue()

    def SetColReadOnly(self, col):
        self._readOnly.append(col)

    def GetAttr(self, row, col, kind):
        if col in self._readOnly:
            self._roAttr.IncRef()
            return self._roAttr
        return None

    def Sort(self, col, ascending):
        self._data.sort(None, lambda data: data[col], not ascending)

    def GetNumberRows(self):
        return len(self._data) if self._data else 0

    def GetNumberCols(self):
        return len(self._header) if self._header else 0

    def GetValue(self, row, col):
        if not self._data:
            return ""
        else:
            return self._data[row][col]

    def SetValue(self, row, col, value):
        if self._data:
            self._data[row][col] = value

    def GetColLabelValue(self, col):
        return self._header[col] if self._header else None

class CSVEditorGrid(gridlib.Grid):
    def __init__(self, parent):
        super().__init__(parent)

        self._data = CSVDataSource()
        self.SetTable(self._data)

        self.Bind(gridlib.EVT_GRID_COL_SORT, self.OnSort)

    def OnSort(self, event):
        self._data.Sort(event.Col,
                        self.IsSortOrderAscending())

    def LoadFile(self, fileName):
        self._data.LoadFile(fileName)
        self.SetTable(self._data)
        self.AutoSizeColumns()

    def SaveFile(self, fileName):
        with open(fileName, 'w+') as fileObj:
            fileObj.write(self._data.GetData())

    def SetColReadOnly(self, col):
        self._data.SetColReadOnly(col)

#------- Sample Application ---------#

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)

        menub = wx.MenuBar()
        fmenu = wx.Menu()
        fmenu.Append(wx.ID_OPEN)
        fmenu.Append(wx.ID_SAVE)
        menub.Append(fmenu, "File")
        self.SetMenuBar(menub)
        self.CreateStatusBar()

        sizer = wx.BoxSizer()
        self._file = 'sample_data.csv'
        self._grid = CSVEditorGrid(self)
        self._grid.LoadFile(self._file)
        self._grid.SetColReadOnly(0)

        sizer.Add(self._grid, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize()

        self.Bind(wx.EVT_MENU, self.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)

    def OnOpen(self, event):
        dlg = wx.FileDialog(self, "Open CSV File", wildcard="*.csv")
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self._grid.LoadFile(dlg.Path)
        dlg.Destroy()

    def OnSave(self, event):
        self._grid.SaveFile(self._file)
        self.SetStatusText("Saved file: %s" % self._file)

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Data Grid")
        self.frame.Show();
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()