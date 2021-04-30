import numpy as np
import matplotlib.image as mpimg


def test_pyplot(correct_plot,answer_plot):
    a=np.array(mpimg.imread(correct_plot).astype(float))
    b=np.array(mpimg.imread(answer_plot).astype(float))  
    #valid=np.all(a[:,:,0:1]==a[:,:,:3],2)==False#eliminates white/greys/black
    valid=np.all(a[:,:,:3]<1,2)#eliminate white
    return np.sum(np.all(a[valid]==b[valid],1))/np.sum(valid)
