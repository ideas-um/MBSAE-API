"""

UPDATE ADH:

    Read a JSON file and compare all value properties and 
    requirements to those already in the SysML model. If any
    value properties or requirements are different, update
    them in the SysML model from the JSON file.

    IMPORTANT: the JSON file and SysML file must represent
    the same system architecture. If importing a new system
    architecture, use the ReadADH plugin instead.

Written by Paul Mokotoff, prmoko@umich.edu

Last Updated: 21 Mar 2025

Inputs:

    ADH File within the "Magic Systems of Systems Architect"
    directory on your computer.

    SysML model for the system architecture.

Outputs:

    Updated SysML model with any values or requirements
    overwritten.

    Text file in the "Magic Systems of Systems Architect"
    directory entitled <ADHName>-ModifiedValues.txt, where
    <ADHName> is the name of the ADH file input, and contains
    a list of the model elements that were updated from the
    operation.

"""

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

# import magicdraw packages
import com.nomagic.magicdraw.actions.ActionsConfiguratorsManager     as ACM
import com.nomagic.magicdraw.actions.BrowserContextAMConfigurator    as BCAMC
import com.nomagic.magicdraw.actions.MDActionsCategory               as MDActionsCategory
import com.nomagic.magicdraw.core.Application                        as Application
import com.nomagic.magicdraw.openapi.uml.SessionManager              as SM
import com.nomagic.magicdraw.openapi.uml.ModelElementsManager        as MEM
import com.nomagic.magicdraw.plugins.Plugin                          as Plugin
import com.nomagic.magicdraw.ui.browser.actions.DefaultBrowserAction as DBA
import com.nomagic.magicdraw.ui.dialogs.MDDialogParentProvider       as MDDPP
import com.nomagic.magicdraw.uml.BaseElement                         as BaseElement
import com.nomagic.magicdraw.uml.Finder                              as Finder
import com.nomagic.uml2.ext.jmi.helpers.StereotypesHelper            as SH
import com.nomagic.uml2.ext.magicdraw.classes.mdkernel               as MDKernel
import com.nomagic.uml2.ext.jmi.helpers.CoreHelper                   as CH

# import java packages
import java.awt.Color     as Color
import java.awt.Dimension as Dimension
import java.awt.Font      as Font
import java.lang.Short    as Short

# import javax packages
import javax.swing.BorderFactory                  as BorderFactory
import javax.swing.GroupLayout                    as GroupLayout
import javax.swing.JButton                        as JButton
import javax.swing.JDialog                        as JDialog
import javax.swing.JLabel                         as JLabel
import javax.swing.JPanel                         as JPanel
import javax.swing.JTextField                     as JTextField
import javax.swing.LayoutStyle.ComponentPlacement as ComponentPlacement
import javax.swing.WindowConstants                as WindowConstants

# additional python/jython imports
import json

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

###############################
#                             #
# BROWSER ACTION              #
#                             #
###############################

class BrowserAction(DBA):

    # initialize the action
    def __init__(self, ID, Name):
        """

        __init__(self, ID, Name)

        Initialization function for a browser action

        INPUTS:
            self: the BrowserAction

            ID  : a string to identify the action

            Name: a string to define the action in the browser (what the user sees)

        OUTPUTS:
            none

        """        

        # initialize the action
        DBA.__init__(self, ID, Name, None, None)

    # end __init__

    # -------------------------------------------------------

    # define the action performed
    def actionPerformed(self, ActionEvent):
        """

        actionPerformed(self, ActionEvent)

        Function to define what should happen after the browser option is selected.

        INPUTS:
            self       : the browser action

            ActionEvent: the event that triggered the function to be executed

        OUTPUTS:
            none

        """
        
        # get the tree
        Tree = self.getTreeOrActiveTree()

        # get the selected node
        SelectedNode = Tree.getSelectedNode()

        # check that the node exists
        if (SelectedNode != None):

            # check that the node is an instance of the base element
            if (isinstance(SelectedNode.getUserObject(), BaseElement)):

                # get the object
                Element = SelectedNode.getUserObject()

                # get the parent dialog
                Parent = MDDPP.getProvider().getDialogParent(True)
                
                # get the dialog
                Dialog = FilenameDialog(Parent, Element)
                
                # turn the dialog visibility on
                Dialog.setVisible(True)

            # end if
        # end if
    # end actionPerformed

    # -------------------------------------------------------
    
# end BrowserAction

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

###############################
#                             #
# BROWSER CONFIGURATION       #
#                             #
###############################

class BrowserConfiguration(BCAMC):

    def __init__(self, Action):
        """

        __init__(self, Action)

        Initialization function for the browser configuration.

        INPUTS:
            self  : the browser configuration

            Action: the action to be performed if the browser option is selected

        OUTPUTS:
            none

        """
        
        # remember the action
        self.BrowserAction = Action
        
    # end __init__

    # -------------------------------------------------------
    
    def configure(self, Manager, Tree):
        """

        configure(self, Manager, Tree)

        Function to add the browser option to the browser menu.

        INPUTS:
            self   : the browser configuration

            Manager: internal to MagicDraw that adds options to the browser menu

            Tree   : the current tree breakdown of the system model

        OUTPUTS:
            none

        """
        
        # make an action
        Category = MDActionsCategory("", "")

        # add the action
        Category.addAction(self.BrowserAction)

        # add the action
        Manager.addCategory(Category)
                
    # end configure

    # -------------------------------------------------------

    def getPriority(self):
        """

        getPriority(self)

        Function to define the priority/placement of the menu option.

        INPUTS:
            self: the browser configuration

        OUTPUTS:
            the priority of where the menu option should be placed

        """
        
        # place the option towards the bottom of the menu (low priority)
        return BCAMC.LOW_PRIORITY

    # end getPriority

    # -------------------------------------------------------

# end BrowserConfiguration

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

###############################
#                             #
# PLUGIN CLASS                #
#                             #
###############################

class UpdateADH(Plugin):

    # initialization
    def __init__(self):
        """

        __init__(self)

        Initialization function for the plugin.

        INPUTS:
            self: the plugin

        OUTPUTS:
            none

        """
        
        # create the action
        Action = BrowserAction("UpdateADH", "MBSA&E: Update ADH")

        # create the configuration
        Configuration = BrowserConfiguration(Action)

        # add the configuration
        ACM.getInstance().addContainmentBrowserContextConfigurator(Configuration)

    # end __init__

    # -------------------------------------------------------
    
    def close(self):
        """

        close(self)

        Function to close the plugin after running it.

        INPUTS:
            self: the plugin class

        OUTPUTS:
            status to indicate whether the plugin can be terminated or not

        """
        
        return True

    # end close

    # -------------------------------------------------------
    
    def isSupported(self):
        """

        isSupported(self)

        Function to determine if the plugin is supported in MagicDraw.

        INPUTS:
            self: the plugin class

        OUTPUTS:
            status to indicate whether the plugin is supported or not

        """
        
        return True

    # end isSupported
    
# end UpdateADH

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

###############################
#                             #
# FILENAME PANEL              #
#                             #
###############################

