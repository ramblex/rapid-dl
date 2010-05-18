#!/usr/bin/python

import subprocess
import os
import time
import wx
import wx.grid

ID_URL = 1

class AddURL(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(800, 500))

        panel = wx.Panel(self, -1)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        input_txt = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE)
        hbox1.Add(input_txt, 1, wx.EXPAND)

        panel.SetSizer(hbox1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        add_btn = wx.Button(self, -1, 'Add', size=(70, 30))
        cancel_btn = wx.Button(self, -1, 'Cancel', size=(70, 30))
        hbox2.Add(add_btn, 1)
        hbox2.Add(cancel_btn, 1, wx.LEFT, 5)

        vbox.Add((-1, 10))
        vbox.Add(wx.StaticText(self, -1, 'URLs'), 0, wx.LEFT, 10)
        vbox.Add(panel, 1, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        vbox.Add((-1, 10))
        vbox.Add(hbox2, 2, wx.ALIGN_CENTER | wx.TOP, 10)

        self.SetSizer(vbox)
        
class GridData(wx.grid.PyGridTableBase):
    _cols = "Filename %".split()
    _data = []

    def GetColLabelValue(self, col):
        return self._cols[col]

    def GetNumberRows(self):
        return len(self._data)

    def GetNumberCols(self):
        return len(self._cols)

    def GetValue(self, row, col):
        return self._data[row][col]

    def SetValue(self, row, col, val):
        self._data[row][col] = val

    def AddDownload(self, filename):
        self._data.append([filename, "0"])
        self.GetView().ProcessTableMessage(
            wx.grid.GridTableMessage(self, 
                                     wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1))
        return True
    
class RapidGUIFrame(wx.Frame):

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(800, 500))
        self.grid_has_been_setup = False
        self.panel = wx.Panel(self, -1)

        # toolbar = self.CreateToolBar()
        # toolbar.AddLabelTool(ID_URL, '', wx.Bitmap('icons/add.png'))
        # toolbar.Realize()
        # self.Bind(wx.EVT_TOOL, self.OnAddURL, id=ID_URL)

        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # URLs textfield
        hbox1 = wx.BoxSizer
        self.urls_txt = wx.TextCtrl(self.panel, -1, style=wx.TE_MULTILINE)

        # Download button
        download_btn = wx.Button(self.panel, -1, label='Download')
        download_btn.Bind(wx.EVT_BUTTON, self.on_download_btn)

        self.data = GridData()
        grid = wx.grid.Grid(self.panel)
        grid.EnableEditing(0)
        grid.SetTable(self.data, True, selmode=wx.grid.Grid.SelectRows)
        grid.SetColSize(0, 610)

        # Add everything to the sizer
        self.vbox.Add(self.urls_txt, 2, wx.ALL | wx.EXPAND, 10)
        self.vbox.Add(download_btn, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.vbox.Add(grid, 2, wx.ALIGN_CENTER | wx.ALL, 10)

        self.panel.SetSizerAndFit(self.vbox)
        self.Centre()
        self.Show(True)

    def on_download_btn(self, event):
        [self.data.AddDownload(url) for url in self.urls_txt.GetValue().splitlines()]

    def OnAddURL(self, event):
        addurl = AddURL(None, -1, 'Add URL(s)')
        addurl.ShowModal()
        addurl.Destroy()

class RapidGUI(wx.App):
    logdir = "/Users/alexduller/.rapid-dl/logs/"
    processes = {}

    def OnInit(self):
        frame = RapidGUIFrame(None, -1, "Rapidshare Downloader")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

    def download(url):
        filename = os.path.basename(url)
        self.processes[filename] = subprocess.Popen(['rapid-dl', url])
        print "Downloading '"+filename+"'"

app = RapidGUI(0)
app.MainLoop()
