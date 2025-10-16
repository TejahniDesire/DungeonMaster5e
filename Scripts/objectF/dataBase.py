import copy
import re
import numpy as np 
import gc
from . import pyHelper
from ..metaF import directoryCrawler 

def saveLayeredDiction(dict,string=''):

    for key in dict.keys():
        saveLayeredDiction(dict[key])
    
stopLine = '#$#*@@!!!'

class DataBasePage:

    def __init__(self):
        self.pages = {}

    def readPage(self,dir):
        txt = open(dir)
        HeadViewer = ViewerDict(file_dir=dir)
        lines = txt.readlines()
        last = lines[-1]
        l=0
        current_line = lines[l]
        last_order = None
        keylist= []
        repeat_orders = {}
        while stopLine not in current_line:
            
            skip_conditions = [
                current_line[0] == '#',
                current_line.isspace()
            ]
            if True in skip_conditions:
                l += 1
                current_line = lines[l]
                continue

            if ';' in current_line:
                tparts = current_line.split(';')
                hasStopMarker = tparts[-1].isspace() 

            else:
                hasStopMarker = False
            if not hasStopMarker:
                l += 1
                current_line += lines[l]
                continue
            
            if HeadViewer.getValue() is None:
                HeadViewer.setValue(current_line.split(';')[0].strip())
                l += 1
                current_line = lines[l]
                continue
            #_____________________________
            
            line_parts = current_line.split("<x>")
            if len(line_parts) > 2:
                raise ValueError("Multiple '<x>' splitters detected at line {}, maybe you missed a ';'?".format(l + 1))
            line_parts[1] = line_parts[1].split(';')[-2]
            current_order = line_parts[0].count('&')
            key = '&' * current_order
            if last_order is not None:  # first appearence of lowest (most general) order

                if current_order > last_order: # this entry is a child of the last
                    repeat_orders[key] = 1
                    last_order = current_order
                    keylist += [key]
                    HeadViewer.recursiveSet(keylist,line_parts[1])

                elif current_order == last_order: # this entry is a sibling of the last
                    repeat_orders[key] += 1
                    last_order = current_order
                    keylist[len(keylist)-1] = key + str(repeat_orders[key])
                    HeadViewer.recursiveSet(keylist,line_parts[1])

                elif current_order < last_order: # this entry is of a more general order than the last
                    repeat_orders[key] += 1
                    last_order = current_order

                    new_keylist= []
                    for subkey in keylist: # find the first entry in the keylist that is younger than the current order
                        cleaned_string = re.sub(r'\d+', '', subkey)
                        sub_order = len(cleaned_string)
                        if current_order > sub_order:
                            new_keylist += [subkey]
                            
                        else: # younger entry found
                            if repeat_orders[key] > 1:
                                suffix = repeat_orders[key]
                            else:
                                suffix = ''
                            new_keylist += [key + str(suffix)]
                            break
                    keylist = new_keylist
                    
                    HeadViewer.recursiveSet(keylist,line_parts[1])
            else:
                repeat_orders[key] = 1
                last_order = current_order
                keylist += [key]
                HeadViewer.recursiveSet(keylist,line_parts[1])
            #_____________________________
            
            l += 1
            current_line = lines[l]

        page_key = pyHelper.name_to_key(HeadViewer.getValue())

        if page_key in self.pages.keys():
            raise ValueError("Page with existing title detected")
        self.pages[page_key] = HeadViewer
        HeadViewer.allItemsOfDepth()
        print("Page '{}' successfully read.".format(HeadViewer.getValue()))

    def getPage(self,title):
        title = pyHelper.name_to_key(title)
        return self.pages[title]
    
    def combinePages(self,pageList):
        if len(pageList) < 2:
            raise ValueError("Need 2 or more pages to combine")
        
        combinedPage = ViewerDict()
        i = 0
        for page in pageList:
            inputKey = str(i+1)
            combinedPage[inputKey] = self.getPage(page)
            combinedPage[inputKey].setParent(combinedPage)
            combinedPage[inputKey].setKey(inputKey)
            i += 1

        combinedPage.allItemsOfDepth() 
        return combinedPage
    
    def AddPage(self,str_diction,title, file_dir,replace_old=False):
        HeadViewer = convertStrDict(str_diction,title=title,file_dir=file_dir)
        page_key = pyHelper.name_to_key(HeadViewer.getValue())

        if (page_key in self.pages.keys()) and (not replace_old):
            raise ValueError("Page with existing title detected")
        self.pages[page_key] = HeadViewer
        HeadViewer.allItemsOfDepth()
        print("Page '{}' successfully Created.".format(HeadViewer.getValue()))


    def writePage(self,title):
        page = self.getPage(title=title)
        
        string = page.recursiveCodePrint()
        directoryCrawler.createTxtFile(page.getFileDir(),string,True)
        
