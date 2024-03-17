#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
# Title        : Control Autorig
# Version      : 0.02
# Description  : This autorig creates FK/IK controls for your rig with just 
#                joint hierarchy.
# How to use   : Select all the joints that need FK controls. Run this script.
#                Manually resize the controls based on your needs. Controls are 
#                color coded.
#                Note: Select root joint first!                
# Creation Date: 02/20/2024
# Author       : Namrakant Tamrakar
#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#

import os
import sys
import maya.cmds as mc
# import maya.mel as mel
# from functools import partial
import maya.OpenMayaUI as omui

from PySide2 import QtUiTools
from PySide2 import QtCore, QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

from Qt import QtWidgets, QtGui, QtCore, QtCompat


# import ui.ControlAutorig
# VARIABLE
TITLE = 'ControlAutorig'#os.path.splitext(os.path.basename(__file__))[0]
print("Title = ", TITLE)
#---------------------------------------------------------------------------------#
# Function to keep the User Interface on top of Maya
#---------------------------------------------------------------------------------#
def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)#QWidget)
main_window = maya_main_window()
#---------------------------------------------------------------------------------#
# Class to create control autorig UI
#---------------------------------------------------------------------------------#
class ControlAutorig(QtWidgets.QDialog):
    def __init__(self):
        super(ControlAutorig, self).__init__(main_window)
        # # UI always stays on top
        # QtWidgets.QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(QtCore.Qt.Window)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        print("Hello")
        path_ui = 'D:/ControlAutorig/04_ui/ui/ControlAutorig.ui'#("/").join([os.path.dirname(__file__), "ui", TITLE + ".ui"])
        print('path ui = ', path_ui)
        # LOAD ui with absolute path
        # self.wgUtil = QtCompat.loadUi(path_ui)
        self.wgUtil = QtUiTools.QUiLoader().load(path_ui)
        self.wgUtil.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.wgUtil.setWindowTitle("Control Autorig")
        # QtWidgets.QMainWindow.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)

        # SHOW the UI
        self.wgUtil.show()

        self.create_connections()



