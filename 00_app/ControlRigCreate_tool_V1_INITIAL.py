#---------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------#
# Title        : Control Autorig
# Version      : 0.01
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
import maya.cmds as mc
import maya.mel as mel
from functools import partial
import maya.OpenMayaUI as omui

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

#---------------------------------------------------------------------------------#
# Function to keep the User Interface on top of Maya
#---------------------------------------------------------------------------------#
def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

#---------------------------------------------------------------------------------#
# Class to smooth the animation on the FBX in the scene
#---------------------------------------------------------------------------------#
class ControlAutorig(QtWidgets.QDialog):

    def __init__(self, parent=maya_main_window()):
        """
        Constructor used to call all the methods
        """
        super(ControlAutorig, self).__init__(parent)

        self.setWindowTitle("Control Autorig Tool")
        self.setMinimumWidth(500)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        """
        This method creates widgets such as radiobutton, lineedit and button
        """
        self.rootJointLineedit = QtWidgets.QLineEdit("example- main_jnt")
        self.rootJointBtn = QtWidgets.QPushButton("Select Root Joint")

        self.hipJointLineedit = QtWidgets.QLineEdit("example- l_hip_jnt")
        self.hipJointBtn = QtWidgets.QPushButton("Select Hip Joint")

        self.shoulderJointLineedit = QtWidgets.QLineEdit("example- l_shoulder_jnt")
        self.shoulderJointBtn = QtWidgets.QPushButton("Select Shoulder Joint")
        
        self.select_FK = QtWidgets.QRadioButton('FK Controls only')
        self.select_FK.setChecked(True)
        self.select_FKIK = QtWidgets.QRadioButton('FK/IK Controls')

        self.createControlsBtn = QtWidgets.QPushButton("Create Controls")

    def create_layouts(self):
        """
        This method creates the layout to hold the widgets. 
        Without this, you won't see the widgets you have created in Maya.
        """

        FKIK_rb_layout = QtWidgets.QHBoxLayout()
        FKIK_rb_layout.addWidget(self.select_FK)
        FKIK_rb_layout.addWidget(self.select_FKIK)

        root_button_layout = QtWidgets.QHBoxLayout()
        # root_button_layout.addStretch()
        root_button_layout.addWidget(self.rootJointLineedit)
        root_button_layout.addWidget(self.rootJointBtn)
        
        hip_button_layout = QtWidgets.QHBoxLayout()
        # hip_button_layout.addStretch()
        hip_button_layout.addWidget(self.hipJointLineedit)
        hip_button_layout.addWidget(self.hipJointBtn)

        shoulder_button_layout = QtWidgets.QHBoxLayout()
        # shoulder_button_layout.addStretch()
        shoulder_button_layout.addWidget(self.shoulderJointLineedit)
        shoulder_button_layout.addWidget(self.shoulderJointBtn)

        form_layout = QtWidgets.QFormLayout()
        # form_layout.addRow("Select all joints", self.selectAllJoints)
        form_layout.addRow("Select root joint and Press", root_button_layout)
        form_layout.addRow("Select hip joint and Press", hip_button_layout)
        form_layout.addRow("Select shoulder joint and Press", shoulder_button_layout)

        form_layout.addRow("", FKIK_rb_layout)
        form_layout.addRow("", self.createControlsBtn)
        
        # Main Layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)

