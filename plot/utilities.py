import matplotlib.pyplot as plt
import numpy as np


def renderPlot(data):
    t = []
    s = []
    for i in data:
        t.append(i[0])
        s.append(i[1])

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='hour', ylabel='price',
           title='Test')
    ax.grid()

    fig.savefig("test.png")