class FilenamePanel(JPanel):

    # initialization
    def __init__(self):
        """

        __init__(self)

        Function to initalize the panel for providing an ADH file.

        INPUTS:
            self: the java panel

        OUTPUTS:
            none

        """

        # initialize the components
        self.initComponents()

    # end __init__

    # -------------------------------------------------------
    
    # initialize the components
    def initComponents(self):

        self.MainPanel = JPanel();
        self.Title = JLabel();
        self.ObjLabel = JLabel();
        self.ObjFunInput = JTextField();
        self.DoneButton = JButton();

        self.MainPanel.setBackground(Color(255, 255, 255))
        self.MainPanel.setBorder(BorderFactory.createLineBorder(Color(0, 0, 0), 4))
        self.MainPanel.setPreferredSize(Dimension(780, 600))

        self.Title.setBackground(Color(255, 255, 255))
        self.Title.setFont(Font("Times New Roman", 1, 24))
        self.Title.setText("ADH Read/Write/Update")

        self.ObjLabel.setBackground(Color(255, 255, 255))
        self.ObjLabel.setFont(Font("Times New Roman", 1, 18))
        self.ObjLabel.setText("Filename (must be in Program Files --- Magic System of Systems Architect folder):")

        self.ObjFunInput.setFont(Font("Times New Roman", 0, 14))
        self.ObjFunInput.setText("Input filename to be read/written/updated")

        self.DoneButton.setFont(Font("Times New Roman", 1, 12))
        self.DoneButton.setText("Run");
        self.DoneButton.addActionListener(self.DoneListener)

        MainPanelLayout = GroupLayout(self.MainPanel);
        self.MainPanel.setLayout(MainPanelLayout);
        MainPanelLayout.setHorizontalGroup( \
            MainPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING) \
            .addGroup(MainPanelLayout.createSequentialGroup() \
                .addContainerGap() \
                .addGroup(MainPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING) \
                    .addComponent(self.Title, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE) \
                    .addGroup(MainPanelLayout.createSequentialGroup() \
                        .addGap(0, 0, Short.MAX_VALUE) \
                        .addComponent(self.DoneButton)) \
                    .addGroup(MainPanelLayout.createSequentialGroup() \
                        .addComponent(self.ObjFunInput, GroupLayout.PREFERRED_SIZE, 500, GroupLayout.PREFERRED_SIZE) \
                        .addGap(0, 0, Short.MAX_VALUE)) \
                    .addComponent(self.ObjLabel, GroupLayout.DEFAULT_SIZE, 718, Short.MAX_VALUE)) \
                .addContainerGap()) \
        )
        MainPanelLayout.setVerticalGroup( \
            MainPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING) \
            .addGroup(MainPanelLayout.createSequentialGroup() \
                .addContainerGap() \
                .addComponent(self.Title, GroupLayout.PREFERRED_SIZE, 33, GroupLayout.PREFERRED_SIZE) \
                .addGap(18, 18, 18) \
                .addComponent(self.ObjLabel) \
                .addPreferredGap(ComponentPlacement.RELATED) \
                .addComponent(self.ObjFunInput, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE) \
                .addPreferredGap(ComponentPlacement.RELATED, 28, Short.MAX_VALUE) \
                .addComponent(self.DoneButton)
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)) \
        )

        layout = GroupLayout(self);
        self.setLayout(layout);
        layout.setHorizontalGroup( \
            layout.createParallelGroup(GroupLayout.Alignment.LEADING) \
            .addGroup(layout.createSequentialGroup() \
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE) \
                .addComponent(self.MainPanel, GroupLayout.PREFERRED_SIZE, 746, GroupLayout.PREFERRED_SIZE)) \
        )
        layout.setVerticalGroup( \
            layout.createParallelGroup(GroupLayout.Alignment.LEADING) \
            .addComponent(self.MainPanel, GroupLayout.PREFERRED_SIZE, 180, GroupLayout.PREFERRED_SIZE) \
        )

    # end initComponents

    # -------------------------------------------------------
    
    # listener for the Done button
    def DoneListener(self, Event):
        """

        DoneListener(self, Event)

        Function that is called once the user inputs an ADH file name and clicks done/run.

        INPUTS:
            self : the java panel

            Event: the event (mouse click) that caused this function to be called

        OUTPUTS:
            none

        """
        
        # get the text input
        Filename = self.ObjFunInput.getText()

        # generate the model structure
        Generator = ModelStructureGenerator()
        
        # execute the generator on the object
        Generator.execute(self.MyParentElement, Filename)
        
    # end DoneListener

    # -------------------------------------------------------

# end FilenamePanel

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

###############################
#                             #
# FUNCTION FOR FLATTENING AN  #
# ARRAY                       #
#                             #
###############################

def Flatten(Arr):

    # remember the result
    result = []

    # define helper function
    def SubFlatten(SubArr):

        # loop through all subarrays
        for element in SubArr:

            # check if it's a list
            if isinstance(element, list):

                # if so, flatten in
                SubFlatten(element)
            else:

                # append it to the result
                result.append(element)

            # end if
        # end for
    # end SubFlatten

    # recursively flatten each dimension
    SubFlatten(Arr)

    # return the flattenened array
    return result

# end Flatten

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

###############################
#                             #
# FUNCTION FOR GETTING AN     #
# ARRAY'S SIZE                #
#                             #
###############################

def GetShape(Arr):

    # check if the Array is a list
    if isinstance(Arr, list):

        # get the inner shape recursively
        InnerShape = GetShape(Arr[0])

        # return the recursively called shape
        return (len(Arr),) + InnerShape if InnerShape else (len(Arr),)

    # end if

    # return nothing if it's not a list
    return ()

# end GetShape

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

###############################
#                             #
# FUNCTION FOR RETURNING ALL  #
# NAMES OF ARRAY ELEMENTS FOR #
# AN N-DIMENSIONAL ARRAY      #
#                             #
###############################

def WriteIndices(Name, *Shapes):

    # create an array of ranges for each dimension
    Indices = [list(range(s)) for s in Shapes]

    # initialize an index tuple to track current positions
    CurIndex = [0] * len(Shapes)

    # iterate until breaking out down below
    while True:
        
        # remember the string "prefix"
        OutString = Name

        # get the number of array dimensions
        nshape = len(Shapes)

        # loop through the array dimensions
        for ishape in range(nshape):

            # append a "dunder" (double underscore) and the next dimension's index
            OutString += "__" + str(CurIndex[ishape])

        # end for

        # yield the current string
        yield OutString
        
        # start incrementing from the last dimension
        for idim in reversed(range(len(Shapes))):

            # increment the dimension
            CurIndex[idim] += 1

            # check for overflow
            if (CurIndex[idim] < Shapes[idim]):

                # break out of the loop
                break
            
            else:
                
                # reset current dimension and carry over to the next
                CurIndex[idim] = 0
                
        else:
            
            # stop generating results
            return

        # end for
    # end while
# end WriteIndices

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

def ReshapeArray(Arr, NewShape):

    # helper function to recursively construct the reShaped array
    def ConstructNewShape(Arr, Shape):

        # check if the shape represents a scalar
        if len(Shape) == 1:

            # return the first elements in the array (to match the first dimension)
            return Arr[:Shape[0]]
        
        # determine the size of the sub-arrays based on the shape
        size = Shape[0]

        # find the remaining 
        SubShape = Shape[1:]

        # get the length of the shape nested within
        SubArrLength = len(Arr) // size
        
        # return the new shape recursively
        return [ConstructNewShape(Arr[i * SubArrLength:(i + 1) * SubArrLength], SubShape) for i in range(size)]

    # check that the total number of elements match
    TotalElements = 1

    # loop through the dimensions in the new shape
    for dim in NewShape:

        # account for the current dimension
        TotalElements *= dim

    # end for

    # check that the number of elements match
    assert TotalElements == len(Arr), "The total size of the new Arr must be unchanged."

    # recursively construct a new array
    return ConstructNewShape(Arr, NewShape)

# end ReshapeArray

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

###############################
#                             #
# MODEL STRUCTURE GENERATOR   #
#                             #
###############################

