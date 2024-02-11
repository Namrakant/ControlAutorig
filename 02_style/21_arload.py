#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
# Title: 
# Version: 
# Description: 
#              
#              
#              
# Creation Date: 
# Author: 
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#

import os 
import re
import sys
import shutil
import getpass
import datetime
import subprocess

from Qt import QtWidgets, QtGui, QtCore, QtCompat

import libLog
import libData
import libFunc
import arNotice
from tank import Tank
from arUtil import ArUtil

# Variables
TITLE = "load"
LOG = libLog.init(script=TITLE)

#---------------------------------------------------------------------------------#
#  Class ArLoad
#---------------------------------------------------------------------------------#
class ArLoad(ArUtil):

    def __init__(self):
        """
        Class nitialization
        """
        super(ArLoad, self).__init__()

        path_ui = ("/").join([os.path.dirname(__file__), "ui", TITLE + ".ui"])

        self.wgLoad = QtCompat.loadUi(path_ui)
        self.load_dir = ''
        self.load_file = ''

        self.software_format = {y:x.upper() for x,y in self.data['software']['EXTENSION'].items()} # simplify this line of code
        self.software_keys = list(self.software_format.keys())

        self.wgLoad.lstScene.clear()
        self.wgLoad.lstStatus.clear()
        self.wgLoad.lstSet.clear()

        self.clear_meta()

        self.resize_widget(self.wgLoad)

        self.wgLoad.show()

        LOG.info('START : ArLoad')

    #---------------------------------------------------------------------------------#
    # Accept Button
    #---------------------------------------------------------------------------------#
    def press_btnAccept(self):
        """
        This method checks if the path exists or not
        """
        if not os.path.exists(self.load_file):
            self.set_status('FAILED LOADING : Path doesn\'t exists: {}'.format(self.load_file), msg_type=3)
            return False
    
    #---------------------------------------------------------------------------------#
    # Menu Item Add Folder
    #---------------------------------------------------------------------------------#
    def press_menuItemAddFolder(self):
        """
        Add Item Folder
        """
        import arSaveAs

        self.save_as = arSaveAs.start(new_file=False)

    #---------------------------------------------------------------------------------#
    # Menu Sort Method
    #---------------------------------------------------------------------------------#
    def press_menuSort(self, list_widget, reverse=False):
        """
        Sort the menu items
        """
        file_list = []

        for index in xrange(list_widget.count()):
             file_list.append(list_widget.item(index).text())

        list_widget.clear()

        list_widget.addItems(sorted(file_list, reverse=reverse))

    #---------------------------------------------------------------------------------#
    # Change list scene Method
    #---------------------------------------------------------------------------------#
    def change_lstScene(self):
        """
        Change list scene
        """
        self.load_dir = self.data['project']['PATH'][self.wgLoad.lstScene.currentItem().text()]
        tmp_content = libFunc.get_file_list(self.load_dir)

        self.scene_steps = len(self.data['rules']['SCENES'][self.wgLoad.lstScene.currentItem().text()].split('/'))
        
        if self.scene_steps < 5:
            self.wgLoad.lstAsset.hide()
        else:
            self.wgLoad.lstAsset.itemSelectionChanged.connect(self.change_lstAsset)
            self.wgLoad.lstAsset.show()

        self.wgLoad.lstSet.clear()

        if tmp_content:
            self.wgLoad.lstSet.addItems(sorted(tmp_content))
            self.wgLoad.lstSet.setCurrentRow(0)

    #---------------------------------------------------------------------------------#
    # Change list set Method
    #---------------------------------------------------------------------------------#
    def change_lstSet(self):
        """
        Change list set
        """
        new_path = self.load_dir + '/' + self.wgLoad.lstSet.currentItem().text()
        tmp_content = libFunc.get_file_list(new_path)

        if self.scene_steps < 5:            
            self.wgLoad.lstTask.clear()
            if tmp_content:
                self.wgLoad.lstTask.addItems(sorted(tmp_content))
                self.wgLoad.lstTask.setCurrentRow(0)
        else:
            self.wgLoad.lstAsset.clear()
            if tmp_content:
                self.wgLoad.lstAsset.addItems(sorted(tmp_content))
                self.wgLoad.lstAsset.setCurrentRow(0)

    #---------------------------------------------------------------------------------#
    # Change list Asset Method
    #---------------------------------------------------------------------------------#
    def change_lstAsset(self):
        """
        Change list Asset
        """
        new_path = self.load_dir + '/' + self.wgLoad.lstSet.currentItem().text() \
                   + '/' + self.wgLoad.lstAsset.currentItem().text()
        tmp_content = libFunc.get_file_list(new_path)

        self.wgLoad.lstTask.clear()

        if tmp_content:
            self.wgLoad.lstTask.addItems(sorted(tmp_content))
            self.wgLoad.lstTask.setCurrentRow(0)

    #---------------------------------------------------------------------------------#
    # Fill meta Method
    #---------------------------------------------------------------------------------#
    def fill_meta(self):
        """
        Fill the Text fields- Title, Date and Size of the file
        """
        self.wgPreview.lblTitle.setText(self.file_name)
        self.wgPreview.lblDate.setText(str(datetime.datetime.fromtimestamp(os.path.getmtime(self.load_file))).split(".")[0])
        self.wgPreview.lblSize.setText(str("{0:.2f}".format(os.path.getsize(self.load_file)/(1024*1024.0)) + " MB"))
    
    #---------------------------------------------------------------------------------#
    # Clear meta Method
    #---------------------------------------------------------------------------------#
    def clear_meta(self):
        """
        Clear the texts in the Textfields
        """
        self.wgPreview.lblUser.setText('')
        self.wgPreview.lblTitle.setText('')
        self.wgPreview.lblDate.setText('')

#---------------------------------------------------------------------------------#
# Main Function
#---------------------------------------------------------------------------------#
def execute_the_class_ar_load():
    """
    Main function
    """
    global main_widget
    main_widget = ArLoad()