import wx

class DrawPanel(wx.Frame):

    """Draw a line to a panel."""

    def __init__(self):
        wx.Frame.__init__(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event=None):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 4))
        dc.DrawLine(0, 0, 50, 50)

if __name__ == '__main__':
    app = wx.App(False)
    frame = DrawPanel()
    frame.Show()
    app.MainLoop()