#!/usr/bin/env python

import wx
import wx.grid

class RapidGUIFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.grid = wx.GridBagSizer(hgap=5, vgap=10)

        self.download_btn = wx.Button(self, -1, "Add URL(s) to download")
        self.current_dls = wx.grid.Grid(self, -1, size=(600, 300))

        self.setupGrid()
        self.doLayout()

    def setupGrid(self):
        self.current_dls.CreateGrid(0, 3)
        self.current_dls.EnableEditing(0)
        self.current_dls.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
        self.current_dls.SetColLabelValue(0, "Filename")
        self.current_dls.SetColLabelValue(1, "%")
        self.current_dls.SetColLabelValue(2, "Speed")

    def doLayout(self):
        self.grid.Add(self.download_btn, pos=(0,0))
        self.grid.Add(self.current_dls, pos=(1,0))

        self.mainSizer.Add(self.grid, 0, wx.ALL, 10)

        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.mainSizer)
        self.Layout()

class RapidGUI(wx.App):
    def OnInit(self):
        frame = RapidGUIFrame(None, -1, "Rapidshare Downloader")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == "__main__":
    app = RapidGUI(0)
    app.MainLoop()
