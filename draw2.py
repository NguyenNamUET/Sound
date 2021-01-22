# import wx
#
#
# class MovingLine(wx.Panel):
#     def __init__(self, parent, slider):
#         wx.Panel.__init__(self, parent, size=(-1, 30), style=wx.SUNKEN_BORDER)
#         self.parent = parent
#         self.slider = slider
#         self.font = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
#             wx.FONTWEIGHT_NORMAL, False, 'Courier 10 Pitch')
#
#         self.Bind(wx.EVT_PAINT, self.OnPaint)
#         self.Bind(wx.EVT_SIZE, self.OnSize)
#
#
#     def OnPaint(self, e):
#         num = range(75, 700, 75)
#         dc = wx.PaintDC(self)
#         dc.SetFont(self.font)
#         w, h = self.GetSize()
#
#         dc.SetPen(wx.Pen('#5C5142'))
#
#         dc.DrawLine(self.slider, h, self.slider, h+100)
#
#     def OnSize(self, e):
#         self.Refresh()
#
# # class CustomSlider(wx.Slider):
# #     def getCursorPosition(self):
# #         self.
#
#
# class Example(wx.Panel):
#
#     def __init__(self, *args, **kwargs):
#         super(Example, self).__init__(*args, **kwargs)
#
#         self.InitUI()
#
#     def InitUI(self):
#         self.cw = 75
#         grid = wx.GridBagSizer(hgap=10, vgap=5)
#         panel = wx.Panel(self)
#         sld1panel = wx.Panel(panel)
#         # sld2panel = wx.Panel(panel)
#         vbox = wx.BoxSizer(wx.VERTICAL)
#         hbox = wx.BoxSizer(wx.HORIZONTAL)
#         hbox2 = wx.BoxSizer(wx.HORIZONTAL)
#         hbox3 = wx.BoxSizer(wx.HORIZONTAL)
#         self.sld1 = wx.Slider(sld1panel, value=75, maxValue=750, size=(200, -1),
#                               style=wx.SL_LABELS)
#         self.line = MovingLine(panel, self.sld1.GetValue())
#         self.sld2 = wx.Slider(sld2panel, value=75, maxValue=750, size=(200, -1),
#                               style=wx.SL_LABELS)
#         hbox.Add(self.line, 1, wx.EXPAND)
#         hbox2.Add(sld1panel, 1, wx.EXPAND)
#         hbox3.Add(self.sld1, 0, wx.LEFT | wx.TOP, 35)
#
#         sld1panel.SetSizer(hbox3)
#         sld1panel.SetSizer(hbox3)
#
#         vbox.Add(hbox2, 1, wx.EXPAND)
#         vbox.Add(hbox, 0, wx.EXPAND)
#         # self.sld1.SetFocus()
#         self.Bind(wx.EVT_SCROLL, self.OnScroll1, self.sld1)
#         self.Bind(wx.EVT_SCROLL, self.OnScroll2, self.sld2)
#         self.Bind(wx.EVT_PAINT, lambda event: self.OnPaint(event, [0,40,0,150]))
#         grid.Add(self.sld1, pos=(0, 0), flag=wx.EXPAND)
#         grid.Add(self.sld2, pos=(5, 0), flag=wx.EXPAND)
#         bigbox.Add(grid, 0, wx.ALL, 5)
#         self.SetSizerAndFit(bigbox)
#         self.Centre()
#
#     def OnPaint(self, event, pos):
#         dc = wx.PaintDC(self)
#         dc.Clear()
#         dc.SetPen(wx.Pen(wx.BLACK, 1))
#         print(self.cw)
#         dc.DrawLine(self.cw,pos[1],self.cw,pos[3])
#
#     def OnScroll1(self, e):
#         self.cw = self.sld1.GetValue()
#         self.sld2.SetValue(self.cw)
#     def OnScroll2(self, e):
#         self.cw = self.sld2.GetValue()
#         self.sld1.SetValue(self.cw)
#
#
# def main():
#     app = wx.App(False)
#     frame = wx.Frame(None)
#     panel = Example(frame)
#     frame.Show()
#     app.MainLoop()
#
#
# if __name__ == '__main__':
#     main()
import wx
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLUT import *
import matplotlib as plt
plt.use('WXAgg')
import numpy as np
import random
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import wx.lib.inspection
x1,y1 = 3, 500
x2,y2 = 3, -500


class glCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.lastx = self.x = 0
        self.lasty = self.y = 0
        self.init = False
        self.context = glcanvas.GLContext(self)

        # initial mouse position at first line
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def OnSize(self, event):
        wx.CallAfter(self.DoSetViewport)
        event.Skip()

    def DoSetViewport(self):
        size = self.size = self.GetClientSize()
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def OnMouseDown(self, evt):
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = evt.GetPosition()

    def OnMouseUp(self, evt):
        self.ReleaseMouse()

    def OnMouseMotion(self, evt):
        print(self.x, self.y,  self.lastx, self.lasty)
        if evt.Dragging() and evt.LeftIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = evt.GetPosition()
            self.Refresh(False)


class LineCanvas(glCanvas):
    def InitGL(self):
        # set viewing projection
        glClearColor(0,0,0,0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # position viewer
        glOrtho(-500, 500, -500, 500, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

    def OnDraw(self):
        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glTranslatef((self.x - self.lastx) * 2.75, 0, 0)
        glBegin(GL_LINES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()
        glPopMatrix()

        glPushMatrix()
        glTranslatef((self.x - self.lastx) * 2.75, 0, 0)
        glBegin(GL_LINES)
        glVertex2f(x1 + 100, y1)
        glVertex2f(x2 + 100, y2)
        glEnd()
        glLoadIdentity()
        glPopMatrix()

        self.SwapBuffers()


class MainApp(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        frame = wx.Frame(None, -1, 'CubeCanvas', size=(400, 400))
        panel = wx.Panel(frame, -1)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.sizer.Add(LineCanvas(panel), 1, wx.EXPAND)

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