#------------------------------- CREATE CONNECTIONS METHOD --------------------------#
    def create_connections(self):
        """
        This method connects the buttons to its respective methods
        """
        self.rootJointBtn.clicked.connect(self.rootJointMethod)
            
        self.hipJointBtn.clicked.connect(self.hipJointMethod)
        # if self.hipJointName != "":
        #     self.hipJointLineedit.setText(self.hipJointName)

        self.shoulderJointBtn.clicked.connect(self.shoulderJointMethod)
        self.createControlsBtn.clicked.connect(self.createControlsMethod)
        # if self.shoulderJointName != "":
        #     self.shoulderJointLineedit.setText(self.shoulderJointName)
        # self.weightedTangents.clicked.connect(self.convertToWeightedTangents)

        # Get the filepath if it already has one
        # fullfilepath = mc.file(q=True, sn=True)
        # # if self.save_playblast_path:
        # #     self.playblastFilepath.setText(self.save_playblast_path)
        # if fullfilepath:
        #     self.filepath = os.path.split(fullfilepath)[0]
        #     self.filename = os.path.split(fullfilepath)[1].split('.')[0]

        #     self.playblastFilepath.setText(self.filepath)
        #     self.playblastFilename.setText(self.filename)

        #     self.exportFBXFilepath.setText(self.filepath)
        #     self.exportFBXFilename.setText(self.filename)

        #     # self.playblastFilepath.editingFinished.connect(self.filepath)
        #     # self.playblastFilename.editingFinished.connect(self.filename)
        # # self.numberOfIteration.editingFinished.connect(self.numberOfIterations)
        # self.smooth.clicked.connect(self.smoothCurve)

    def rootJointMethod(self):
        self.rootJointName = mc.ls(sl=True, type='joint') # Do a check if any other joint exist above it or not
        print(self.rootJointName)
        if self.rootJointName != []:
            self.rootJointLineedit.setText(self.rootJointName[0])
            print(type(self.rootJointName), self.rootJointName)
        else:
            print("Please select root joint")
        # return str(self.rootJointName)
    
    def hipJointMethod(self):
        self.hipJointName = mc.ls(sl=True, type='joint') # Do a check if any other joint exist above it or not
        print(self.hipJointName)
        if self.hipJointName != []:
            self.hipJointLineedit.setText(self.hipJointName[0])
            print(type(self.hipJointName), self.hipJointName)
        else:
            print("Please select hip joint")
    
    def shoulderJointMethod(self):
        self.shoulderJointName = mc.ls(sl=True, type='joint') # Do a check if any other joint exist above it or not
        print(self.shoulderJointName)
        if self.shoulderJointName != []:
            self.shoulderJointLineedit.setText(self.shoulderJointName[0])
            print(type(self.shoulderJointName), self.shoulderJointName)
        else:
            print("Please select shoulder joint")
    
    def createControlsMethod(self):
        #-------------------------------------------------------------------------------#
        #-------------------- CALL CONTROL CREATION FUNCTION ---------------------------#
        #-------------------------------------------------------------------------------#

        # select joints
        selected_joints = mc.ls(sl=True, type='joint')
        # selected_joints = mc.listRelatives('m_avg_root', ad=True, type='joint') # this doesn't work because of sequence order
        # temp_circle = mc.circle( n = 'temp_ctrl', ch = False, normal = [0,1,0], radius = 1.0 )[0] #ch = channel history
        # mc.setAttr(str(temp_circle)+ '.translateY', 200)

        for jnt in selected_joints:
            # get the name for control
            ctrl_name_prefix = jnt.split("m_avg_")[-1]
            print()
            print('-----------------------------------------')
            # print(ctrl_name_prefix)

            # identify rotateTo joint, basically the child joint
            
            # rotateTo_jnt = find_child(jnt)
            # print("Rotate To for " + jnt + " joint = " + str(rotateTo_jnt))

            # create controls. passing below parameters -
                        # prefix = 'new', 
                        # scale = 1.0, 
                        # translateTo = '',
                        # rotateTo = '',
                        # parent = '',
                        # shape = 'circle',
                        # lockChannels = ['s','v']
            
            ctrl_name, ctrlOffsetName = create_controls( prefix=ctrl_name_prefix, scale=20.0, 
                            translateTo=jnt, rotateTo=jnt, 
                            parent="", shape='circleY', lockChannels=[])
            
            # find the parent and parent the offset control to its parent control similar to joint hierarchy
            parent_of_jnt = find_parent(jnt)

            # parent respective controllers hierarchy, similar to joint hierarchy
            controller_hierarchy(parent_of_jnt, ctrlOffsetName)    
            
            # parent constraint the controllers to respective joint
            parent_constraint_control_to_jnt(ctrl_name, jnt)


        # mc.delete(temp_circle)

prefix = 'new'
scale = 1.0
translateTo = ''
rotateTo = ''
parent = ''
shape = 'circle'
lockChannels = ['s','v']

def create_controls( prefix = 'new', 
                scale = 1.0, 
                translateTo = '',
                rotateTo = '',
                parent = '',
                shape = 'circle',
                lockChannels = ['s','v'],
                jnt = ''):    
    """
    Creating the controller and its offset group, coloring it based on its name, changing the shape based on the input

    @param prefix: str, prefix to name new objects
    @param scale: float, general scale of the rig
    @param translateTo: str, reference object for control position
    @param rotateTo: str, reference object for control orientation
    @param parent: str, object to be parent of new control
    @param shape: str, controller shape type
    @param lockChannels: list(str), list of channels on control to be locked and non-keyable
    @param jnt: str, joint name to be used to identify its parent
    @return: None
    """
    # print("hello")
    # return
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

    # if prefix.startswith('L_') or "Left" in ctrlShapes: # for naming convention and coloring based on that
    #     [ mc.setAttr( s + '.ovc', 6)  for s in ctrlShapes ] #ovc= override color, 6 = blue

    # elif prefix.startswith('R_') or "Right" in ctrlShapes:
    #     [ mc.setAttr( s +'.ovc', 13 )  for s in ctrlShapes ] #13 = red

    # else:
    #     [ mc.setAttr( s + '.ovc', 22)  for s in ctrlShapes ] #22 = yellow

    # translate control

    if mc.objExists( translateTo ):
        mc.delete(mc.pointConstraint( translateTo, ctrlOffset ) )

    # rotate control

    if mc.objExists( rotateTo ):
        # mc.delete(mc.orientConstraint( rotateTo, ctrlOffset ) )
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

