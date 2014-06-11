# Home/config/sublime-text-2/Packages/Ilpaijin

import sublime, sublime_plugin, os, re, threading, codecs
from os.path import basename

#
# AutoimportSignature Command
#
class AutoimportSignatureCommand(sublime_plugin.TextCommand):
    """ 
    Command class for importing signature from implements and extends keyword in php
    """

    def run(self, edit):    

        word = self.view.word(self.view.sel()[0]) #only single cursor, hence [0] the first
        keyword = self.view.substr(word)
        rawline = self.view.substr(self.view.line(word))
        currentFile = self.view.file_name()
        topFolder = self.view.window().folders()[0]
        self.selector = Selector()
        self.CP = CurrentPage(currentFile, self.selector)

        #
        # read and parse the selection

        self.selector.parseUserSelection(rawline);

        filepaths = self.CP.generateFilepath(self.selector.userSelection)
        
        filepathsList = []

        if os.path.isfile(filepaths) and os.access(filepaths, os.R_OK):
            filepathsList.append(self.CP.addContractPage(ContractPage(filepaths))) 
        else:    
            filepathsList = self.recursive_search_file(topFolder, filepaths[(filepaths.rfind("/")+1):])  

        if not len(filepathsList):
            return AutoimportError.fatal("No file found within current folders (starting from root: "+topFolder+" )")  
        
        #
        # Insert the signatures
        self.view.insert(edit, self.view.full_line(self.view.sel()[-1]).end() + 1, self.CP.getOutput(topFolder))

        #
        #dialog referenced file
        if sublime.ok_cancel_dialog("Do you want me to open (new tab) the referenced file?"):    
            self.view.window().open_file(filepathsList[0])
        

    def recursive_search_file(self, targetDir, targetFile, filesList = []):

        for files in os.listdir(targetDir):

            dirfile = os.path.join(targetDir, files)

            if os.path.isfile(dirfile):
                filename = dirfile[(dirfile.rfind("/")+1):]

                if filename == targetFile:
                    filesList.append(self.CP.addContractPage(ContractPage(os.path.join(targetDir,filename))))      

            elif os.path.isdir(dirfile):
                self.recursive_search_file(dirfile, targetFile, filesList)   

        return filesList        


#
# Selector class
#
class Selector:
    """ This class is responsible to elaborate the selection captured and to make the correct filepaths ready for autoimporting """

    _validKeywords = ["implements", "extends"]

    userSelection = ""

    def parseUserSelection(self, line):

        selectionTokens = self.tokenizeSelection(line)
        
        if (set(selectionTokens) & set(self._validKeywords)):
            self.userSelection = selectionTokens[3]
        else:
            return AutoimportError.fatal("No keyword or keyword not valid")  

    def tokenizeSelection(self, line):
        return re.findall(re.compile('\s*(\w+[\\\\\w+]+)'),line)    


#
# CurrentPage class
#
class CurrentPage():
    """ The calling page, where the user make the selection """
    
    file = ""
    namespacedRoot = ""
    alias = ""
    ext = ".php"
    declaredMethods = ""

    def __init__(self, file, selector):
        self.file = file
        self.selector = selector

    def addContractPage(self, contractPage):
        self.contractPage = contractPage 
    
    def generateFilepath(self, selection):
        for line in codecs.open(self.file, encoding='utf8'):
            if "namespace" in line:
                self.namespacedRoot = re.findall(re.compile('namespace\s+(.*?);'),line)[0]    
            if "use" in line:
                useTokens = re.findall(re.compile('\s*(\w+[\\\\\w*]*)'),line)
                self.alias = useTokens[3]
                used = useTokens[1]
                if alias == keyword:
                    selection = used.replace(self.namespacedRoot+'\\', "")
            elif ("require" in line) or ("require_once" in line) or ("include" in line):
                filenameTokens = re.findall(re.compile('\"(.*?)'+self.ext+'\"'),line)[0]
                selection = filenameTokens  

        return self.formatFilepath(selection)

    def formatFilepath(self, sel):
        return os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(self.file)), sel.replace("\\", "/") + self.ext))            

    def getDeclaredMethods(self):
        return self.setDeclaredMethods()

    def setDeclaredMethods(self):
        if not self.declaredMethods:
            with open(self.file, 'r') as content_file:
                content = content_file.read()
                self.declaredMethods = re.findall('(\w+\s+function\s+\w+[\(|\s+])', content)

        return self.declaredMethods               

    def getOutput(self, topFolder):         
        output = "";  

        autoimportMethods = self.contractPage.getMethods()  

        for method in range(0, len(autoimportMethods)):
            newMethod = """
    /**
     * @link """+self.contractPage.file.replace(topFolder, "")+"""
     * @see """+self.selector.userSelection+"""
     */
    """ + autoimportMethods[method][0:-1] + """
    {
        //Do something
    }
            """

            alreadyDeclared = """
    // ***WARNING*** Method \""""+autoimportMethods[method][0:-1]+"""\" already declared
            """

            if autoimportMethods[method] in self.getDeclaredMethods():
                output += alreadyDeclared
            else:
                output += newMethod

        return output        


#
# ContractPage class
#
class ContractPage():
    """ Should be created for each contract defined by the user """

    file = ""
    autoimportMethods = []

    def __init__(self, file):
        self.file = file

    def getMethods(self):
        
        if not self.autoimportMethods:
            self.setMethods()

        return self.autoimportMethods            

    def setMethods(self):
        # for file in filepathsList:
        with open(self.file, 'r') as content_file:
            content = content_file.read()
            self.autoimportMethods = re.findall('(\w+\s+function\s+\w+[\(|\s+])', content)    


#
# Error class
#
class AutoimportError:
    @staticmethod
    def fatal(str):
        print "AutoimportSignature: " + str;
        return