class ModelStructureGenerator():

    # -------------------------------------------------------

    # initialization
    def __init__(self):
        
        # get the project
        self.Project = Application.getInstance().getProject()

        # get the elements factory
        self.Factory = self.Project.getElementsFactory()

        # get the model element manager
        self.Manager = MEM.getInstance()

        # get the model
        self.Model = self.Project.getModel()
        
    # end __init__

    # -------------------------------------------------------

    # action execution
    def execute(self, ParentPackage, Filename):
        
        # try to create a session
        try:

            # create the session
            SM.getInstance().createSession(self.Project, "Modify ADH")

            # get the block stereotype from the SysML stereotype profile
            self.BlockSter = SH.getStereotype(self.Project, "Block", "SysML::Blocks")

            # get the requirement stereotype from the SysML stereotype profile
            self.ReqSter = SH.getStereotype(self.Project, "Requirement", "SysML::Requirements")

            # get the types for integers, reals, and strings
            self.Integer = Finder.byQualifiedName().find(self.Project, "SysML::Libraries::PrimitiveValueTypes::Integer")
            self.Real    = Finder.byQualifiedName().find(self.Project, "SysML::Libraries::PrimitiveValueTypes::Real")
            self.String  = Finder.byQualifiedName().find(self.Project, "SysML::Libraries::PrimitiveValueTypes::String")
            self.Boolean = Finder.byQualifiedName().find(self.Project, "SysML::Libraries::PrimitiveValueTypes::Boolean")

            # remember the ADH profile
            self.Profile = SH.getProfile(self.Project, "ImportADHProfile")

            # if there's no profile, throw a warning
            if (self.Profile is None):

                # throw failure
                self.ProfileFlag = -1
                
                # print a warning
                Application.getInstance().getGUILog().showMessage("WARNING: No ADH Profile imported ... stereotypes won't be assigned.")
                
            else:
                
                # throw success
                self.ProfileFlag = 0
                
            # end if

            # get the class metadata
            self.MetaClass = SH.getMetaClassByName(self.Project, "Class")
        
            # open a JSON file
            f = open(Filename, "r")
            
            # read the file
            MyString = f.read()
            
            # convert to a JSON string
            MyJSON = json.loads(MyString)

            # close the file
            f.close()

            # remove the JSON suffix
            NewName = Filename.split(".json")[0]
            
            # create a new file for writing differences
            NewFileName = NewName + "-ModifiedValues.txt"

            # create a new file
            self.OutFile = open(NewFileName, "w")
            
            # get the dictionary needed for writing to the ADH
            MyDict = self.GetBlock(ParentPackage)

            # get the parent package name
            ParentPackageName = ParentPackage.getName()

            print("COMPARING DICTIONARIES")
            
            # compare the two dictionaries
            self.CompareDict(MyDict, MyJSON[ParentPackageName], ParentPackageName, "", 0, [None, None])

            # close the file
            self.OutFile.close()
            
            # close the session
            SM.getInstance().closeSession(self.Project)

        except Exception as e:
            
            # print that an exception occurred
            Application.getInstance().getGUILog().showMessage("Exception occurred: " + repr(e))
        
            # cancel the session
            SM.getInstance().cancelSession(self.Project)

        # end try-except
    # end execute

    # -------------------------------------------------------

    def CompareDict(self, Data1, Data2, Name, ParentKeys, SpecialFlag, LastDict):
        
        # check that both items are dictionaries
        if (isinstance(Data1, dict)) and (isinstance(Data2, dict)):
            
            # loop through each level of the dictionaries
            Items1 = Data1.items()
            
            # loop through one dictionary
            for ikey, ival in Items1:
                
                # assume a floating point value
                DataType = 0
                
                # check if the value is a dictionary
                if (isinstance(ival, dict)):
                    
                    # assume it is a block with data inside it
                    DataType = -1
                    
                    # try seeing it a WBS number exists
                    try:
                        
                        # get the WBS number
                        if ("wbs_no" in ival.keys()):
                            
                            # it is a component that will may have folders
                            DataType = +1
                            
                        # end if
                        
                    except:
                        
                        # do nothing
                        pass
                    
                    # end try-except
                # end if
                
                # check if the value is a list
                if (isinstance(ival, list)):
                    
                    # it is an array to be opened up
                    DataType = +2
                    
                # end if
                
                # check for reserved words
                if (ikey == "components") or (ikey == "requirements") or (ikey == "performance") or (ikey == "behavior"):
                    
                    # it also needs to be opened up
                    DataType = +2
                    
                # end if
                
                # check how the data must be handled
                if (DataType == -1):

                    # assume no extra quotes are needed
                    ExtraBlock1 = ""
                    ExtraBlock2 = ""

                    # try to check if there are keys from the parent item
                    try:

                        # check if there are keys
                        if ("wbs_no" in ParentKeys):
                            
                            # get the last part of the name
                            ExtraBlock1 = "::Architecture"
                            
                    except:

                        # do nothing if it fails
                        pass

                    # try to check if there are keys in the current item
                    try:

                        # check if there are keys
                        if ("wbs_no" in Data1.keys()):
                            
                            # get the last part of the name
                            ExtraBlock2 = "::Architecture"
                            
                    except:

                        # do nothing if it fails
                        pass
                    
                    # end try-except
                    
                    # modify the name accordingly
                    if (SpecialFlag >= 0):

                        # modify the name
                        NewName = Name + ExtraBlock1 + ExtraBlock2 + "::" + ikey
                        
                    else:

                        # don't add extra blocks when modifying the name
                        NewName = Name + "::" + ikey
                        
                    # end if

                    # open up the data more
                    self.CompareDict(Data1[ikey], Data2[ikey], NewName, Data1.keys(), -1, [LastDict[1], Data2])
                    
                elif (DataType == 0):

                    # assume no extra text is needed
                    ExtraBlock = ""

                    # try to see if there's a wbs number in the data
                    try:

                        # see if there's a wbs number
                        if ("wbs_no" in Data1):

                            # add the extra text required
                            ExtraBlock = "::" + Name.split("::")[-1]

                        # end if
                        
                    except:

                        # do nothing if it fails
                        pass

                    # end try-except
                
                    # modify the name
                    NewName = Name + ExtraBlock + "::" + ikey

                    # open up the data more
                    self.CompareDict(Data1[ikey], Data2[ikey], NewName, Data1.keys(), 0, [LastDict[1], Data2])
                    
                elif (DataType == 1):
                    
                    # check for reserved words
                    if (ikey != "wbs_no") and (ikey != "name") and (ikey != "description"):
                        
                        # add a string for the extra package to be traversed
                        ExtraString = "::Architecture"
                        
                    else:
                        
                        # no extra string is needed
                        ExtraString = ""
                        
                    # end if
                                        
                    # check if the name has been set yet
                    if (Name == ""):
                        
                        # recursively search the structure
                        self.CompareDict(Data1[ikey], Data2[ikey], ikey, Data1.keys(), 0, [LastDict[1], Data2])
                        
                    else:
                        
                        # modify the names
                        NewName = Name + ExtraString + "::" + ikey

                        # recursively search the structure
                        self.CompareDict(Data1[ikey], Data2[ikey], NewName, Data1.keys(), 0, [LastDict[1], Data2])
                        
                    # end if
                
                elif (DataType == 2):
                    
                    # check if it's a requirement
                    if (ikey == "requirements"):
                        
                        # add the path for the requirements
                        ExtraString = "::Requirements"

                        # set a special flag
                        Flag = -2
                        
                    elif (ikey == "performance"):
                        
                        # add the path for the performance package
                        ExtraString = "::Performance"

                        # set a special flag
                        Flag = -2
                        
                    elif (ikey == "behavior"):
                        
                        # add the path for the behavior package
                        ExtraString = "::Behavior"

                        # set a special flag
                        Flag = -2
                        
                    else:

                        # don't add an extra path
                        ExtraString = ""

                        # don't set a special flag
                        Flag = 0
                        
                    # end if
                    
                    # check if the value is a list
                    if (isinstance(ival, list)):
                        
                        # get the value from the other dictionary
                        val2 = Data2[ikey]

                        # check that the list has a nonzero length
                        if (len(ival) > 0):
                        
                            # loop through each component
                            for icomp in range(len(ival)):
                            
                                # get the component name
                                CompName = ikey + "__" + str(icomp)
                            
                                # modify the names
                                NewName = Name + ExtraString
                            
                                # read the entry
                                self.CompareDict({CompName : ival[icomp]}, {CompName : val2[icomp]}, NewName, Data1.keys(), Flag, [LastDict[1], Data2])
                            
                            # end for
                        # end if                        
                            
                    else:
                        
                        # get the value from the other dictionary
                        val2 = Data2[ikey]
                        
                        # loop through the dictionary contents
                        for jkey, jval in ival.items():
                            
                            # modify the name
                            NewName = Name + ExtraString
                            
                            # read the entry
                            self.CompareDict({jkey : ival[jkey]}, {jkey : val2[jkey]}, NewName, Data1.keys(), Flag, [LastDict[1], Data2])
                            
                        # end for
                    # end if
                    
                else:
                    
                    # throw an error
                    print("ERROR - CompareDict: invalid DataType selected.")
                    
                    # break out of the loop for now
                    break
                
                # end if
            # end for
        
        else:
            
            # check if each is a list
            if (isinstance(Data1, list)) and (isinstance(Data2, list)):
            
                # get the length of the list
                ListLen = len(Data1)
            
                # loop through each entry
                for ielem in range(ListLen):

                    # check if the values are different
                    if (Data1[ielem] != Data2[ielem]):

                        # print a note indicating this
                        self.OutFile.write("Changed " + repr(Name) + " from " + repr(Data1[ielem]) + " to " + repr(Data2[ielem]) + "\n\n")
                        
                        # call a function
                        self.CorrectValue(Name, Data2, LastDict)
            
                    # end if
                # end for

            elif (isinstance(Data1, list)) and (not isinstance(Data2, list)):
                
                # get the last part of the name
                LastPart = Name.split("::")[-1]
                
                # convert into a dictionary
                TempData1 = {LastPart : Data1[0]}
                TempData2 = {LastPart : Data2   }

                # modify the name
                NewName = Name.replace("::" + LastPart, "")

                # re-evaluate the dictionary
                self.CompareDict(TempData1, TempData2, NewName, TempData2.keys(), 0, [LastDict[1], Data2])

            elif (not isinstance(Data1, list)) and (isinstance(Data2, list)):

                # get the last part of the name
                LastPart = Name.split("::")[-1]

                # convert into a dictionary
                TempData1 = {LastPart : Data1   }
                TempData2 = {LastPart : Data2[0]}

                # modify the name
                NewName = Name.replace("::" + LastPart, "")

                # re-evaluate the dictionary
                self.CompareDict(TempData1, TempData2, NewName, TempData1.keys(), 0, [LastDict[1], Data2])
            
            else:

                # check if the values are different
                if (Data1 != Data2):

                    # print a note indicating this
                    self.OutFile.write("Changed " + repr(Name) + " from " + repr(Data1) + " to " + repr(Data2) + "\n\n")
                    
                    # call a function
                    self.CorrectValue(Name, Data2, LastDict)
                    
                # end if
                
            # end if
            
    # end CompareDict

    # -------------------------------------------------------

    def CorrectValue(self, Name, Data2, LastDict):
        
        # check if the qualified name is for a requirement
        HasReq = Name.find("Requirements")
        
        # check if a requirement block was found
        if (HasReq != -1):
            
            # split the text at the requirement
            SplitText = Name.split("Requirements")
            
            # get the text before/after the requirement
            Prefix = SplitText[ 0]
            Suffix = SplitText[-1]
            
            # get the requirement name
            ReqName = Suffix.split("::")[1]
            
            # modify the name being searched
            QualName = Prefix + "Requirements::" + ReqName
            
        else:
            
            # use the given qualified name
            QualName = Name
            
        # end if                        
               
        # get the entity with the qualified name
        MyEntity = Finder.byQualifiedName().find(self.Project, QualName)
        
        if (MyEntity != None):
            
            # modify the value
            if (HasReq == -1):
                
                # check the value type
                if (isinstance(Data2, int)):
                    
                    # assign the type
                    MyType = self.Integer
                    
                    # create the integer
                    MyValueInst = self.Factory.createLiteralIntegerInstance()
                    
                elif (isinstance(Data2, float)):
                    
                    # assign the type
                    MyType = self.Real
                    
                    # create the real
                    MyValueInst = self.Factory.createLiteralRealInstance()
                    
                elif (isinstance(Data2, unicode)) or (isinstance(Data2, str)):
                    
                    # assign the type
                    MyType = self.String
                    
                    # create the string
                    MyValueInst = self.Factory.createLiteralStringInstance()
                    
                else:
                    
                    # print an error
                    print("ERROR: the type for " + QualName + " is not known ... not creating a value property.")
                    
                    # do nothing and exit
                    return
                
                # end if
                
                # set the value
                MyValueInst.setValue(Data2)                                
                
                # set the value in the ValueProperty
                MyEntity.setDefaultValue(MyValueInst)
                
            else:
                                
                try:
                    
                    # get the prior dictionary
                    TempDict = LastDict[1]
                    
                    # get the name, description, and value
                    TempName = TempDict["name"]
                    TempDesc = TempDict["description"]
                    TempValu = TempDict["value"]
                    
                    # get the actual value and units                        
                    FinalValue = TempValu["value"]
                    FinalUnits = TempValu["units"]
                    
                    # change the whole requirement
                    SH.setStereotypePropertyValue(MyEntity, self.ReqSter, "Text", "(" + TempName + "): " + TempDesc + " shall be " + str(FinalValue) + " " + FinalUnits)
                    
                except:
                    
                    try:
                        
                        # get two dictionaries prior
                        TempDict = LastDict[0]
                        
                        # get the name and description
                        TempName = TempDict["name"]
                        TempDesc = TempDict["description"]
                        
                        # get the value and units from the more recent dictionary
                        TempDict = LastDict[1]
                        
                        # get the value and units
                        FinalValue = TempDict["value"]
                        FinalUnits = TempDict["units"]
                        
                        # change the whole requirement
                        SH.setStereotypePropertyValue(MyEntity, self.ReqSter, "Text", "(" + TempName + "): " + TempDesc + " shall be " + str(FinalValue) + " " + FinalUnits)
                        
                    except:
                        
                        # print error
                        print("ERROR - requirement (" + repr(QualName) + ") not updated.")
                        
                    # end try-except
                # end try-execept
            # end if
                        
        else:
            
            # print error
            print("ERROR - model element with name " + QualName + " not found ... cannot update.")
            
        # end if
        
    # end CorrectValue

    # -------------------------------------------------------

    def GetData(self, MyJSON, ParentPackage, ReqSterFlag, HigherLevelComp = None):

        try:                
            
            # loop through each of the items at this level
            for ikey, ivalue in MyJSON.items():
                
                # assume it is a floating value
                DataType = 0
                
                # check if the value is a dictionary
                if (isinstance(ivalue, dict)):
                    
                    # it is a block with additional data inside of it
                    DataType = -1
                    
                    # check if the value has a WBS number
                    try:
                        if ("wbs_no" in ivalue.keys()):
                            
                            # then, it is a component that can have folders
                            DataType = +1
                            
                            # end if
                            
                    except:
                        
                        # do nothing
                        pass
                    
                    # end try-except
            
                # end if

                # check if the data is a list
                if (isinstance(ivalue, list)):

                    # it is an array that must be opened up
                    DataType = +2

                # end if

                # check for keywords
                if (ikey == "components") or (ikey == "requirements") or (ikey == "performance") or (ikey == "behavior"):

                    # open up the data type
                    DataType = +2

                # end if
                    
                # check how data must be handlded
                if (DataType == 0):
                    
                    # we want the package above for storing floating point values
                    Parent = ParentPackage.getOwner()
                    
                    # read the floating parameter
                    self.ReadFloatingValue(Parent, ikey, ivalue)
                    
                elif (DataType == -1):
                    
                    # read a data structure
                    self.ReadDataStructure(ParentPackage, ikey, ivalue, ReqSterFlag)
                    
                elif (DataType == +1):
                    
                    # create a new package and (possibly) set of folders
                    MainPackage = self.CreatePackage(ikey)
                    
                    # set the owner of the package to be the parent
                    MainPackage.setOwner(ParentPackage)

                    # create an instance of the component as normal
                    ComponentClass = self.CreateInstance(ikey, ReqSterFlag)

                    # set the owner of the class to be the package just created
                    ComponentClass.setOwner(MainPackage)
                    
                    # check if the stereotype must be added
                    if (self.ProfileFlag == 0):
                            
                        # get the stereotype
                        Stereotype = SH.getStereotype(self.Project, ikey, self.Profile)

                        # check if it's non-existant
                        if (Stereotype == None):

                            # get the value
                            TempValue = MyJSON[ikey]
                                  
                            # now, look for the name
                            TempName = TempValue["name"]

                            # now, try getting the stereotype
                            Stereotype = SH.getStereotype(self.Project, TempName, self.Profile)

                        # end if

                        # check if the stereotype exists
                        if (Stereotype != None):

                            # if so, add the stereotype
                            SH.addStereotype(ComponentClass, Stereotype)
                            
                        # end if

                    # end if
                    
                    # create the necessary folders
                    self.MakeFolders(ivalue, MainPackage)
                    
                    # get the children of the main package
                    Children = MainPackage.getOwnedElement()
                
                    # assume that the parent is the main package
                    Parent = MainPackage
                    
                    # loop through all the children
                    for ichild in Children:
                        
                        # get the name of the child
                        Name = ichild.getHumanName()
                        
                        # check if it is the architecture package
                        if (Name == "Package Architecture"):
                            
                            # update the parent
                            Parent = ichild
                            
                            # break out of the loop
                            break
                        
                        # end if
                    # end for

                    # check if there's a higher-level component for decomposition relation
                    if (HigherLevelComp != None):

                        # create a relation
                        Decomp = self.Factory.createAssociationInstance()

                        # set the supplier and client elements
                        CH.setSupplierElement(Decomp, ComponentClass)
                        CH.setClientElement(Decomp, HigherLevelComp)

                        # get the ends of the relation
                        Members = Decomp.getMemberEnd()

                        # get the supplier end
                        SupplierEnd = Members[1]

                        # set it as a decomposition
                        SupplierEnd.setAggregation(MDKernel.AggregationKindEnum.COMPOSITE)

                        # get the parent of the higher level component
                        OwnerParent = HigherLevelComp.getOwner()

                        # add the dependency to the package
                        self.Manager.addElement(Decomp, OwnerParent)

                    # end if
                    
                    # explore the next level of the component
                    self.GetData(ivalue, Parent, ReqSterFlag, ComponentClass)
                    
                elif (DataType == +2):

                    # assume not a requirement
                    ReqSterFlag = 0
                    
                    # get the appropriate target name
                    if (ikey == "requirements"):

                        # provide the target name
                        TargetName = "Package Requirements"

                        # the parent pacakage is the higher-level package
                        Parent = ParentPackage.getOwner()

                        # flag that we're dealing with a requirement
                        ReqSterFlag = 1

                    elif (ikey == "performance"):

                        # provide the target name
                        TargetName = "Package Performance"

                        # the parent pacakage is the higher-level package
                        Parent = ParentPackage.getOwner()

                    elif (ikey == "behavior"):

                        # provide the target name
                        TargetName = "Package Behavior"

                        # the parent pacakage is the higher-level package
                        Parent = ParentPackage.getOwner()

                    else:

                        # provide the target name
                        TargetName = "Package Architecture"

                        # the parent package remains the same
                        Parent = ParentPackage

                    # end if
                                            
                    # get the children of the main package
                    Children = Parent.getOwnedElement()
                    
                    # loop through all of the children
                    for ichild in Children:
                        
                        # get the name of the child
                        Name = ichild.getHumanName()
                        
                        # check if it matches the architecture folder
                        if (Name == TargetName):
                            
                            # remember this as the parent package
                            Parent = ichild
                            
                            # break out of the loop
                            break
                        
                        # end if
                    # end for
                    
                    # check if the value is a list
                    if (isinstance(ivalue, list)):

                        # check for a nonzero-length list
                        if (len(ivalue) > 0):
                            
                            # loop through each of the components
                            for icomp in range(len(ivalue)):

                                # create the name
                                CompName = ikey + "__" + str(icomp)
                                                
                                # read each component separately
                                self.GetData({CompName : ivalue[icomp]}, Parent, ReqSterFlag, HigherLevelComp)
                            
                            # end for
                        # end if
                        
                    else:

                        # loop through the contents of the dictionary
                        for jkey, jvalue in ivalue.items():
            
                            # there is only one element, no loops or lists needed
                            self.GetData({jkey : jvalue}, Parent, ReqSterFlag, HigherLevelComp)

                        # end for
                        
                    # end if
                    
                else:
                    
                    # throw an error
                    print("ERROR - GetData: Invalid DataType selected.")
                    
                    # break out of the loop for now
                    break
                
                # end if    
            # end for

        except Exception as e:

            print("Bad: " + repr(MyJSON) + "\n")
            print("Exception: " + repr(e))

        # end try-except

    # end GetData

    # -------------------------------------------------------

    def CreatePackage(self, Name):

        # create a package
        NewPackage = self.Factory.createPackageInstance()

        # set the name
        NewPackage.setName(Name)

        # return the package
        return NewPackage

    # end CreatePackage

    # -------------------------------------------------------

    def CreateInstance(self, Name, ReqFlag = 0):

        # create an instance
        NewClass = self.Factory.createClassInstance()

        if (ReqFlag == 1):

            # represent it as a requirement
            SH.addStereotype(NewClass, self.ReqSter)

        else:
            
            # represent it as a block
            SH.addStereotype(NewClass, self.BlockSter)

        # end if

        # set the name
        NewClass.setName(Name)

        # return the new class
        return NewClass

    # end CreateInstance

    # -------------------------------------------------------

    def ReadData(self, Block, Key, Value, ReqFlag):
        
        # check if the value is a list
        if (not isinstance(Value, list)):

            # make it a list
            Value = [Value]

        # end if

        # check that the list has a length
        if (len(Value) > 0):
            
            # get the shape of the list
            MyShape = GetShape(Value)

            # get all of the names of entries
            MyNames = WriteIndices(Key, *MyShape)
            
            # flatten the array
            FlattenedValue = Flatten(Value)
            
            # assume one element
            nelem = 1
            
            for idim in MyShape:
                nelem *= idim
                
            # set a counter
            ielem = 0
            
            # loop through each item
            for iname in MyNames:
                
                # rename the key to have individual blocks, if needed
                if (nelem > 1):
                    
                    # update the key to account for multiple items
                    NewKey = iname
                    
                else:
                    
                    # keep the same key
                    NewKey = Key
                    
                # end if

                # get the current element
                CurVal = FlattenedValue[ielem]
            
                # check for a dictionary
                if (isinstance(CurVal, dict)):
                    
                    # create a block
                    NewBlock = self.CreateInstance(NewKey, ReqFlag)
                    
                    # set the owner to be the parent
                    NewBlock.setOwner(Block)
                    
                    # check for a requirement
                    if (ReqFlag == 1):
                        
                        # get the name, desription, and value
                        TempName = CurVal["name"]
                        TempDesc = CurVal["description"]
                        TempValu = CurVal["value"]
                        
                        # extract the actual value and units
                        FinalValue = TempValu["value"]
                        FinalUnits = TempValu["units"]
                        
                        # set the requirement text
                        SH.setStereotypePropertyValue(NewBlock, self.ReqSter, "Text", "(" + TempName + "): " + TempDesc + " shall be " + str(FinalValue) + " " + FinalUnits)
                        
                    else:
                        
                        # check that it is not empty
                        try:
                            
                            # read the dictionary
                            for key, value in CurVal.items():
                                
                                # get the data for each of the items
                                self.ReadData(NewBlock, key, value, ReqFlag)
                                
                            # end for
                            
                        except:
                            
                            # do nothing
                            pass
                        
                        # end try-except

                    # end if
                    
                else:

                    # create the value property
                    Block = self.CreateProperty(Block, NewKey, CurVal)

                # end if
                    
                # increment the element count
                ielem += 1
            
            # end for

        else:

            # create an property
            Block = self.CreateProperty(Block, Key, None)

        # end if
        
        # return the block
        return Block
        
    # end ReadData

    # -------------------------------------------------------

    def CreateProperty(self, Block, Key, Value):
        
        # check the value type
        if isinstance(Value, bool):

            # assign the type
            MyType = self.Boolean

            # create the boolean
            MyValueInst = self.Factory.createLiteralBooleanInstance()
            
        elif isinstance(Value, int):
            
            # assign the type
            MyType = self.Integer
            
            # create the integer
            MyValueInst = self.Factory.createLiteralIntegerInstance()
            
        elif isinstance(Value, float):
            
            # assign the type
            MyType = self.Real
            
            # create the real
            MyValueInst = self.Factory.createLiteralRealInstance()
            
        elif isinstance(Value, unicode) or isinstance(Value, str):
            
            # assign the type
            MyType = self.String
            
            # create the string
            MyValueInst = self.Factory.createLiteralStringInstance()

        elif Value is None:

            # no type needed
            MyType = None

            # create a null instance
            MyValueInst = self.Factory.createLiteralNullInstance()
            
        else:
            
            # print a warning that the type is not known
            print("WARNING: the type for " + repr(Key) + " is not known ... not creating value property.")
            
            # don't proceed
            return Block
        
        # end if

        # check that the value exists
        if (Value is not None):
            
            # set the value
            MyValueInst.setValue(Value)

        # end if
        
        # create a value property
        NewProperty = self.Factory.createPropertyInstance()
        
        # set the property name
        NewProperty.setName(Key)

        # check if the type exists
        if (MyType is not None):
            
            # set the property type
            NewProperty.setType(MyType)

        # end if
        
        # set the value
        NewProperty.setDefaultValue(MyValueInst)
        
        # add the property to the block
        self.Manager.addElement(NewProperty, Block)

        # return the Block
        return Block
        
    # end CreateProperty

    # -------------------------------------------------------

    def AddStereotype(self, Block, Name):
        
        # get the stereotype
        MyStereotype = SH.getStereotype(self.Project, Name, self.Profile)
        
        # check if the stereotype exists
        if (MyStereotype is not None):

            # apply the stereotype
            SH.addStereotype(Block, MyStereotype)

        # end if

        # return the block
        return Block

    # end AddStereotype

    # -------------------------------------------------------

    def ReadFloatingValue(self, ParentPackage, ikey, ivalue):

        # get the children of the parent package
        Children = ParentPackage.getOwnedElement()
    
        # assume the block isn't found
        FoundBlock = 0
        
        # loop through all children until we reach a block
        for ichild in range(len(Children)):                   
            
            # get the child's stereotype
            Stereotype = Children[ichild].getAppliedStereotype()
            
            # loop through all stereotypes
            for itype in Stereotype:
                
                # get the stereotype name
                SterName = str(itype.getName())
                
                # if it's a block, stop
                if (SterName == "Block"):
                    
                    # read the data as a parameter
                    Children[ichild] = self.ReadData(Children[ichild], ikey, ivalue, 0)
                    
                    # flag for finding the block
                    FoundBlock = 1
                    
                    # break out of the loop
                    break
                
                # end if
                
            # end for
            
            # break out if the block was found
            if (FoundBlock == 1):
                break
            # end if
            
        # end for

    # end ReadFloatingValue
    
    # -------------------------------------------------------

    def ReadDataStructure(self, ParentPackage, ikey, ivalue, ReqFlag):
       
        # check if it is a requirement, performance, or behavior block
        if (ikey == "requirements"):

            # place the information in the requirements package
            TargetName = "Package Requirements"

        elif (ikey == "performance"):

            # place the information in the performance package
            TargetName = "Package Performance"

        elif (ikey == "behavior"):

            # place the information in the behavior package
            TargetName = "Package Behavior"

        else:

            # place the information in the architecture package
            TargetName = "Package Architecture"

        # end if
        
        # get the children of the parent package
        Children = ParentPackage.getOwnedElement()
        
        # flag for finding the architecture package
        FoundPackage = 0
        
        # loop through all children until we reach a block
        for ichild in range(len(Children)):
            
            # get the child's stereotype
            Name = Children[ichild].getHumanName()
            
            # check for the appropriate name
            if (Name == TargetName):
                
                # flag that the package was found
                FoundPackage = 1
                
                # read the data as a parameter
                Children[ichild] = self.ReadData(Children[ichild], ikey, ivalue, ReqFlag)
                
                # break out of the loop
                break
            
            # end if                    
        # end for
        
        # check that a package was found
        if (FoundPackage == 0):
            
            # we must be at the highest level, so create a new block for it
            ParentPackage = self.ReadData(ParentPackage, ikey, ivalue, ReqFlag)
            
        # end if
        
    # end ReadDataStructure
    
    # -------------------------------------------------------

    def MakeFolders(self, ivalue, MainPackage):
        
        # assume no packages need to be made
        NeedArch = 0
        NeedReqs = 0
        NeedPerf = 0
        NeedBhav = 0

        try:
            
            # loop through all of the keys
            for jkey in ivalue.keys():
                
                # check if the key indicates components are present
                if (jkey == "components"):
                    
                    # an architecture package must be created
                    NeedArch = 1
                    
                    # continue on in the loop
                    continue
                
                # end if
                
                # check if the key indicates requirements are present
                if (jkey == "requirements"):
                    
                    # a requirements package must be created
                    NeedReqs = 1
                    
                    # continue on in the loop
                    continue
                
                # end if
                
                # check if the key indicates performance information is present
                if (jkey == "performance"):
                    
                    # a performance package must be created
                    NeedPerf = 1
                    
                    # continue on in the loop
                    continue
                
                # end if
                
                # check if the key indicates behaviors are present
                if (jkey == "behavior"):
                    
                    # a behavior package must be created
                    NeedBhav = 1
                    
                    # continue on in the loop
                    continue
                
                # end if
                
                # check if it is another reserved word
                if ((jkey != "wbs_no") and (jkey != "name") and (jkey != "description")):
                    
                    # create an architecture folder
                    NeedArch = 1
                    
                # end if
            # end for
            
            # check if an architecture package must be made
            if (NeedArch == 1):
                
                # create the architecture package
                ArchPackage = self.CreatePackage("Architecture")
                
                # set the owner to be the main package
                ArchPackage.setOwner(MainPackage)
                
            # end if
            
            # check if a requirements package must be made
            if (NeedReqs == 1):
                
                # create the requirements package
                ReqsPackage = self.CreatePackage("Requirements")
                
                # set the owner to be the main package
                ReqsPackage.setOwner(MainPackage)
                
            # end if
            
            # check if a performance package must be made
            if (NeedPerf == 1):
                
                # create the performance package
                PerfPackage = self.CreatePackage("Performance")
                
                # set the owner to be the main package
                PerfPackage.setOwner(MainPackage)
                
            # end if
        
            # check if a behavior package must be made
            if (NeedBhav == 1):
                
                # create the behavior package
                BhavPackage = self.CreatePackage("Behavior")
                
                # set the owner to be the main package
                BhavPackage.setOwner(MainPackage)
                
            # end if

        except:

            pass

        # end try-except

    # end MakeFolders
    
    # -------------------------------------------------------

    def GetBlock(self, ParentBlock):

        # create empty dictionary
        MySysDict = {}

        # try to get the name of the block
        try:

            # get the name
            TempName = ParentBlock.getHumanName()

        except:

            # not a valid block
            return MySysDict

        # end if

        # isolate the model entity type and name
        TypeName = str(TempName.split(" ")[0])
        CompName = str(TempName.split(" ")[1])

        # check for a block or package
        if (TypeName == "Block"):

            # tag the component as a block
            BlockType = 1

        elif (TypeName == "Package"):

            # tag the component as a package
            BlockType = 2

        elif (TypeName == "Requirement"):

            # tag the component as a requirement
            BlockType = 3

        else:

            # pass for now
            BlockType = -1

        # end if

        print("TempName = " + repr(TempName) + ", BlockType = " + repr(BlockType))

        # check if a valid block was selected
        if (BlockType > 0):
            
            # get the children of the current model
            MyChildren = ParentBlock.getOwnedElement()

        else:

            # not a valid block
            return MySysDict

        # end if

        # proceed for the appropriate block type
        if (BlockType == 1):
            
            # flag for names with underscores
            UseArray = 0
            
            # old string to compare base string to
            OldBaseString = ""
            
            # loop through all children
            for ichild in range(len(MyChildren)):
                
                # get the block name
                BlockName = MyChildren[ichild].getName()
                
                # check if a double underscore exists
                HasUnder = BlockName.find("__")
                
                # if an underscore exists, check if we're in an array
                if (HasUnder != -1):
                                        
                    # get the new base string
                    NewBaseString = BlockName[:HasUnder]
                    
                    # check if the strings match
                    if (NewBaseString == OldBaseString):

                        # remember the indices
                        Indices = BlockName.split("__")[1:]
                    
                        # change each index to an integer (and add 1 for reshaping)
                        for ival in range(len(Indices)):
                            
                            # convert the value and take the maximum for array space allocation
                            IntIndices[ival] = max(IntIndices[ival], int(Indices[ival]))
                            
                        # end for
                        
                        # get the value
                        BlockValue = self.GetBlockValue(MyChildren[ichild])
                        
                        # append to the array
                        TempArray.append(BlockValue)
                        
                    else:
                        
                        # check if another array already exists
                        if (UseArray == 1):

                            # increment the indices by 1
                            for ival in range(len(IntIndices)):
                                IntIndices[ival] += 1
                            # end for
                            
                            # reshape the temporary array
                            FinalArray = ReshapeArray(TempArray, IntIndices)

                            # reset the integer indices
                            for ival in range(len(IntIndices)):
                                IntIndices[ival] = 0
                            # end for

                            # write out the first array
                            MySysDict.update({str(OldBaseString) : FinalArray})
                            
                        else:
                            
                            # start using the array
                            UseArray = 1

                        # end if

                        # remember the indices
                        Indices = BlockName.split("__")[1:]
                        
                        # create a list for the actual indices
                        IntIndices = [0] * len(Indices)
                        
                        # change each index to an integer (and add 1 for reshaping)
                        for ival in range(len(Indices)):
                            
                            # convert the value and take the maximum for array space allocation
                            IntIndices[ival] = max(IntIndices[ival], int(Indices[ival]))
                            
                        # end for
                            
                        # remember the new string
                        OldBaseString = NewBaseString
                        
                        # get the value
                        BlockValue = self.GetBlockValue(MyChildren[ichild])
                        
                        # start the array
                        TempArray = [BlockValue]
                        
                    # end if
                    
                else:
                    
                    # check if we were in an array
                    if (UseArray == 1):

                        # increment the indices by 1
                        for ival in range(len(IntIndices)):
                            IntIndices[ival] += 1
                        # end for
                        
                        # reshape the temporary array
                        FinalArray = ReshapeArray(TempArray, IntIndices)

                        # reset the integer indices
                        for ival in range(len(IntIndices)):
                            IntIndices[ival] = 0
                        # end for
                        
                        # write out the first array
                        MySysDict.update({str(OldBaseString) : FinalArray})
                        
                        # the array is no longer being used
                        UseArray = 0
                        
                    # end if
                    
                    # get the value
                    MyValu = self.GetBlockValue(MyChildren[ichild])

                    # check if the value is unicode
                    if (isinstance(MyValu, unicode)):

                        # convert it to a string
                        MyValu = str(MyValu)

                    # end if
                    
                    # add the element as normal
                    MySysDict.update({str(BlockName) : MyValu})
                    
                # end if
            # end for

            # check if we were in an array
            if (UseArray == 1):
                
                # increment the indices by 1
                for ival in range(len(IntIndices)):
                    IntIndices[ival] += 1
                # end for
                
                # reshape the temporary array
                FinalArray = ReshapeArray(TempArray, IntIndices)

                # reset the integer indices
                for ival in range(len(IntIndices)):
                    IntIndices[ival] = 0
                # end for
                
                # write out the first array
                MySysDict.update({str(OldBaseString) : FinalArray})
                
                # the array is no longer being used
                UseArray = 0
                
            # end if

        elif (BlockType == 2):

            # create a temporary dictionary to aggregate everything
            TempDict = {}

            # loop through the children
            for ichild in range(len(MyChildren)):

                # get the entity name
                Name = MyChildren[ichild].getName()

                # check if the name is a reserved word
                FindArch = Name == "Architecture"
                FindPerf = Name == "Performance"
                FindReqs = Name == "Requirements"
                FindBhvr = Name == "Behavior"

                # check if the name matches the current entity
                if (CompName == Name):

                    # get out all of the floating parameters
                    MyValue = self.GetBlock(MyChildren[ichild])

                    # loop through all of the values
                    for ikey, ival in MyValue.items():

                        # get the value
                        MyVal = ival

                        # convert the unicode to a string
                        if (isinstance(MyVal, unicode)):
                            MyVal = str(MyVal)
                        # end if

                        # add them to the current dictionary
                        TempDict.update({str(ikey) : MyVal})

                    # end for
                # end if

                # look for the system architecture
                if (FindArch == True):

                    # flag for names with understcores
                    UseArray = 0

                    # old string to compare base string to
                    OldBaseString = ""

                    # get the children of this branch package
                    MoreChildren = MyChildren[ichild].getOwnedElement()

                    # loop through these children
                    for jchild in range(len(MoreChildren)):

                        # get the child's name
                        ChildName = MoreChildren[jchild].getName()

                        # check if a double underscore exists
                        HasUnder = ChildName.find("__")

                        # if an underscore exists, check if we're in an array
                        if (HasUnder != -1):

                            # get the new base string
                            NewBaseString = ChildName[:HasUnder]

                            # check if the strings match
                            if (NewBaseString == OldBaseString):

                                # remember the indices
                                Indices = ChildName.split("__")[1:]

                                # change each index to an integer
                                for ival in range(len(Indices)):
                                    IntIndices[ival] = max(IntIndices[ival], int(Indices[ival]))
                                # end for
                                
                                # get the information
                                MyValue = self.GetBlock(MoreChildren[jchild])
                                
                                # convert the unicode to a string
                                if (isinstance(MyValue, unicode)):
                                    MyValue = str(MyValue)
                                # end if

                                # append to the array
                                TempArray.append(MyValue)

                            else:

                                # check if another array already exists
                                if (UseArray == 1):

                                    # increment the indices by 1
                                    for ival in range(len(IntIndices)):
                                        IntIndices[ival] += 1
                                    # end for

                                    # reshape the temporary array
                                    FinalArray = ReshapeArray(TempArray, IntIndices)

                                    # reset the integer indices
                                    for ival in range(len(IntIndices)):
                                        IntIndices[ival] = 0
                                    # end for
                                    
                                    # write out the first array
                                    TempDict.update({str(OldBaseString): FinalArray})

                                else:

                                    # strt using the array
                                    UseArray = 1

                                # end if

                                # remember the indices
                                Indices = ChildName.split("__")[1:]
                                
                                # create a list for the actual indices
                                IntIndices = [0] * len(Indices)
                                
                                # change each index to an integer
                                for ival in range(len(Indices)):
                                    IntIndices[ival] = max(IntIndices[ival], int(Indices[ival]))
                                # end for
                                
                                # remember the new string
                                OldBaseString = NewBaseString

                                # get the value
                                MyValue = self.GetBlock(MoreChildren[jchild])

                                # start the array
                                TempArray = [MyValue]

                            # end if

                        else:

                            # check if we were in an array
                            if (UseArray == 1):

                                # increment the indices by 1
                                for ival in range(len(IntIndices)):
                                    IntIndices[ival] += 1
                                # end for

                                # reshape the temporary array
                                FinalArray = ReshapeArray(TempArray, IntIndices)

                                # reset the integer indices
                                for ival in range(len(IntIndices)):
                                    IntIndices[ival] = 0
                                # end for
                                
                                # write out the array
                                TempDict.update({str(OldBaseString) :  FinalArray})

                                # the array is no longer being used
                                UseArray = 0

                            # end if

                            # get the value
                            MyValue = self.GetBlock(MoreChildren[jchild])

                            # check if the value is unicode
                            if (isinstance(MyValue, unicode)):

                                # convert it to a string
                                MyValue = str(MyValue)

                            # end if

                            # add the element as normal
                            TempDict.update({str(ChildName) : MyValue})

                        # end if
                    # end for

                    # check if an array needs to be written
                    if (UseArray == 1):

                        # increment the indices by 1
                        for ival in range(len(IntIndices)):
                            IntIndices[ival] += 1
                        # end for
                        
                        # reshape the temporary array
                        FinalArray = ReshapeArray(TempArray, IntIndices)

                        # reset the integer indices
                        for ival in range(len(IntIndices)):
                            IntIndices[ival] = 0
                        # end for
                        
                        # turn off the flag
                        UseArray = 0
                        
                        # write out the first array
                        TempDict.update({str(OldBaseString) : FinalArray})
                        
                    # end if
                    
                # end if

                # look for the other reserved words
                if (FindPerf == True) or (FindReqs == True) or (FindBhvr == True):

                    # get the children of this branch's package
                    MoreChildren = MyChildren[ichild].getOwnedElement()

                    # define a local dictionary
                    LocalDict = {}

                    # flag for names with underscores
                    UseArray = 0

                    # old string to compare base string to
                    OldBaseString = ""

                    # loop through these children
                    for jchild in range(len(MoreChildren)):

                        # get the child's name
                        ChildName = MoreChildren[jchild].getName()

                        # check if a double underscore exists
                        HasUnder = ChildName.find("__")

                        # if an underscoreexists, check if we're in an array
                        if (HasUnder != -1):

                            # get the new base string
                            NewBaseString = ChildName[:HasUnder]

                            # check if the strings match
                            if (NewBaseString == OldBaseString):

                                # remember the indices
                                Indices = ChildName.split("__")[1:]

                                # change each index to an integer
                                for ival in range(len(Indices)):
                                    IntIndices[ival] = max(IntIndices[ival], int(Indices[ival]))
                                # end for

                                # get the information
                                MyValue = self.GetBlock(MoreChildren[jchild])

                                # check for unicode values
                                if (isinstance(MyValue, unicode)):
                                    MyValue = str(MyValue)
                                # end if

                                # append to the array
                                TempArray.append(MyValue)

                            else:

                                # check if another array already exists
                                if (UseArray == 1):

                                    # increment indices by 1
                                    for ival in range(len(IntIndices)):
                                        IntIndices[ival] += 1
                                    # end for

                                    # reshape the temporary array
                                    FinalArray = ReshapeArray(TempArray, IntIndices)

                                    # reset the integer indices
                                    for ival in range(len(IntIndices)):
                                        IntIndices[ival] = 0
                                    # end for
                                    
                                    # write out the first array
                                    LocalDict.update({str(OldBaseString) : FinalArray})

                                else:

                                    # start using the array
                                    UseArray = 1

                                    # remember the indices
                                    Indices = ChildName.split("__")[1:]

                                    # create a list for the actual indices
                                    IntIndices = [0] * len(Indices)

                                    # change each index to an integer
                                    for ival in range(len(Indices)):
                                        IntIndices[ival] = max(IntIndices[ival], int(Indices[ival]))
                                    # end for
                                # end if

                                # remember the new string
                                OldBaseString = NewBaseString

                                # get the value
                                MyValue = self.GetBlock(MoreChildren[jchild])

                                # start the array
                                TempArray = [MyValue]

                            # end if

                        else:

                            # check if we were in an array
                            if (UseArray == 1):

                                # increment the indices by 1
                                for ival in range(len(IntIndices)):
                                    IntIndices[ival] += 1
                                # end for

                                # reshape the temporary array
                                FinalArray = ReshapeArray(TempArray, IntIndices)

                                # reset the integer indices
                                for ival in range(len(IntIndices)):
                                    IntIndices[ival] = 0
                                # end for
                                
                                # write out the array
                                LocalDict.update({str(OldBaseString) : FinalArray})

                                # the array is no longer being used
                                UseArray = 0

                            # end if

                            # get the value
                            MyValue = self.GetBlock(MoreChildren[jchild])

                            # make sure unicode becomes a string
                            if (isinstance(MyValue, unicode)):
                                MyValue = str(MyValue)
                            # end if

                            # add them to the current dictionary
                            LocalDict.update({str(ChildName) : MyValue})

                        # end if
                    # end for

                    # check if an array nneeds to be written
                    if (UseArray == 1):

                        # increment the indices by 1
                        for ival in range(len(IntIndices)):
                            IntIndices[ival] += 1
                        # end for

                        # reshape the temporary array
                        FinalArray = ReshapeArray(TempArray, IntIndices)

                        # reset the integer indices
                        for ival in range(len(IntIndices)):
                            IntIndices[ival] = 0
                        # end for
                        
                        # turn off the flag
                        UseArray = 0

                        # write out the array
                        LocalDict.update({str(OldBaseString) : FinalArray})

                    # end if

                    # get the keys from the current local dictionary
                    try:

                        # assume the dictionary is not loaded
                        DictLoaded = 0

                        # loop through all the keys
                        for ikey in LocalDict.keys():
                            
                            # check if the key matches the reserved word
                            if (str(Name).lower() == ikey):

                                # load the dictionary without the key
                                TempDict.update(LocalDict)

                                # flag that the dictionary was loaded
                                DictLoaded = 1
                                
                            # end if
                        # end for

                        # check if the dictionary was not loaded
                        if (DictLoaded == 0):

                            # add in a key to pair with the value
                            TempDict.update({str(Name).lower() : LocalDict})
                            
                        # end if

                    except:
                        pass

                    # end try-except
                # end if
            # end for

            # assemble into the larger dictionary
            MySysDict.update(TempDict)

        elif (BlockType == 3):

            # get the requirement text
            MyReq = SH.getStereotypePropertyFirst(ParentBlock, self.ReqSter, "Text")

            # split the string into parts
            StringParts = MyReq.split(" ")

            # get the value and units
            MyVals = float(StringParts[-2])
            MyUnit = StringParts[-1]

            # get the description
            MyDesc = MyReq.split(" shall be ")[0]
            MyDesc = MyDesc.split(": ")[1]

            # get the name
            MyName = MyReq.split("):")[0]
            
            # update the existing dictionary
            MySysDict.update({"name" : MyName[1:]})
            MySysDict.update({"description" : MyDesc})
            MySysDict.update({"value" : {"value" : MyVals, "units" : str(MyUnit)}})
            
        # end if
        
        # return the dictionary
        return MySysDict

    # end GetBlock

    # -------------------------------------------------------

    def GetBlockValue(self, Block, ParentBlock = None):
        
        # get the element type
        MyStereotype = Block.getAppliedStereotype()
        
        # assume an empty dictionary
        MyValu = {}

        # check if there are stereotypes
        if (len(MyStereotype) > 0):
        
            # loop through all the stereotypes
            for itype in MyStereotype:

                # get the stereotype name and convert to a string
                foo = str(itype.getName())
                
                # check if the stereotype is a block
                if (foo == "Block"):
                    
                    # search a level deeper
                    MyValu = self.GetBlock(Block)
                    
                # check if the stereotype is a value property
                elif (foo == "ValueProperty"):
                    
                    # get the value property
                    ValSpec = Block.getDefaultValue()
                    
                    # get the type of property it is
                    Type = str(ValSpec.getHumanName())
                    
                    # check if the value specification exists
                    if ValSpec is None:

                        # return an empty array
                        MyValue = []
                        
                    elif Type == "Literal Boolean":
                        
                        # return the value
                        MyValu = ValSpec.isValue()
                        
                    else:
                        
                        # try getting the value
                        MyValu = ValSpec.getValue()
                        
                    # end if
                    
                # end if
            # end for

        else:

            # assume that it is a null property and return an empty array
            MyValu = []

        # end if

        # return the value
        return MyValu

    # end GetBlockValue

    # -------------------------------------------------------    
    
