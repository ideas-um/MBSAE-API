"""

WRITE INSTANCE:

    From an Instance Specification in a SysML model, write a
    JSON file, which includes all part properties and value
    properties nested within the Instance Specification.

Written by Paul Mokotoff, prmoko@umich.edu

Last Updated: 21 Mar 2025

Inputs:

    SysML model containing at least one Instance
    Specification.

Outputs:

    JSON file with all of the part and value properties
    nested within the highest-level Instance Specification
    selected.

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

class WriteInstance(Plugin):

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
        Action = BrowserAction("WriteADH", "MBSA&E: Write Instance to ADH")

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
    
# end WriteInstance

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
        Writer = ADHInstanceWriter()
        
        # execute the generator on the object
        Writer.execute(self.MyParentElement, Filename)
        
    # end DoneListener

    # -------------------------------------------------------

# end FilenamePanel

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

###############################
#                             #
# FUNCTION TO RESHAPE ARRAYS  #
#                             #
###############################

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

    # end ConstructNewShape
    
    # -------------------------------------------------------

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

class ADHInstanceWriter():

    # initialization
    def __init__(self):
        """

        __init__(self)

        Initialization function for the ADH instance writer.

        INPUTS:
            self: the class for writing the instance.

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

        Function to run the ADH instance writer.

        INPUTS:
            self         : the ADH instance writer class.

            ParentPackage: the highest-level model element selected.

            Filename     : the name of the JSON file input by the user.

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
            MyDict = self.GetBlock(ParentPackage, 1)

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

    def GetBlock(self, ParentBlock, HighestLevel):
        """

        GetBlock(self, ParentBlock, HighestLevel)

        Function to recursively explore a branch of the instance to be written.

        INPUTS:
            self        : the ADH instance writer class

            ParentBlock : the highest-level block selected

            HighestLevel: flag to indicate whether this block was selected by the user (1) or not (0)

        OUTPUTS:
            MySysDict   : dictionary representing the system and its nested part and value properties

        """

        # create two dictionaries for storing data
        MySysDict = {}
        TempDict  = {}
        
        # get the name
        TempName = ParentBlock.getHumanName()

        # get the component name
        CompName = TempName.split("Instance Specification ")[1]

        # try to get only the component name (not the entire path)
        try:

            # split up all of the sub-names and take the last one
            CompName = CompName.split(".")[-1]

        except:

            # do nothing
            pass

        # end try-except
        
        # get the children of the current block
        MyChildren = ParentBlock.getSlot()

        # flag for names with underscores
        UseArray = 0

        # string to compare other strings to (for array writing)
        OldBaseString = ""
        
        for ichild in range(len(MyChildren)):
            
            # get the defining feature
            MyFeature = MyChildren[ichild].getDefiningFeature()
            
            # get the name
            FeatureName = MyFeature.getHumanName()
            
            # get the value
            MyValue = MyChildren[ichild].getValue()                

            # check for the type of feature
            if ("Value Property " in FeatureName):

                # get the property name
                PropertyName = str(FeatureName.split("Value Property ")[1])

                # get the value
                PropertyValue = MyValue[0].getValue()

                # check if the name has an underscore
                HasUnder = PropertyName.find("__")

                # if an underscore exists, follow the procedure
                if (HasUnder != -1):

                    # get the new base string
                    NewBaseString = PropertyName[:HasUnder]

                    # get the indices
                    Indices = PropertyName.split("__")[1:]
                    
                    # check if the strings match
                    if (NewBaseString == OldBaseString):

                        # change each index to an integer
                        for ival in range(len(Indices)):

                            # convert the value and take the maximum for array space allocation
                            IntIndices[ival] = max(IntIndices[ival], int(Indices[ival]))

                        # end for

                        # append to the array
                        TempArray.append(PropertyValue)

                    else:

                        # check if another array already exists
                        if (UseArray == 1):

                            # loop through all indices
                            for ival in range(len(IntIndices)):

                                # increment the indices by 1
                                IntIndices[ival] += 1

                            # end for

                            # reshape the temporary array
                            FinalArray = ReshapeArray(TempArray, IntIndices)

                            # write out the first array
                            TempDict.update({str(OldBaseString) : FinalArray})

                        else:

                            # start using the array
                            UseArray = 1

                            # create a list for the actual indices
                            IntIndices = [0] * len(Indices)

                            # change each index to an integer
                            for ival in range(len(Indices)):

                                # convert the value and take the maximum for array space allocation
                                IntIndices[ival] = max(IntIndices[ival], int(Indices[ival]))

                            # end for
                        # end if

                        # remember the new string
                        OldBaseString = NewBaseString

                        # remember the value in an array
                        TempArray = [PropertyValue]

                    # end if

                else:

                    # check if we were in an array
                    if (UseArray == 1):

                        # loop through all the indices
                        for ival in range(len(IntIndices)):

                            # increment the indices by 1
                            IntIndices[ival] += 1

                        # end for

                        # reshape the temporary array
                        FinalArray = ReshapeArray(TempArray, IntIndices)

                        # write out the first array
                        TempDict.update({str(OldBaseString) : FinalArray})

                        # the array is no longer used, turn off the flag
                        UseArray = 0

                    # end if

                    # check if the value is unicode
                    if (isinstance(PropertyValue, unicode)):

                        # convert it to a string
                        PropertyValue = str(PropertyValue)

                    # end if
                
                    # update the dictionary
                    TempDict.update({PropertyName : PropertyValue})
                                
            elif ("Part Property " in FeatureName):

                # get the part property name
                PropertyName = str(FeatureName.split("Part Property ")[1])

                # get the next instance specification
                NextInst = MyChildren[ichild].getOwnedElement()[0]
                
                # get the instance value
                InstanceValue = NextInst.getInstance()

                # recursively search the model
                NewDict = self.GetBlock(InstanceValue, 0)

                # check if a double underscore exists
                HasUnder = PropertyName.find("__")

                # if an underscore exists, check if we're in an array
                if (HasUnder != -1):

                    # get the new base string
                    NewBaseString = PropertyName[:HasUnder]

                    # get the indices
                    Indices = PropertyName.split("__")[1:]

                    # check if the strings match
                    if (NewBaseString == OldBaseString):

                        # change each index to an integer
                        for ival in range(len(Indices)):

                            # convert the value to an integer and take the maximum for array space allocation
                            IntIndices[ival] = max(IntIndices[ival], int(Indices[ival]))

                        # end for

                        # append to the array
                        TempArray.append(NewDict[PropertyName])

                    else:

                        # check if another array already exists
                        if (UseArray == 1):

                            # loop through all the indices
                            for ival in range(len(IntIndices)):

                                # increment the indices by 1
                                IntIndices[ival] += 1

                            # end for

                            # reshape the temporary array
                            FinalArray = ReshapeArray(TempArray, IntIndices)

                            # write out the first array
                            TempDict.update({OldBaseString : FinalArray})

                        else:

                            # start using the array
                            UseArray = 1

                            # create a list for the actual indices
                            IntIndices = [0] * len(Indices)

                            # change each index to an integer
                            for ival in range(len(Indices)):

                                # conert the value to an integer and take the maximum for array space allocation
                                IntIndices[ival] = max(IntIndices[ival], int(Indices[ival]))

                            # end for
                        # end if

                        # remember the new string
                        OldBaseString = NewBaseString

                        # remmeber the value in an array
                        TempArray = [NewDict[PropertyName]]

                    # end if

                else:

                    # check if we were in an array
                    if (UseArray == 1):

                        # loop through all the indices
                        for ival in range(len(IntIndices)):

                            # increment the indices by 1
                            IntIndices[ival] += 1

                        # end for

                        # reshape the temporary array
                        FinalArray = ReshapeArray(TempArray, IntIndices)

                        # write out the first array
                        TempDict.update({OldBaseString : FinalArray})

                        # the array is no longer used, turn off the flag
                        UseArray = 0

                    # end if

                    # update the dictionary
                    TempDict.update(NewDict)

                # end if
            # end if

        # end for

        # check if the array is still in use after iterating
        if (UseArray == 1):

            # loop through all the indices
            for ival in range(len(IntIndices)):
                
                # increment the indices by 1
                IntIndices[ival] += 1
                
            # end for
            
            # reshape the temporary array
            FinalArray = ReshapeArray(TempArray, IntIndices)
            
            # write out the first array
            TempDict.update({OldBaseString : FinalArray})
            
            # the array is no longer used, turn off the flag
            UseArray = 0

        # end if

        # check whether the block name must be written or not
        if (HighestLevel == 1):
            
            # update with only the dictionary
            MySysDict.update(TempDict)
            
        else:
            
            # add a name with the dictionary
            MySysDict.update({str(CompName) : TempDict})
            
        # end if

        return MySysDict

    # end GetBlock

    # -------------------------------------------------------
    
# end ADHInstanceWriter

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
    
    # write an instance to the ADH
    WriteInstance()

except Exception as e:
    
    # print exception header
    print("Code run error - WriteInstance")
    
    # print the exception
    print(e)

# end try-except
