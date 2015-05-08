import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.interactive(False)

plt.plot([1,2,3,4], [0,4,9,16], 'ro')
plt.axis([0,6,0,20])

plt.show()