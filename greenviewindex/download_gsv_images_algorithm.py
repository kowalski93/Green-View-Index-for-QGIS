# -*- coding: utf-8 -*-

"""
/***************************************************************************
 GreenViewIndex
                                 A QGIS plugin
 A plugin for Green View Index (GVI) operations
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-04-21
        copyright            : (C) 2023 by Alexandros Voukenas
        email                : avoukenas@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Alexandros Voukenas'
__date__ = '2023-04-21'
__copyright__ = '(C) 2023 by Alexandros Voukenas'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'
import os
import inspect
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterField,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterString,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFolderDestination,
                       QgsField,
                       QgsFields,
                       QgsFeature)
from qgis import processing
import requests,csv,os


class DownloadGoogleStreetViewImages(QgsProcessingAlgorithm):
    
    INPUT_POINTS = 'INPUT POINTS'
    
    INPUT_FIELD="ID FIELD"
    
    INPUT_KEY='API KEY'
    INPUT_FOV='FOV'
    INPUT_SIZE='SIZE'
    INPUT_HEADINGS='HEADINGS'
    INPUT_PITCHES='PITCHES'
    INPUT_GEOTAG='GEOTAG'
    INPUT_METADATA_ONLY='METADATA ONLY'
    
    OUTPUT = 'OUTPUT FOLDER'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)
        
    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'download_logo.png')))
        return icon
        
    def createInstance(self):
        return DownloadGoogleStreetViewImages()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'download_gsv_images'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Download Google Street View Images')
        
    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return ''

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("""Given a point layer of sample locations, this script downloads Google Street View images for those locations.
        The point layer must have a unique identifier field in Integer format. You can use the output from tool 'Generate Sample Points'.
        The user must set the Google Street View API parameters, starting from the key. They must also set:
        The Field of View value (FOV): determines the horizontal field of view of the image (smaller numbers indicate higher level of zoom).
        Heading values: Indicate the compass of the camera, i.e. the horizontal angle(s) in which to obtain the images. If multiple angles are needed, they must be separated by comma.
        Pitch values: Specifies the up or down angle of the camera. If multiple angles are needed, they must be separated by comma.
        Image size: Specifies the output image size in width x height.
        Option to geotag images: If selected, the images' metadata will be edited to include their latitude and longitude coordinates. You can then use the Import photos plugin to import them into your project.
        Option to download metadata only: If selected, no images will be downloaded, only a csv file will be created with the image metadata (status and date) for each point. This does not affect your API cost balance.
        Output folder: A real folder and not a temporary one must be set. Also, it must be a folder dedicated for those images, with no other image files.
        More info on how to obtain a key and documentation here: 
        https://developers.google.com/maps/documentation/streetview/overview""")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        #add the input parameters to the algorithm
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_POINTS,
                self.tr('Input sample points layer'),
                [QgsProcessing.TypeVectorPoint]
            )
        )
        
        self.addParameter(
        QgsProcessingParameterField(
                self.INPUT_FIELD,
                'Unique ID field from sample points layer',
                '',
                self.INPUT_POINTS)
        )
        
        self.addParameter(
            QgsProcessingParameterString(
                self.INPUT_KEY,
                self.tr('Google Street View API key'),
                defaultValue=None
            )
        )
        
        self.addParameter(
            QgsProcessingParameterString(
                self.INPUT_FOV,
                self.tr('Field of View (FOV) value'),
                defaultValue='60'
            )
        )
        
        self.addParameter(
            QgsProcessingParameterString(
                self.INPUT_HEADINGS,
                self.tr('Heading values (horizontal angle) for which to download images, separated by semicolon'),
                defaultValue='0;60;120;180;240;300'
            )
        )
        
        self.addParameter(
            QgsProcessingParameterString(
                self.INPUT_PITCHES,
                self.tr('Pitch values (vertical angle) for which to download images, separated by semicolon'),
                defaultValue='-45;0;45'
            )
        )
        
        self.addParameter(
            QgsProcessingParameterString(
                self.INPUT_SIZE,
                self.tr('Image size'),
                defaultValue='600x600'
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.INPUT_GEOTAG,
                self.tr('Geotag images'),
                defaultValue=False
            )
        )
        self.addParameter(
                QgsProcessingParameterBoolean(
                    self.INPUT_METADATA_ONLY,
                    self.tr('Metadata only'),
                    defaultValue=False
            )
        )        
        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT,
                self.tr('Output Folder')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        #define the parameters for the processing algorithm
        source = self.parameterAsSource(
            parameters,
            self.INPUT_POINTS,
            context
        )
        
        api_key=self.parameterAsString(
            parameters,
            self.INPUT_KEY,
            context
        )
        
        fov=self.parameterAsString(
            parameters,
            self.INPUT_FOV,
            context
        )
        
        headings=self.parameterAsString(
            parameters,
            self.INPUT_HEADINGS,
            context
        )
        
        headings=headings.split(';') #split the headings input into a list so that we can loop into it later
        
        pitches=self.parameterAsString(
            parameters,
            self.INPUT_PITCHES,
            context
        )
        pitches=pitches.split(';') #same split for the pitches
        
        img_size=self.parameterAsString(
            parameters,
            self.INPUT_SIZE,
            context
        )
        
        id_field=self.parameterAsString(
            parameters,
            self.INPUT_FIELD,
            context
        )
        
        geotag=self.parameterAsBoolean(
            parameters,
            self.INPUT_GEOTAG,
            context
        )
        if geotag==True:
            from GPSPhoto import gpsphoto
            
        metadata_only=self.parameterAsBoolean(
            parameters,
            self.INPUT_METADATA_ONLY,
            context
        )
        
        output_path=self.parameterAsString(
            parameters,
            self.OUTPUT,
            context
        )

        if source is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_POINTS))
        
        #list the unique values in the Unique ID field of the input layer    
        unique_values=processing.run("qgis:listuniquevalues", 
        {'INPUT':parameters[self.INPUT_POINTS],
        'FIELDS':[parameters[self.INPUT_FIELD]],
        'OUTPUT':'TEMPORARY_OUTPUT',
        'OUTPUT_HTML_FILE':'TEMPORARY_OUTPUT'})['OUTPUT']
        
        #list the null values of the Unique ID field of the input layer
        null_out=processing.run("native:extractbyattribute", 
        {'INPUT':parameters[self.INPUT_POINTS],
        'FIELD':parameters[self.INPUT_FIELD],
        'OPERATOR':8,
        'VALUE':'',
        'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
        
        if len(unique_values)<len(source): #if there is a duplicate in the unique values (two or more points with the same unique ID)
            raise QgsProcessingException("Duplicate values found at unique ID field of sample points")
        if len(null_out): #or if there is a null value in the unique ID field
            raise QgsProcessingException("NULL found at unique ID field of sample points")    
        
        #prepare the links for the requests. The link to retrieve the image and the link for the image's metadata
        SV_link="https://maps.googleapis.com/maps/api/streetview?"
        MD_link="https://maps.googleapis.com/maps/api/streetview/metadata?"
        
        #get the features of source in an iterator
        it=source.getFeatures()
        #prepare a list for the points
        csv_fields=["pointID","status","date"]
        survey_point_list=[]
        
        p=999
        
        for i,feature in enumerate(it):
            
            #get elements from the feature. Latitude, longitude, and the value from its ID field
            geom=feature.geometry()
            lat=geom.asPoint()[0]
            long=geom.asPoint()[1]
            location=str(long)+","+str(lat)
            point_ID=int(feature[id_field])
            
            #make an initial metadata request to check the status           
            requestMD_link="{}size={}&location={}&fov={}&heading=0&pitch=0&key={}".format(MD_link,img_size,location,fov,api_key)
            metadata=requests.get(requestMD_link).json()
                    
            status=metadata['status'] 
            date=''
            if status=="OK": #if image was found
            
                #get the date of the image at that point. Year and Month is as detailed as it goes.
                date=metadata['date']
            
                year=int(date.split("-")[0])
                month=int(date.split("-")[1])
                
                if metadata_only==False:
                #iterate through the heading and pitch values to get street view images at the lat and long positions
                    for heading in headings:
                        for pitch in pitches:
                            requestSV_link="{}size={}&location={}&fov={}&heading={}&pitch={}&key={}".format(SV_link,img_size,location,fov,heading,pitch,api_key)
                            img_data=requests.get(requestSV_link).content
                            
                            #write it on the folder, with a name based on the ID, the heading and the pitch. 
                            filename=r"{}//pointID_{}_heading_{}_pitch_{}".format(output_path,point_ID,heading,pitch)+".jpg"

                            with open(filename,'wb') as handler:
                                handler.write(img_data)
                            
                            #if geotag was selected, also geotag the image based on the lat and long we have
                            if geotag==True:
                                photo=gpsphoto.GPSPhoto(filename)
                                info = gpsphoto.GPSInfo((long,lat))
                                photo.modGPSData(info,filename)
                            
                #populate the list that keeps ID, status and image date of the points
                survey_point_list.append([point_ID,status,date])
            else: #if image was not found, populate the list accordingly
                feedback.pushInfo('Images not found for point with ID {}'.format(point_ID))
                survey_point_list.append([point_ID,status,None])
            #push some info on percentage of points completed
            pct=int((i+1)/len(unique_values)*100)
            if pct in [10,20,25,30,33,40,50,60,66,70,75,80,90,100]:
                if pct!=p:
                    feedback.pushInfo('Finished with {}% of points'.format(pct))
                    p=pct
                    
        #operations to write a csv and a csvt file with the data of the points (status and date)
        csvfile=os.path.join(output_path,"Points_data.csv")
        csvtfile=os.path.join(output_path,"Points_data.csvt")
        with open(csvfile, 'w') as f:
            write = csv.writer(f)
              
            write.writerow(csv_fields)
            write.writerows(survey_point_list)
            
        with open(csvtfile, 'w') as file:
            a = csv.writer(file)
            a.writerow(["Integer","String","String"])
            
        return {'OUTPUT RESULTS': survey_point_list}