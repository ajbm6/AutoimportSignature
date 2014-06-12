# Home/config/sublime-text-2/Packages/Ilpaijin

import sublime, sublime_plugin, os, re, threading
from os.path import basename
from random import randint

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
        filepathsList = []

        #
        # read and parse the selection

        self.selector.parseUserSelection(rawline);

        filepaths = self.CP.generateFilepath(self.selector.userSelection)

        if os.path.isfile(filepaths) and os.access(filepaths, os.R_OK):
            self.CP.addContractPage(ContractPage(filepaths))
        else:    
            self.recursive_search_file(topFolder, filepaths[(filepaths.rfind("/")+1):], filepathsList)  
        
        filepathsList.append(self.CP.contractPage)     
        
        if not len(filepathsList):
            return AutoimportError.fatal("No file found within current folders (starting from root: "+topFolder+" )")  

        #
        # Insert the signatures
        self.view.insert(edit, self.view.full_line(self.view.sel()[-1]).end() + 1, self.CP.getOutput(topFolder))

        #
        #dialog referenced file
        if sublime.ok_cancel_dialog("Do you want me to open (new tab) the referenced file?"):    
            self.view.window().open_file(filepathsList[0].file)
        

    def recursive_search_file(self, targetDir, targetFile, filesList = []):
        for files in os.listdir(targetDir):

            dirfile = os.path.join(targetDir, files)

            if os.path.isfile(dirfile):
                filename = dirfile[(dirfile.rfind("/")+1):]

                if filename == targetFile:
                    self.CP.addContractPage(ContractPage(os.path.join(targetDir,filename)))    

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
    declaredMethods = []
    output = ""

    def __init__(self, file, selector):
        self.file = file
        self.selector = selector

    def addContractPage(self, contractPage):
        self.contractPage = contractPage 
    
    def generateFilepath(self, selection):
        with open(self.file, 'r') as content_file:
            content = content_file.read()
            for line in content:
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
                methodsFound = re.findall('(\w+\s+function\s+\w+\s?\(.*\))', content)  
  
            for method in methodsFound:
                self.declaredMethods.append(Method(method))    

        return self.declaredMethods               

    def getOutput(self, topFolder):          
        aiMethods = self.contractPage.getMethods()
        dMethods = self.getDeclaredMethods()

        self.output += """
    /***************************
    ***** BEGIN AUTOIMPORT """ +self.selector.userSelection+ """ *****
    ***************************/
    """

        for method in range(0, len(aiMethods)):

            signature = aiMethods[method].visibility + " function " + aiMethods[method].fnName + "(" + ', '.join(aiMethods[method].params) + ")"

            newMethod = """
    /**
     * @link """+self.contractPage.file.replace(topFolder, "")+"""
     * @see """+self.selector.userSelection+"""
     */
    """ + signature + """
    {
        //Do something
    }
            """

            fnNameAlreadyDeclared = """
    // ***WARNING*** Method \""""+aiMethods[method].fnName+"""\" already declared
            """

            missingParams = """
    // ***WARNING*** The correct signature is: """ + signature + """
    """

            exists = 0
            for dMethod in dMethods:
                if aiMethods[method].fnName == dMethod.fnName:
                    self.output += fnNameAlreadyDeclared
                    exists = 1
                    same = set(aiMethods[method].params) - set(dMethod.params)
                    if same:
                        self.output += missingParams
                        break
            
            if not exists:
                self.output += newMethod

        self.output += """
    /*************************
    ***** END AUTOIMPORT *****
    *************************/
    """

        return self.output        


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
            methodsFound = re.findall('(\w+\s+function\s+\w+\s?\(.*\))', content)  

            for method in methodsFound:
                self.autoimportMethods.append(Method(method))

#
# Method class
#
class Method():
    def __init__(self, signature):
        signature = signature 
        visibility = ""
        fnName = ""
        params = []
        self.parseSignature(signature)

    def parseSignature(self, signature):
        self.visibility, null, self.tokenName = signature.split(" ", 2)
        self.fnName = self.tokenName.split("(")[0]
        self.params = re.findall("\((.*)\)?", self.tokenName[0:-1])[0].split(",")

        self.params = [w.strip() for w in self.params]

        print self.params
        return


#
# Error class
#
class AutoimportError:
    @staticmethod
    def fatal(str):
        print "AutoimportSignature: " + str;
        return