def convertStrDict(str_diction,title=None,higherdict=None,order=1,file_dir=None,keylist=None):
    if higherdict is None:
        if title is None: raise ValueError("Title must be given at start of recersion")
        higherdict = ViewerDict(value=title,file_dir=file_dir)
        keylist = []
    i = 0
    if type(str_diction) is dict:
        for current_value in str_diction.keys():
            current_dict = str_diction[current_value]
            new_key = '&' * order
            if i > 0: new_key += str(i+1)
            higherdict.recursiveSet(keylist + [new_key],ViewerDict(value=current_value,key=new_key))
            convertStrDict(current_dict,higherdict=higherdict,order=order + 1,file_dir=file_dir,keylist=keylist + [new_key])
            i += 1
    return higherdict

class ViewerDict:

    def __init__(self,value=None,key=None,header=None,parent=None,file_dir=None):
        if key is None:
            self.isHead = True
        else:
            self.isHead = False
        self.value = value
        self.key=key
        self.header = header
        self.parent=parent

        self.dictionary = {}
        self.depth_dict = {} # set by allItemsOfDepth
        self.clean_depth_dict = {} # set by allItemsOfDepth
        self.viewers_of_depth = {}

        if file_dir is not None:
            file_dir= file_dir.strip()
            text_dir = file_dir.split('/')[-1]
            folder_dir = file_dir[:len(file_dir)-len(text_dir)]
        else:
            text_dir = None
            folder_dir = None
        self.dirs = {
            'text_dir': text_dir,
            'folder_dir': folder_dir
        }

    def keys(self):
        return self.dictionary.keys()
    
    def getFolderDir(self):
        if self.dirs['folder_dir'] is None:
            raise KeyError("This ViewerDict has no folder directory. Maybe try asking its parent?")
        return self.dirs['folder_dir']
    
    def getTextDir(self):
        if self.dirs['folder_dir'] is None:
            raise KeyError("This ViewerDict has no text file directory. Maybe try asking its parent?")
        return self.dirs['text_dir']
    
    def getFileDir(self):
        return self.getFolderDir() + self.getTextDir()

    def getValue(self):
        return self.value
    
    def getHeader(self):
        return self.header
    
    def getAllParents(self,keylist=None,parentList=None):
        if keylist is None:
            keylist = []
            parentList = []
        
        keylist += [self.key]
        parentList += [self]


        if self.parent is None:
            del keylist[-1]
            return np.flip(keylist),np.flip(parentList)
        else:
            return self.parent.getAllParents(keylist=keylist,parentList=parentList)
        
    def setFolderDir(self,folder_dir):
        self.dirs['folder_dir'] = folder_dir

    def setTextDir(self,text_dir):
        self.dirs['text_dir'] = text_dir

    def setFileDir(self,file_dir):
        file_dir= file_dir.strip()
        text_dir = file_dir.split('/')[-1]
        folder_dir = file_dir[:len(file_dir)-len(text_dir)]

        self.dirs = {
            'text_dir': text_dir,
            'folder_dir': folder_dir
        }
    
    def setValue(self,value):
        self.value = value
    
    def setParent(self,parent):
        self.parent = parent

    def setKey(self,key):
        self.key = key

    def setHeader(self,header):
        self.header = header

    # ALL RECURSION {----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def recursiveCopy(self,pastViewer=None):
        if pastViewer is None: # beginning of recursion
            pastViewer = ViewerDict(self.getValue(),self.key,self.header,self.parent)
        else: 
            pastViewer.setKey(self.key)
            pastViewer.setValue(self.getValue())
            pastViewer.setHeader(self.header)
            pastViewer.setParent(self.parent)
        for key in self.keys():
            pastViewer[key] = ViewerDict()
            self[key].recursiveCopy(pastViewer = pastViewer[key])

        return pastViewer        

    def recursiveSet(self,keyList,value):
        keyList = keyList.copy()
        key = keyList[0]
        del keyList[0]
        if len(keyList) == 0:
            self[key] = value
            gc.collect()
            return
        else:
            
            self[key].recursiveSet(keyList,value)

    def recursiveStringPrint(self,depth=0,string=''):
        pre_text_type = ['number','letter','LETTER'][depth % 3]
        tabSize = 6
        if self.key is None:
            current_string = string
            depth = depth - 1
        else:
            key = self.key

            numbers_only = re.sub(r'\D', '', str(key))
            if len(numbers_only) == 0:
                numbers_only = 1
            number = int(numbers_only)

            if len(string) != 0:
                string += '\n'
            text = str(self.value)
            notebook_order = noteBookOrder(number,type=pre_text_type) + ') '
            text = text.replace( '\n', '\n' + depth * tabSize * ' ' + len(notebook_order) * ' ' )

            current_string = string + depth * tabSize * ' ' + notebook_order + text

        if len(list(self.keys())) ==0:
            return current_string
        else:
            for key in self.keys():
                current_string = self[key].recursiveStringPrint(depth = depth + 1, string = current_string)
        return current_string
        
    def recursiveValueList(self,desired_depth=0,current_depth=0,clean=False,use_depth_dict_if_possible=True):
        
        if desired_depth < 0:
            raise ValueError("Desired depth must be atleast 0")
        if current_depth > desired_depth:
            raise ValueError("Current Depth exceeds desired depth")
        
        if (len(self.depth_dict.keys()) == 0) or (not use_depth_dict_if_possible): 
            
            if current_depth == desired_depth:
                keysValues = []
                viewers = []
                for key in self.keys():
                    keysValues += [self[key].getValue()]
                    viewers += [self[key]]
                return keysValues,viewers
            else:
                finalKeyList = []
                viewers = []
                for key in self.keys():
                    finalKeyList_i,viewrs_i = self[key].recursiveValueList(desired_depth=desired_depth,current_depth=current_depth + 1,use_depth_dict_if_possible=use_depth_dict_if_possible)
                    finalKeyList += finalKeyList_i
                    viewers += viewrs_i
                return finalKeyList,viewers
        else:
            if clean:
                values = self.clean_depth_dict[desired_depth] 
            else:
                values = self.depth_dict[desired_depth]
            
            return values, self.viewers_of_depth[desired_depth]
        
    def recursiveCodePrint(self,string=''):
        if self.key is None:
            string += self.getValue() + ';\n'
        else:
            string += pyHelper.keep_only_char(self.key,'&') + '<x>' + self.getValue() + ';\n'
        for key in self.keys():
            string = self[key].recursiveCodePrint(string = string)

        if self.key is None:
            string += stopLine
        return string


    # } ALL RECURSION END ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def allItemsOfDepth(self):
        depth = 0
        depth_dict = {}

        values_of_depth=[]
        i = 0
        while ((i == 0) or (len(values_of_depth) != 0)):
            values_of_depth,viewers = self.recursiveValueList(desired_depth=depth,use_depth_dict_if_possible=False)
            self.viewers_of_depth[depth] =viewers
            if (len(values_of_depth) !=0) and type(values_of_depth[0]) is ViewerDict:
                values_of_depth_name = []
                
                for value in values_of_depth:
                    values_of_depth_name += [value.getValue()]
                values_of_depth = values_of_depth_name 
            depth_dict[depth] = values_of_depth
            depth += 1
            i += 1
        del depth_dict[depth-1]
        del self.viewers_of_depth[depth-1]
        self.depth_dict = depth_dict
        max_depth = depth - 2

        for i in range(max_depth + 1):
            cleanValueList = []
            for entry in self.depth_dict[i]:
                cleanValueList += [pyHelper.name_to_key(entry)]
            self.clean_depth_dict[i] = cleanValueList

    def searchValueOfDepth(self,query,depth):
        values,viewers = self.recursiveValueList(desired_depth = depth,clean=True)
        matches = pyHelper.regexSearch(query,values)
        if len(matches) == 1:
            matching_viewers = [viewers[values.index(matches[0])]]

        else:
            matching_viewers = []
            for match in matches:
                matching_viewers += [viewers[values.index(match)]]
        return matches,matching_viewers
    
    # Built-in ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def __getitem__(self,key):
        if type(key) == int:
            key = list(self.keys())[key]
        return self.dictionary[key]

    # def __setitem__(self, key, value_header):
    def __setitem__(self, key, value):
        # if type(value_header) is not tuple:
        #     value = value_header
        #     header = None
        # else:
        #     value = value_header[0]
        #     header = value_header[1]
        
        # self.dictionary[key] = ViewerDict(value=value,key=key,header=header)
        if type(value) is ViewerDict:
            self.dictionary[key] = value
            self.dictionary[key].setKey(key)
            self.dictionary[key].setParent(self)
        else:
            self.dictionary[key] = ViewerDict(value=value,key=key,parent=self)

    def __str__(self):
        string = ''
        
        if self.header is not None:
            string += '"{}" with '.format(self.header)
        else:
            string += "ViewerDict with "

        if self.value is not None:
            string += 'value "{}", and '.format(self.value)
        
        string += '"{}" entries'.format(len(self.dictionary))
        return string
        
    def __repr__(self):
        return str(self)
        

