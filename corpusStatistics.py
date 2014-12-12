import wx
import os
import nltk
import threading
from nltk.collocations import * 
from nltk.tag.stanford import NERTagger

stopwords = []

class NLPFile(threading.Thread) :
    def __init__(self, path) :
	super(NLPFile, self).__init__()
	self.name = path
	self.word_dict = {}
	self.ProcessFile()

    def ProcessFile(self) :
	self.t = threading.Thread(target = self.ProcessFileInThread)
	self.t.start()

    def ProcessFileInThread(self) :
	global lock
	lock.acquire()
	global bigramMeasure
	global tagger
	f = open(self.name, 'r')
	self.data = f.read()
	f.close()
	self.tokens = [item for item in nltk.word_tokenize(self.data) if item not in stopwords]
	self.bigrams = BigramCollocationFinder.from_words(self.tokens).score_ngrams(bigramMeasure.raw_freq)
	self.word_dict.update(tagger.tag(self.tokens))
	lock.release()

    def ProcessingComplete(self) :
	global lock
	lock.acquire()
	lock.release()
	return True

    def PrintName(self) :
	if self.ProcessingComplete() :
	    return self.name

    def PrintTokens(self) :
	if self.ProcessingComplete() :
	    return ', '.join(self.tokens)

    def PrintBigrams(self) :
	if self.ProcessingComplete() :
	    return ', '.join("(%s,%s)" % tup for tup in self.bigrams)

    def PrintMatches(self, criteria) :
	if self.ProcessingComplete() :
	    result = ""
	    for word, val in self.word_dict.items():
		if val in criteria:
		    result = result + word + " "
	    return result

    def SearchPhrase(self, value) :
	if self.ProcessingComplete() :
	    if value in self.data.lower() :
		message = "Phrase / word present in document"
	    else :
		message = "Phrase / word not present in document"
	    return message