#------------------------------- CREATE CONNECTIONS METHOD --------------------------#
    def create_connections(self):
        """
        This method connects the buttons to its respective methods
        """
        self.wgUtil.btnRootJoint.clicked.connect(self.rootJointMethod)
            
        self.wgUtil.btnShoulderJoint.clicked.connect(self.shoulderJointMethod)

        self.wgUtil.btnUpperLegJoint.clicked.connect(self.hipJointMethod)

        self.wgUtil.btnCreateControls.clicked.connect(self.createControlsMethod)

    def identifyPrefixMethod(self):
        self.prefix = mc.ls(sl=1)[0].split("_")[0]

    def rootJointMethod(self): # used in Connection
        self.identifyPrefixMethod()
        self.rootJointName = mc.ls(sl=True, type='joint') # Do a check if any other joint exist above it or not
        print(self.rootJointName)
        if self.rootJointName != []:
            self.wgUtil.lineEditRootJoint.setText(self.rootJointName[0])
            print(type(self.rootJointName), self.rootJointName)
        else:
            print("Please select root joint")
    
    def hipJointMethod(self): # used in Connection
        self.identifyPrefixMethod()
        self.hipJointName = mc.ls(sl=True, type='joint') # Do a check if any other joint exist above it or not
        print(self.hipJointName)
        if self.hipJointName != []:
            self.wgUtil.lineEditUpperLegJoint.setText(self.hipJointName[0])
            print(type(self.hipJointName), self.hipJointName)
        else:
            print("Please select hip joint")
    
    def shoulderJointMethod(self): # used in Connection
        self.identifyPrefixMethod()
        self.shoulderJointName = mc.ls(sl=True, type='joint') # Do a check if any other joint exist above it or not
        print(self.shoulderJointName)
        if self.shoulderJointName != []:
            self.wgUtil.lineEditShoulderJoint.setText(self.shoulderJointName[0])
            print(type(self.shoulderJointName), self.shoulderJointName)
        else:
            print("Please select shoulder joint")
    
    #-------------------- Create FK Controls Method ---------------------------#
    def createControlsMethod(self): # used in Connection
        
        self.identifyPrefixMethod()
        # select joints
        selected_joints = mc.ls(sl=True, type='joint')
        # print(selected_joints)

        for jnt in selected_joints:
            # get the name for control
            ctrl_name_prefix = jnt.split(self.prefix)[-1]

            ctrl_name, ctrlOffsetName = self.create_controls( prefix=ctrl_name_prefix, scale=20.0, 
                            translateTo=jnt, rotateTo=jnt, 
                            parent="", shape='circleY', lockChannels=[])
            
            # find the parent and parent the offset control to its parent control similar to joint hierarchy
            parent_of_jnt = self.find_parent(jnt)

            # parent respective controllers hierarchy, similar to joint hierarchy
            self.controller_hierarchy(parent_of_jnt, ctrlOffsetName)    
            
            # parent constraint the controllers to respective joint
            self.parent_constraint_control_to_jnt(ctrl_name, jnt)

    def create_controls(self, prefix = 'new',   # Create a new class for this
                    scale = 1.0, 
                    translateTo = '',
                    rotateTo = '',
                    parent = '',
                    shape = 'circle',
                    lockChannels = ['s','v'],
                    jnt = ''):    
        """
        Creating the controller and its offset group, coloring it based on its name, changing the shape based on the input
        Attr:
            prefix      : str, prefix to name new objects
            scale       : float, general scale of the rig
            translateTo : str, reference object for control position
            rotateTo    : str, reference object for control orientation
            parent      : str, object to be parent of new control
            shape       : str, controller shape type
            lockChannels: list(str), list of channels on control to be locked and non-keyable
            jnt         : str, joint name to be used to identify its parent
        """
        # creating the shape of the NURBS controls and parenting under the offset group

        ctrlObject = None
        circleNormal = [1,0,0]

        if shape in ['circle', 'circleX']:
            circleNormal = [1,0,0]
        elif shape == 'circleY':
            circleNormal = [0,1,0]
        elif shape == 'circleZ':
            circleNormal = [0,0,1]
        elif shape == 'sphere':
            ctrlObject = mc.circle( n = prefix + '_ctrl', ch = False, normal = [1,0,0], radius = scale )[0]
            addShape = mc.circle( n = prefix + '_ctrl', ch = False, normal = [0,0,1], radius = scale )[0]
            mc.parent( mc.listRelatives( addShape, s = 1 ), ctrlObject, r = 1, s = 1 )
            mc.delete( addShape )

        if not ctrlObject:

            ctrlObject = mc.circle( n = prefix + '_ctrl', ch = False, normal = circleNormal, radius = scale )[0] #ch = channel history

        ctrlZero = mc.group( n = prefix + '_Zero_grp', em = 1 )
        mc.parent( ctrlObject, ctrlZero )
        ctrlOffset = mc.group( n = prefix + '_Offset_grp', em = 1 )
        mc.parent( ctrlZero, ctrlOffset )

        # color control

        ctrlShapes = mc.listRelatives( ctrlObject, s = 1) # s= shape
        [ mc.setAttr( s + '.ove', 1 ) for s in ctrlShapes ] # ove= override enable

        for s in ctrlShapes:
            # print(s)
            if len(s.split("L_")) == 2 or len(s.split("Left")) == 2 or len(s.split("l_")) == 2 or len(s.split("left")) == 2 :
                mc.setAttr( s + '.ovc', 6)  #ovc= override color, 6 = blue
                # print("Blue")
            elif len(s.split("R_")) == 2 or len(s.split("Right")) == 2 or len(s.split("r_")) == 2 or len(s.split("right")) == 2 :
                mc.setAttr( s + '.ovc', 13)  #ovc= override color, 13 = red
                # print("Red")
            else :
                mc.setAttr( s + '.ovc', 22)  #ovc= override color, 22 = yellow

        # translate control
        if mc.objExists( translateTo ):
            mc.delete(mc.pointConstraint( translateTo, ctrlOffset ) )

        # rotate control
        if mc.objExists( rotateTo ):
            mc.delete(mc.orientConstraint( rotateTo, ctrlOffset ) )

        # parent control
        if mc.objExists( parent ):
            mc.parent( ctrlOffset, parent )

        # lock control channels
        singleAttributeLockList = []

        for lockChannel in lockChannels:
            if lockChannel in ['t','r','s']:
                for axis in ['x','y','z']:
                    at = lockChannel + axis
                    singleAttributeLockList.append(at)
            
            else:
                singleAttributeLockList.append( lockChannel )
            
        for at in singleAttributeLockList:
            mc.setAttr( ctrlObject + '.' + at, l = 1, k = 0) # l = lock, k = keyable
        

        return ctrlObject, ctrlOffset

    def find_parent(self, jnt):
        """
        Find the parent of the current joint
        """
        # this will identify the parent of the joint
        parents = mc.ls(jnt, long=True)[0].split('|')
        print(jnt, parents, len(parents))
        if parents != [] and len(parents) > 2:
            parents.reverse()
            # print(jnt, parents[1])
            return parents[1]
        else:
            # print(jnt, parents[0])
            return parents[0]

    def parent_constraint_control_to_jnt(self, ctrl_name, jnt):
        """
        Parent constraint controllers to respective joints
        """
        # print("parent_constraint_control_to_jnt")
        mc.parentConstraint(ctrl_name, jnt, mo=True)

    def controller_hierarchy(self, parent_of_jnt, ctrlOffsetName):
        if parent_of_jnt == '':
            pass
        else:
            print(parent_of_jnt)
            parent_of_jnt_prefix = parent_of_jnt.split(self.prefix)[-1]    
            mc.parent(ctrlOffsetName, parent_of_jnt_prefix + '_ctrl')
  
#---------------------------------------------------------------------------------#
#                 CALLING THE CONTROL AUTORIG TOOL
#---------------------------------------------------------------------------------#
if __name__ == "__main__":
    
    try:
        classVar.deleteLater()
        classVar = None
    except:
        pass
    
    classVar = ControlAutorig()