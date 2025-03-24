"""

WRITE ADH:

    From a SysML model, write a JSON file, which includes all
    blocks, value properties, packages, and requirements.

Written by Paul Mokotoff, prmoko@uich.edu

Last Updated: 21 Mar 2025

Inputs:

    SysML model for the system architecture to be written.

Outputs:

    JSON file with all blocks, value properties, packages,
    and requirements from the SysML model.

"""

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

###############################
#                             #
# IMPORTS                     #
#                             #
###############################

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
import com.nomagic.uml2.ext.jmi.helpers.StereotypesHelper            as SH

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

class WriteADH(Plugin):

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
        Action = BrowserAction("WriteADH", "MBSA&E: Write to ADH")

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

    # -------------------------------------------------------
    
# end WriteADH

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
        """

        initComponents(self)

        Function to initalize the components and layout for the ADH file popup

        INPUTS:
            self: the java panel

        OUTPUTS:
            none

        """

        # define the components
        self.MainPanel = JPanel()
        self.Title = JLabel()
        self.TextLabel = JLabel()
        self.FilenameInput = JTextField()
        self.RunButton = JButton()

        # setup the main panel
        self.MainPanel.setBackground(Color(255, 255, 255))
        self.MainPanel.setBorder(BorderFactory.createLineBorder(Color(0, 0, 0), 4))
        self.MainPanel.setPreferredSize(Dimension(780, 600))

        # setup the title
        self.Title.setBackground(Color(255, 255, 255))
        self.Title.setFont(Font("Times New Roman", 1, 24))
        self.Title.setText("ADH Read/Write/Update")

        # setup the label below the title
        self.TextLabel.setBackground(Color(255, 255, 255))
        self.TextLabel.setFont(Font("Times New Roman", 1, 18))
        self.TextLabel.setText("Filename (must be in Program Files --- Magic System of Systems Architect folder):")

        # setup the filename box
        self.FilenameInput.setFont(Font("Times New Roman", 0, 14))
        self.FilenameInput.setText("Input filename to be read/written/updated")

        # setup the "run" button
        self.RunButton.setFont(Font("Times New Roman", 1, 12))
        self.RunButton.setText("Run")
        self.RunButton.addActionListener(self.DoneListener)

        # create the main panel layout
        MainPanelLayout = GroupLayout(self.MainPanel)
        self.MainPanel.setLayout(MainPanelLayout)

        # arranage horizontally
        MainPanelLayout.setHorizontalGroup( \
            MainPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING) \
            .addGroup(MainPanelLayout.createSequentialGroup() \
                .addContainerGap() \
                .addGroup(MainPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING) \
                    .addComponent(self.Title, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE) \
                    .addGroup(MainPanelLayout.createSequentialGroup() \
                        .addGap(0, 0, Short.MAX_VALUE) \
                        .addComponent(self.RunButton)) \
                    .addGroup(MainPanelLayout.createSequentialGroup() \
                        .addComponent(self.FilenameInput, GroupLayout.PREFERRED_SIZE, 500, GroupLayout.PREFERRED_SIZE) \
                        .addGap(0, 0, Short.MAX_VALUE)) \
                    .addComponent(self.TextLabel, GroupLayout.DEFAULT_SIZE, 718, Short.MAX_VALUE)) \
                .addContainerGap()) \
        )

        # arrange vertically
        MainPanelLayout.setVerticalGroup( \
            MainPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING) \
            .addGroup(MainPanelLayout.createSequentialGroup() \
                .addContainerGap() \
                .addComponent(self.Title, GroupLayout.PREFERRED_SIZE, 33, GroupLayout.PREFERRED_SIZE) \
                .addGap(18, 18, 18) \
                .addComponent(self.TextLabel) \
                .addPreferredGap(ComponentPlacement.RELATED) \
                .addComponent(self.FilenameInput, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE) \
                .addPreferredGap(ComponentPlacement.RELATED, 28, Short.MAX_VALUE) \
                .addComponent(self.RunButton)
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)) \
        )

        # create the overall panel layout
        layout = GroupLayout(self)
        self.setLayout(layout)

        # arrange horizontally
        layout.setHorizontalGroup( \
            layout.createParallelGroup(GroupLayout.Alignment.LEADING) \
            .addGroup(layout.createSequentialGroup() \
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE) \
                .addComponent(self.MainPanel, GroupLayout.PREFERRED_SIZE, 746, GroupLayout.PREFERRED_SIZE)) \
        )

        # arrange vertically
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
        Filename = self.FilenameInput.getText()

        # generate the model structure
        Writer = ADHWriter()
        
        # execute the generator on the object
        Writer.execute(self.MyParentElement, Filename)
        
    # end DoneListener

    # -------------------------------------------------------

# end FilenamePanel

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

