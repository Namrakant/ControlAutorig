# ADVANCED ***************************************************************************
# content = assignment
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
#************************************************************************************

"""
CUBE CLASS

1. CREATE an abstract class "Cube" with the functions:
   translate(x, y, z), rotate(x, y, z), scale(x, y, z) and color(R, G, B)
   All functions store and print out the data in the cube (translate, rotate, scale and color).

2. ADD an __init__(name) and create 3 cube objects.

3. ADD the function print_status() which prints all the variables nicely formatted.

4. ADD the function update_transform(ttype, value).
   "ttype" can be "translate", "rotate" and "scale" while "value" is a list of 3 floats.
   This function should trigger either the translate, rotate or scale function.

   BONUS: Can you do it without using ifs?

5. CREATE a parent class "Object" which has a name, translate, rotate and scale.
   Use Object as the parent for your Cube class.
   Update the Cube class to not repeat the content of Object.

"""

#---------------------------------------------------------------------------------#
#  CLASS OBJECT
#---------------------------------------------------------------------------------#
class Object:
    def __init__(self):
        self.name       = "Cube1"
        self.translate_x  = 1
        self.translate_y  = 1
        self.translate_z  = 1
        self.rotate_x     = 10
        self.rotate_y     = 10
        self.rotate_z     = 10
        self.scale_x      = 2
        self.scale_y      = 2
        self.scale_z      = 2
        self.color_r      = 255
        self.color_g      = 0
        self.color_b      = 255
        print("Super class object!")

#---------------------------------------------------------------------------------#
#  CLASS CUBE
#---------------------------------------------------------------------------------#
class Cube(Object):
    def __init__(self):
        super(Cube, self).__init__()
      #   self.name       = name

    def translate(self, translate_x, translate_y, translate_z):
        self.translate_x = translate_x
        self.translate_y = translate_y
        self.translate_z = translate_z
      #   print("Translate (x,y,z) = ({}, {}, {})".format(translate_x, translate_y, translate_z))

    def rotate(self, rotate_x, rotate_y, rotate_z):
        self.rotate_x = rotate_x
        self.rotate_y = rotate_y
        self.rotate_z = rotate_z
      #   print("Rotate    (x,y,z) = ({}, {}, {})".format(rotate_x, rotate_y, rotate_z))

    def scale(self, scale_x, scale_y, scale_z):
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.scale_z = scale_z
      #   print("Scale     (x,y,z) = ({}, {}, {})".format(scale_x, scale_y, scale_z))

    def color(self, color_r, color_g, color_b):
        self.color_r = color_r
        self.color_g = color_g
        self.color_b = color_b
      #   print("Color     (R,G,B) = ({}, {}, {})".format(color_r, color_g, color_b))

    def print_status(self):
        print("\nName = ", self.name)
      #   self.translate(self.translate_x, self.translate_y, self.translate_z)
      #   self.rotate(self.rotate_x, self.rotate_y, self.rotate_z)
      #   self.scale(self.scale_x, self.scale_y, self.scale_z)
      #   self.color(self.color_r, self.color_g, self.color_b)
        print("Translate (x,y,z) = ({}, {}, {})".format(self.translate_x, self.translate_y, self.translate_z))
        print("Rotate    (x,y,z) = ({}, {}, {})".format(self.rotate_x, self.rotate_y, self.rotate_z))
        print("Scale     (x,y,z) = ({}, {}, {})".format(self.scale_x, self.scale_y, self.scale_z))
        print("Color     (R,G,B) = ({}, {}, {})".format(self.color_r, self.color_g, self.color_b))
    
    def update_transform(self, ttype, value):
        """
        ttype : String : translate, rotate, scale, color
        value : float  : (x,y,z) 
        """
        if ttype == "translate":
            self.translate(value[0], value[1], value[2])
        if ttype == "rotate":
            self.rotate(value[0], value[1], value[2])
        if ttype == "scale":
            self.scale(value[0], value[1], value[2])
        if ttype == "color":
            self.color(value[0], value[1], value[2])

#---------------------------------------------------------------------------------#
#  CALLING METHODS
#---------------------------------------------------------------------------------#

# cube5 = Cube("Cube5")

# cube5.translate(1,2,3)
# cube5.rotate(10, 20, 30)
# cube5.scale(2,2,2)
# cube5.color(255, 0, 255)

# cube5.print_status()
# value = [12, 23, 34]
# cube5.update_transform("translate", value)
# cube5.update_transform("rotate", value)
# cube5.update_transform("scale", value)
# cube5.print_status()

cubeParent = Cube()
cubeParent.print_status()

cube2 = Cube()
cube2.name = "Cube2"
translate_value = [12, 23, 34]
cube2.update_transform("translate", translate_value)
rotate_value = [120, 230, 340]
cube2.update_transform("rotate", rotate_value)
scale_value = [3, 3, 3]
cube2.update_transform("scale", scale_value)
color_value = [0, 255, 0]
cube2.update_transform("color", color_value)
cube2.print_status()