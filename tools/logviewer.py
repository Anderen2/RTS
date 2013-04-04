#Logviewer

from __future__ import division
import wx
import wx.lib.mixins.listctrl as listmix

import functions as f
import parser
import shared

Multipiler=1.25
Mp=Multipiler
WXApp=wx.App(False)


class MainWindow(wx.Frame, listmix.ColumnSorterMixin):
	def __init__(self,parent,title):
		wx.Frame.__init__(self, parent, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER, title=title, size=(640*Mp,480*Mp))
		GlobalColor='#FFFFF'

		#Filemenu:
		filemenu=wx.Menu()

		fileconnect=filemenu.Append(wx.ID_REFRESH, "Reconnect", "Reconnect to the server")
		#self.Bind(wx.EVT_MENU, f.fileconnect, fileconnect)
		fileload=filemenu.Append(wx.ID_OPEN, "Load Serverlist/Config", "Loads a .serverconfig file")
		#self.Bind(wx.EVT_MENU, f.fileload, fileload)
		filesave=filemenu.Append(wx.ID_SAVE, "Save Serverlist/Config", "Saves a .serverconfig file")
		#self.Bind(wx.EVT_MENU, f.filesave, filesave)
		filerfsh=filemenu.Append(wx.ID_NONE, "Debug: Alive threads", "Prints")
		#self.Bind(wx.EVT_MENU, f.b_Refresh, filerfsh)

		filemenu.AppendSeparator()
		
		fileabout=filemenu.Append(wx.ID_ABOUT, "About", "About this application")
		#self.Bind(wx.EVT_MENU, f.fileabout, fileabout)
		fileexit=filemenu.Append(wx.ID_EXIT, "Exit", "Close this application")
		#self.Bind(wx.EVT_MENU, f.fileexit, fileexit)

		#Menubar:
		menubar=wx.MenuBar()
		menubar.Append(filemenu,"File")
		self.SetMenuBar(menubar)

		#Panels:
		Pbigicons        = wx.Panel(self, wx.ID_ANY, (0,       0)   , size=(640*Mp,  30*Mp)) #100
		Pprojectlist     = wx.Panel(self, wx.ID_ANY, (0,      30*Mp), size=(150*Mp, 250*Mp)) #200
		Pprojectsettings = wx.Panel(self, wx.ID_ANY, (150*Mp, 30*Mp), size=(490*Mp, 430*Mp)) #300
		Pstdin           = wx.Panel(self, wx.ID_ANY, (150*Mp,     460*Mp), size=(640*Mp, 20*Mp))

		Pbigicons.SetBackgroundColour(GlobalColor)
		Pprojectlist.SetBackgroundColour("#33223")
		Pprojectsettings.SetBackgroundColour("#f0f0f")

		#BigIcons(13):
		BigIconList=["Open", "Search", "_", "Run", "Stop", "LiveView"]
		print("-------------------------------")
		print("BigIcons:")
		for x in BigIconList:
			foo=BigIconList.index(x)
			tset=wx.Button(Pbigicons, 100+foo, x, (0+(foo*50)*Mp, 0), (50*Mp, 30*Mp))
			#self.Bind(wx.EVT_BUTTON,f.getFunc()["b_"+x],tset)
			print(x+" : "+str(0+(foo*50))+" x "+str(50+(foo*50)))
		wx.Button(Pbigicons, 113, ">>", (600*Mp,0), (35*Mp, 30*Mp))

		#Projectlist:
		shared.LISTprojectlist = wx.ListBox(Pprojectlist, 200, (0,0), (150*Mp, 250*Mp), [], wx.LB_SINGLE)
		shared.LISTprojectlist.SetBackgroundColour(GlobalColor)
		#self.Bind(wx.EVT_LISTBOX, f.selection, shared.LISTprojectlist)

		#Projectsettings:
		#logfile=open("../logs/engine.log", "r")
		#shared.console2=wx.TextCtrl(Pprojectsettings, 801, logfile.read(), (0,0), (490*Mp, 430*Mp), style = wx.TE_MULTILINE | wx.TE_READONLY)
		shared.console2=wx.ListCtrl(Pprojectsettings, 801, (0,0), (490*Mp, 430*Mp), name="Fap", style=wx.LC_REPORT|wx.BORDER_SUNKEN|wx.LC_SORT_ASCENDING)
		shared.console2.InsertColumn(0, "Time", format=wx.LIST_FORMAT_LEFT, width=-1)
		shared.console2.InsertColumn(1, "Urgency")
		shared.console2.InsertColumn(2, "Module")
		shared.console2.InsertColumn(3, "Message")

		parser.parsefile("../logs/engine.log")
		parser.printNice(parser.Lines)
		parser.printListctl(parser.Lines, shared.console2)

		self.itemDataMap = parser.Lines
		listmix.ColumnSorterMixin.__init__(self, 4)
		self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, shared.console2)
		#self.SortListItems(2, 1)

		#Stdin
		shared.stdin=wx.TextCtrl(Pstdin, 801, "", (0,0*Mp), (490*Mp, 20*Mp), style=wx.TE_PROCESS_ENTER)
		#self.Bind(wx.EVT_TEXT_ENTER, f.stdinEnter, shared.stdin)

		##__________________________________________________________________
		##End!
		self.Show(True)

	def GetListCtrl(self):
		return shared.console2

	def OnColClick(self, event):
		event.Skip()
		print("Ouch!")

shared.MainWindowI=MainWindow(None, "YARTS TOOL - LogDebugger")
WXApp.MainLoop()