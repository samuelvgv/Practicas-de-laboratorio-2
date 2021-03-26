import wx

app = wx.App(clearSigInt=True) # clearSigInt to allow terminating the program by CTRL+C
frame = wx.Frame(parent=None, title="") ## main window object
panel = wx.Panel(parent=frame)
text = wx.StaticText(parent=panel, label="Hello, from wxPython!!", pos = (40,40))
frame.Show()
app.MainLoop()

import wx
import webbrowser

class MyApp(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)

        # init frame
        self.InitFrame()

    def InitFrame(self):
        frame = MyFrame(parent=None, title="Basic Frame", pos=(100, 100))
        frame.Show(True)


class MyFrame(wx.Frame):
    # subclass of wx.Window; Frame is a top level window
    # A frame is a window whose size and position can (usually) be changed by the user.
    # Usually represents the first/main window a user will see
    def __init__(self, parent, title, pos=pos):
        super().__init__(parent=parent, title=title, pos=pos)

    def OnInit(self):
        panel = MyPanel(parent=self)