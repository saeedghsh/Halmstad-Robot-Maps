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

import numpy as np
import PySide

# the address to the arrangement package is added to sys.path
# by the gui script that imports this library, so no need to do it again

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
matplotlib.rcParams['text.usetex']=True
matplotlib.rcParams['text.latex.unicode']=True
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg

################################################################################
################################################################################
################################################################################
class MyMplCanvas(FigureCanvasQTAgg):
    '''
    Ultimately, this is a QWidget (as well as a FigureCanvasQTAgg, etc.).
    I connect this to graphicsView in the ui
    '''

    ########################################
    def __init__(self, parent=None):#, width=5, height=4, dpi=100):
        ''' '''

        self.alpha = 1.0
        self.markers = [ 'r.','g.','b.','k.', # 0,1,2,3
                         'r,','g,','b,','k,', # 4,5,6,7
                         'ro','go','bo','ko', # 8,9,10,11
                         'r*','g*','b*','k*', # 12,13,14,15
                         'r^','g^','b^','k^',] # 16,17,18,19
        
        self.fig, self.axes = plt.subplots(1, 1)#, figsize=(20,12))#, sharex=True, sharey=True)
        self.axes.axis('off')
        plt.tight_layout(pad=0)

        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvasQTAgg.setSizePolicy(self, PySide.QtGui.QSizePolicy.Expanding, PySide.QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

        self.draw()

    ########################################
    def clear_axes(self):
        self.axes.cla()
        self.draw()

    ################################################################################
    def plot_image(self, image):
        '''
        '''
        self.axes.imshow(image, cmap = 'gray', interpolation='nearest', origin='lower')
        self.axes.axis('off')
        self.draw()

    ################################################################################
    def plot_points(self, points, marker_idx=0):
        ''' '''
        pts = np.array(points)
        self.axes.plot(pts[:,0],pts[:,1] , self.markers[marker_idx]) 
        self.draw()



################################################################################
################################################################################
################################################################################
class MyMplCanvas_sub_plots(FigureCanvasQTAgg):
    '''
    Ultimately, this is a QWidget (as well as a FigureCanvasQTAgg, etc.).
    I connect this to graphicsView in the ui
    '''

    ########################################
    def __init__(self, parent=None):#, width=5, height=4, dpi=100):
        ''' '''

        self.alpha = 1.0
        self.markers = [ 'r.','g.','b.','k.', # 0,1,2,3
                         'r,','g,','b,','k,', # 4,5,6,7
                         'ro','go','bo','ko', # 8,9,10,11
                         'r*','g*','b*','k*', # 12,13,14,15
                         'r^','g^','b^','k^',] # 16,17,18,19
        
        self.fig, self.axes = plt.subplots(1, 3)#, figsize=(20,12))#, sharex=True, sharey=True)
        for axis in self.axes: axis.axis('off')
        plt.tight_layout(pad=0)

        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvasQTAgg.setSizePolicy(self, PySide.QtGui.QSizePolicy.Expanding, PySide.QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

        self.draw()

    # ########################################
    # def clear_axis(self, axis_idx=None):
    #     ''''''
    #     if axis_idx is None:
    #         for axis self.axes: axis.cla()
    #     else:
    #         for idx in axis_idx: self.axes[idx].cla()
           
    #     self.draw()

    # ################################################################################
    # def plot_image(self, image, axis_idx):
    #     '''
    #     '''
    #     self.axes[axis_idx].imshow(image, cmap = 'gray', interpolation='nearest', origin='lower')
    #     self.draw()

    # ################################################################################
    # def plot_points(self, points, axis_idx, marker_idx=0):
    #     ''' '''
    #     pts = np.array(points)
    #     self.axes[axis_idx].plot(pts[:,0],pts[:,1] , self.markers[marker_idx]) 
    #     self.draw()