def ReshapeArray(Arr, NewShape):
    """

    ReshapeArray(Arr, NewShape)

    Function to change the shape of an array into a new one for processing.

    INPUTS:
        Arr     : the current array

        NewShape: a tuple representing the shape of the new array to be returned

    OUTPUTS:
        the new array after being reshaped

    """

    # helper function to recursively construct the reShaped array
    def ConstructNewShape(Arr, Shape):
        """

        ConstructNewShape(Arr, Shape)

        Helper function to take parts of an array and put them together to make a larger array.

        INPUTS:
            Arr  : the current array

            Shape: a tuple describing the desired shape of the array

        OUTPUTS:
            pieces of the newly shaped array, one dimension at a time

        """

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
# ADH WRITER                  #
#                             #
###############################

class ADHWriter():

    # -------------------------------------------------------

    # initialization
    def __init__(self):
        """

        __init__(self)

        Initialize the writer, which exports the SysML model.

        INPUTS:
            self: the SysML model

        OUTPUTS:
            none

        """
        
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
        """

        execute(self, ParentPackage, Filename)

        Extract the model elements from the SysML model and convert their information to a JSON string.

        INPUTS:
            self         : the SysML model

            ParentPackage: the highest-level model element that the model elements will be stored in

            Filename     : the name of the JSON file to be read for updating the SysML model

        OUTPUTS:
            none

        """
                
        # try to create a session
        try:

            # create the session
            SM.getInstance().createSession(self.Project, "Write ADH")

            # get the requirement stereotype from the SysML stereotype profile
            self.ReqSter = SH.getStereotype(self.Project, "Requirement", "SysML::Requirements")

            # get the name of the parent pacakge
            ParentPackageName = ParentPackage.getName()
            
            # get the dictionary needed for writing to the ADH
            MyDict = self.GetBlock(ParentPackage)

            # convert the dictionaries to JSON strings
            OutJSON = json.dumps({ParentPackageName : MyDict}, indent = 4, ensure_ascii = True)
            
            # open a file
            f = open(Filename, "w")

            # print the JSON string to the file
            f.write(OutJSON)

            # close the file
            f.close()

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

    def GetBlock(self, ParentBlock):
        """

        GetBlock(self, ParentBlock)

        Get the JSON string associated with a block and its owned model elements.

        INPUTS:
            self       : the SysML model

            ParentBlock: the block whose children will be searched

        OUTPUTS:
            MySysDict  : dictionary to be converted to a JSON string

        """
        
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

                            # reset indices
                            for ival in range(len(IntIndices)):
                                IntIndices[ival] = 0
                            # end for

                            # write out the first array
                            MySysDict.update({str(OldBaseString) : FinalArray})

                        else:

                            # begin using the array
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

                        # reset indices
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

                # reset indices
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

                                    # reset indices
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

                                # reset indices
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

                        # reset indices
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

                                    # reset indices
                                    for ival in range(len(IntIndices)):
                                        IntIndices[ival] = 0
                                    # end for
                                    
                                    # write out the first array
                                    LocalDict.update({str(OldBaseString) : FinalArray})

                                else:

                                    # start using the array
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

                                # reset indices
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

                        # reset indices
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

    def GetBlockValue(self, Block):
        """

        GetBlockValue(self, Block)

        Look at a single model element and extract information based on its stereotype.

        INPUTS:
            self       : the SysML model

            Block      : the model element being analyzed

        OUTPUTS:
            MyValu     : a dictionary to be converted to a JSON string, which contains the information about the model element

        """
        
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
                        MyValu = []
                        
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

            # assume that it is a null property (i.e., an empty value property) and return an empty array
            MyValu = []

        # end if

        # return the value
        return MyValu

    # end GetBlockValue

    # -------------------------------------------------------
    
# end ADHWriter

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
        """

        __init__(self, Element)

        Function to initialize the panel that requests an ADH file name.

        INPUTS:
            self   : the java panel

            Element: the highest-level model element selected in the system model.

        OUTPUTS:
            none

        """

        # remember the parent element
        self.MyParentElement = Element

        # initialize
        FilenamePanel.__init__(self)

        # update the components
        self.updateComponents()

    # end __init__

    # -------------------------------------------------------
    
    # update components
    def updateComponents(self):
        """

        updateComponents(self)

        Function to update the panel, not used.

        INPUTS:
            self: the java panel

        OUTPUTS:
            none

        """

        # do nothing
        pass

    # end updateComponents

    # -------------------------------------------------------
    
# end InterfacePanel

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

###############################
#                             #
# FILENAME DIALOG             #
#                             #
###############################

class FilenameDialog(JDialog):

    # initialization
    def __init__(self, Parent, Element):
        """

        __init__(self, Parent, Element)

        Function to initialize the dialog panel to request an ADH file name.

        INPUTS:
            self   : the java dialog class

            Parent : the parent container for the dialog box

            Element: the highest-level element in the system model selected by the user

        OUTPUTS:
            none

        """

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

    # -------------------------------------------------------
    
# end FilenameDialog

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------


###############################
#                             #
# EXECUTE THE CODE            #
#                             #
###############################

# run the code
try:
    
    # write out the ADH
    WriteADH()

except Exception as e:
    
    # print exception header
    print("Code run error - WriteADH")
    
    # print the exception
    print(e)

# end try-except