class NLP(wx.Frame):

    def __init__(self, parent, title):
        super(NLP, self).__init__(parent, title=title, size=(500, 450)) 
	self.InitParams()
        self.InitUI()
        self.Centre()
        self.Show()     

    def InitParams(self) :
	f = open('Smart.English.stop') 
	stopwords = filter(None, f.read().split('\n'))
	f.close();
	global lock
	lock = threading.Lock()
	global bigramMeasure
	global tagger
	bigramMeasure = nltk.collocations.BigramAssocMeasures()
	tagger = NERTagger('./stanford-ner-2014-10-26/classifiers/english.all.3class.distsim.crf.ser.gz', './stanford-ner-2014-10-26/stanford-ner.jar')
	self.search_criteria = []
	self.NLPFileList = []

    def ProcessFile(self, path) :
	self.NLPFileList.append(NLPFile(path))

    def ProcessDir(self, path) :
	self.NLPFileList[:] = []
	for files in os.listdir(path) :
	    if files.endswith(".txt") :
		self.ProcessFile(os.path.join(path,files))

    def SelectFile(self, event) :
	wildcard = "All files (*.*)|*.*"
	dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
	if dialog.ShowModal() == wx.ID_OK:
	    self.ProcessFile(dialog.GetPath())
	dialog.Destroy()

    def SelectDir(self, event) :
	dlg = wx.DirDialog(None, "Choose a directory:")
	if dlg.ShowModal() == wx.ID_OK:
	    self.ProcessDir(dlg.GetPath())
	dlg.Destroy()

    def ViewWords(self, event) :
	self.tc.SetValue("PRINTING TOKENS")
	for f in self.NLPFileList :
	    self.tc.AppendText("\n\n----------------------------------------------------------")
	    self.tc.AppendText("\n"+f.PrintName())
	    self.tc.AppendText("\n\n"+f.PrintTokens())

    def ViewBigrams(self, event) :
	self.tc.SetValue("PRINTING BIGRAMS")
	for f in self.NLPFileList :
	    self.tc.AppendText("\n\n----------------------------------------------------------")
	    self.tc.AppendText("\n"+f.PrintName())
	    self.tc.AppendText("\n\n"+f.PrintBigrams())

    def ShowOrHideTitle(self, event) :
	sender = event.GetEventObject()
	label = sender.GetLabel()
	isChecked = sender.GetValue()
	if isChecked:
	    self.search_criteria.append(sender.GetName())
	else: 
	    self.search_criteria.remove(sender.GetName())

    def ViewNames(self, event) :
	self.tc.SetValue("PRINTING MATCHES")
	for f in self.NLPFileList :
	    self.tc.AppendText("\n\n----------------------------------------------------------")
	    self.tc.AppendText("\n"+f.PrintName())
	    self.tc.AppendText("\n\n"+f.PrintMatches(self.search_criteria))

    def SearchPhrase(self, event) :
	self.tc.SetValue("PRINTING SEARCH RESULTS")
	for f in self.NLPFileList :
	    self.tc.AppendText("\n\n----------------------------------------------------------")
	    self.tc.AppendText("\n"+f.PrintName())
	    self.tc.AppendText("\n\n"+f.SearchPhrase(self.tc2.GetValue().lower()))

    def InitUI(self): 
        panel = wx.Panel(self)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Explore Text with Corpus Statistics')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.ALIGN_CENTER)
        vbox.Add(hbox1, flag=wx.ALIGN_CENTER|wx.TOP, border=10)
        
	vbox.Add((-1, 10))

	hbox2 = wx.BoxSizer(wx.HORIZONTAL)
	browseFile = wx.Button(panel, label="Select File to Process")
        browseFile.Bind(wx.EVT_BUTTON, self.SelectFile)
	hbox2.Add(browseFile, flag=wx.ALIGN_CENTER)

	browseDir = wx.Button(panel, label="Select Directory to Process")
	browseDir.Bind(wx.EVT_BUTTON, self.SelectDir)
	hbox2.Add(browseDir, flag=wx.ALIGN_CENTER)
        vbox.Add(hbox2, flag=wx.ALIGN_CENTER|wx.TOP, border=10)
        
	vbox.Add((-1, 10))

	hbox3 = wx.BoxSizer(wx.HORIZONTAL)

	vbox1 = wx.BoxSizer(wx.VERTICAL)
	viewWordsBtn = wx.Button(panel, label="View Words")
        viewWordsBtn.Bind(wx.EVT_BUTTON, self.ViewWords)
	viewBigramsBtn = wx.Button(panel, label="View Bigrams")
        viewBigramsBtn.Bind(wx.EVT_BUTTON, self.ViewBigrams)
	viewNamesBtn = wx.Button(panel, label="View Names")
        viewNamesBtn.Bind(wx.EVT_BUTTON, self.ViewNames)

	vbox1.Add(viewWordsBtn, flag=wx.ALIGN_CENTER)
	vbox1.Add((-1, 10))

	vbox1.Add(viewBigramsBtn, flag=wx.ALIGN_CENTER)
	vbox1.Add((-1, 10))

	vbox1.Add(viewNamesBtn, flag=wx.ALIGN_CENTER)
	vbox1.Add((-1, 10))

	cb1 = wx.CheckBox(panel, label='People', name='PERSON')
        cb1.SetFont(font)
	cb1.Bind(wx.EVT_CHECKBOX, self.ShowOrHideTitle)
        vbox1.Add(cb1)
	vbox1.Add((-1, 10))
        
        cb2 = wx.CheckBox(panel, label='Organizations', name='ORGANIZATION')
        cb2.SetFont(font)
	cb2.Bind(wx.EVT_CHECKBOX, self.ShowOrHideTitle)
        vbox1.Add(cb2)
	vbox1.Add((-1, 10))

        cb3 = wx.CheckBox(panel, label='Locations', name='LOCATION')
        cb3.SetFont(font)
	cb3.Bind(wx.EVT_CHECKBOX, self.ShowOrHideTitle)
        vbox1.Add(cb3)
	vbox1.Add((-1, 10))

	searchPhraseBtn = wx.Button(panel, label="Search for Phrase")
        searchPhraseBtn.Bind(wx.EVT_BUTTON, self.SearchPhrase)
	self.tc2 = wx.TextCtrl(panel)
	vbox1.Add(searchPhraseBtn, flag=wx.ALIGN_CENTER)
	vbox1.Add((-1, 10))
	
	vbox1.Add(self.tc2, flag=wx.ALIGN_CENTER)
	vbox1.Add((-1, 10))

        hbox3.Add(vbox1, flag=wx.ALIGN_LEFT|wx.TOP, border=10)
	
        self.tc = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        hbox3.Add(self.tc, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=25)
	
        vbox.Add((-1, 25))

        panel.SetSizer(vbox)

if __name__ == '__main__':
    #/usr/lib/jvm/jdk1.8.0_25/jre/bin/java
    print "In order to run this program you will need jdk version 1.8. In case the path is not set then please enter it here (q to skip this in case environment variables are already set) : "
    java_path = raw_input()
    if java_path != 'q' :
        os.environ['JAVAHOME'] = java_path
    app = wx.App()
    NLP(None, title='Corpus Statistics')
    app.MainLoop()
