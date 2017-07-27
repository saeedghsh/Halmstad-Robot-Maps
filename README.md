A 2D Occupancy Map Dataset For Map Alignment Challenge
------------------------------------------------------
A collection layout maps and sensor maps of different environments.
This repository of maps has been collected for the verification of a map alignment method presented in the following publication.
- S. G. Shahbandi, M. Magnusson, "2D Map Alignment With Region Decomposition", submitted to Autonomous Robots, 2017.

Description
-----------
This repositoy contains a collection of maps from four different environments.
For each environment, a set of sensor-based occupancy-like map is provided.
These sensor map are collected as 3D meshes with a [Google Tango tablet](https://developers.google.com/tango/hardware/tablet) with the [Constructor](https://play.google.com/store/apps/details?id=com.projecttango.constructor&hl=en) application provided by Google.
Each 3D mesh is horizontally sliced and converted to occupancy-like map.
Sensor maps vary in their global consistency and coverage of the area.
In addition, a single layout map (in bitmap format, occupancy-like) is also provided for each environment.
Following table provides details for each set.  

Name | Type | #sensor maps | #layout | location
---- | ---- | ------------ | ------- | --------
E5 | office building | 14 | 1 | Halmstad University, Sweden
F5 | office building | 14 | 1 | Halmstad University, Sweden
HIH | apartment | 4| 1 | Intelligent Home Environment at Halmstad University, Sweden
KPT4A | apartment | 4 | 1 | a residential apartment in Halmstad, Sweden

* E5  
  [E5](https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/docs/E5.png)
* F5  
  [F5](https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/docs/F5.png)
* HIH  
  [HIH](https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/docs/HIH.png)
* KPT4  
  [KPT4A](https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/docs/KPT4A.png)



Dependencies for scripts (annotations, loading, and visualization)
------------------------------------------------------------------
```
numpy >= 1.10.2
opencv >= 2
matplotlib >= 1.4.3
PySide
scikit-image 
```

Script/GUI instructions
-----------------------
To come:
- manual annotation: selecting key points
- manual annotation: associating key points
- visualizing keypoint associations and transform estimations

License
-------
Distributed with a GPLv3 license; see LICENSE.
```
Copyright (C) Saeed Gholami Shahbandi <saeed.gh.sh@gmail.com>
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
<!-- In cases where maps are globaly inconsistence (e.g, bent or broken), these transformation do not result in a perfect local alignment. -->

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
