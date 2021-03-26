def createMenu(self):
        menuBar = wx.MenuBar()

        fileMenu = wx.Menu() # first 
        newItem = wx.MenuItem(parentMenu=fileMenu, id=wx.ID_NEW, 
                text='New Page\tCtrl+N', helpString='Create New Page', 
                kind=wx.ITEM_NORMAL) # subMenu is final option
        fileMenu.Append(newItem)
        self.Bind(event=wx.EVT_MENU, handler=self.onNewItem, source=newItem)

        # finally, append the File Menu
        menuBar.Append(fileMenu, '&File')

        # finally, add the Menu Bar
        self.SetMenuBar(menuBar)

    def onNewItem(self, event):

        count = self.nb.GetPageCount() + 1 # add 1 for extra page
        message = "This is page {}".format(count)
        page = NBPage(self.nb, message)
        self.nb.AddPage(page, "Page " + str(count))



if __name__ == "__main__":
    app = MyApp()
    app.MainLoop() 