# class ViewerList:

#     def __init__(self,viewer_list=None):
#         self.ValueDict = {}
#         if viewer_list is None:
#             self.list = []
#         else: 
#             self.list = viewer_list
#             self.updateDict()

#         # self.HeaderDict = {}


#     def updateDict(self):
#         self.ValueDict = {}
#         # self.HeaderDict = {}

#         for viewer in self.list:
#             # header = viewer.getHeader()
#             value = str(viewer.getValue())
#             self.ValueDict[suffixDepth(self.ValueDict.keys(),value)] = viewer

#     def __getitem__(self,name,returnViewList=False):
#         if type(name) is int:
#             return self.list[name]
#         elif type(name) is str:
#             return self.ValueDict[name]
#         elif type(name) is list or type(name) is tuple:
#             returnList = []
#             for runname in name:
#                 returnList += [self.ValueDict[runname]]

#             if returnViewList==True:
#                 returnList = ViewerList(returnList)

#             return returnList
        
    
#     def __str__(self):

#         string = 'Viewer list: \n'
#         for viewer in self.list:
#             string += '  ' + str(viewer.getValue()) + '\n'
#         return string
    
#     def __repr__(self):
#         return str(self)
        


def suffixDepth(list,key,depth = 0):

    if depth == 0:
        tkey = key
    else:
        tkey = key + "({})".format(depth)
    if tkey in list:
        return suffixDepth(list,key,depth + 1)

    else:
        if depth == 0:
            return key
            
        else:
            return tkey
        

def noteBookOrder(number,type):
    if type == 'number':
        return str(number)
    else:
        return numberToLetter(number,capital= type=='LETTER')


def numberToLetter(number,capital=False):

    if number > 26:
        suffix = str(int(number / 26))
        number = number % 26
    else:
        suffix = ''

    if capital: 
        string = chr(ord('@')+number) + suffix
    else:
        string = chr(ord('`')+number) + suffix
    return string 
    