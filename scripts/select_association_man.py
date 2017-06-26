from __future__ import print_function

import sys

import cv2
import numpy as np
import matplotlib.pyplot as plt


################################################################################
def _extract_target_file_name(img_src, img_dst, method=None):
    '''
    '''
    spl_src = img_src.split('/')
    spl_dst = img_dst.split('/')
    if len(spl_src)>1 and len(spl_dst)>1:
        # include the current directories name in the target file's name
        tmp = spl_src[-2]+'_'+spl_src[-1][:-4] + '__' + spl_dst[-2]+'_'+spl_dst[-1][:-4]
    else:
        # only include the input files' name in the target file's name
        tmp = spl_src[-1][:-4] + '__' + spl_dst[-1][:-4]

    return tmp if method is None else method+'_'+ tmp

################################################################################
def _extract_keypoint_file_name(img_name, path=''):
    '''
    if path is not provided, it is assumed the keypoint files are stored next to 
    the script, or whereever the script is called from
    '''
    spl_ = img_name.split('/')
    if len(spl_)>1:
        # include the current directories name in the target file's name
        return path+ 'kps_'+ spl_[-2]+ '_'+ spl_[-1][:-4] + '.npy'
    else:
        # only include the input files' name in the target file's name
        return path+ 'kps_'+ spl_[-1][:-4] + '.npy'

################################################################################
class Association_Select:
    def __init__(self, src_img_name, dst_img_name, path_2_keypoints=''):
        ''''''
        # load images
        self.src_img = np.flipud( cv2.imread( src_img_name, cv2.IMREAD_GRAYSCALE) )
        self.dst_img = np.flipud( cv2.imread( dst_img_name, cv2.IMREAD_GRAYSCALE) )

        # load key points
        src_kpt_file_name = _extract_keypoint_file_name(src_img_name, path_2_keypoints)
        dst_kpt_file_name = _extract_keypoint_file_name(dst_img_name, path_2_keypoints)
        
        self.src_pts = [tuple(pt) for pt in np.atleast_1d( np.load(src_kpt_file_name) )]
        self.dst_pts = [tuple(pt) for pt in np.atleast_1d( np.load(dst_kpt_file_name) )]

        # note:
        # the way I use pick_event is to read the label of an "artist" object (i.e. plotted points)
        # this label is the index of that point in two tuples self.src_pts_plt and self.src_pts
        # after associating two points I want them not be visible any more!
        # But I can not remove them from the tuple, otherwise that would mess up th indexig!
        # Hence the use of tuple instead of list
        
        self.src_pt_idx = None
        self.dst_pt_idx = None

        self.src_pt_marker = []
        self.dst_pt_marker = []
                
        self.associated_pairs_idx = [] # (src_pt_idx, dst_pt_idx)
        
        self.fig, self.axes = plt.subplots(1,2, figsize=(20,12))
        self.fig.suptitle('1)select a pair of points (l-click), 2)r-click on any point -> they will disappear (i.e. associated)')

        # plot images
        self.axes[0].imshow(self.src_img, cmap='gray', alpha=.7, interpolation='nearest', origin='lower')
        self.axes[0].set_label('src')
        self.axes[1].imshow(self.dst_img, cmap='gray', alpha=.7, interpolation='nearest', origin='lower')
        self.axes[1].set_label('dst')

        # plot key points
        self.src_pts_plt = []
        for p_idx,pt in enumerate(self.src_pts):
            self.src_pts_plt.append( self.axes[0].plot(pt[0], pt[1], 'ro', picker=10, label=str(p_idx))[0] )

        self.dst_pts_plt = []
        for p_idx,pt in enumerate(self.dst_pts):
            self.dst_pts_plt.append( self.axes[1].plot(pt[0], pt[1], 'ro', picker=10, label=str(p_idx))[0] )

        # connect canvas to call method
        self.fig.canvas.mpl_connect('pick_event', self)
        plt.tight_layout()
        plt.show()
        

    ########################################
    def __call__(self, event):
        ''''''
        if event.mouseevent.button == 1:
            # left click: adds a new point
            [x, y] = [int(event.mouseevent.xdata), int(event.mouseevent.ydata)]
            # print (event.mouseevent.inaxes._label, x,y)

            if event.mouseevent.inaxes._label == 'src':
                # print ('index to \'self.src_pts_plt\' and \'self.src_pts\' ', int(event.artist._label))
                self.src_pt_idx = int(event.artist._label)
                
                if len(self.src_pt_marker) > 0:
                    self.src_pt_marker[0].remove()

                self.src_pt_marker = self.axes[0].plot(self.src_pts[self.src_pt_idx][0],
                                                       self.src_pts[self.src_pt_idx][1],
                                                       'g*')

            elif event.mouseevent.inaxes._label == 'dst':
                # print ('index to \'self.dst_pts_plt\' and \'self.dst_pts\' ', int(event.artist._label))
                self.dst_pt_idx = int(event.artist._label)

                if len(self.dst_pt_marker)>0:
                    self.dst_pt_marker[0].remove()

                self.dst_pt_marker = self.axes[1].plot(self.dst_pts[self.dst_pt_idx][0],
                                                       self.dst_pts[self.dst_pt_idx][1],
                                                       'g*')

            
        elif (event.mouseevent.button == 2) or (event.mouseevent.button == 3):
            # right-middle click: 
            self.associated_pairs_idx.append( (self.src_pt_idx, self.dst_pt_idx) )
            self.src_pt_marker.pop().remove()
            self.src_pts_plt[self.src_pt_idx].remove() # dont pop! just remvoe from drawing!
            self.src_pt_idx = None

            self.dst_pt_marker.pop().remove()
            self.dst_pts_plt[self.dst_pt_idx].remove() # dont pop! just remvoe from drawing!
            self.dst_pt_idx = None

            assert len(self.src_pt_marker) == len(self.dst_pt_marker) == 0
        
        plt.draw()

################################################################################
################################################################################
################################################################################
################################################################################
if __name__ == '__main__':
    '''    
    example
    -------
    python select_association_man.py --img_src '../E5/E5_1.png' --img_dst '../E5/E5_layout.png'
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

    out_file_name = _extract_target_file_name(img_src, img_dst)
    ase = Association_Select(img_src, img_dst)

    ###### save the result
    np.save(out_file_name, ase.associated_pairs_idx)
    





