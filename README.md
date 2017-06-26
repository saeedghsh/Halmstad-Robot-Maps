A 2D Occupancy Map Dataset For Map Alignment Challenge
------------------------------------------------------
A collection layout maps and sensor maps of different environments.

<!-- <E5_layout src="https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/E5/layout/E5_layout.png" alt="none" width="50" height="50"> -->
<!-- <E5_1 src="https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/E5/pseudo_occupancy/E5_1.png" alt="none" width="50" height="50"> -->

<!-- <F5_layout src="https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/F5/layout/F5_layout.png" alt="none" width="50" height="50"> -->
<!-- <F5_1 src="https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/F5/pseudo_occupancy/F5_1.png" alt="none" width="50" height="50"> -->

<!-- <HIH_layout src="https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/HIH/layout/HIH_layout.png" alt="none" width="50" height="50"> -->
<!-- <HIH_01 src="https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/HIH/pseudo_occupancy/HIH_01.png" alt="none" width="50" height="50"> -->

<!-- <KPT4A_layout src="https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/KPT4A/layout/KPT4A_layout.png" alt="none" width="50" height="50"> -->
<!-- <KPT4A_01 src="https://github.com/saeedghsh/Halmstad-Robot-Maps/blob/master/KPT4A/pseudo_occupancy/KPT4A_01.png" alt="none" width="50" height="50"> -->


Requirements for scripts (loading GT and visualization)
-------------------------------------------------------
numpy >= 1.10.2
opencv >= 2
matplotlib >= 1.4.3


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

Ground Truth
------------
The ground truth is provided in the form of a 3x3 matrix representing an affine transformation, stored in a NumPy binary file format ```.npy```.

Provided for all pairs of maps from the same environment, sensor to sensor and sensor to layout.

Important note: these ground truth are constructed from manual annotation and are estimated after the maps were generated.
In cases where maps are globaly inconsistence (e.g, bent or broken), these transformation do not result in a perfect local alignment.

To load transformations:
```python
M = numpy.load('E5_01_E5_layout.npy')
print (M)
```

And here is how to construct transformation objects from those matrices in different libraries:
```python
import numpy as np
import skimage.transform
import matplotlib.transform
import cv2
M = numpy.load('E5_01_E5_layout.npy')
```

Visualize
---------
```shell
python scrt.py --map_pair E5_5 % plots sensor map E5_5 versus the layout map of the E5
```
<!-- * HH_E5: office building (E5) at Halmstad University, Sweden -->
<!-- * HH_F5: office building (F5) at Halmstad University, Sweden -->
<!-- * HH_HIH: Intelligent Home Environment at Halmstad University, Sweden -->
<!-- * KPT4A: a residential apartment in Halmstad, Sweden -->

NOTE
----
- In SVG format, the origin of the coordinate frame is at the top-left corner.
  In order to create a bitmap from the SVG, it must be flipped upside-down.
  In order to parse the SVG to extract geometric traits, it must be left as it appears, seemingly upside-down.

TODO
----
* [ ] Provide a "ground truth" for the alignment transformation (the ground truth will be in form of keypoint association)
  * [x] (script) for each map select key points
  * [ ] (task) for each map select key points
  * [x] (script) for each pair of maps select associated key points
  * [ ] (task) for each pair of maps select associated key points
  * [ ] Put all the keypoints, and matched pairs into single files rather per/map and per/pairMap
* [ ] A visualization script, src+dst+aligned... with:
  * [ ] matplotlib
  * [ ] opencv
* [ ] Who should be credited for layout maps?
* [ ] Link to layouts images in this readme file
* [ ] other modalities, e.g. drone, range scanner, omni cam.
* [x] Fix name inconsistencies
* [x] Include the mesh files from tango in the repository.

License
-------
Distributed with a GPLv3 license; see LICENSE.
```
Copyright (C) Saeed Gholami Shahbandi <saeed.gh.sh@gmail.com>
```

This repository of maps has been collected for the verification of a map alignment method presented in the following publication:
- S. G. Shahbandi, M. Magnusson, "2D Map Alignment With Region Decomposition", submitted to Autonomous Robots, 2017.
