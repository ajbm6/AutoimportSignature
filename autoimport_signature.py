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

        print("word",word)
        print("keyword",keyword)
        print("line", line)

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


#
# Method Class
#
class Method:
    """
    Method class
    """

    _name = ""

    _signature = ""

    _filename = ""

    def __init__(self, name, signature, filename):
        self._name = name
        self._filename = filename;
        self._signature = signature

    def name(self):
        return self._name

    def signature(self):
        return self._signature

    def filename(self):
        return self._filename

#
# Signature
#
class Signature:
    """
    Signature class
    """

    _functions = []

    MAX_WORD_SIZE = 100
    MAX_FUNC_SIZE = 50

    def clear(self):
        self._functions = []

    def addFunc(self, name, signature, filename):
        self._functions.append(Method(name, signature, filename))

    def get_autocomplete_list(self, word):
        autocomplete_list = []
        for method_obj in self._functions:
            if word in method_obj.name():
                method_str_to_append = method_obj.name() + '(' + method_obj.signature()+ ')'
                method_file_location = method_obj.filename();
                autocomplete_list.append((method_str_to_append + '\t' + method_file_location,method_str_to_append)) 
        return autocomplete_list


def is_php_file(filename):
    return '.php' in filename

#
# Signature Collector
#
class SignatureCollector(Signature, sublime_plugin.EventListener):
    """
    Base class for all GitHub commands. Handles getting an auth token.
    """

    _collector_thread = None

    def on_post_save(self, view):
        self.clear()
        open_folder_arr = view.window().folders()

        if self._collector_thread != None:
            self._collector_thread.stop()
        self._collector_thread = SignatureCollectorThread(self, open_folder_arr, 30)        
        self._collector_thread.start()

    def on_query_completions(self, view, prefix, locations):
        current_file = view.file_name()
        completions = []
        if is_php_file(current_file):
            return self.get_autocomplete_list(prefix)
            completions.sort()
        return (completions,sublime.INHIBIT_EXPLICIT_COMPLETIONS)    

#
# Signature Collector Thread
#
class SignatureCollectorThread(threading.Thread):

    def __init__(self, collector, open_folder_arr, timeout_seconds):  
        self.collector = collector
        self.timeout = timeout_seconds
        self.open_folder_arr = open_folder_arr
        threading.Thread.__init__(self)

    def save_method_signature(self, file_name):
        # file_lines = open(file_name, "r", "utf-8")
        file_lines = codecs.open(file_name, encoding='utf8')
        for line in file_lines:
            print("linea", line)
            # if "function" in line:
            #     matches = re.search('(\w+)\s*[: | =]\s*function\s*\((.*)\)', line)
            #     matches2 = re.search('function\s*(\w+)\s*\((.*)\)', line)
            #     if matches != None and (len(matches.group(1)) < self.collector.MAX_FUNC_SIZE and len(matches.group(2)) < self.collector.MAX_FUNC_SIZE):
            #         self.collector.addFunc(matches.group(1), matches.group(2), basename(file_name))
            #     elif matches2 != None and (len(matches2.group(1)) < self.collector.MAX_FUNC_SIZE and len(matches2.group(2)) < self.collector.MAX_FUNC_SIZE):
            #         self.collector.addFunc(matches2.group(1), matches2.group(2), basename(file_name))

    def get_php_files(self, dir_name, *args):
        fileList = []
        for file in os.listdir(dir_name):
            dirfile = os.path.join(dir_name, file)
            if os.path.isfile(dirfile):
                fileName, fileExtension = os.path.splitext(dirfile)
                if fileExtension == ".php" and ".min." not in fileName:
                    fileList.append(dirfile)
            elif os.path.isdir(dirfile):
                fileList += self.get_php_files(dirfile, *args)
        return fileList

    def run(self):
        for folder in self.open_folder_arr:
            phpfiles = self.get_php_files(folder)
            for file_name in phpfiles:
                self.save_method_signature(file_name)

    def stop(self):
        if self.isAlive():
            self._Thread__stop()
            