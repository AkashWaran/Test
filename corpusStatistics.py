import wx
import os
import nltk
from nltk.collocations import * 
from nltk.tag.stanford import NERTagger

class NLP(wx.Frame):

    data = ""
    tokens = []
    bigrams = []
    namedict = {}
    search_criteria = []

    def __init__(self, parent, title):
        super(NLP, self).__init__(parent, title=title, 
            size=(500, 450)) 
        self.InitUI()
        self.Centre()
        self.Show()     

    def ProcessFile(self, path) :
	self.data = open(path,'r').read()
	f = open('Smart.English.stop') 
	stopwords = filter(None, f.read().split('\n'))
	f.close();
	self.tokens = [item for item in nltk.word_tokenize(self.data) if item not in stopwords]
	self.bigrams = BigramCollocationFinder.from_words(self.tokens).score_ngrams(nltk.collocations.BigramAssocMeasures().raw_freq)
	st = NERTagger('./stanford-ner-2014-10-26/classifiers/english.all.3class.distsim.crf.ser.gz', './stanford-ner-2014-10-26/stanford-ner.jar')
	self.namedict.update(st.tag(self.tokens))

    def SelectFile(self, event) :
	wildcard = "All files (*.*)|*.*"
	dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
	if dialog.ShowModal() == wx.ID_OK:
	    self.ProcessFile(dialog.GetPath())
	dialog.Destroy()

    def ViewWords(self, event) :
	print self.tokens
	self.tc.SetValue(', '.join(self.tokens))

    def ViewBigrams(self, event) :
	print self.bigrams
	self.tc.SetValue(', '.join("(%s,%s)" % tup for tup in self.bigrams))

    def ShowOrHideTitle(self, event) :
	sender = event.GetEventObject()
	label = sender.GetLabel()
	if (label == "People") :
	    value = "PERSON"
	elif (label == "Organizations") :
	    value = "ORGANIZATION"
	else :
	    value = "LOCATION"
	isChecked = sender.GetValue()
	if isChecked:
	    self.search_criteria.append(value)
	else: 
	    self.search_criteria.remove(value)

    def ViewNames(self, event) :
	result = ""
	for word, val in self.namedict.items():
	    if val in self.search_criteria:
		result = result + " " + word
	print result
	self.tc.SetValue(result)

    def SearchPhrase(self, event) :
	message = ""
	if self.tc2.GetValue().lower() in self.data.lower() :
	    message = "Phrase / word present in document"
	else :
	    message = "Phrase / word not present in document"
	print message
	self.tc.SetValue(message)

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
	browseFile = wx.Button(panel, label="Select File or Directory of Files to Process")
        browseFile.Bind(wx.EVT_BUTTON, self.SelectFile)
	hbox2.Add(browseFile, flag=wx.ALIGN_CENTER)
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

	cb1 = wx.CheckBox(panel, label='People')
        cb1.SetFont(font)
	cb1.Bind(wx.EVT_CHECKBOX, self.ShowOrHideTitle)
        vbox1.Add(cb1)
	vbox1.Add((-1, 10))
        
        cb2 = wx.CheckBox(panel, label='Organizations')
        cb2.SetFont(font)
	cb2.Bind(wx.EVT_CHECKBOX, self.ShowOrHideTitle)
        vbox1.Add(cb2)
	vbox1.Add((-1, 10))

        cb3 = wx.CheckBox(panel, label='Locations')
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
    NLP(None, title='Go To Class')
    app.MainLoop()
