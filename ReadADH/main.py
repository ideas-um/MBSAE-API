"""

READ ADH:

    Read in the JSON file, creating SysML blocks for each
    component with a work breakdown structure (WBS) number
    and any structured/nested data. The lowest level data not
    attributed with a WBS number is set as a value property
    to the next lowest level block. Requirements are created
    as requirement blocks in the SysML model.

Written by Paul Mokotoff, prmoko@umich.edu

Last Updated: 21 Mar 2025

Inputs:

    ADH File within the "Magic Systems of Systems Architect"
    directory on your computer.

Outputs:

    SysML model representative of the input JSON file.

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
import com.nomagic.magicdraw.uml.Finder                              as Finder
import com.nomagic.uml2.ext.jmi.helpers.StereotypesHelper            as SH
import com.nomagic.uml2.ext.magicdraw.classes.mdkernel               as MDKernel

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

    # initialization function
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

    # initialization function
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

    # configuration function
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

    # priority function for MagicDraw
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

class ReadADH(Plugin):

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
        Action = BrowserAction("ReadADH", "MBSA&E: Read ADH")

        # create the configuration
        Configuration = BrowserConfiguration(Action)

        # add the configuration
        ACM.getInstance().addContainmentBrowserContextConfigurator(Configuration)

    # end __init__

    # -------------------------------------------------------

    # MagicDraw routine to close the plugin
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

    # MagicDraw routine to check if the plugin is supported
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
    
# end ReadADH

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

###############################
#                             #
# FILENAME PANEL              #
#                             #
###############################

class FilenamePanel(JPanel):

    # initialization function
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
        Generator = ModelStructureGenerator()
        
        # execute the generator on the object
        Generator.execute(Filename)
        
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
    """

    Flatten(Arr)

    Flatten an array from a n-dimensional array into a 1-dimensional array.

    INPUTS:
        Arr   : the n-dimensional array to be flattened

    OUTPUTS:
        result: the flattened 1-dimensional array

    """

    # remember the result
    result = []

    # -------------------------------------------------------
    
    # define helper function
    def SubFlatten(SubArr):
        """

        SubFlatten(SubArr)

        Recursively called function that takes each array element and expands it into a 1-dimensional array.

        INPUTS:
            SubArr: the subset of the array being flattened

        OUTPUTS:
            none (appended to "result" variable defined previously)

        """

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

    # -------------------------------------------------------
    
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
    """

    GetShape(Arr)

    Get the shape of an n-dimensional array by looking at the shape of its zero'th element recursively.

    INPUTS:
        Arr: the array to be analyzed

    OUTPUTS:
        a tuple of length n, where n is the number of dimensions in the input array.

    """
    
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
    """

    WriteIndices(Name, *Shapes)

    Given an n-dimensional array, write all the names of the array elements as: VarName__i__j__...__k

    INPUTS:
        Name     : the name of the variable that will be repeated

        *Shapes  : a tuple representing the shape of the array whose elements will be written out as described above

    OUTPUTS:
        OutString: a list of strings following the naming convention outlined previously

    """

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

###############################
#                             #
# MODEL STRUCTURE GENERATOR   #
#                             #
###############################

class ModelStructureGenerator():

    # initialization function
    def __init__(self):
        """

        __init__(self)

        Initialize the model structure generator, which creates a SysML model.

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
    def execute(self, Filename):
        """

        execute(self, Filename)

        Run the JSON parser and create the model elements for the SysML model.

        INPUTS:
            self         : the SysML model

            Filename     : the name of the JSON file to be read for creating the SysML model

        OUTPUTS:
            none

        """        
        
        # try to create a session
        try:

            # create the session
            SM.getInstance().createSession(self.Project, "Read ADH")            

            # get the block stereotype from the SysML stereotype profile
            self.BlockSter = SH.getStereotype(self.Project, "Block", "SysML::Blocks")

            # get the requirement stereotype from the SysML stereotype profile
            self.ReqSter = SH.getStereotype(self.Project, "Requirement", "SysML::Requirements")

            # get the types for integers, reals, and strings
            self.Integer = Finder.byQualifiedName().find(self.Project, "SysML::Libraries::PrimitiveValueTypes::Integer")
            self.Real    = Finder.byQualifiedName().find(self.Project, "SysML::Libraries::PrimitiveValueTypes::Real")
            self.String  = Finder.byQualifiedName().find(self.Project, "SysML::Libraries::PrimitiveValueTypes::String")
            self.Boolean = Finder.byQualifiedName().find(self.Project, "SysML::Libraries::PrimitiveValueTypes::Boolean")
            
            # import the ADH and create stereotypes
            self.ImportADH(Filename)

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

    # read a JSON file
    def ImportADH(self, Filename):
        """

        ImportADH(self, Filename)

        Read a JSON file to create the system model.

        INPUTS:
            self    : the SysML model

            Filename: the JSON file to read and create the SysML model from

        OUTPUTS:
            none

        """
        
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
        
        # try to open and read the JSON file
        try:

            # open a JSON file
            f = open(Filename, "r")

            # read the file
            MyString = f.read()

            # convert to a JSON string
            MyJSON = json.loads(MyString)

            # close the file
            f.close()
                
            # create a finder for the model
            self.QualNameFind = Finder.byName()
            
            # traverse the nested dictionary and create stereotypes within the input class
            self.GetData(MyJSON, self.Model, 0, None)

        except Exception as e:
        
            # print the exception
            Application.getInstance().getGUILog().showMessage("ADH Import Failed:\n" + repr(e))

        # end try-except
    # end ImportADH

    # -------------------------------------------------------

    # function to recursively get data from the JSON file
    def GetData(self, MyJSON, ParentPackage, ReqSterFlag, HigherLevelComp = None):
        """

        GetData(self, MyJSON, ParentPackage, ReqSterFlag, HigherLevelComp = None):

        Look for all components with WBS numbers, create stereotypes for them, and establish dependency relationships between the higher- and lower-level components.

        INPUTS:
            self           : the SysML model

            MyJSON         : the subset of the JSON string being analyzed

            ParentPackage  : the higher-level package that has already been created (if any) and where the next set of model elements will reside

            ReqSterFlag    : flag to show that a requirement needs to be made (1) or not (0)

            HigherLevelComp: (optional, assumed None) the higher-level component used as theowner of the part property generated between a higher-/lower-level component pair

        OUTPUTS:
            none

        """
        
        # try to get the data
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
                    self.MakePackages(ivalue, MainPackage)
                    
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

                        # create a property
                        PartProperty = self.Factory.createPropertyInstance()

                        # set the owner to the higher level component
                        PartProperty.setOwner(HigherLevelComp)

                        # set the part property type as the lower level component
                        PartProperty.setType(ComponentClass)

                        # use the lower level component's name as the property name
                        PartProperty.setName(ComponentClass.getName())

                        # set a composite association
                        PartProperty.setAggregation(MDKernel.AggregationKindEnum.COMPOSITE)

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

                        # get the length of the list
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

    # function to create a new package
    def CreatePackage(self, Name):
        """

        CreatePackage(self, Name)

        Create a package for the system model.

        INPUTS:
            self      : the SysML model

            Name      : the name of the package

        OUTPUTS:
            NewPackage: the package created

        """

        # create a package
        NewPackage = self.Factory.createPackageInstance()

        # set the name
        NewPackage.setName(Name)

        # return the package
        return NewPackage

    # end CreatePackage

    # -------------------------------------------------------

    # function to create a new instance
    def CreateInstance(self, Name, ReqFlag = 0):
        """

        CreateInstance(self, Name, ReqFlag = 0)

        Create a block or stereotype instance.

        INPUTS:
            self    : the SysML model

            Name    : the name of the instance

            ReqFlag : flag to make a requirement (1) or block (0), default is block (0)

        OUTPUTS:
            NewClass: an instance in the SysML model

        """

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

    # function to read data and make specific values for each array element (if needed)
    def ReadData(self, Block, Key, Value, ReqFlag):
        """

        ReadData(self, Block, Key, Value, ReqFlag)

        Read a key-value pair from a JSON string and process it by making the appropriate model elements in the SysML model.

        INPUTS:
            self   : the SysML model

            Block  : the current block that additional model elements will be built on

            Key    : the current key from the JSON string

            Value  : the current value corresponding to the key in the JSON string

            ReqFlag: flag to make a requirement (1) or not (0)

        OUTPUTS:
            Block  : the current block with additional model elements built off of it

        """
        
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
                
            # end for
                
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

            # create an empty value property
            Block = self.CreateProperty(Block, Key, None)
                    
        # end if
        
        # return the block
        return Block
        
    # end ReadData

    # -------------------------------------------------------

    # function to create value properties
    def CreateProperty(self, Block, Key, Value):
        """

        CreateProperty(self, Block, Key, Value)

        Create a value property using either a Boolean, integer, float, or string

        INPUTS:
            self : the SysML model

            Block: the curent block that the value properties will be built on

            Key  : the name  of the value property to be created

            Value: the value of the value property to be created

        OUTPUTS:
            Block: the block with the value properties built on

        """
        
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

    # function to add a stereotype from a stereotype profile
    def AddStereotype(self, Block, Name):
        """

        AddStereotype(self, Block, Name)

        Add a stereotype from the stereotype profile to a block that was just created.

        INPUTS:
            self : the SysML model

            Block: the block that the stereotype is being added to

            Name : the name of the stereotype to be added

        OUTPUTS:
            Block: the block with the stereotype added on

        """
        
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

    # function to read a value into a value property
    def ReadFloatingValue(self, ParentPackage, ikey, ivalue):
        """

        ReadFloatingValue(self, ParentPackage, ikey, ivalue)

        Read a value into a value property by finding the appropriate model element (a block).

        INPUTS:
            self         : the SysML model

            ParentPackage: the higher-level package that contains a block to read Value Properties into

            ikey         : the Value Property name

            ivalue       : the Value Property value

        OUTPUTS:
            none

        """

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

    # function to read a data structure into a specialized package
    def ReadDataStructure(self, ParentPackage, ikey, ivalue, ReqFlag):
        """

        ReadDataStructure(self, ParentPackage, ikey, ivalue, ReqFlag)

        Read the data structure within a JSON string and process it accordingly by finding the appropriate package to add data.

        INPUTS:
            self         : the SysML model

            ParentPackage: the higher-level package that contains packages for checking

            ikey         : the reserved word that creates a special package

            ivalue       : the model element to be created in the package

            ReqFlag      : flag to indicate whether a requirement should be made (1) or not (0)

        OUTPUTS:
            none

        """
       
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

    # function to make the necessary packages
    def MakePackages(self, ivalue, MainPackage):
        """

        MakePackages(self, ivalue, MainPackage)

        Given a new package corresponding to a component with a WBS number, make the necessary sub-packages based on the words in the JSON string value.

        INPUTS:
            self       : the SysML model

            ivalue     : the JSON string value to be processed (another dictionary)

            MainPackage: the parent package that will house the packages constructed here

        OUTPUTS:
            none

        """
        
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

    # end MakePackages
    
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

    # initialization function
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
    
    # read the ADH
    ReadADH()

except Exception as e:
    
    # print exception header
    print("Code run error - ReadADH")
    
    # print the exception
    print(e)

# end try-except
