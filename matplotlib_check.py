import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import os


def main():
    img1,img2='img/fig1.png','img/fig2.png'
    
    line_dashes_answ(img1)
    line_dashes(img2)    
    
    print(test_pyplot(img1,img2))



def line_dashes(path):
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), linestyle=(0, (3, 3)), lw=5)
    p,f=os.path.split(path)
    if not os.path.isdir(p):
        os.makedirs(p)
    plt.savefig(path)    



def line_dashes_answ(path):
    fig, ax = plt.subplots()
    ax.plot(0.5*np.arange(10), linestyle=(0, (3, 3)), lw=5)
    if not os.path.isdir(os.path.split(path)[0]):
        os.makedirs('img')
    plt.savefig(path)    
    return 

def test_pyplot(correct_plot,answer_plot):
    a=np.array(mpimg.imread(correct_plot).astype(float))
    b=np.array(mpimg.imread(answer_plot).astype(float))  
    #valid=np.all(a[:,:,0:1]==a[:,:,:3],2)==False#eliminates white/greys/black
    valid=np.all(a[:,:,:3]<1,2)#eliminate white
    return np.sum(np.all(a[valid]==b[valid],1))/np.sum(valid)


main()