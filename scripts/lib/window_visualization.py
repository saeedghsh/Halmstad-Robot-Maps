'''
Copyright (C) 2017 Saeed Gholami Shahbandi. All rights reserved.

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License
as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this program. If not, see
<http://www.gnu.org/licenses/>
'''

from __future__ import print_function

import sys, os, platform, time
import cv2
import PySide

import numpy as np
import matplotlib
import matplotlib.transforms
import skimage.transform

# this repo
import canvas_lib
import gui_visualization

#####################################################################
#####################################################################
#####################################################################
class MainWindow(PySide.QtGui.QMainWindow, gui_visualization.Ui_MainWindow):
    ''''''
    def __init__(self, parent=None):
        ''' '''
        super(MainWindow, self).__init__(parent)
        self.ui = gui_visualization.Ui_MainWindow()
        self.ui.setupUi(self)
        
        #####################################################################
        ############################## connecting graphicsViews to mpl canvas
        #####################################################################
        main_canvas = self.ui.graphicsView_main
        self.main_canvas = canvas_lib.MyMplCanvas_sub_plots(main_canvas)
        layout = PySide.QtGui.QVBoxLayout(main_canvas)
        layout.addWidget(self.main_canvas)

        #####################################################################
        #####################################################################
        #####################################################################
        # self.ui.graphicsView_main

        # self.ui.textEdit_src_path
        self.ui.pushButton_src_load.clicked.connect(self._get_src_file_name)
        self.ui.pushButton_src_next.clicked.connect(self._src_next)
        self.ui.pushButton_src_previous.clicked.connect(self._src_previous)

        # self.ui.textEdit_dst_path
        self.ui.pushButton_dst_load.clicked.connect(self._get_dst_file_name)
        self.ui.pushButton_dst_next.clicked.connect(self._dst_next)
        self.ui.pushButton_dst_previous.clicked.connect(self._dst_previous)


        # plot keypoints and association anyway, with toggle change visibility
        self.ui.checkBox_show_association.toggled.connect(self._set_visibility)
        self.ui.checkBox_show_keypoints.toggled.connect(self._set_visibility)
        self.ui.comboBox_tform_type.currentIndexChanged.connect(self._plot_overlay)
        # self.ui.textEdit_tform_frw
        # self.ui.textEdit_tform_inv

        #####################################################################
        #####################################################################
        #####################################################################

        # setting to None, so when both src and dst are selected
        # check for the existence of association file
        self.src_current_file_idx, self.dst_current_file_idx = None, None
        self.src_pts_plt, self.dst_pts_plt = [], []
        
        # address to result files, ie keypoints and associations
        self.results_path = os.getcwd()+'/../keypoints_associations/'
    

    ################################################################################ 
    ########################################################### methods of the class
    ################################################################################ 

    ################################################################################ generic
    def _get_file_name(self):
        ''''''
        # trigger pop-up to select a file
        dir_suggestion = '/home/saesha/Dropbox/myGits/Halmstad-Robot-Maps/HIH/pseudo_occupancy'
        file_path_name = PySide.QtGui.QFileDialog.getOpenFileName(None, 'Open File', dir_suggestion)[0]
        # file_path_name = PySide.QtGui.QFileDialog.getOpenFileName()[0]

        # extract file path
        spl = file_path_name.split('/')
        file_path = '/'.join(spl[:-1])+'/'

        # get a list of other png files in the same dir
        file_list = [fn for fn in os.listdir(file_path) if fn[-3:]=='png']
        if len( file_list ) == 0:
            print ('\t *** WARNING: I could not find any png file in the current path ***')
            return None
        file_list.sort()

        # get the index of the current file and set the text
        current_file_idx = file_list.index( spl[-1] ) if spl[-1][-3:] == 'png' else 0

        ### NOTE that the path-name to current file is always given by:
        # file_path + file_list[ current_file_idx ]

        return file_path, file_list, current_file_idx

    ######################################## generic
    def _load_files(self, file_path, file_list, current_file_idx):
        ''''''
        # load image
        image = np.flipud( cv2.imread( file_path + file_list[current_file_idx], cv2.IMREAD_GRAYSCALE) )

        # check if a key_point_file already exists, if so load from file
        keypoint_name = 'keypoints_'+file_list[ current_file_idx ][:-3]+'npy'

        if keypoint_name in os.listdir(self.results_path):
            key_pts = np.load(self.results_path+keypoint_name)
        else:
            key_pts = np.array([])# []


        # if both images are selected and already selected
        # check for the existence of the association file
        association_exists = False
        if (self.src_current_file_idx is not None) and (self.dst_current_file_idx is not None):
            src_name = self.src_file_list[ self.src_current_file_idx ]
            dst_name = self.dst_file_list[ self.dst_current_file_idx ]
            association_name = 'association_'+src_name[:-4]+'_'+dst_name[:-4]+'.npy'
            association_exists = association_name in os.listdir(self.results_path)
            
        if association_exists:
            self.associated_pairs_idx = np.load(self.results_path+association_name)
        else:
            self.associated_pairs_idx = np.array([])
        self.associated_plt = []

        return image, key_pts
        

    ######################################## generic
    def _plot_overlay(self):
        ''''''
        self.main_canvas.axes[2].cla()

        if (self.associated_pairs_idx is not None) and (self.associated_pairs_idx.shape[0]>3) :
            ### estimate transformation
            src_idx, dst_idx = self.associated_pairs_idx[:,0], self.associated_pairs_idx[:,1]
            src_pts, dst_pts = self.src_key_pts[src_idx,:], self.dst_key_pts[dst_idx,:]

            tform_type = self.ui.comboBox_tform_type.currentText()
            tform = skimage.transform.estimate_transform( tform_type, src_pts, dst_pts )

            # the rest of this method does not work with for 'piecewise-affine' and 'polynomial'
            # for these two cases, I only print the matrices now, later check out this guy:
            # http://scikit-image.org/docs/0.12.x/api/skimage.transform.html#skimage.transform.warp

            if tform_type == 'piecewise-affine':
                frw_str = '**** totally {:d} matrices'.format(len(tform.affines))
                frw_str += '\n--------------------------'
                for m_idx, affine in enumerate(tform.affines):
                    frw_str += '\n * matrix {:d} \n'.format(m_idx)
                    frw_str += '\n'.join(['|{:.5f}, {:.5f}, {:.5f}|'.format(a,b,c) for a,b,c in affine.params])
                    frw_str += '\n--------------------------\n'

                inv_str = '**** totally {:d} matrices'.format(len(tform.inverse_affines))
                inv_str += '\n--------------------------'
                for m_idx, affine in enumerate(tform.inverse_affines):
                    inv_str += '\n * matrix {:d} \n'.format(m_idx)
                    inv_str += '\n'.join(['|{:.5f}, {:.5f}, {:.5f}|'.format(a,b,c) for a,b,c in affine.params])
                    inv_str += '\n--------------------------\n'

                self.ui.textEdit_tform_frw.setText( frw_str )
                self.ui.textEdit_tform_inv.setText( inv_str )
                self.main_canvas.draw()
                return 

            
            if tform_type == 'polynomial':
                frw_str = '\n'.join(['|{:.5f}, {:.5f}, {:.5f},\n {:.5f}, {:.5f}, {:.5f}|'.format(a,b,c,d,e,f)
                                     for a,b,c,d,e,f in tform.params])
                inv_str = ' "Polynomial Transform" does not have inverse matrix'

                self.ui.textEdit_tform_frw.setText( frw_str )
                self.ui.textEdit_tform_inv.setText( inv_str )
                self.main_canvas.draw()
                return 


            # print the forward and inverse transformation matrices
            frw_str = '\n'.join(['|{:.5f}, {:.5f}, {:.5f}|'.format(a,b,c) for a,b,c in tform.params])
            inv_str = '\n'.join(['|{:.5f}, {:.5f}, {:.5f}|'.format(a,b,c) for a,b,c in tform._inv_matrix])
            self.ui.textEdit_tform_frw.setText( frw_str )
            self.ui.textEdit_tform_inv.setText( inv_str )

            ### drawing images and transforming src image
            aff2d = matplotlib.transforms.Affine2D( tform.params )
            im_dst = self.main_canvas.axes[2].imshow(self.dst_image, origin='lower', cmap='gray', alpha=.5, clip_on=True)
            im_src = self.main_canvas.axes[2].imshow(self.src_image, origin='lower', cmap='gray', alpha=.5, clip_on=True)
            im_src.set_transform( aff2d + self.main_canvas.axes[2].transData )

            # finding the extent of of dst and transformed src
            xmin_d,xmax_d, ymin_d,ymax_d = im_dst.get_extent()
            x1, x2, y1, y2 = im_src.get_extent()
            pts = [[x1,y1], [x2,y1], [x2,y2], [x1,y2]]
            pts_tfrom = aff2d.transform(pts)
            
            xmin_s, xmax_s = np.min(pts_tfrom[:,0]), np.max(pts_tfrom[:,0]) 
            ymin_s, ymax_s = np.min(pts_tfrom[:,1]), np.max(pts_tfrom[:,1])

            # setting the limits of axis to the extents of images
            self.main_canvas.axes[2].set_xlim( min(xmin_s,xmin_d), max(xmax_s,xmax_d) )
            self.main_canvas.axes[2].set_ylim( min(ymin_s,ymin_d), max(ymax_s,ymax_d) )

        self.main_canvas.draw()

    ######################################## generic
    def _plot_image_pts(self):
        ''''''

        # clear all axis, figure line (associations), matrix prints
        for axis in self.main_canvas.axes: axis.cla()
        self.main_canvas.fig.lines = []
        self.ui.textEdit_tform_frw.setText( '' )
        self.ui.textEdit_tform_inv.setText( '' )

        # check who is ready to be plotted
        src_loaded = self.src_current_file_idx is not None
        dst_loaded = self.dst_current_file_idx is not None

        if src_loaded:
            self.main_canvas.axes[0].imshow(self.src_image, cmap = 'gray', interpolation='nearest', origin='lower')
            self.src_pts_plt = [ self.main_canvas.axes[0].plot(pt[0], pt[1], 'r.')[0]
                                 for pt in self.src_key_pts ]

        if dst_loaded:
            self.main_canvas.axes[1].imshow(self.dst_image, cmap = 'gray', interpolation='nearest', origin='lower')
            self.dst_pts_plt = [ self.main_canvas.axes[1].plot(pt[0], pt[1], 'r.')[0]
                                 for pt in self.dst_key_pts ]

        # this method won't be called before "_load_files", so self.associated_pairs_idx
        # must be already declared, either empty, or not!
        self.associated_plt = []
        if src_loaded and dst_loaded and (self.associated_pairs_idx.shape[0]>0):

            # step 1: plot the overlay in the axis[2]
            self._plot_overlay()

            # step 2: plot the association with lines across subplots
            # fetch associated points 
            src_idx, dst_idx = self.associated_pairs_idx[:,0], self.associated_pairs_idx[:,1]
            src_pts, dst_pts = self.src_key_pts[src_idx,:], self.dst_key_pts[dst_idx,:]

            fig_tform = self.main_canvas.fig.transFigure.inverted()
            lines = []

            pts_src_in_fig = fig_tform.transform(self.main_canvas.axes[0].transData.transform(src_pts))
            pts_dst_in_fig = fig_tform.transform(self.main_canvas.axes[1].transData.transform(dst_pts))

            for pt_s, pt_d in zip(pts_src_in_fig, pts_dst_in_fig):
                self.associated_plt.append( matplotlib.lines.Line2D((pt_s[0], pt_d[0]), (pt_s[1], pt_d[1]),
                                                                    transform=self.main_canvas.fig.transFigure,
                                                                    color='r', linestyle='--') )
            self.main_canvas.fig.lines = self.associated_plt

        # set visibility - "self.main_canvas.draw()" will be called inside the _set_visibility method
        self._set_visibility()

    ######################################## generic
    def _set_visibility(self, ):
        ''''''
        # set visibility of association lines
        for l in self.associated_plt:
            l.set_visible( self.ui.checkBox_show_association.isChecked() )

        # set visibility of keypoints
        for p in self.src_pts_plt + self.dst_pts_plt:
            p.set_visible( self.ui.checkBox_show_keypoints.isChecked() )

        self.main_canvas.draw()
                
    ################################################################################ Source stuff
    def _setup_src(self):
        ''''''
        # set the name in the textEdit
        self.ui.textEdit_src_path.setText( self.src_file_path + self.src_file_list[ self.src_current_file_idx ] )

        # loading file
        self.src_image, self.src_key_pts = self._load_files(self.src_file_path, self.src_file_list, self.src_current_file_idx)

        # plotting image and key points and receiving back the list of plot objects
        self._plot_image_pts()


    ########################################
    def _get_src_file_name(self):
        ''''''
        # load file path, list of files, and the index to the selected file
        res = self._get_file_name()
        if res is None: return None
        self.src_file_path, self.src_file_list, self.src_current_file_idx = res

        # set the name in the textEdit, loading file, plotting        
        self._setup_src()

    ######################################## Source stuff
    def _src_next(self):
        ''''''
        # increment the current file idx
        self.src_current_file_idx = (self.src_current_file_idx+1) % len(self.src_file_list)

        # set the name in the textEdit, loading file, plotting        
        self._setup_src()


    ########################################
    def _src_previous(self):
        ''''''
        # decrement the current file idx
        self.src_current_file_idx = (self.src_current_file_idx-1) % len(self.src_file_list)

        # set the name in the textEdit, loading file, plotting        
        self._setup_src()


    ################################################################################ Destination stuff
    def _setup_dst(self):
        ''''''
        # set the name in the textEdit
        self.ui.textEdit_dst_path.setText( self.dst_file_path + self.dst_file_list[ self.dst_current_file_idx ] )

        # loading file
        self.dst_image, self.dst_key_pts = self._load_files(self.dst_file_path, self.dst_file_list, self.dst_current_file_idx)

        # plotting image and key points and receiving back the list of plot objects
        self._plot_image_pts()

    ########################################
    def _get_dst_file_name(self):
        ''''''
        # load file path, list of files, and the index to the selected file
        res = self._get_file_name()
        if res is None: return None
        self.dst_file_path, self.dst_file_list, self.dst_current_file_idx = res

        # set the name in the textEdit, loading file, plotting        
        self._setup_dst()

    ########################################
    def _dst_next(self):
        ''''''
        # increment the current file idx
        self.dst_current_file_idx = (self.dst_current_file_idx+1) % len(self.dst_file_list)

        # set the name in the textEdit, loading file, plotting        
        self._setup_dst()

    ########################################
    def _dst_previous(self):
        ''''''
        # decrement the current file idx
        self.dst_current_file_idx = (self.dst_current_file_idx-1) % len(self.dst_file_list)

        # set the name in the textEdit, loading file, plotting        
        self._setup_dst()

    #########################################################################
    #################################################################### MISC
    #########################################################################
    ########################################
    def _dummy(self, event=None):
        print ( 'dummy is called...' )
    
    ########################################
    def _about(self):
        __version__ = .1
        about = '''
        Version {:s}
        Copyright (c) 2017 Saeed Gholami Shahbandi.
        All rights reserved in accordance with GNU license

        Python {:s} - PySide version {:s} - Qt version {:s} on {:s}
        '''.format( str(__version__),
                    platform.python_version(),
                    PySide.__version__,
                    PySide.QtCore.__version__,
                    platform.system() )

        PySide.QtGui.QMessageBox.about(self, "xxx", about)
