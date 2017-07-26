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
import gui_keypoint


#####################################################################
#####################################################################
#####################################################################

class MainWindow(PySide.QtGui.QMainWindow, gui_keypoint.Ui_MainWindow):
    
    def __init__(self, parent=None):
        ''' '''
        super(MainWindow, self).__init__(parent)
        self.ui = gui_keypoint.Ui_MainWindow()
        self.ui.setupUi(self)

        #####################################################################
        ############################## connecting graphicsViews to mpl canvas
        #####################################################################
        map_canvas = self.ui.graphicsView_map
        self.map_canvas = canvas_lib.MyMplCanvas(map_canvas)
        layout = PySide.QtGui.QVBoxLayout(map_canvas)
        layout.addWidget(self.map_canvas)
        self.map_canvas.mpl_connect('button_press_event', self._mouse_click)

        #####################################################################
        #####################################################################
        #####################################################################
        self.ui.pushButton_load_map.clicked.connect(self._get_file_name)
        self.ui.pushButton_next.clicked.connect(self._next)
        self.ui.pushButton_previous.clicked.connect(self._previous)
        self.ui.pushButton_save.clicked.connect(self._save)
        self.ui.checkBox_save_with_nxt_prv.toggled.connect(self._print_save_warning)


    #########################################################################
    #################################################### methods of the class
    #########################################################################
    def _get_file_name(self):
        ''''''
        # trigger pop-up to select a file
        file_path_name = PySide.QtGui.QFileDialog.getOpenFileName()[0]

        # extract file path and file name
        spl = file_path_name.split('/')
        self.file_path = '/'.join(spl[:-1])+'/'

        # get a list of other png files in the same dir
        self.file_list = [fn for fn in os.listdir(self.file_path) if fn[-3:]=='png']
        if len( self.file_list ) == 0:
            print ('\t *** WARNING: I could not find any png file in the current path ***')
            return None
        self.file_list.sort()

        # get the index of the current file and set the text
        self.current_file_idx = self.file_list.index( spl[-1] ) if spl[-1][-3:] == 'png' else 0
        self.ui.textEdit_file_path.setText(self.file_path + self.file_list[ self.current_file_idx ])

        # note that the path-name to current file is always given by:
        # self.file_path + self.file_list[ self.current_file_idx ]
        
        self._load_files()
        self._plot_image_pts()

    ########################################
    def _load_files(self):
        ''''''
        # load image
        image_name = self.file_list[ self.current_file_idx ]
        self.image = np.flipud( cv2.imread( self.file_path + image_name, cv2.IMREAD_GRAYSCALE) )

        # check if a key_point_file already exists, if so load from file
        if image_name[:-3]+'npy' in os.listdir(self.file_path):
            self.key_pts = [list(pt) for pt in np.load(self.file_path+image_name[:-3]+'npy')]
        else:
            self.key_pts = []

    ########################################
    def _plot_image_pts(self):
        ''''''
        # clear canvas - because I lazily use this method for both:
        # 1) initial plot, and
        # 2) redraw everthing after removing last point (instead of removing the plot object)
        self.map_canvas.clear_axes()
        # plot image
        self.map_canvas.plot_image(self.image)
        # plot points if exists
        if len( self.key_pts ) >0 :
            self.map_canvas.plot_points(self.key_pts, marker_idx=0)
        
    ########################################
    def _next(self):
        ''''''
        
        # save key points befor moving to another image
        if self.ui.checkBox_save_with_nxt_prv.isChecked(): self._save()

        # increment the current file idx
        self.current_file_idx = (self.current_file_idx+1) % len(self.file_list)
        self.ui.textEdit_file_path.setText(self.file_path + self.file_list[ self.current_file_idx ])

        # load files, clear canvas and plot new stuff
        self._load_files()
        self._plot_image_pts()

    ########################################
    def _previous(self):
        ''''''

        # save key points befor moving to another image
        if self.ui.checkBox_save_with_nxt_prv.isChecked(): self._save()

        # decrement the current file idx
        self.current_file_idx = (self.current_file_idx-1) % len(self.file_list)
        self.ui.textEdit_file_path.setText(self.file_path + self.file_list[ self.current_file_idx ])

        # load files, clear canvas and plot new stuff
        self._load_files()
        self._plot_image_pts()


    ########################################
    def _save(self):
        ''''''
        if len(self.key_pts)>0:
            image_name = self.file_list[ self.current_file_idx ]
            np.save(self.file_path+image_name[:-3]+'npy', self.key_pts)

    ########################################
    def _mouse_click(self, event):
        ''''''
        if (event.xdata is None) or (event.ydata is None):
            # if clicked out of axes
            return None            

        if event.button == 1:
            self.key_pts.append([event.xdata, event.ydata])
            self.map_canvas.plot_points([[event.xdata, event.ydata]], marker_idx=0)
        
        elif event.button == 3 and len(self.key_pts)>0:
            self.key_pts.pop(-1)
            self._plot_image_pts()
        
    ########################################
            


    #########################################################################
    #################################################################### MISC
    #########################################################################
    def _print_save_warning(self):
        if not( self.ui.checkBox_save_with_nxt_prv.isChecked() ):
            print ('\t *** Warning: by unchecking this option you have to save manually ***')

    ########################################
    def dummy(self, event=None):
        print ( 'dummy is called...' )
        
    ########################################
    def about(self):
        PySide.QtGui.QMessageBox.about(self, "xxx",
                                       """<b>Version</b> %s
                                       <p>Copyright &copy; 2017 Saeed Gholami Shahbandi.
                                       All rights reserved in accordance with GNU license
                                       <p>This GUI ... 
                                       <p>Python %s - PySide version %s - Qt version %s on %s""" % (__version__,
                                                                                                    platform.python_version(), PySide.__version__, QtCore.__version__,
                                                                                                    platform.system()))
