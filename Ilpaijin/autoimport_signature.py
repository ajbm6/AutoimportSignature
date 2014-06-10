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

        # print("*****************************************************************************") 
        word = self.view.word(self.view.sel()[0]) #only single cursor, hence [0] the first
        scope = self.view.scope_name(word.begin()).strip()
        extracted_scope = scope.rpartition('.')[2]
        keyword = self.view.substr(word)
        line = self.view.substr(self.view.line(word))
        triggerFile = codecs.open(self.view.file_name(), encoding='utf8')

        # print("word",word)
        # print("keyword",keyword)
        # print("line", line)

        # nsContract = re.compile('\s*(\w+\\\\'+keyword+'|'+keyword+'\\\\\w+)')
        contractTokens = re.findall(re.compile('\s*(\w+[\\\\\w+]+)'),line)
        whiteKeywords = ["implements", "extends"]
        
        if (set(contractTokens) & set(whiteKeywords)):
            nsContract = contractTokens[3]
        else:
            print "AutoimportSignature: No keyword or keyword not valid";
            return;                     

        for line in triggerFile:
            if "namespace" in line:
                nsTokens = re.findall(re.compile('namespace\s+(.*?);'),line)  
                namespace = nsTokens[0]              
            if "use" in line:

                useTokens = re.findall(re.compile('\s*(\w+[\\\\\w*]*)'),line)

                if useTokens[3] == keyword:
                    nsContract = useTokens[1].replace(namespace+'\\', "")
                    break   
            elif ("require" in line) or ("require_once" in line) or ("include" in line):
                filenameTokens = re.findall(re.compile('\"(.*?)\.php\"'),line)
                nsContract = filenameTokens[0]  

        currentDir = os.path.realpath(self.view.file_name())

        filepaths = os.path.join(os.path.dirname(currentDir), nsContract.replace("\\", "/") + ".php")
        filepathsList = []

        if os.path.isfile(filepaths) and os.access(filepaths, os.R_OK):
            filepathsList.append(filepaths) 
        else:    
            filepathsList = self.recursive_search_file(self.view.window().folders()[0], filepaths[(filepaths.rfind("/")+1):])

        # Interface methods    
        for file in filepathsList:
            with open(file, 'r') as content_file:
                content = content_file.read()
                autoimportMethods = re.findall('(\w+\s+function\s+\w+[\(|\s+])', content)
        
        # current file methods            
        with open(self.view.file_name(), 'r') as content_file:
            content = content_file.read()
            declaredMethods = re.findall('(\w+\s+function\s+\w+[\(|\s+])', content)                


        outputMethods = "";    

        for method in range(0, len(autoimportMethods)):
            newMethod = """
    /**
     * @link """+filepaths.replace(self.view.window().folders()[0], "")+"""
     * @see """+nsContract+"""
     */
    """ + autoimportMethods[method][0:-1] + """
    {
        //Do something
    }
            """

            alreadyDeclared = """
    // ***WARNING*** Method \""""+autoimportMethods[method][0:-1]+"""\" already declared
            """

            if autoimportMethods[method] in declaredMethods:
                outputMethods += alreadyDeclared
            else:
                outputMethods += newMethod

        
        self.view.insert(edit, self.view.full_line(self.view.sel()[-1]).end() + 1, outputMethods)

        if sublime.ok_cancel_dialog("Do you want me to open (new tab) the referenced file?"):    
            self.view.window().open_file(filepaths)
        

        
        # self.view.insert(edit, 0, keyword)

    def recursive_search_file(self, targetDir, targetFile, filesList = []):

        for files in os.listdir(targetDir):

            dirfile = os.path.join(targetDir, files)

            if os.path.isfile(dirfile):
                filename = dirfile[(dirfile.rfind("/")+1):]

                if filename == targetFile:
                    filesList.append(os.path.join(targetDir,filename))      

            elif os.path.isdir(dirfile):
                self.recursive_search_file(dirfile, targetFile, filesList)   

        return filesList        

