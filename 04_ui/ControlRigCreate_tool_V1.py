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
# import maya.cmds as mc          # ModuleNotFoundError: No module named 'maya' if run on OS. Moved inside main call.

from Qt.QtWidgets import QMessageBox
from Qt import QtWidgets, QtGui, QtCore, QtCompat

#---------------------------------------------------------------------------------#
# Class to create control autorig UI by loading the ControlAutorig.ui File
#---------------------------------------------------------------------------------#
class ControlAutorig(QtWidgets.QDialog):
    def __init__(self):
        # LOAD ui with absolute path
        self.wgUtil = QtCompat.loadUi(path_ui)
        
        # UI always stays on top. Issue: Need to move it sometimes to see the warning/error dialog box.
        self.wgUtil.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # SHOW the UI
        self.wgUtil.show()

        self.createConnections()

    def createConnections(self):
        """
        This method connects the buttons to its respective methods
        """
        self.wgUtil.btnRootJoint.clicked.connect(self.rootJointMethod)
            
        self.wgUtil.btnShoulderJoint.clicked.connect(self.shoulderJointMethod)

        self.wgUtil.btnUpperLegJoint.clicked.connect(self.hipJointMethod)

        self.wgUtil.btnCreateControls.clicked.connect(self.createControlsMethod)

    def identifyPrefixMethod(self):
        try:
            self.prefix = mc.ls(sl=1)[0].split("_")[0]
        except:
            QMessageBox.critical(None, 'Critical', 'Please select the root joint')

    def rootJointMethod(self): # used in Connection
        self.rootJointName = mc.ls(sl=True, type='joint') # Do a check if any other joint exist above it or not
        print(self.rootJointName)
        if self.rootJointName != []:
            self.wgUtil.lineEditRootJoint.setText(self.rootJointName[0])
        else:
            QMessageBox.warning(None, 'Warning', 'Please select root joint')
    
    def hipJointMethod(self): # used in Connection
        self.hipJointName = mc.ls(sl=True, type='joint') # Do a check if any other joint exist above it or not
        print(self.hipJointName)
        if self.hipJointName != []:
            self.wgUtil.lineEditUpperLegJoint.setText(self.hipJointName[0])
        else:
            QMessageBox.warning(None, 'Warning', 'Please select upper leg joint')
    
    def shoulderJointMethod(self): # used in Connection
        self.shoulderJointName = mc.ls(sl=True, type='joint') # Do a check if any other joint exist above it or not
        print(self.shoulderJointName)
        if self.shoulderJointName != []:
            self.wgUtil.lineEditShoulderJoint.setText(self.shoulderJointName[0])
        else:
            QMessageBox.warning(None, 'Warning', 'Please select shoulder joint')
    
    #-------------------- Create FK Controls Method ---------------------------#
    def createControlsMethod(self): # used in Connection
        
        self.identifyPrefixMethod()

        # select all joints. Root joint should be the first joint
        selected_root_joint = mc.ls(sl=True, type='joint')

        for jnt in selected_root_joint:
            # get the name for control
            ctrl_name_prefix = jnt.split(self.prefix)[-1]

            ctrl_name, ctrlOffsetName = self.createControls( prefix=ctrl_name_prefix, scale=20.0, 
                            translateTo=jnt, rotateTo=jnt, 
                            parent="", shape='circleY', lockChannels=[])
            
            # find the parent and parent the offset control to its parent control similar to joint hierarchy
            parent_of_jnt = self.findParent(jnt)

            # parent respective controllers hierarchy, similar to joint hierarchy
            self.controllerHierarchy(parent_of_jnt, ctrlOffsetName)    
            
            # parent constraint the controllers to respective joint
            self.parentConstraintControlToJnt(ctrl_name, jnt)

    def createControls(self, prefix = 'new',   # Create a new class for this in future
                    scale = 1.0, 
                    translateTo = '',
                    rotateTo = '',
                    parent = '',
                    shape = 'circle',
                    lockChannels = ['s','v'],
                    jnt = ''):    
        """
        Creates the controller and its offset group, coloring it based on its name, changing the shape based on the input
        Attr:
            prefix      : str,   prefix to name new objects
            scale       : float, general scale of the rig
            translateTo : str,   reference object for control position
            rotateTo    : str,   reference object for control orientation
            parent      : str,   object to be parent of new control
            shape       : str,   controller shape type
            lockChannels: list(str), list of channels on control to be locked and non-keyable
            jnt         : str,   joint name to be used to identify its parent
        """
        # creates the shape of the NURBS controls and parenting under the offset group
        ctrlObject   = None
        circleNormal = [1,0,0]
        # prefix = self.prefix

        if shape in ['circle', 'circleX']:
            circleNormal = [1,0,0]
        elif shape == 'circleY':
            circleNormal = [0,1,0]
        elif shape == 'circleZ':
            circleNormal = [0,0,1]
        elif shape == 'sphere':
            ctrlObject = mc.circle( name =  prefix + '_ctrl', constructionHistory = False, normal = [1,0,0], radius = scale )[0]
            addShape   = mc.circle( name =  prefix + '_ctrl', constructionHistory = False, normal = [0,0,1], radius = scale )[0]
            mc.parent( mc.listRelatives( addShape, shapes = True ), ctrlObject, relative = True, shape = True )
            mc.delete( addShape )

        if not ctrlObject:

            ctrlObject = mc.circle( name =  prefix + '_Ctrl', constructionHistory = False, normal = circleNormal, radius = scale )[0] #ch = channel history

        ctrlZero   = mc.group( name = prefix + '_Zero_grp',   empty = 1 )
        mc.parent( ctrlObject, ctrlZero )
        ctrlOffset = mc.group( name = prefix + '_Offset_grp', empty = 1 )
        mc.parent( ctrlZero, ctrlOffset )

        # color control
        ctrlShapes = mc.listRelatives( ctrlObject, shapes = True) 
        [ mc.setAttr( shapes + '.ove', 1 ) for shapes in ctrlShapes ] # ove= override enable

        for ctrlShape in ctrlShapes:
            # print(s)
            if len(ctrlShape.split("L_")) == 2 or len(ctrlShape.split("Left")) == 2 or len(ctrlShape.split("l_")) == 2 or len(ctrlShape.split("left")) == 2 :
                mc.setAttr( ctrlShape + '.ovc', 6)   #ovc= override color, 6 = blue
                # print("Blue")
            elif len(ctrlShape.split("R_")) == 2 or len(ctrlShape.split("Right")) == 2 or len(ctrlShape.split("r_")) == 2 or len(ctrlShape.split("right")) == 2 :
                mc.setAttr( ctrlShape + '.ovc', 13)  #ovc= override color, 13 = red
                # print("Red")
            else :
                mc.setAttr( ctrlShape + '.ovc', 22)  #ovc= override color, 22 = yellow

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
                    attribute = lockChannel + axis
                    singleAttributeLockList.append(attribute)
            
            else:
                singleAttributeLockList.append(lockChannel)
            
        for attribute in singleAttributeLockList:
            mc.setAttr( ctrlObject + '.' + attribute, lock = True, keyable = False) 

        return ctrlObject, ctrlOffset

    def findParent(self, jnt):
        # this will identify the parent of the joint
        parents = mc.ls(jnt, long=True)[0].split('|')
        print(jnt, parents, len(parents))
        if parents != [] and len(parents) > 2:
            parents.reverse()
            return parents[1]
        else:
            return parents[0]

    def controllerHierarchy(self, parent_of_jnt, ctrlOffsetName):
        if parent_of_jnt == '':
            pass
        else:
            print(parent_of_jnt)
            parent_of_jnt_prefix = parent_of_jnt.split(self.prefix)[-1]    
            mc.parent(ctrlOffsetName, parent_of_jnt_prefix + '_Ctrl')

    def parentConstraintControlToJnt(self, ctrl_name, jnt):
        mc.parentConstraint(ctrl_name, jnt, maintainOffset=True)
  
#---------------------------------------------------------------------------------#
#                 CALLING THE CONTROL AUTORIG TOOL
#---------------------------------------------------------------------------------#
if __name__ == "__main__":
    try:
        import maya.cmds as mc
        # Maya
        path_ui = 'D:/ControlAutorig/04_ui/ui/ControlAutorig.ui'    # This path needs to be changed based on where the script is placed
        try:
            classVar.deleteLater()
            classVar = None
        except:
            pass
        
        classVar = ControlAutorig()
    except ImportError: 
        # OS : Although this script won't function outside Maya. It is there just to see the UI.
        import sys
        app = QtWidgets.QApplication(sys.argv)
        path_ui = ("/").join([os.path.dirname(__file__), "ui", "ControlAutorig.ui"])
        classVarOS = ControlAutorig()
        app.exec_()