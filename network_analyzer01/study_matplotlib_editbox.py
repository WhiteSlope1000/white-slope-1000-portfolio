import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets


fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
t = np.arange(-2.0, 2.0, 0.001)
s = t ** 2
l, = plt.plot(t, s, lw=2)


def on_submit(formula_by_text):
    ydata = eval(formula_by_text)
    l.set_ydata(ydata)
    ax.set_ylim(
        np.min(ydata),
        np.max(ydata),
    )
    plt.draw()


axbox = plt.axes([0.1, 0.05, 0.8, 0.075])
label = 'Evaluate'
formula = 't ** 2'
text_box = matplotlib.widgets.TextBox(axbox, label, initial=formula)
text_box.on_submit(on_submit)

if 0:
    plt.savefig('screenshot_matplotlib.png')

if 1:
    plt.show()

if 0:
    print(*dir(matplotlib.widgets), sep='\n')
