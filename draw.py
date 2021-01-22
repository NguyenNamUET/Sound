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

sound_x = np.arange(0.0, 3.0, 0.01)
sound_y = np.sin(2 * np.pi * sound_x)

width, height = 0, 0
points = []
class Plot(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.plot(sound_x, sound_y)
        self.points = [(min(sound_x),0)]
        self.axes.vlines(x=min(sound_x), ymin=min(sound_y), ymax=max(sound_y), colors='red')
        self.axes.vlines(x=max(sound_x), ymin=min(sound_y), ymax=max(sound_y), colors='red')
        for i in np.arange(0.0, 2.5, 0.5):
            coor_x = i+random.random()
            self.points.append((coor_x,0))
            self.axes.vlines(x=coor_x, ymin=min(sound_y), ymax=max(sound_y), colors='orange')
        self.points.append((max(sound_x),0))
        self.canvas = FigureCanvas(self, -1, self.figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        #self.Bind(wx.EVT_SIZE, self.OnSize)
        self.calculateGrid(None)
        self.SetSizer(self.sizer)
        self.Fit()

    def calculateGrid(self, event):
        # bbox = self.axes.get_window_extent().transformed(self.figure.dpi_scale_trans.inverted())
        # width, height = bbox.width, bbox.height
        # width *= self.figure.dpi
        # height *= self.figure.dpi
        # print(width, height)
        print(len(self.points))
        x = [x for x,_ in self.points]
        y = [y for _, y in self.points]
        xy_pixels = self.axes.transData.transform(np.vstack([x, y]).T)
        xpix, ypix = xy_pixels.T

        # In matplotlib, 0,0 is the lower left corner, whereas it's usually the upper
        # left for most image software, so we'll flip the y-coords...
        width, height = self.figure.canvas.get_width_height()
        ypix = height - ypix

        for xp, yp in zip(xpix, ypix):
            print('{x:0.2f}\t{y:0.2f}'.format(x=xp, y=yp))
            points.append((xp,yp))

        print(points)


class glCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        self.context = glcanvas.GLContext(self)

        # initial mouse position at first line
        self.lastx = self.x = points[0][0]
        self.lasty = self.y = points[0][1]
        self.size = None
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
        #glFrustum(-0.5, 0.5, -0.5, 0.5, 1.0, 3.0)

        # position viewer
        glOrtho(-200, 200, -200, 200, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

    def OnDraw(self):
        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # draw six faces of a cube
        glBegin(GL_POINTS)
        # glVertex2f(self.lastx, self.lasty)
        # glVertex2f(self.lastx, self.lasty+10)
        for i, j in zip(sound_x, sound_y):
            glVertex2f(i*50-len(sound_x)/2, j*50)
        glEnd()
        glBegin(GL_LINES)
        glVertex2f(0,100)
        glVertex2f(0, -100)
        glVertex2f(100, 0)
        glVertex2f(-100, 0)
        glEnd()
        print(self.x, self.y, self.lastx, self.lasty)
        # if self.size is None:
        #     self.size = self.GetClientSize()
        # w, h = self.size
        # w = max(w, 1.0)
        # h = max(h, 1.0)
        # xScale = 180.0 / w
        # yScale = 180.0 / h
        # glRotatef((self.y - self.lasty) * yScale, 1.0, 0.0, 0.0)
        # # glRotatef((self.x - self.lastx) * xScale, 0.0, 1.0, 0.0)

        self.SwapBuffers()


class MainApp(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        frame = wx.Frame(None, -1, 'CubeCanvas', size=(400, 400))
        panel = wx.Panel(frame, -1)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        plot = Plot(panel)
        self.sizer.Add(plot, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(LineCanvas(panel), 1, wx.LEFT | wx.TOP | wx.GROW)
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
    app.MainLoop()