# end ModelStructureGenerator

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

###############################
#                             #
# INTERFACE PANEL             #
#                             #
###############################

class InterfacePanel(FilenamePanel):

    # initialization
    def __init__(self, Element):

        # remember the parent element
        self.MyParentElement = Element

        # initialize
        FilenamePanel.__init__(self)

        # update the components
        self.updateComponents()

    # end __init__


    
    # update components
    def updateComponents(self):

        # do nothing
        pass

    # end updateComponents
# end InterfacePanel

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

###############################
#                             #
# OPTIMIZATION DIALOG         #
#                             #
###############################

class FilenameDialog(JDialog):

    # initialization
    def __init__(self, Parent, Element):

        # remember the parent element
        self.MyParentElement = Element

        # initlaize the dialog
        JDialog.__init__(self, Parent, "ADH Filename Input", False)

        # create the panels
        self.Panel = InterfacePanel(Element)

        # set the content
        self.setContentPane(self.Panel)

        # pack the content
        self.pack()

        # set the location
        self.setLocationRelativeTo(Parent)

        # set the closing operation
        self.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE)

    # end __init__
# end FilenameDialog

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------


###############################
#                             #
# execute the code            #
#                             #
###############################

# run the code
try:
    
    # run the plugin class
    UpdateADH()

except Exception as e:
    
    # print exception header
    print "Code run error - UpdateADH with Dialog"
    
    # print the exception
    print(e)

# end try-except
