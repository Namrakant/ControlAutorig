# ADVANCED ***************************************************************************
# content = assignment
#
# date    = 2022-08-07
# email   = contact@alexanderrichtertd.com
#************************************************************************************


"""
0. CONNECT the decorator "print_process" with all sleeping functions.
   Print START and END before and after.

   START *******
   main_function
   END *********


1. Print the processing time of all sleeping functions.
END - 00:00:00


2. PRINT the name of the sleeping function in the decorator.
   How can you get the information inside it?

START - long_sleeping

"""


import time
from datetime import datetime

#*********************************************************************
# DECORATOR
def print_process1(func):
    def wrapper(*args, **kwargs):
        startTime = datetime.now()
        print("START TIME: {}".format(datetime.now()) )
        func(args)                  # main_function
        print("END TIME: {}".format(datetime.now()) )

        functionName = func.__name__
        processingTime = (datetime.now() - startTime).total_seconds()
        print("Processing Time of function '{}' is {} seconds".format(functionName, processingTime))
    return wrapper

# DECORATOR
def print_process2(func):
    def wrapper(*args, **kwargs):
        startTime = datetime.now()
        print("START TIME: {}".format(datetime.now()) )
        func()                  # main_function
        print("END TIME: {}".format(datetime.now()) )

        functionName = func.__name__
        processingTime = (datetime.now() - startTime).total_seconds()
        print("Processing Time of function '{}' is {} seconds".format(functionName, processingTime))
    return wrapper


#*********************************************************************
# FUNC
@print_process1
def short_sleeping(name):
    time.sleep(.1)
    print(name)

@print_process2
def mid_sleeping():
    time.sleep(2)

@print_process2
def long_sleeping():
    time.sleep(4)

short_sleeping("so sleepy")
mid_sleeping()
long_sleeping()