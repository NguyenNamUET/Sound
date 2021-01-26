# import wx
# import matplotlib as plt
# plt.use('WXAgg')
# import numpy as np
# import random
# from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
# from matplotlib.backends.backend_wx import NavigationToolbar2Wx
# from matplotlib.figure import Figure
# import wx.lib.inspection
# sound_x = np.arange(0.0, 3.0, 0.01)
# sound_y = np.sin(2 * np.pi * sound_x)
#
#
# class DrawPanel(wx.Frame):
#     """Draw a line to a panel."""
#     def __init__(self):
#         wx.Frame.__init__(self, title="Draw on Panel")
#         self.Bind(wx.EVT_PAINT, self.OnPaint)
#
#     def OnPaint(self, event=None):
#         dc = wx.PaintDC(self)
#         dc.Clear()
#         dc.SetPen(wx.Pen(wx.BLACK, 1))
#         dc.DrawLine(0, 0, 50, 50)
#
#
# class PlotT(wx.Panel):
#     def __init__(self, parent):
#         wx.Panel.__init__(self, parent)
#         self.box = wx.BoxSizer(wx.HORIZONTAL)
#         self.line1 = wx.StaticLine(self, pos=wx.Point(360,0), size=wx.Size(1, 1000), style=wx.LI_VERTICAL)
#         self.line2 = wx.StaticLine(self, pos=wx.Point(10,0), size=wx.Size(1, 1000), style=wx.LI_VERTICAL)
#         self.line3 = wx.StaticLine(self, pos=wx.Point(20,0), size=wx.Size(1, 1000), style=wx.LI_VERTICAL)
#         self.panel1 = wx.Panel(self.line1)
#         self.panel2 = wx.Panel(self.line2)
#         self.panel3 = wx.Panel(self.line3)
#         self.Bind(wx.EVT_MOTION, self.MouseDown, self.line1)
#         self.box.Add(self.panel1, 1, wx.EXPAND)
#         self.box.Add(self.panel2, 1, wx.EXPAND)
#         self.box.Add(self.panel3, 1, wx.EXPAND)
#         self.SetSizerAndFit(self.box)
#
#     def MouseDown(self, evt):
#         print("MOVING1")
#         if evt.Dragging() and evt.LeftIsDown():
#             print("MOVING2")
#             # self.lastx, self.lasty = self.x, self.y
#             # self.x, self.y = evt.GetPosition()
#             self.Refresh(False)
#
#
# class Plot(wx.Panel):
#     def __init__(self, parent):
#         wx.Panel.__init__(self, parent)
#         self.figure = Figure()
#         self.axes = self.figure.add_subplot(111)
#         self.axes.axis('off')
#         self.axes.plot(sound_x, sound_y)
#         self.points = [(min(sound_x),0)]
#         self.axes.vlines(x=min(sound_x), ymin=min(sound_y), ymax=max(sound_y), colors='red')
#         self.axes.vlines(x=max(sound_x), ymin=min(sound_y), ymax=max(sound_y), colors='red')
#         for i in np.arange(0.0, 2.5, 0.5):
#             coor_x = i+random.random()
#             self.points.append((coor_x,0))
#             self.axes.vlines(x=coor_x, ymin=min(sound_y), ymax=max(sound_y), colors='orange')
#         self.points.append((max(sound_x),0))
#         self.canvas1 = FigureCanvas(self, -1, self.figure)
#         self.canvas2 = FigureCanvas(self, -1, self.figure)
#         self.sizer = wx.BoxSizer(wx.VERTICAL)
#         self.sizer.Add(self.canvas1, 1, wx.EXPAND)
#         self.sizer.Add(self.canvas2, 1, wx.EXPAND)
#         #self.Bind(wx.EVT_SIZE, self.OnSize)
#         self.SetSizer(self.sizer)
#         self.Fit()
#
#
# class MainApp(wx.App):
#     def __init__(self):
#         wx.App.__init__(self, redirect=False)
#
#     def OnInit(self):
#         frame = wx.Frame(None, -1, 'CubeCanvas3', size=(400, 400))
#         panel = wx.Panel(frame, -1)
#         self.sizer = wx.BoxSizer(wx.HORIZONTAL)
#
#         plot = PlotT(panel)
#         self.sizer.Add(plot, 1, wx.EXPAND)
#         panel.SetSizer(self.sizer)
#         panel.Fit()
#
#         frame.Show(True)
#
#         self.frame = frame
#         return True
#
#     def OnExitApp(self, evt):
#         self.frame.Close(True)
#
#     def OnCloseFrame(self, evt):
#         if hasattr(self, "window") and hasattr(self.window, "ShutdownDemo"):
#             self.window.ShutdownDemo()
#         evt.Skip()
#
#
# if __name__ == '__main__':
#     app = MainApp()
#     wx.lib.inspection.InspectionTool().Show()
#     app.MainLoop()
# import wx
#
#
# class WindowDragger:
#     def __init__(self, window):
#         self.window = window
#         self.isDragStarted = False
#         self.window.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
#         self.window.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
#         self.window.Bind(wx.EVT_MOTION, self.OnMouseMove)
#
#     def OnLeftDown(self, evt):
#         self.isDragStarted = True
#         self.window.CaptureMouse()
#         self.prevMousePos = evt.GetPosition()
#         evt.Skip()
#
#     def OnLeftUp(self, evt):
#         self.isDragStarted = False
#         if self.window.HasCapture():
#             self.window.ReleaseMouse()
#         evt.Skip()
#
#     def OnMouseMove(self, evt):
#         if evt.Dragging() and evt.LeftIsDown() and self.isDragStarted:
#             mousePos = evt.GetPosition()
#             wndPos = self.window.GetPosition()
#             self.window.Move(wndPos - (self.prevMousePos - mousePos))
#         evt.Skip()
#
#
# class MainFrame(wx.Frame):
#     def __init__(self):
#         wx.Frame.__init__(self, None, -1, 'Title', size=(200,150))
#         panel = wx.Panel(self)
#         childPanel = wx.Panel(panel, size=(30,30), pos=(10,10))
#         childPanel.SetBackgroundColour('red')
#         # Enable windows to drag.
#         dragger = WindowDragger(childPanel)
#
#
# if __name__ == '__main__':
#     app = wx.PySimpleApp()
#     MainFrame().Show()
#     app.MainLoop()


