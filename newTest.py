import wx
from wx import glcanvas
import matplotlib as plt
plt.use('WXAgg')
import numpy as np
import random
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

sound_x = np.arange(0.0, 3.0, 0.01)
sound_y = np.sin(2 * np.pi * sound_x)

width, height = 0, 0
points = []


class Line(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(20, 20))
        self.SetBackgroundColour("red")
        self.isDragStarted = False
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)

    def OnLeftDown(self, evt):
        print("ON LEFT MOUSE DOWN")
        self.isDragStarted = True
        self.CaptureMouse()
        self.prevMousePos = evt.GetPosition()
        evt.Skip()

    def OnLeftUp(self, evt):
        self.isDragStarted = False
        if self.HasCapture():
            self.ReleaseMouse()
        evt.Skip()

    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown() and self.isDragStarted:
            mousePos = evt.GetPosition()
            wndPos = self.GetPosition()
            self.Move(wndPos - (self.prevMousePos - mousePos))
        evt.Skip()


class Plot(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.plot(sound_x, sound_y)
        self.points = [(min(sound_x),0)]
        self.axes.vlines(x=min(sound_x), ymin=min(sound_y), ymax=max(sound_y), colors='red')
        self.axes.vlines(x=max(sound_x), ymin=min(sound_y), ymax=max(sound_y), colors='red')
        for i in np.arange(0.5, 2.5, 0.5):
            coor_x = i
            self.points.append((coor_x,0))
            self.axes.vlines(x=coor_x, ymin=min(sound_y), ymax=max(sound_y), colors='orange')
        self.points.append((max(sound_x),0))
        self.canvas = FigureCanvas(self, -1, self.figure)

        # self.sizer = wx.BoxSizer(wx.VERTICAL)
        # self.sizer.Add(self.canvas, 1, wx.EXPAND)
        # self.Bind(wx.EVT_SIZE, self.OnSize)
        self.calculateGrid(None)

        # self.SetSizer(self.sizer)
        self.Fit()

    def calculateGrid(self, event):
        # bbox = self.axes.get_window_extent().transformed(self.figure.dpi_scale_trans.inverted())
        # width, height = bbox.width, bbox.height
        # width *= self.figure.dpi
        # height *= self.figure.dpi
        # print(width, height)
        x = [x for x,_ in self.points]
        y = [y for _, y in self.points]
        xy_pixels = self.axes.transData.transform(np.vstack([x, y]).T)
        xpix, ypix = xy_pixels.T

        # In matplotlib, 0,0 is the lower left corner, whereas it's usually the upper
        # left for most image software, so we'll flip the y-coords...
        width, height = self.figure.canvas.get_width_height()
        ypix = height - ypix

        for xp, yp in zip(xpix, ypix):
            points.append((xp,yp))

        print(points)


class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        panel = wx.Panel(self)
        linePanel = Line(panel)
        plotPanel = Plot(self)
        self.Show()


if __name__ == '__main__':
    app = wx.App(False)
    MainFrame(None)
    app.MainLoop()
