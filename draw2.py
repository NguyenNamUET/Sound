import matplotlib.pyplot as plt
if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt

    sound_x = np.arange(0.0, 3.0, 0.01)
    sound_y = np.sin(2 * np.pi * sound_x)
    collected_points = [(min(sound_x), 0)]

    fig, ax = plt.subplots()
    points, = ax.plot(sound_x, sound_y)
    ax.vlines(x=min(sound_x), ymin=min(sound_y), ymax=max(sound_y), colors='red')
    ax.axes.vlines(x=max(sound_x), ymin=min(sound_y), ymax=max(sound_y), colors='red')
    for i in np.arange(0.5, 2.5, 0.5):
        coor_x = i
        collected_points.append((coor_x, 0))
        ax.vlines(x=coor_x, ymin=min(sound_y), ymax=max(sound_y), colors='orange')
    collected_points.append((max(sound_x), 0))

    # Get the x and y data and transform it into pixel coordinates
    x = [x for x, _ in collected_points]
    y = [y for _, y in collected_points]
    xy_pixels = ax.transData.transform(np.vstack([x, y]).T)
    xpix, ypix = xy_pixels.T

    # In matplotlib, 0,0 is the lower left corner, whereas it's usually the upper
    # left for most image software, so we'll flip the y-coords...
    width, height = fig.canvas.get_width_height()
    ypix = height - ypix


    for xp, yp in zip(xpix, ypix):
        print('{x:0.2f}\t{y:0.2f}'.format(x=xp, y=yp))

    # We have to be sure to save the figure with it's current DPI
    # (savfig overrides the DPI of the figure, by default)
    fig.savefig('test.png', dpi=fig.dpi)