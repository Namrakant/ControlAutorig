# STYLE ***************************************************************************
# content = assignment
#
# date    = 2024-02-11
# email   = contact@alexanderrichtertd.com
#************************************************************************************

# original: logging.init.py

import os

#---------------------------------------------------------------------------------#
# This function finds the caller
#---------------------------------------------------------------------------------#
def findCaller(self):
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """
    currentFrame = currentframe()

    #On some versions of IronPython, currentframe() returns None if
    #IronPython isn't run with -X:Frames.

    if currentFrame is not None:
        currentFrame = currentFrame.frame_back   # changing the names would break the code, so I would update it in the source file as well

    returnValue = "(unknown file)", 0, "(unknown function)"

    while hasattr(currentFrame, "frame_code"):
        currentFrameCode = currentFrame.frame_code                     
        filename = os.path.normcase(currentFrameCode.currentFrameCode_filename)   

        if filename == _srcfile:
            currentFrame = currentFrame.frame_back
            continue

        returnValue = (currentFrameCode.currentFrameCode_filename, currentFrame.frame_lineno, currentFrameCode.currentFrameCode_name) 

        break

    return returnValue

# How can we make this code better?
