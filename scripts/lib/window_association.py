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

# this repo
import canvas_lib
import gui_association

#####################################################################
#####################################################################
#####################################################################
class MainWindow(PySide.QtGui.QMainWindow, gui_association.Ui_MainWindow):
    ''''''
    def __init__(self, parent=None):
        ''' '''
        super(MainWindow, self).__init__(parent)
        self.ui = gui_association.Ui_MainWindow()
        self.ui.setupUi(self)
        
        #####################################################################
        ############################## connecting graphicsViews to mpl canvas
        #####################################################################
        # src
        src_canvas = self.ui.graphicsView_src_map
        self.src_canvas = canvas_lib.MyMplCanvas(src_canvas)
        layout = PySide.QtGui.QVBoxLayout(src_canvas)
        layout.addWidget(self.src_canvas)
        self.src_canvas.mpl_connect('pick_event', self._src_mouse_click) 

        # dst
        dst_canvas = self.ui.graphicsView_dst_map
        self.dst_canvas = canvas_lib.MyMplCanvas(dst_canvas)
        layout = PySide.QtGui.QVBoxLayout(dst_canvas)
        layout.addWidget(self.dst_canvas)
        self.dst_canvas.mpl_connect('pick_event', self._dst_mouse_click) 

        #####################################################################
        #####################################################################
        #####################################################################

        ### src stuff
        # self.ui.graphicsView_src_map
        # self.ui.textEdit_src_path
        self.ui.pushButton_src_load_map.clicked.connect(self._get_src_file_name)
        self.ui.pushButton_src_next.clicked.connect(self._src_next)
        self.ui.pushButton_src_previous.clicked.connect(self._src_previous)

        ### dst stuff
        # self.ui.graphicsView_dst_map
        # self.ui.textEdit_dst_path
        self.ui.pushButton_dst_load_map.clicked.connect(self._get_dst_file_name)
        self.ui.pushButton_dst_next.clicked.connect(self._dst_next)
        self.ui.pushButton_dst_previous.clicked.connect(self._dst_previous)
        
        ### ctrl
        # self.ui.checkBox_association_exists
        # self.ui.checkBox_show_association
        self.ui.checkBox_save_with_nxt_prv.toggled.connect(self._print_save_warning)
        self.ui.pushButton_reset.clicked.connect(self._reset)
        self.ui.pushButton_save.clicked.connect(self._save)

        ### info
        self.ui.pushButton_about.clicked.connect(self._about)
        self.ui.pushButton_instructions.clicked.connect(self._instructions)

        #####################################################################
        #####################################################################
        #####################################################################

        # setting to None, so when both src and dst are selected
        # check for the existence of association file
        self.src_current_file_idx, self.dst_current_file_idx = None, None

        # idx to selected point in each set
        self.src_pt_idx = None
        self.dst_pt_idx = None

        # markers are to highlight selected point
        self.src_pt_marker = []
        self.dst_pt_marker = []

        # a list of indices to paired key points
        self.associated_pairs_idx = [] # (src_pt_idx, dst_pt_idx)

        # make a dir for saving association results
        self.results_path = os.getcwd()+'/../annotations/'
        if not( os.path.isdir( self.results_path ) ):
            os.system( 'mkdir {:s}'.format(self.results_path) )

        # self._instructions()


    ################################################################################ 
    ########################################################### methods of the class
    ################################################################################ 

    ################################################################################ generic
    def _get_file_name(self):
        ''''''
        # trigger pop-up to select a file
        file_path_name = PySide.QtGui.QFileDialog.getOpenFileName()[0]

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
            key_pts = [list(pt) for pt in np.load(self.results_path+keypoint_name)]
        else:
            key_pts = []

        # both images are selected and already selected
        # check for the existence of the association files
        association_exists = False
        if (self.src_current_file_idx is not None) and (self.dst_current_file_idx is not None):
            src_name = self.src_file_list[ self.src_current_file_idx ]
            dst_name = self.dst_file_list[ self.dst_current_file_idx ]
            association_name = 'association_'+src_name[:-4]+'_'+dst_name[:-4]+'.npy'
            association_exists = association_name in os.listdir(self.results_path)
            self.ui.checkBox_association_exists.setChecked(association_exists)

        if association_exists:
            self.associated_pairs_idx = [ [src_idx, dst_idx]
                                          for src_idx,dst_idx in np.load(self.results_path+association_name)
                                          if src_idx is not None and  dst_idx is not None ]            
        else:
            self.associated_pairs_idx = []


        return image, key_pts
        
    ######################################## generic
    def _plot_image_pts(self, canvas, image, points):
        ''''''
        # clear canvas
        canvas.clear_axes()

        # plot image
        canvas.axes.imshow(image, cmap='gray', alpha=1., interpolation='nearest', origin='lower')
        canvas.axes.axis('off')

        # plot key points - pts_plt is a list of plot object
        pts_plt = [ canvas.axes.plot(pt[0], pt[1], 'ro', picker=10, label=str(p_idx))[0]
                    for p_idx,pt in enumerate(points) ]

        canvas.draw()

        return canvas, pts_plt

    ######################################## generic
    def _mouse_left_click(self, event, canvas, points, pt_marker):
        ''' left click: select and mark a new point '''
 
        ### fetch the index of the selected key point
        pt_idx = int(event.artist._label)
        
        ### mark selected point
        # if a point is already marked, delete it
        if len(pt_marker) > 0: pt_marker[0].remove()
        pt_marker = canvas.axes.plot(points[pt_idx][0], points[pt_idx][1], 'g*')

        canvas.draw()

        return pt_marker, canvas, pt_idx

    ######################################## generic
    def _change_kp_appreance(self, plt_obj):
        # plt_obj.remove()
        plt_obj.set_picker(0) # this point won't be pickable anymore
        plt_obj.set_color('b')
        plt_obj.set_alpha(0.7)
        # plt_obj.set_marker('*')

    ######################################## generic
    def _mouse_right_click(self):
        ''' right-middle click: establish association '''

        # add new pair to association list
        self.associated_pairs_idx.append( (self.src_pt_idx, self.dst_pt_idx) )

        # remove original and marker on the selected point in the src image
        self.src_pt_marker.pop().remove()
        # self.src_pts_plt[self.src_pt_idx].remove() # dont pop! just remvoe from drawing!
        self._change_kp_appreance(self.src_pts_plt[self.src_pt_idx])
        self.src_pt_idx = None

        # remove original and marker on the selected point in the dst image
        self.dst_pt_marker.pop().remove()
        # self.dst_pts_plt[self.dst_pt_idx].remove() # dont pop! just remvoe from drawing!
        self._change_kp_appreance(self.dst_pts_plt[self.dst_pt_idx])
        self.dst_pt_idx = None

        assert len(self.src_pt_marker) == len(self.dst_pt_marker) == 0

        # print ( self.associated_pairs_idx )

        self.src_canvas.draw()
        self.dst_canvas.draw()

    ########################################
    def _save(self):
        ''''''
        if len(self.associated_pairs_idx)>0:
            src_name = self.src_file_list[ self.src_current_file_idx ]
            dst_name = self.dst_file_list[ self.dst_current_file_idx ]
            # from source to destination
            association_name = 'association_'+src_name[:-4]+'_'+dst_name[:-4]+'.npy'
            np.save(self.results_path+association_name, self.associated_pairs_idx)
            # from destination to source
            association_name = 'association_'+dst_name[:-4]+'_'+src_name[:-4]+'.npy'
            np.save(self.results_path+association_name, np.roll( self.associated_pairs_idx,1, axis=1) )

    ########################################
    def _reset(self):
        ''''''
        self.associated_pairs_idx = []
        self.src_canvas, self.src_pts_plt = self._plot_image_pts( self.src_canvas, self.src_image, self.src_key_pts )
        self.dst_canvas, self.dst_pts_plt = self._plot_image_pts( self.dst_canvas, self.dst_image, self.dst_key_pts )

    ################################################################################ Source stuff

    ########################################
    def _setup_src(self):
        ''''''
        # set the name in the textEdit
        self.ui.textEdit_src_path.setText( self.src_file_path + self.src_file_list[ self.src_current_file_idx ] )

        # loading file
        self.src_image, self.src_key_pts = self._load_files(self.src_file_path, self.src_file_list, self.src_current_file_idx)

        # plotting image and key points and receiving back the list of plot objects
        self.src_canvas, self.src_pts_plt = self._plot_image_pts( self.src_canvas, self.src_image, self.src_key_pts )

        # mark associated points - this would only happen if both are loaded and drawn
        if len(self.associated_pairs_idx) > 0:
            for src_pt_idx, dst_pt_idx in self.associated_pairs_idx:
                self._change_kp_appreance(self.src_pts_plt[src_pt_idx])
                self._change_kp_appreance(self.dst_pts_plt[dst_pt_idx])
            
            self.src_canvas.draw()
            self.dst_canvas.draw()


    ########################################
    def _get_src_file_name(self):
        ''''''
        # load file path, list of files, and the index to the selected file
        res = self._get_file_name()
        if res is None: return None
        self.src_file_path, self.src_file_list, self.src_current_file_idx = res

        # set the name in the textEdit, loading file, plotting
        self._setup_src()

    ########################################
    def _src_mouse_click(self, event):
        ''''''
        # print ('src_ this is easy!')
        if event.mouseevent.button == 1:
            can, k_pts, pt_mkr = self.src_canvas, self.src_key_pts, self.src_pt_marker
            self.src_pt_marker, self.src_canvas, self.src_pt_idx = self._mouse_left_click(event, can, k_pts, pt_mkr)

        elif (event.mouseevent.button == 2) or (event.mouseevent.button == 3):
            self._mouse_right_click()

    ######################################## Source stuff
    def _src_next(self):
        ''''''
        # save key points befor moving to another image
        if self.ui.checkBox_save_with_nxt_prv.isChecked(): self._save()
        self.associated_pairs_idx = []

        # increment the current file idx
        self.src_current_file_idx = (self.src_current_file_idx+1) % len(self.src_file_list)

        # set the name in the textEdit, loading file, plotting
        self._setup_src()
        self._setup_dst() # just for the sake of reseting the drawing

    ########################################
    def _src_previous(self):
        ''''''
        # save key points befor moving to another image
        if self.ui.checkBox_save_with_nxt_prv.isChecked(): self._save()
        self.associated_pairs_idx = []

        # decrement the current file idx
        self.src_current_file_idx = (self.src_current_file_idx-1) % len(self.src_file_list)

        # set the name in the textEdit, loading file, plotting
        self._setup_src()
        self._setup_dst()  # just for the sake of reseting the drawing

    ################################################################################ Destination stuff

    ########################################
    def _setup_dst(self):
        ''''''
        # set the name in the textEdit
        self.ui.textEdit_dst_path.setText( self.dst_file_path + self.dst_file_list[ self.dst_current_file_idx ] )

        # loading file
        self.dst_image, self.dst_key_pts = self._load_files(self.dst_file_path, self.dst_file_list, self.dst_current_file_idx)

        # plotting image and key points and receiving back the list of plot objects
        self.dst_canvas, self.dst_pts_plt = self._plot_image_pts( self.dst_canvas, self.dst_image, self.dst_key_pts )

        # mark associated points - this would only happen if both are loaded and drawn
        if len(self.associated_pairs_idx) > 0:
            for src_pt_idx, dst_pt_idx in self.associated_pairs_idx:
                self._change_kp_appreance(self.src_pts_plt[src_pt_idx])
                self._change_kp_appreance(self.dst_pts_plt[dst_pt_idx])
            self.src_canvas.draw()
            self.dst_canvas.draw()

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
    def _dst_mouse_click(self, event):
        ''''''
        # print ('src_ this is easy!')
        if event.mouseevent.button == 1:
            can, k_pts, pt_mkr = self.dst_canvas, self.dst_key_pts, self.dst_pt_marker
            self.dst_pt_marker, self.dst_canvas, self.dst_pt_idx = self._mouse_left_click(event, can, k_pts, pt_mkr)

        elif (event.mouseevent.button == 2) or (event.mouseevent.button == 3):
            self._mouse_right_click()

    ########################################
    def _dst_next(self):
        ''''''
        # save key points befor moving to another image
        if self.ui.checkBox_save_with_nxt_prv.isChecked(): self._save()
        self.associated_pairs_idx = []

        # increment the current file idx
        self.dst_current_file_idx = (self.dst_current_file_idx+1) % len(self.dst_file_list)

        # set the name in the textEdit, loading file, plotting
        self._setup_dst()
        self._setup_src() # just for the sake of reseting the drawing

    ########################################
    def _dst_previous(self):
        ''''''
        # save key points befor moving to another image
        if self.ui.checkBox_save_with_nxt_prv.isChecked(): self._save()
        self.associated_pairs_idx = []

        # decrement the current file idx
        self.dst_current_file_idx = (self.dst_current_file_idx-1) % len(self.dst_file_list)

        # set the name in the textEdit, loading file, plotting
        self._setup_dst()
        self._setup_src() # just for the sake of reseting the drawing

    #########################################################################
    #################################################################### MISC
    #########################################################################
    def _print_save_warning(self):
        if not( self.ui.checkBox_save_with_nxt_prv.isChecked() ):
            warning = '''
            *** Warning ***
            By unchecking this option you will have to save manually.
            When you are done with a pair of images you have to save,
            the result by using the "save" button. Otherwise, check
            this box and by using the "next" and "previous" buttons
            the results will be saved automatically.
            '''
            PySide.QtGui.QMessageBox.about(self, 'warning', warning)

    ########################################
    def dummy(self, event=None):
        print ( 'dummy is called...' )

    ########################################
    def _instructions(self):
        instructions = '''
        left-click near a key point to select, it will be marked green.
        left-click near the corresponding key point in the other map.
        right-click* to pair selected points.
        points that are alreay associated will turn blue.
        
        * NOTE
        since "pick_event" is used to select points, a click is only
        registered if it is near a point, even the right-click which
        its location does not matter...
        '''
        PySide.QtGui.QMessageBox.about(self, 'instructions', instructions)
    
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
