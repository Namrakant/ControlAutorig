# STYLE ***************************************************************************
# content = assignment (Python Advanced)
#
# date    = 2024-02-11
# email   = contact@alexanderrichtertd.com
#**********************************************************************************

import maya.cmds as mc

#---------------------------------------------------------------------------------#
# Set the color of controllers using this function
#---------------------------------------------------------------------------------#
def set_color(ctrlList=None, color=None):
    
    for ctrlName in ctrlList:
        try:
            mc.setAttr(ctrlName + 'Shape.overrideEnabled', 1)
        except:
            pass

        try:
            color_mapping = {1:4, 2:13, 3:25, 4:17, 5:17, 6:15, 7:6, 8:16}
            for key, value in color_mapping.items():
                if color == key:
                    mc.setAttr(ctrlName + 'Shape.overrideColor', value)
                    break
        except:
            pass


# EXAMPLE
# set_color(['circle','circle1'], 8)
