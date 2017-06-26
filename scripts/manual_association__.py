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
class Manual_Associator:
    def __init__(self, src_name, dst_name):
        ''''''
        self.src_img = np.flipud( cv2.imread( src_name, cv2.IMREAD_GRAYSCALE) )
        self.dst_img = np.flipud( cv2.imread( dst_name, cv2.IMREAD_GRAYSCALE) )
        
        self.src_pts = []
        self.dst_pts = []
        
        self.src_pts_plt = []
        self.src_txt_plt = []
        
        self.dst_pts_plt = []
        self.dst_txt_plt = []        

        
        self.fig, self.axes = plt.subplots(1,2, figsize=(20,12))
        self.axes[0].imshow(self.src_img, cmap='gray', alpha=.7, interpolation='nearest', origin='lower')
        self.axes[0].set_label('src')
        self.axes[1].imshow(self.dst_img, cmap='gray', alpha=.7, interpolation='nearest', origin='lower')
        self.axes[1].set_label('dst')
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
            
            if event.inaxes._label == 'src':
                self.src_pts.append([x,y])
                self.src_pts_plt.append( self.axes[0].plot( x,y, 'ro')[0] )
                self.src_txt_plt.append( self.axes[0].text( x+10, y+10, str(len(self.src_pts)), fontdict={'color':'r',  'size': 10}) )

            elif event.inaxes._label == 'dst':
                self.dst_pts.append([x,y])
                self.dst_pts_plt.append( self.axes[1].plot( x,y, 'bo')[0] )
                self.dst_txt_plt.append( self.axes[1].text( x+10, y+10, str(len(self.dst_pts)), fontdict={'color':'b',  'size': 10}) )
            
        elif (event.button == 2) or (event.button == 3):
            # right-middle click: remove the last point (and corresponding drawing events)
            if event.inaxes._label == 'src':
                self.src_pts.pop(-1)
                self.src_pts_plt.pop(-1).remove()
                self.src_txt_plt.pop(-1).remove()
                
            elif event.inaxes._label == 'dst':
                self.dst_pts.pop(-1)
                self.dst_pts_plt.pop(-1).remove()
                self.dst_txt_plt.pop(-1).remove()
            
        assert len(self.src_pts) == len(self.src_pts_plt) == len(self.src_txt_plt)
        assert len(self.dst_pts) == len(self.dst_pts_plt) == len(self.dst_txt_plt)            
        plt.draw()

################################################################################
################################################################################
################################################################################
################################################################################
if __name__ == '__main__':
    '''    
    example
    -------
    python manual_association.py --img_src '../E5/E5_1.png' --img_dst '../E5/E5_layout.png'
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
    ma = Manual_Associator(img_src, img_dst)

    ###### save the result
    try:
        assert len(ma.src_pts) == len(ma.dst_pts)
        np.save(out_file_name, {'src_pts': ma.src_pts, 'dst_pts': ma.dst_pts})
    except:
        raise( NameError('Numbers of points in source and destination do not match') )






# dic = np.atleast_1d( np.load('fname') )[0]
# src_pts = np.array(dic['src_pts'])
# dst_pts = np.array(dic['dst_pts'])





################################################################################
############################################################### Functions' Lobby
################################################################################
# def on_click(event):

#     if event.button == 1:
#         # left click: adds a new point
#         [x, y] = [int(event.xdata), int(event.ydata)]
        
#         if event.inaxes._label == 'src':
#             src_pts.append([x,y])
#             src_pts_plt.append( axes[0].plot( x,y, 'ro')[0] )
#             src_txt_plt.append( axes[0].text( x+10, y+10, str(len(src_pts)), fontdict={'color':'r',  'size': 10}) )

            
#         elif event.inaxes._label == 'dst':
#             dst_pts.append([x,y])
#             dst_pts_plt.append( axes[1].plot( x,y, 'bo')[0] )
#             dst_txt_plt.append( axes[1].text( x+10, y+10, str(len(dst_pts)), fontdict={'color':'b',  'size': 10}) )
            
#     elif (event.button == 2) or (event.button == 3):
#         # right-middle click: remove the last point (and corresponding drawing events)
#         if event.inaxes._label == 'src':
#             src_pts.pop(-1)
#             src_pts_plt[-1].remove()
#             src_pts_plt.pop(-1)
#             src_txt_plt[-1].remove()
#             src_txt_plt.pop(-1)            
            
#         elif event.inaxes._label == 'dst':
#             dst_pts.pop(-1)
#             dst_pts_plt[-1].remove()
#             dst_pts_plt.pop(-1)
#             dst_txt_plt[-1].remove()
#             dst_txt_plt.pop(-1)
            
#     assert len(src_pts) == len(src_pts_plt) == len(src_txt_plt)
#     assert len(dst_pts) == len(dst_pts_plt) == len(dst_txt_plt)            
#     plt.draw()

# ################################################################################
# ############################################################### Development Yard
# ################################################################################
# src_name = '../E5/E5_1.png'
# dst_name = '../E5/E5_layout.png'

# src_img = np.flipud( cv2.imread( src_name, cv2.IMREAD_GRAYSCALE) )
# dst_img = np.flipud( cv2.imread( dst_name, cv2.IMREAD_GRAYSCALE) )

# src_pts = []
# dst_pts = []

# src_pts_plt = []
# src_txt_plt = []

# dst_pts_plt = []
# dst_txt_plt = []

# ################################################################################
# ########################################################## Visualization Gallery
# ################################################################################

# fig, axes = plt.subplots(1,2, figsize=(20,12))
# axes[0].imshow(src_img, cmap='gray', alpha=.7, interpolation='nearest', origin='lower')
# axes[0].set_label('src')
# axes[1].imshow(dst_img, cmap='gray', alpha=.7, interpolation='nearest', origin='lower')
# axes[1].set_label('dst')
# fig.canvas.mpl_connect('button_press_event', on_click)
# plt.tight_layout()
# plt.show()
