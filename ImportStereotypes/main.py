"""

IMPORT STEREOTYPES:

    For a given JSON file, identify all components that
    have a work-breakdown structure (WBS) number
    associated with it. Then, make a stereotype for each
    of those components and store them in a stereotype
    profile within a SysML model.

 Written by Paul Mokotoff, prmoko@umich.edu

 Last Updated: 21 Mar 2025

 Inputs:

     ADH file within the "Magic Systems of Systems Architect"
     directory on your computer.

 Outputs:

     Stereotype Profile package called "ImportADHProfile"
     in a SysML model.

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
import com.nomagic.uml2.ext.jmi.helpers.CoreHelper                   as CH

# import java packages
import java.awt.Color     as Color
import java.awt.Dimension as Dimension
import java.awt.Font      as Font
import java.lang.Short    as Short
import java.util.Arrays   as Arrays #from java.util import Arrays

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

class ImportStereotype(Plugin):

    # initialization function
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
        Action = BrowserAction("ImportStereotypes", "MBSA&E: Import Stereotypes")

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
    
# end ImportStereotype

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

###############################
#                             #
# FILENAME DIALOG             #
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
        Generator.execute(self.MyParentElement, Filename)
        
    # end DoneListener

    # -------------------------------------------------------

# end FilenamePanel

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

        Initialize the model structure generator, which creates a stereotype profile.

        INPUTS:
            self: the SysML model

        OUTPUTS:
            none

        """

        # get the project
        self.Project = Application.getInstance().getProject()

        # get the elements factory
        self.Factory = self.Project.getElementsFactory()

        # get the model elements manager instance
        self.Manager = MEM.getInstance()

        # get the model
        self.Model = self.Project.getModel()
        
    # end __init__

    # -------------------------------------------------------

    # action execution
    def execute(self, ParentPackage, Filename):
        """

        execute(self, ParentPackage, Filename)

        Run the stereotype importer and create a stereotype profile.

        INPUTS:
            self         : the SysML model

            ParentPackage: the highest-level model element that the stereotype profile will be stored in

            Filename     : the name of the JSON file to be read for importing the stereotypes

        OUTPUTS:
            none

        """

        # try to create a session
        try:

            # create the session
            SM.getInstance().createSession(self.Project, "Import Stereotypes")

            # remember the parent package for setting up dependencies
            self.ParentPackage = ParentPackage
            
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

    # import the ADH by reading a JSON file
    def ImportADH(self, Filename):
        """

        ImportADH(self, Filename)

        Read a JSON file to create the stereotype profile.

        INPUTS:
            self    : the SysML model

            Filename: the JSON file to read and import the stereotypes from

        OUTPUTS:
            none

        """

        # create a profile
        self.Profile = self.Factory.createProfileInstance()

        # set its name
        self.Profile.setName("ImportADHProfile")

        # add the profile to the model
        MEM.getInstance().addElement(self.Profile, self.Model)

        # get the class metadata
        self.MetaClass = SH.getMetaClassByName(self.Project, "Class")
        
        # try to open and read the JSON file
        try:

            # open a JSON file
            f = open(Filename, "r")

            # read the file and return as a string
            MyString = f.read()

            # convert string to a nested dictionary
            MyJSON = json.loads(MyString)

            # close the file
            f.close()

            # traverse the nested dictionary and create stereotypes within the input class
            self.GetData(MyJSON, self.Profile)

        except Exception as e:
        
            # print the exception
            Application.getInstance().getGUILog().showMessage("ADH Import Failed:\n" + repr(e))

        # end try-except
    # end ImportADH

    # -------------------------------------------------------

    # function to recursively get data from the JSON file
    def GetData(self, MyJSON, MyParent):
        """

        GetData(self, MyJSON, MyParent)

        Look for all components with WBS numbers, create stereotypes for them, and establish dependency relationships between the higher- and lower-level components.

        INPUTS:
            self    : the SysML model

            MyJSON  : the subset of the JSON string being analyzed

            MyParent: the higher-level stereotype that has already been created (if any)

        OUTPUTS:
            none

        """

        # try to get the data
        try:

            # check for a dictionary
            if isinstance(MyJSON, dict):
                
                # loop through the JSON string
                for key, value in MyJSON.items():
                    
                    # check if there is a name and description
                    if "wbs_no" in value:

                        # get the name
                        Name = value["name"]
                        
                        # check for a description
                        if "description" in value:
                            
                            # create a stereotype with a description
                            NewStereotype = self.ImportStereotype(MyParent, key, value["description"])
                            
                        else:
                            
                            # create a stereotype without a description
                            NewStereotype = self.ImportStereotype(MyParent, key)
                            
                        # end if
                        
                        # check if the value is a dictionary
                        if isinstance(value, dict):
                            
                            # go a level deeper
                            self.GetData(value, NewStereotype)
                            
                        # end if            
                    
                    elif isinstance(value, dict):
                        
                        # go a level deeper
                        self.GetData(value, MyParent)
                        
                    elif isinstance(value, list):
                        
                        # loop through each one
                        for ival in range(len(value)):

                            # get the dictionary
                            TempDict = value[ival]

                            # get the name
                            TempName = TempDict["name"]
                            
                            # go a level deeper
                            self.GetData({TempName : value[ival]}, MyParent)
                            
                        # end for                    
                    # end if
                # end for

            elif isinstance(MyJSON, list):
                
                # loop through the elements in the list
                for ielem in range(len(MyJSON)):

                    # get the dictionary
                    TempDict = MyJSON[ielem]

                    # get the component name
                    TempName = TempDict["name"]

                    # get the data from each component
                    self.GetData({TempName : MyJSON[ielem]}, MyParent)
                    
                # end for

            else:

                # do nothing
                pass

            # end if

        except:

            # do nothing
            pass

        # end try-except
    # end GetData

    # -------------------------------------------------------

    # function for creating stereotypes on each block
    def ImportStereotype(self, MyParent, Value, Description = None):
        """

        ImportStereotype(self, MyParent, Value, Description = None)

        Create a stereotype and set a dependency between itself and the higher-level stereotype.

        INPUTS:
            self         : the SysML model

            MyParent     : the higher-level stereotype for setting dependencies

            Value        : the name of the stereotype

            Description  : (optional, assumed to not exist) description of the stereotype, placed in the JSON file as a "description" key and is at the same level as the WBS number

        OUTPUTS:
            NewStereotype: the stereotype added to the profile

        """

        # create a stereotype
        SH.createStereotype(self.Profile, Value, Arrays.asList(self.MetaClass))

        # get the stereotype profile
        MyProfile = SH.getProfile(self.Project, "ImportADHProfile")

        # get the stereotype
        NewStereotype = SH.getStereotype(self.Project, Value, MyProfile)
        
        # check for a description
        if Description:

            # create a comment
            NewComment = self.Factory.createCommentInstance()

            # remember the commnet
            NewComment.setBody(Description)

            # add the comment to the class for now
            NewStereotype.getOwnedComment().add(NewComment)

        # end if

        # create a dependency
        MyDependency = self.Factory.createDependencyInstance()        
        
        # set the supplier and client elements
        CH.setSupplierElement(MyDependency, MyParent     )
        CH.setClientElement(  MyDependency, NewStereotype)

        # add the dependency and stereotype to the profile
        self.Manager.addElement(MyDependency , MyProfile)
        self.Manager.addElement(NewStereotype, MyProfile)

        # return the stereotype
        return NewStereotype
        
    # end ImportStereotype

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

        # initialize the panel and plugin
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
    
    # import the stereotypes
    ImportStereotype()

except Exception as e:
    
    # print exception header
    print("Code run error - ImportStereotype")
    
    # print the exception
    print(e)

# end try-except
