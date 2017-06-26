from __future__ import print_function

import sys

import cv2
import numpy as np
import matplotlib.pyplot as plt


################################################################################
def _extract_target_file_name(img_name):
    '''
    '''
    spl_ = img_name.split('/')
    if len(spl_)>1:
        # include the current directories name in the target file's name
        return 'kps_'+ spl_[-2]+ '_'+ spl_[-1][:-4]
    else:
        # only include the input files' name in the target file's name
        return 'kps_'+ spl_[-1][:-4] 

    

################################################################################
class KeyPoint_Select:
    ''''''
    def __init__(self, img_name):
        ''''''
        self.img = np.flipud( cv2.imread( img_name, cv2.IMREAD_GRAYSCALE) )
      
        self.pts = []        
        self.pts_plt = []
        
        self.fig, self.axes = plt.subplots(1,1, figsize=(20,12))
        self.axes.imshow(self.img, cmap='gray', alpha=1, interpolation='nearest', origin='lower')
        self.axes.set_title('select keypoints - it will save by closing this plot')

        self.fig.canvas.mpl_connect('button_press_event', self)
        plt.tight_layout()
        plt.show()
        
    def __call__(self, event):
        ''''''
        if (event.xdata is None) or (event.ydata is None):
            # if clicked out of axes
            return None
        
        if event.button == 1:
            # left click: adds a new point
            [x, y] = [int(event.xdata), int(event.ydata)]
            self.pts.append([x,y])
            self.pts_plt.append( self.axes.plot( x,y, 'r.')[0] )

            
        elif (event.button == 2) or (event.button == 3):
            # right-middle click: remove the last point (and corresponding drawing events)
            self.pts.pop(-1)
            self.pts_plt.pop(-1).remove()
            
        assert len(self.pts) == len(self.pts_plt)

        plt.draw()

################################################################################
################################################################################
################################################################################
################################################################################
if __name__ == '__main__':
    '''    
    example
    -------
    python select_keypoint_man.py --img_name '../E5/E5_1.png'
    '''    
    args = sys.argv

    # fetching parameters from input arguments
    # parameters are marked with double dash,
    # the value of a parameter is the next argument   
    listiterator = args[1:].__iter__()
    while 1:
        try:
            item = next( listiterator )
            if item[:2] == '--':
                exec(item[2:] + ' = next( listiterator )')
        except:
            break   

    # get the output file name
    out_file_name = _extract_target_file_name(img_name)

    # select keypoints
    kps = KeyPoint_Select(img_name)

    # save the result
    np.save(out_file_name, np.array(kps.pts))




# img_name = '../E5/E5_1.png'
# img_name_pts = _extract_target_file_name(img_name)+ '.npy'
# pts = np.atleast_1d( np.load(img_name_pts) )
# img = np.flipud( cv2.imread( img_name, cv2.IMREAD_GRAYSCALE) )
      
# fig, axes = plt.subplots(1,1, figsize=(20,12))
# axes.imshow(img, cmap='gray', alpha=1, interpolation='nearest', origin='lower')
# axes.plot(pts[:,0],pts[:,1], 'r.')
# plt.tight_layout()
# plt.show()

