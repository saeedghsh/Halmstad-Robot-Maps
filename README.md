A Data-set Of 3D Meshes And 2D Occupancy Map
-------------------------------------------
A collection layout maps and sensor maps of different environments.
This repository of maps has been collected for the verification of methods presented in the following publications.
- Saeed Gholami Shahbandi, Martin Magnusson, *2D Map Alignment With Region Decomposition*, CoRR, abs/1709.00309, 2017. [URL](https://arxiv.org/abs/1709.00309)([code](https://github.com/saeedghsh/Map-Alignment-2D/))
- Saeed Gholami Shahbandi, Martin Magnusson, Karl Iagnemma. *Nonlinear Optimization of Multimodal Two-Dimensional Map Alignment With Application to Prior Knowledge Transfer*, in IEEE Robotics and Automation Letters, vol. 3, no. 3, pp. 2040-2047, July 2018. doi: 10.1109/LRA.2018.2806439. [URL](http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8292790&isnumber=8302435)([code](https://github.com/saeedghsh/Map-Alignment-Nonrigid-Optimization-2D))

<p align="center">
	<img src="https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/docs/rotating_3d_mesh_hih.gif" width="400">
</p>


Description
-----------
This repository contains a collection of maps from four different environments.
For each environment, a set of sensor-based occupancy-like map is provided.
These sensor map are collected as 3D meshes with a [Google Tango tablet](https://developers.google.com/tango/hardware/tablet) with the [Constructor](https://play.google.com/store/apps/details?id=com.projecttango.constructor&hl=en) application provided by Google.
<!-- ![HIH3D](https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/docs/HIH_3D.png) -->
<!-- ![rotatingHIH](https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/docs/rotating_3d_mesh_hih.gif) -->
Each 3D mesh is horizontally sliced and converted to occupancy-like map.
It should be mentioned that due to instability of the Constructor application in handling big meshes, some maps (mostly office maps) only cover the upper half (along z-axis) of the environment in order to increase the coverage of individual maps.
Sensor maps vary in their global consistency and coverage of the area.
In addition, a single layout map (in bitmap format, occupancy-like) is also provided for each environment.
This table provides details for each set, followed by a thumbnail overview of all maps.  

Name | Type | #sensor maps | #layout | location
---- | ---- | ------------ | ------- | --------
E5 | office building | 14 | 1 | E building, [Halmstad University](https://www.hh.se/download/18.38e7400514bc4e0933ad51d7/1497519545385/campus-map.pdf), Sweden
F5 | office building | 14 | 1 | F building, [Halmstad University](https://www.hh.se/download/18.38e7400514bc4e0933ad51d7/1497519545385/campus-map.pdf), Sweden
HIH | apartment | 4| 1 | [Intelligent Home Environment](http://wagdem.ddi.hh.se/smartahemmet/), Halmstad, Sweden
KPT4A | apartment | 4 | 1 | a residential apartment in Halmstad, Sweden

* E5:  
  ![E5](https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/docs/E5.png)
* F5:  
  ![F5](https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/docs/F5.png)
* HIH:  
  ![HIH](https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/docs/HIH.png)
* KPT4:  
  ![KPT4A](https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/docs/KPT4A.png)


Note on mesh to occupancy map conversion:
Due to the absence of sensor's trajectory and pose, identifying the open space and the conversion from mesh format to occupancy map has been done manually in an interactive process.
This process also included manual filtering (eg. noise removal).
As a consequence, the conversion is not deterministically reproducible.
Generating a pseudo trajectory-pose state for sensor over each map, could make it possible to setup an automated procedure for the conversion.
Such a procedure also requires a 3D point cloud filtering to result in a smooth occupancy map.


Annotation Scripts and GUIs
---------------------------
In order to run accompanied scripts for ground truth annotations or visualization of the annotations, the following dependencies must be met:
```
numpy >= 1.10.2
matplotlib >= 2.0
PySide >= 1.2.1
scikit-image >= 0.12
opencv >= 2
```

Most dependencies (except for opencv) could be installed by:
```
git clone https://github.com/saeedghsh/Halmstad-Robot-Maps.git
cd Halmstad-Robot-Maps
pip install -r requirements.txt
```

Instructions on how to use scripts [will come soon](https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/docs/instructions.md).


License
-------
Distributed with a GNU GENERAL PUBLIC LICENSE; see [LICENSE](https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/LICENSE).
```
Copyright (C) Saeed Gholami Shahbandi
```

<!-- Path to maps -->
<!-- ------------ -->
<!-- ``` -->
<!-- 'Halmstad-Robot-Maps/maps/E5/layout/E5_layout.png' -->
<!-- 'Halmstad-Robot-Maps/maps/E5/pseudo_occupancy/E5_01.png' -->
<!-- 'Halmstad-Robot-Maps/maps/E5/pseudo_occupancy/E5_02.png' -->
<!-- 'Halmstad-Robot-Maps/maps/E5/pseudo_occupancy/E5_03.png' -->
<!-- 'Halmstad-Robot-Maps/maps/E5/pseudo_occupancy/E5_04.png' -->
<!-- 'Halmstad-Robot-Maps/maps/E5/pseudo_occupancy/E5_05.png' -->
<!-- 'Halmstad-Robot-Maps/maps/E5/pseudo_occupancy/E5_06.png' -->
<!-- 'Halmstad-Robot-Maps/maps/E5/pseudo_occupancy/E5_07.png' -->
<!-- 'Halmstad-Robot-Maps/maps/E5/pseudo_occupancy/E5_08.png' -->
<!-- 'Halmstad-Robot-Maps/maps/E5/pseudo_occupancy/E5_09.png' -->
<!-- 'Halmstad-Robot-Maps/maps/E5/pseudo_occupancy/E5_10.png' -->
<!-- 'Halmstad-Robot-Maps/maps/E5/pseudo_occupancy/E5_11.png' -->
<!-- 'Halmstad-Robot-Maps/maps/E5/pseudo_occupancy/E5_12.png' -->
<!-- 'Halmstad-Robot-Maps/maps/E5/pseudo_occupancy/E5_13.png' -->
<!-- 'Halmstad-Robot-Maps/maps/E5/pseudo_occupancy/E5_14.png' -->

<!-- 'Halmstad-Robot-Maps/maps/F5/layout/F5_layout.png' -->
<!-- 'Halmstad-Robot-Maps/maps/F5/pseudo_occupancy/F5_01.png' -->
<!-- 'Halmstad-Robot-Maps/maps/F5/pseudo_occupancy/F5_02.png' -->
<!-- 'Halmstad-Robot-Maps/maps/F5/pseudo_occupancy/F5_03.png' -->
<!-- 'Halmstad-Robot-Maps/maps/F5/pseudo_occupancy/F5_04.png' -->
<!-- 'Halmstad-Robot-Maps/maps/F5/pseudo_occupancy/F5_05.png' -->
<!-- 'Halmstad-Robot-Maps/maps/F5/pseudo_occupancy/F5_06.png' -->
<!-- 'Halmstad-Robot-Maps/maps/F5/pseudo_occupancy/F5_07.png' -->
<!-- 'Halmstad-Robot-Maps/maps/F5/pseudo_occupancy/F5_08.png' -->
<!-- 'Halmstad-Robot-Maps/maps/F5/pseudo_occupancy/F5_09.png' -->
<!-- 'Halmstad-Robot-Maps/maps/F5/pseudo_occupancy/F5_10.png' -->
<!-- 'Halmstad-Robot-Maps/maps/F5/pseudo_occupancy/F5_11.png' -->
<!-- 'Halmstad-Robot-Maps/maps/F5/pseudo_occupancy/F5_12.png' -->
<!-- 'Halmstad-Robot-Maps/maps/F5/pseudo_occupancy/F5_13.png' -->
<!-- 'Halmstad-Robot-Maps/maps/F5/pseudo_occupancy/F5_14.png' -->

<!-- 'Halmstad-Robot-Maps/maps/HIH/layout/HIH_layout.png' -->
<!-- 'Halmstad-Robot-Maps/maps/HIH/pseudo_occupancy/HIH_01.png' -->
<!-- 'Halmstad-Robot-Maps/maps/HIH/pseudo_occupancy/HIH_02.png' -->
<!-- 'Halmstad-Robot-Maps/maps/HIH/pseudo_occupancy/HIH_03.png' -->
<!-- 'Halmstad-Robot-Maps/maps/HIH/pseudo_occupancy/HIH_04.png' -->

<!-- 'Halmstad-Robot-Maps/maps/KPT4A/layout/KPT4A_layout.png' -->
<!-- 'Halmstad-Robot-Maps/maps/KPT4A/pseudo_occupancy/KPT4A_01.png' -->
<!-- 'Halmstad-Robot-Maps/maps/KPT4A/pseudo_occupancy/KPT4A_02.png' -->
<!-- 'Halmstad-Robot-Maps/maps/KPT4A/pseudo_occupancy/KPT4A_03.png' -->
<!-- 'Halmstad-Robot-Maps/maps/KPT4A/pseudo_occupancy/KPT4A_04.png' -->
<!-- ``` -->



<!-- Ground Truth -->
<!-- ------------ -->
<!-- The ground truth is provided in the form of a 3x3 matrix representing an affine transformation, stored in a NumPy binary file format ```.npy```. -->
<!-- Provided for all pairs of maps from the same environment, sensor to sensor and sensor to layout. -->
<!-- Important note: these ground truth are constructed from manual annotation and are estimated after the maps were generated. -->
<!-- In cases where maps are globally inconsistent (e.g, bent or broken), these transformation do not result in a perfect local alignment. -->

<!-- To load transformations: -->
<!-- ```python -->
<!-- M = numpy.load('E5_01_E5_layout.npy') -->
<!-- print (M) -->
<!-- ``` -->

<!-- And here is how to construct transformation objects from those matrices in different libraries: -->
<!-- ```python -->
<!-- import numpy as np -->
<!-- import skimage.transform -->
<!-- import matplotlib.transform -->
<!-- import cv2 -->
<!-- M = numpy.load('E5_01_E5_layout.npy') -->
<!-- ``` -->

<!-- Note on the key points coordinate, the origin of the image is lower-left. -->
<!-- I.e. Images are fliped upside-down after loading with opencv. -->

<!-- Visualize -->
<!-- --------- -->
<!-- ```shell -->
<!-- python scrt.py --map_pair E5_5 % plots sensor map E5_5 versus the layout map of the E5 -->
<!-- ``` -->
<!-- <\!-- * HH_E5: office building (E5) at Halmstad University, Sweden -\-> -->
<!-- <\!-- * HH_F5: office building (F5) at Halmstad University, Sweden -\-> -->
<!-- <\!-- * HH_HIH: Intelligent Home Environment at Halmstad University, Sweden -\-> -->
<!-- <\!-- * KPT4A: a residential apartment in Halmstad, Sweden -\-> -->

<!-- NOTE -->
<!-- ---- -->
<!-- - In SVG format, the origin of the coordinate frame is at the top-left corner. -->
<!--   In order to create a bitmap from the SVG, it must be flipped upside-down. -->
<!--   In order to parse the SVG to extract geometric traits, it must be left as it appears, seemingly upside-down. -->

<!-- TODO -->
<!-- ---- -->
<!-- * [ ] manual annotation
<!-- * [ ] Who should be credited for layout maps? -->
<!-- * [ ] Link to layouts images in this readme file -->
<!-- * [ ] other modalities, e.g. drone, range scanner, omni cam. -->
<!-- * [x] A visualization script, src+dst+aligned... with: -->
<!-- * [x] Fix name inconsistencies -->
<!-- * [x] Include the mesh files from tango in the repository. -->
