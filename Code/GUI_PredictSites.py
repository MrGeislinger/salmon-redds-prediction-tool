#!/usr/bin/python

import wx
from importData import *
from predictSitesGeneral import fit_data

# Create a left panel
class LeftPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
        #
        self.calculateReddPercent

        # Get  encompassing window
        self.parentFrame = parent.GetParent()
        # Get the results panel from the main
        self.resultsPanel = self.parentFrame.resultsPanel
        # Set size
        # self.SetSize((500,500))

        ##List of class varaibles
        self.dropMenuSelected = ''
        self.varDict = {}
        self.siteData = []
        self.percentRedds = []
        self.alpha = []

        # Set Fonts
        titleFont = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        titleFont.SetPointSize(24)
        subTitleFont = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        subTitleFont.SetPointSize(16)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(12)
        # Set vertical sizer
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # Set title box of panel
        titleHbox = wx.BoxSizer(wx.HORIZONTAL)
        titleStr = wx.StaticText(self, -1, 'Work With Data:')
        titleStr.SetFont(titleFont)
        titleHbox.Add(titleStr, 0)
        self.vbox.Add(titleHbox, 0, wx.CENTER | wx.TOP, 10)
        self.vbox.Add((-1,10))

        ## Create horizonatl sizer for `Import` sub-title
        importSubTitleHbox = wx.BoxSizer(wx.HORIZONTAL)
        # Sub-title to the right of text field
        importSubTitleStr = wx.StaticText(self, -1, 'Import Data:')
        importSubTitleStr.SetFont(subTitleFont)
        importSubTitleHbox.Add(importSubTitleStr, 0, wx.RIGHT, 8)
        self.vbox.Add(importSubTitleHbox, 0, wx.EXPAND|
                                             wx.LEFT|
                                             wx.RIGHT|
                                             wx.TOP,
                                             10)

        ## Create horizontal sizer for importing data template
        dataTemplateLocHbox = wx.BoxSizer(wx.HORIZONTAL)
        # Text field for data template file to import
        self.dataTemplateTc = wx.TextCtrl(self,
                                          -1,
                                          value = #Default path to data template
                                            '/Users/victorgeislinger/Dropbox/'+
                                            'Desktop_Groups/Projects/Thesis/'+
                                            'Salmon/simulation/'+
                                            'regression.14.06.01/'+
                                            'data_mod.2104.06.01/'+
                                            'templateTest.csv')
        dataTemplateLocHbox.Add(self.dataTemplateTc, 1)
        # Add to overall sizer
        self.vbox.Add(dataTemplateLocHbox,
                      0,
                      wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
                      10)
        ## Create h-sizer for the browse buttons
        templateBtnHbox = wx.BoxSizer(wx.HORIZONTAL)
        # Button for browsing
        browseForTemplateBtn = wx.Button(self, -1, 'Browse for Data Template')
        # Give proper spacing
        templateBtnHbox.Add(browseForTemplateBtn, 0)
        # Add to the overall vertical sizer
        self.vbox.Add(templateBtnHbox,
                      0,
                      wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
                      10)

        ## Create horizontal sizer for importing data text field
        dataFileLocHbox = wx.BoxSizer(wx.HORIZONTAL)
        # Text field for data file to import
        self.dataFileTc = wx.TextCtrl(self,
                                      -1,
                                      value = #Default path to site data
                                        '/Users/victorgeislinger/Dropbox/'+
                                        'Desktop_Groups/Projects/Thesis/'+
                                        'Salmon/simulation/'+
                                        'regression.14.06.01/'+
                                        'data_mod.2104.06.01/siteTest.csv')
        dataFileLocHbox.Add(self.dataFileTc, 1)
        # Add to overall sizer
        self.vbox.Add(dataFileLocHbox,
                      0,
                      wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
                      10)

        ## Create h-sizer for the import buttons
        importBtnHbox = wx.BoxSizer(wx.HORIZONTAL)
        # Buttons for import
        browseForFileBtn   = wx.Button(self, -1, 'Browse for Data File')
        importSubmitBtn   = wx.Button(self, -1, 'Import Data Now')
        # Give proper spacing
        importBtnHbox.Add(browseForFileBtn, 0)
        importBtnHbox.Add(importSubmitBtn, 0, wx.LEFT | wx.BOTTOM , 5)
        # Add to the overall vertical sizer
        self.vbox.Add(importBtnHbox,
                      0,
                      wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
                      10)
        # Add spacing
        self.vbox.Add((-1, 30))

        ## For checkboxes (regression vs. function fit)

        ## Function fitter
        funcFitSubTitleHbox = wx.BoxSizer(wx.HORIZONTAL)
        # Sub-title above text field
        funcFitSubTitleStr = wx.StaticText(self, -1, 'Function To Fit:')
        funcFitSubTitleStr.SetFont(subTitleFont)
        funcFitSubTitleHbox.Add(funcFitSubTitleStr, 0, wx.RIGHT, 8)
        self.vbox.Add(funcFitSubTitleHbox,
                      0,
                      wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
                      10)
        ## Create horizontal sizer for function fitting
        funcFitHbox = wx.BoxSizer(wx.HORIZONTAL)
        # Before text field, place string to the left
        self.funcFitXequals = wx.StaticText(self, -1, 'x  = ')
        self.funcFitXequals.SetFont(font)
        funcFitHbox.Add(self.funcFitXequals, 0, wx.RIGHT, 8)
        # Text Field
        self.funcFitTc = wx.TextCtrl(self, -1)
        # Default function to fit
        self.funcFitTc.SetValue('x+a[0]*(x*a[1]*v[5]+x**(a[2]+1)+x*a[3]*v[6])')
        funcFitHbox.Add(self.funcFitTc, 1)
        # Add to overall sizer
        self.vbox.Add(funcFitHbox,
                      0,
                      wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
                      10)
        self.vbox.Add((-1, 15))


        ## Drop-down menu to choose percent of redds constructed
        dropMenuSubTitleHbox = wx.BoxSizer(wx.HORIZONTAL)
        # Subtitle
        dropMenuSubTitleStr = wx.StaticText(self,
                                            -1,
                                            'Select For Percentage of '+
                                            'Redds Constructed:')
        dropMenuSubTitleStr.SetFont(subTitleFont)
        dropMenuSubTitleHbox.Add(dropMenuSubTitleStr, 0, wx.RIGHT, 8)
        # Drop-down menus
        dropMenuHbox = wx.BoxSizer(wx.HORIZONTAL)
        # ComboBox (see pg.86 of wxPython tutorial )
        # Example of dropdown values (use event to do this)
        exList = ['v1: "Gravel Volume (m^3)"', 'v2: "Vegetation Cover"']
        self.dropMenu = wx.ComboBox(self, -1, choices=exList, style=wx.CB_READONLY)
        dropMenuHbox.Add(self.dropMenu)
        # Add to overall sizer
        self.vbox.Add(dropMenuSubTitleHbox,
                      0,
                      wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
                      10)
        self.vbox.Add(dropMenuHbox,
                      0,
                      wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
                      10)
        self.vbox.Add((-1, 15))



        ## Variables selection
        varSelectSubTitleHbox = wx.BoxSizer(wx.HORIZONTAL)
        # Sub-title above text field
        varSelectSubTitleStr = wx.StaticText(self, -1, 'Variables available:')
        varSelectSubTitleStr.SetFont(subTitleFont)
        varSelectSubTitleHbox.Add(varSelectSubTitleStr, 0, wx.RIGHT, 8)

        ## Button array of variables
        self.varButtonArrayVbox = wx.BoxSizer(wx.VERTICAL)

        # Add to overall sizer
        self.vbox.Add(varSelectSubTitleHbox,
                      0,
                      wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        self.vbox.Add(self.varButtonArrayVbox,
                      0,
                      wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        self.vbox.Add((-1, 15))

        # Perform fit button
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        performFitBtn = wx.Button(self, -1, 'Perform Fit')
        hbox5.Add(performFitBtn, 0)
        self.vbox.Add(hbox5, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)

        ## Number of fit parameters
        self.fitParamNumHbox = wx.BoxSizer(wx.HORIZONTAL)
        # Sub-title above text field
        fitParamNumSubTitleStr = wx.StaticText(self,
                                               -1,
                                               'Number of Fit Parameters:')
        fitParamNumSubTitleStr.SetFont(subTitleFont)
        self.fitParamNumHbox.Add(fitParamNumSubTitleStr, 0, wx.RIGHT, 8)
        # Select the number of fit parameters
        self.fitParamNumSc = wx.SpinCtrl(self,
                                         -1,
                                         '0',
                                         size=(40, -1),
                                         initial=0,
                                         min=0)
        self.fitParamNumHbox.Add(self.fitParamNumSc, 0, wx.LEFT, 10)
        # Add to overall sizer
        self.vbox.Add(self.fitParamNumHbox,
                      0,
                      wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
                      10)
        self.vbox.Add((-1, 10))

        ## Button array of parmeters
        self.varParamArrayVbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.varParamArrayVbox,
                      0,
                      wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
                      10)
        self.vbox.Add((-1, 10))


        # add actions to buttons
        # self.Bind(wx.EVT_BUTTON, self.OnClose, id=closeBtn.GetId())
        self.Bind(wx.EVT_BUTTON,
                  self.OnPerformFit,
                  id=performFitBtn.GetId())
        # Set button when data file is submitted
        self.Bind(wx.EVT_BUTTON,
                  self.OnImportData,
                  id=importSubmitBtn.GetId())
        # Set button for browsing for data file
        self.Bind(wx.EVT_BUTTON,
                  self.OnFindImportFile,
                  id=browseForFileBtn.GetId())
        # Set button for browsing for data template
        self.Bind(wx.EVT_BUTTON,
                  self.OnFindTemplateFile,
                  id=browseForTemplateBtn.GetId())
#         # Set event for drop down menu select
#         self.varSelectDropMenu.Bind(wx.EVT_COMBOBOX, self.OnComboSelect)
        # Set event when the number of fit parameters increase/decrease
        self.Bind(wx.EVT_SPINCTRL, self.OnParamNumSelect)

        self.SetSizer(self.vbox)
        self.Centre()
        self.Show(True)


    def OnClose(self,event):
        self.Close()

    def OnParamNumSelect(self,event):
        # Get value of parameter number
        n = self.fitParamNumSc.GetValue()
        # Reset the alpha parameter
        self.alpha = [0] * n
        # Clear previous set up
        self.varParamArrayVbox.Clear(True) #delete_windows=True
        # Create buttons and text fields (small)
        for i in range(n):
            # Title of button
            titleStr = 'a[%d]' %i
            # Temporary horizonatl box
            tempHbox = wx.BoxSizer(wx.HORIZONTAL)
            # Add button to screen
            tempHbox.Add(wx.Button(self, label=titleStr),0,wx.ALL,5)
            # Add some text
            tempHbox.Add(wx.StaticText(self, -1,'='),0,wx.ALL,5)
            # Save
            alphaValue = wx.TextCtrl(self,-1,value="0.5")
            # Save in array as a number
            self.alpha[i] = alphaValue
            # Add text field (small)
            tempHbox.Add(alphaValue,0,wx.ALL,5)
            self.varParamArrayVbox.Add(tempHbox,0,wx.ALL,5)


        # Refresh the frame
        self.parentFrame.hbox.Layout()
        self.parentFrame.Fit()


#     # Add chosen varaible from drop down menu to the fit function
#     def OnComboSelect(self,event):
#         # Get selected item from drop menu
#         self.dropMenuSelected = self.varSelectDropMenu.GetValue()
#         # use just the varaible name
#         chosenVar = self.varDict[self.dropMenuSelected]
#         # Insert in fit function at cursorx
#         self.funcFitTc.WriteText(chosenVar)

    # Add chosen variable from button to the fit function
    def OnVarSelect(self,event):
        # Get variable name from button
        varSelected = event.GetEventObject().name
        # use just the varaible name
        chosenVar = varSelected
        # Insert in fit function at cursor
        self.funcFitTc.WriteText(chosenVar)

    # Choose import file through browser
    def OnFindImportFile(self,evet):
        # Create file browser dialog
        dialog = wx.FileDialog( self,
                                "Choose some files...",
                                "~", #default directory
                                "",
                                "",
                                wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            path = str(dialog.GetPath())
        dialog.Destroy()
        # Set file string to location
        self.dataFileTc.SetValue(path)

    # Choose template file through browser
    def OnFindTemplateFile(self,event):
        # Create file browser dialog
        dialog = wx.FileDialog( self,
                                "Choose some files...",
                                "~", #default directory
                                "",
                                "",
                                wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            path = str(dialog.GetPath())
        dialog.Destroy()
        # Set file string to location
        self.dataTemplateTc.SetValue(path)


    #
    def CreateButton(self,name,title):
        # Vertical box encompassing title and button
        buttonVbox = wx.BoxSizer(wx.VERTICAL)
        # Button title (above button)
        buttonTitle = wx.StaticText(self, -1, title+':')
        buttonVbox.Add(buttonTitle, 0, wx.CENTER, 8)
        # Button
        newButton = wx.Button(self, label=name)
        newButton.name = name
        self.Bind(wx.EVT_BUTTON, self.OnVarSelect, id=newButton.GetId())
        buttonVbox.Add(newButton, 0, wx.CENTER, 8)
        #
        return buttonVbox


    # Sets data for redds constructed percentage
    def calculateReddPercent(posReddNum,posReddTotal):
        ## TEST - Must choose this later
        # redds constructed at site
        constRedds = [self.siteData[0][posReddNum]]
        ## Breaking down the parts
        riverRedds = [self.siteData[0][posReddTotal]]
        # save empty fields with the proper length that will be zipped below
        self.percentRedds = [None] * max( len(riverRedds), len(constRedds) )

        #
        i = 0
        # save percents into the empty array
        for (riverRedd,constRedd) in zip(riverRedds,constRedds):
            percentReddsTemp = [ float(x)/float(y)
                                 for x,y in zip(constRedd,riverRedd) ]
            self.percentRedds[i] = percentReddsTemp
            i+=1


    # Perform actions to import data
    def OnImportData(self,event):
        from importData import importData
        from regressionAnalysis import noneDataAction
        # Get the file name from list
        fileName     = self.dataFileTc.GetValue()
        templateName = self.dataTemplateTc.GetValue()
        # Get values from files
        (keys, values) = importData(fileName,templateName);
        # # Choose action on how to convert from `None`
        # noneActionChosen = "convertToZero"
        # sites = noneDataAction[noneActionChosen]([values])

        ##ADDITION
        # Just renaming for easier reading in function
        self.siteData = [values]

        self.calculateReddPercent(4,3)

        # ## TEST - Must choose this later
        # ## Breaking down the parts
        # riverRedds = [self.siteData[0][3]]
        # # redds constructed at site
        # constRedds = [self.siteData[0][4]]
        # # save empty fields with the proper length that will be zipped below
        # self.percentRedds = [None] * max( len(riverRedds), len(constRedds) )
        #
        # #
        # i = 0
        # # save percents into the empty array
        # for (riverRedd,constRedd) in zip(riverRedds,constRedds):
        #     percentReddsTemp = [ float(x)/float(y)
        #                          for x,y in zip(constRedd,riverRedd) ]
        #     self.percentRedds[i] = percentReddsTemp
        #     i+=1

        # Create new parameter list (just for this time `t`)
        # If only one parameter for each time, make it a list (list within list)
        if type(self.siteData[0]) != type([]):
            values = [values]
        # List of tuples with each tuple for that time
        # Note the smallest list size is the standard size for new list
        self.siteData = zip(*values)

        ##ADDITION

        ## Set varaibles names in dictionary
        i = 0
        # Reset the dictionary
        self.varDict = {}
        for key in keys:
            # Add variable name by description (variable name then details)
            #self.varDict['%d-%s' %(i,key)] = 'v[%d]' %i
            self.varDict['v[%d]' %i] = '%d-%s' %(i,key)
            i += 1
        # Add details
        varNames = self.varDict.keys()
        varNames.sort()
        #self.varSelectDropMenu.SetItems(varNames)


        # self.siteData = values

        # Reset the button array
        self.varButtonArrayVbox.Clear(True) #delete_windows=True
        # Initial horizontal sizer to put in varButtonArrayVbox
        varButtonArrayRow = wx.BoxSizer(wx.HORIZONTAL)
        # Add variables as buttons in an array
        counter = 0
        for varName in varNames:
            # Get rid of position part of string
            titleStr = self.varDict[varName][2:]
            buttonVbox = self.CreateButton(varName,titleStr)
            # After every third button, form a new row
            if (counter%3 == 0):
                # Add (completed) row to the vertical sizer (button array)
                self.varButtonArrayVbox.Add(varButtonArrayRow, 0, wx.ALL, 5)
                # Make new row
                varButtonArrayRow = wx.BoxSizer(wx.HORIZONTAL)
            # Add to button to row
            varButtonArrayRow.Add(buttonVbox, 0, wx.ALL, 10)
            counter += 1
        # Add leftover in row
        self.varButtonArrayVbox.Add(varButtonArrayRow, 0, wx.ALL, 5)

        # Refresh the frame
        self.parentFrame.hbox.Layout()
        self.parentFrame.Fit()


    # Performs fit after button press
    def OnPerformFit(self,event):
        # Set to show results
        self.parentFrame.showResults = True

        # Get Fit Function
        functString = self.funcFitTc.GetValue()
        # Define function
        def fitEq(a,x,v):
            # Evaluate string
            result = eval(functString)
            return result

        # Get what varaibles are used
        # Make variable storage
        rangeOfVars = []
        # Copy over string
        tempStr = functString
        # Loop through until all "v[n]" are found
        while True:
            # Find the next "v["
            try:
                str0 = 'v['
                index = tempStr.index(str0)
                # Remove all the stuff beofre
                tempStr = tempStr[indext+len(str0):]
                # Get the number until "]"
                try:
                    str1 = ']'
                    index = tempStr.index(str1)
                    # Save number
                    num = tempStr[:index]
                    # Get the rest of the string
                    tempStr = tempStr[index+len(str1):]
                    # Add to variable array
                    rangeOfVars.append(int(num))
                # Failure to get end of varaible
                except:
                    break
            # Failure to get beginning of variable
            except:
                break

        #TEST Input
        dt = 1    #increase time (1 = one year)
        yrs = [2001,2004]



        # Perform the fit
        try:
            # Convert alpha to numbers
            alpha = [float(a.GetValue()) for a in self.alpha]
            # print alpha
            # alpha = [ 1.97692763e+01,
            #          -2.18681671e-03,
            #          -4.63475834e-02,
            #           1.88316523e-04]
            # Get output of fit
            alpha = fit_data( alpha, self.percentRedds, self.siteData,\
                                    fitEq, rangeOfVars, "temp", dt, yrs)
            # String of results
            paramResultStr = [ "a[%i] = %e" %(i,alpha[i])
                               for i in range(len(alpha))]
            self.resultsPanel.fitParamStr.SetLabel('\n'.join(paramResultStr))

            image = wx.ImageFromBitmap(wx.Bitmap('figure_temp_0.png'))
            image = image.Scale(600, 450, wx.IMAGE_QUALITY_HIGH)
            result = wx.BitmapFromImage(image)
            self.resultsPanel.graph.SetBitmap(result)


        # Unable to get a proper value (warn user to try again)
        except:
            # ADD WARNING WINDOW
            # Stop running
            print "STOPPED!!!"



        # newSize = (1000,2500)
        # self.parentFrame.SetSize(newSize)
        # self.parentFrame.Centre()


class RightPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)

        # Set Fonts
        titleFont = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        titleFont.SetPointSize(24)
        subTitleFont = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        subTitleFont.SetPointSize(16)
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(12)

        # Set vertical sizer
        self.vbox = wx.BoxSizer(wx.VERTICAL)



        # Set title box of panel
        titleHbox = wx.BoxSizer(wx.HORIZONTAL)
        titleStr = wx.StaticText(self, -1, 'Results:')
        titleStr.SetFont(titleFont)
        titleHbox.Add(titleStr, 0)
        self.vbox.Add(titleHbox, 0, wx.CENTER | wx.TOP, 10)
        self.vbox.Add((-1,10))

        # Add placeholder for fit parameters
        self.fitParamHbox = wx.BoxSizer(wx.HORIZONTAL)
        # Subtitle of panel
        self.subTitleStr = wx.StaticText(self, -1, '\nFitting Parameters: \n')
        self.subTitleStr.SetFont(subTitleFont)
        self.fitParamHbox.Add(self.subTitleStr, 0)
        # Parameters
        self.fitParamStr = wx.StaticText(self, -1, 'hi')
        self.fitParamHbox.Add(self.fitParamStr, 0)
        self.vbox.Add(self.fitParamHbox, 0, wx.CENTER | wx.TOP, 10)
        self.vbox.Add((-1, 25))

        # Add placeholder for graph
        graphHbox = wx.BoxSizer(wx.HORIZONTAL)
        # Create a graph object
        self.graph = wx.StaticBitmap(self)
        graphHbox.Add(self.graph)
        # Add to overall sizer
        self.vbox.Add(graphHbox, 0,  wx.CENTER | wx.TOP, 10)
        self.vbox.Add((-1, 15))


        #
        self.SetSizer(self.vbox)
        self.Centre()
        self.Show(True)


class Communicate(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)#, size=(600, 800))
        # panel = wx.Panel(self, -1)
        panel = wx.PyScrolledWindow( self, -1,
                                     style = wx.HSCROLL|
                                             wx.VSCROLL|
                                             wx.ALWAYS_SHOW_SB)
        # panel.SetScrollbars( 0, 5,  0, 20/5 )
        # Pixels per scroll increment
        panel.SetScrollRate(1,1)
        # Save whether to show results
        self.showResults = False
        # Create results in right panel
        self.resultsPanel = RightPanel(panel, -1)
        # Create fitting panel in left panel
        leftPanel = LeftPanel(panel, -1)

        self.hbox = wx.BoxSizer()
        self.hbox.Add(leftPanel, 1, wx.EXPAND | wx.ALL, 5)
        # if (self.showResults):
        self.hbox.Add(self.resultsPanel, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(self.hbox)
        self.Update
        # self.Left()#Centre()
        self.Show(True)




app = wx.App()
Communicate(None, -1, 'widgets communicate')
app.MainLoop()