def find_parent(jnt):
    """
    Find the parent of the current joint

    @param jnt: str, name of the joint who's parent needs to be searched/identified 
    """
    # this will identify the parent of the joint
    parents = mc.ls(jnt, long=True)[0].split('|')
    # print(jnt, parents, len(parents))
    if parents != [] and len(parents) > 2:
        parents.reverse()
        # print(jnt, parents[1])
        return parents[1]
    else:
        # print(jnt, parents[0])
        return parents[0]
    

# def find_child(jnt):
#     """
#     Find the parent of the current joint

#     @param jnt: str, name of the joint who's parent needs to be searched/identified 
#     """
#     # if no child, then use parent's. If more than 1 child, then use general y-up, If 1 child, then point towards it.
#     child_jnt = mc.listRelatives(jnt)
#     # print(child_jnt)
#     if child_jnt == None:
#         child_jnt_len = 0
#     else:
#         child_jnt_len = len(child_jnt)
#     # print(child_jnt_len)
#     if child_jnt_len == 1:
#         return child_jnt[0]
#     # elif child_jnt_len > 1:
#     #     return jnt #should point up in world if it is pointing to itself?
#     elif child_jnt_len == 0: # i.e., if child_jnt == None, No child then use the same direction as its parent or itself?
#         return jnt
#     else:

#         return '' #str(temp_circle)


def parent_constraint_control_to_jnt(ctrl_name, jnt):
    """
    Parent constraint controllers to respective joints

    @param ctrl_name: str, name of the newly created controller
    @param jnt: str, name of the joint who will be parent constrained to above controller 
    """
    # print("parent_constraint_control_to_jnt")
    mc.parentConstraint(ctrl_name, jnt, mo=True)

def controller_hierarchy(parent_of_jnt, ctrlOffsetName):
    if parent_of_jnt == '':
        pass
    else:
        # print(parent_of_jnt)
        parent_of_jnt_prefix = parent_of_jnt.split("m_avg_")[-1]    
        mc.parent(ctrlOffsetName, parent_of_jnt_prefix + '_ctrl')

# #-------------------------------------------------------------------------------#
# #-------------------- CALL CONTROL CREATION FUNCTION ---------------------------#
# #-------------------------------------------------------------------------------#

# # select joints
# selected_joints = mc.ls(sl=True, type='joint')
# # selected_joints = mc.listRelatives('m_avg_root', ad=True, type='joint') # this doesn't work because of sequence order
# # temp_circle = mc.circle( n = 'temp_ctrl', ch = False, normal = [0,1,0], radius = 1.0 )[0] #ch = channel history
# # mc.setAttr(str(temp_circle)+ '.translateY', 200)

# for jnt in selected_joints:
#     # get the name for control
#     ctrl_name_prefix = jnt.split("m_avg_")[-1]
#     print()
#     print('-----------------------------------------')
#     # print(ctrl_name_prefix)

#     # identify rotateTo joint, basically the child joint
    
#     # rotateTo_jnt = find_child(jnt)
#     # print("Rotate To for " + jnt + " joint = " + str(rotateTo_jnt))

#     # create controls. passing below parameters -
#                 # prefix = 'new', 
#                 # scale = 1.0, 
#                 # translateTo = '',
#                 # rotateTo = '',
#                 # parent = '',
#                 # shape = 'circle',
#                 # lockChannels = ['s','v']
    
#     ctrl_name, ctrlOffsetName = create_controls( prefix=ctrl_name_prefix, scale=20.0, 
#                     translateTo=jnt, rotateTo=jnt, 
#                     parent="", shape='circleY', lockChannels=[])
    
#     # find the parent and parent the offset control to its parent control similar to joint hierarchy
#     parent_of_jnt = find_parent(jnt)

#     # parent respective controllers hierarchy, similar to joint hierarchy
#     controller_hierarchy(parent_of_jnt, ctrlOffsetName)    
    
#     # parent constraint the controllers to respective joint
#     parent_constraint_control_to_jnt(ctrl_name, jnt)


# mc.delete(temp_circle)
    

#---------------------------------------------------------------------------------#
#                 CALLING THE CONTROL AUTORIG TOOL
#---------------------------------------------------------------------------------#
if __name__ == "__main__":

    try:
        ControlAutorig.close(ControlAutorigUI)
        ControlAutorig.deleteLater()
    except:
        pass

    ControlAutorigUI = ControlAutorig()
    ControlAutorigUI.show()