import io
import wx


def loadBitmap(path):
    data = open(path, "rb").read()
    bitmap = wx.Bitmap(wx.Image(io.BytesIO(data)))
    return bitmap


class DragImage(wx.Panel):
    def __init__(self, parent):
        bitmap = loadBitmap("C:/Users/namn/Desktop/trollface.jpg")
        self.drag_image = wx.DragImage(bitmap)
        self.panel = parent
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.beginDrag)
        self.panel.Bind(wx.EVT_MOTION, self.doDrag)
        self.panel.Bind(wx.EVT_LEFT_UP, self.endDrag)

    def beginDrag(self, evt):
        print("BEGIN DRAGGING...")
        x, y = evt.GetPosition()
        self.drag_image.BeginDrag(wx.Point(x,y), self.panel)


    def doDrag(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            print("DRAGGING")
            self.CaptureMouse()
            x,y = evt.GetPosition()
            print(x,y)
            self.drag_image.Show()
            self.drag_image.Move(wx.Point(x,y))

    def endDrag(self, evt):
        print("FINSISH DRAGGING...")
        self.drag_image.EndDrag()


class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, 'Title', size=(200,150))
        panel = wx.Panel(self)
        childPanel = wx.Panel(panel, pos=(10,10))
        #childPanel.SetBackgroundColour('red')
        # Enable windows to drag.
        dragger = DragImage(childPanel)
        self.Show()

if __name__ == '__main__':
    app = wx.App(False)
    MainFrame(None)
    app.MainLoop()