import wx
import matplotlib as plt
plt.use('WXAgg')
import numpy as np
import random
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import wx.lib.inspection
sound_x = np.arange(0.0, 3.0, 0.01)
sound_y = np.sin(2 * np.pi * sound_x)


class DrawPanel(wx.Frame):
    """Draw a line to a panel."""
    def __init__(self):
        wx.Frame.__init__(self, title="Draw on Panel")
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event=None):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 1))
        dc.DrawLine(0, 0, 50, 50)


class PlotT(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.box = wx.BoxSizer(wx.HORIZONTAL)
        self.line1 = wx.StaticLine(self, pos=wx.Point(360,0), size=wx.Size(1, 1000), style=wx.LI_VERTICAL)
        self.line2 = wx.StaticLine(self, pos=wx.Point(10,0), size=wx.Size(1, 1000), style=wx.LI_VERTICAL)
        self.line3 = wx.StaticLine(self, pos=wx.Point(20,0), size=wx.Size(1, 1000), style=wx.LI_VERTICAL)
        self.panel1 = wx.Panel(self.line1)
        self.panel2 = wx.Panel(self.line2)
        self.panel3 = wx.Panel(self.line3)
        self.Bind(wx.EVT_MOTION, self.MouseDown, self.line1)
        self.box.Add(self.panel1, 1, wx.EXPAND)
        self.box.Add(self.panel2, 1, wx.EXPAND)
        self.box.Add(self.panel3, 1, wx.EXPAND)
        self.SetSizerAndFit(self.box)

    def MouseDown(self, evt):
        print("MOVING1")
        if evt.Dragging() and evt.LeftIsDown():
            print("MOVING2")
            # self.lastx, self.lasty = self.x, self.y
            # self.x, self.y = evt.GetPosition()
            self.Refresh(False)


class Plot(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.axis('off')
        self.axes.plot(sound_x, sound_y)
        self.points = [(min(sound_x),0)]
        self.axes.vlines(x=min(sound_x), ymin=min(sound_y), ymax=max(sound_y), colors='red')
        self.axes.vlines(x=max(sound_x), ymin=min(sound_y), ymax=max(sound_y), colors='red')
        for i in np.arange(0.0, 2.5, 0.5):
            coor_x = i+random.random()
            self.points.append((coor_x,0))
            self.axes.vlines(x=coor_x, ymin=min(sound_y), ymax=max(sound_y), colors='orange')
        self.points.append((max(sound_x),0))
        self.canvas1 = FigureCanvas(self, -1, self.figure)
        self.canvas2 = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas1, 1, wx.EXPAND)
        self.sizer.Add(self.canvas2, 1, wx.EXPAND)
        #self.Bind(wx.EVT_SIZE, self.OnSize)
        self.SetSizer(self.sizer)
        self.Fit()


class MainApp(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        frame = wx.Frame(None, -1, 'CubeCanvas3', size=(400, 400))
        panel = wx.Panel(frame, -1)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        plot = PlotT(panel)
        self.sizer.Add(plot, 1, wx.EXPAND)
        panel.SetSizer(self.sizer)
        panel.Fit()

        frame.Show(True)

        self.frame = frame
        return True

    def OnExitApp(self, evt):
        self.frame.Close(True)

    def OnCloseFrame(self, evt):
        if hasattr(self, "window") and hasattr(self.window, "ShutdownDemo"):
            self.window.ShutdownDemo()
        evt.Skip()


if __name__ == '__main__':
    app = MainApp()
    wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()