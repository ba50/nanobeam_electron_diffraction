import numpy as np
import matplotlib.pyplot as pp
import time

def animate_data(data):

    fig,ax = pp.subplots(1,1)

    # I'm not convinced that animated=True does anything either...
    image = ax.imshow(data[0,:,:],animated=True)

    # pp.draw()
    fig.canvas.draw()

    start = time.time()
    tic = start
    for ii in range(1,data.shape[0]):
        if not(ii % 10):
            toc = time.time()
            print("FPS =\t%.6G" %(10./(toc-tic)))
            tic = time.time()
        image.set_data(data[ii,:,:])

        # pp.draw()
        fig.canvas.draw()

    print("Average FPS =\t%.6G" %(data.shape[0]/(time.time()-start)))

fakedata = np.random.randn(200,512,512)
animate_data(fakedata)
