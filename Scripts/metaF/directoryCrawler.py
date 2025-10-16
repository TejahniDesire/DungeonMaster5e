import os
import re
import subprocess
import sys
import shutil
from os import listdir
from os.path import isfile, join

import numpy as np


def createSubDirectory(path_chosen,purpose:str = '',kill_policy=False,silent_nothing=False):
    isDir = os.path.exists(path_chosen)
    if kill_policy:
        if isDir:

            print("Subdirectory for " + purpose + " '{}' already exist, removing...".format(path_chosen))

            existing_file = os.listdir(path_chosen)
            if len(existing_file) == 0:
                print("Empty directory, removing...")
                os.rmdir(path_chosen)
            else:
                print("Not empty directory, removing...")
                shutil.rmtree(path_chosen)

            os.makedirs(path_chosen)
            print("A Subdirectory for " + purpose + " '{}' was created".format(path_chosen))
        else:
            os.makedirs(path_chosen)
            print("A Subdirectory for " + purpose + " '{}' was created".format(path_chosen))

    else:
        if not isDir:
            os.makedirs(path_chosen)
            print("A Subdirectory for " + purpose + " '{}' was created".format(path_chosen))
        else:
            if silent_nothing != True: print("Subdirectory for " + purpose + " '{}' already exist, doing nothing".format(path_chosen))

def createTxtFile(path_chosen,text='',kill_policy=False,policy='x'):
    """_summary_

    Args:
        path_chosen (_type_): _description_
        text (str, optional): _description_. Defaults to ''.
        purpose (str, optional): _description_. Defaults to ''.
        kill_policy (bool, optional): _description_. Defaults to False.
        policy (str, optional): x=write only if file doesnt exist, a=append to end.
    """
    isTxt = os.path.exists(path_chosen)
    if kill_policy:
        if isTxt:
            print("Text File Already Exist, Deleting...")
            os.remove(path_chosen)
        with open(path_chosen, 'x') as file:
            file.write(text)
            print("File '{}' created".format(path_chosen))
    else:
        with open(path_chosen, 'a') as file:
            file.write(text)
        
        if isTxt:
            print("File '{}' appended to".format(path_chosen))
        else:
            print("File '{}' created".format(path_chosen))
