import wx


class MovingLine(wx.Panel):
    def __init__(self, parent, slider):
        wx.Panel.__init__(self, parent, size=(-1, 30), style=wx.SUNKEN_BORDER)
        self.parent = parent
        self.slider = slider
        self.font = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL, False, 'Courier 10 Pitch')

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def OnPaint(self, e):
        num = range(75, 700, 75)
        dc = wx.PaintDC(self)
        dc.SetFont(self.font)
        w, h = self.GetSize()

        dc.SetPen(wx.Pen('#5C5142'))

        dc.DrawLine(self.slider, h, self.slider, h+100)

    def OnSize(self, e):
        self.Refresh()

# class CustomSlider(wx.Slider):
#     def getCursorPosition(self):
#         self.


class Example(wx.Panel):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):
        self.cw = 75
        grid = wx.GridBagSizer(hgap=10, vgap=5)
        panel = wx.Panel(self)
        sld1panel = wx.Panel(panel)
        # sld2panel = wx.Panel(panel)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sld1 = wx.Slider(sld1panel, value=75, maxValue=750, size=(200, -1),
                              style=wx.SL_LABELS)
        self.line = MovingLine(panel, self.sld1.GetValue())
        self.sld2 = wx.Slider(sld2panel, value=75, maxValue=750, size=(200, -1),
                              style=wx.SL_LABELS)
        hbox.Add(self.line, 1, wx.EXPAND)
        hbox2.Add(sld1panel, 1, wx.EXPAND)
        hbox3.Add(self.sld1, 0, wx.LEFT | wx.TOP, 35)

        sld1panel.SetSizer(hbox3)
        sld1panel.SetSizer(hbox3)

        vbox.Add(hbox2, 1, wx.EXPAND)
        vbox.Add(hbox, 0, wx.EXPAND)
        # self.sld1.SetFocus()
        self.Bind(wx.EVT_SCROLL, self.OnScroll1, self.sld1)
        self.Bind(wx.EVT_SCROLL, self.OnScroll2, self.sld2)
        self.Bind(wx.EVT_PAINT, lambda event: self.OnPaint(event, [0,40,0,150]))
        grid.Add(self.sld1, pos=(0, 0), flag=wx.EXPAND)
        grid.Add(self.sld2, pos=(5, 0), flag=wx.EXPAND)
        bigbox.Add(grid, 0, wx.ALL, 5)
        self.SetSizerAndFit(bigbox)
        self.Centre()

    def OnPaint(self, event, pos):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 1))
        print(self.cw)
        dc.DrawLine(self.cw,pos[1],self.cw,pos[3])

    def OnScroll1(self, e):
        self.cw = self.sld1.GetValue()
        self.sld2.SetValue(self.cw)
    def OnScroll2(self, e):
        self.cw = self.sld2.GetValue()
        self.sld1.SetValue(self.cw)


def main():
    app = wx.App(False)
    frame = wx.Frame(None)
    panel = Example(frame)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
