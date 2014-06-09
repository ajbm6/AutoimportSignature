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

        print("*****************************************************************************") 
        word = self.view.word(self.view.sel()[0]) #only one cursor, hence [0] the first
        scope = self.view.scope_name(word.begin()).strip()
        extracted_scope = scope.rpartition('.')[2]
        keyword = self.view.substr(word)
        line = self.view.substr(self.view.line(word))

        # print("word",word)
        # print("keyword",keyword)
        # print("line", line)

        nsKeyword = re.compile('\s*(\w+\\\\'+keyword+'|'+keyword+'\\\\\w+)')

        match = re.findall(nsKeyword,line)

        if match:
            print match[0]


        file_lines = codecs.open(self.view.file_name(), encoding='utf8')
        for line in file_lines:
            if "require_once" in line:
                print (line)
            else:
               print('no require')     

        # self.view.window().open_file(keyword+"."+extracted_scope)
        
        # self.view.insert(edit, 0, keyword)


