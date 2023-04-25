# Green View Index for QGIS
A QGIS plugin to easily calculate Green View Index through Google Street View images.

## Overview
Green View Index (GVI) is an objective measurement of urban green, which utilizes street-level imagery. Most popularly, Google Street View images are used as input. Very simply put, the GVI for an image is the ratio of vegetation pixels to the total number of pixels of the image. 

<img width="600" height="300" src="https://user-images.githubusercontent.com/39091833/234233763-e58f5c74-e087-48b2-b7b2-a3c9f36522ab.png">

To calculate the GVI of a point, multiple images are acquired in different direction angles, and the GVIs of each image are summed. 

The plugin performs the main operations required for Green View Index calculations of a given area. These operations are organized in three separate scripts:

1. Generate Sample Points: Creates random points within an area. Those points can be used as input in the next tools
2. Download Google Street View Images: For a point dataset, it downloads street view locations with parameters given by the user (such as field of view, image size and direction angles)
3. Calculate Green View Index: For the images downloaded by the previous tool, the vegetation pixels are extracted and the Green View Index of its point is calculated

<p align="Left">
  <img src="https://user-images.githubusercontent.com/39091833/233847655-8218b5df-c298-403e-bfa6-74277ee5de96.jpg">
</p>

The plugin aims to popularize the Green View Index (GVI) among planners and researchers who are not well acquainted with code. 

## Installation - Requirements

The plugin has two dependencies: The python libraries scikit-image and gpsphoto. Both can easily be installed with OSGeo4W shell and pip. Simply run the two following commands:
```
pip install gpsphoto
pip install scikit-image
```
You also need to register to Google Cloud Console and generate a Street View API key. Instructions can be found [here](https://www.youtube.com/watch?v=O-o8xSacFPY&ab_channel=ThemeIsle%3AWordPressTutorials%26Reviews).

To install the plugin, use the plugin repository from QGIS (recommended), or download this repository as .zip file and use the option Install from ZIP  from Plugin manager.

Full documentaion can be found in the [pdf document](https://github.com/kowalski93/Green-View-Index-for-QGIS/blob/main/Green%20View%20Index%20for%20QGIS.pdf) of this repository.
