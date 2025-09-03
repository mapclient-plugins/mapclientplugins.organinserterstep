"""
MAP Client Plugin Step
"""
from PySide6 import QtGui
from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.organinserterstep.configuredialog import ConfigureDialog
from mapclientplugins.organinserterstep.model.organ_inserter import OrganInserter

import json
import os


class OrganInserterStep(WorkflowStepMountPoint):
    def __init__(self, location):
        super(OrganInserterStep, self).__init__('Organ Inserter', location)
        self._configured = False  # A step cannot be executed until it has been configured.
        self._category = 'Registration'
        # Add any other initialisation code here:
        self._icon = QtGui.QImage(':/organinserterstep/images/registration.png')
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#file_location'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses-list-of',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#file_location'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#file_location'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses-list-of',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#file_location'))
        # Port data:
        self._port0_inputHostFile = None  # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location
        self._port1_inputOrgansToEmbedFile = None  # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location
        self._port2_output_marker_data_file = None  # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location
        self._port3_inputTemplatesFile = None  # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location
        # Config:
        self._config = {'identifier': '',
                        'common trunk keywords': '[MFr]\d{3}-left, [MFr]\d{3}-right',
                        'pass through keywords': 'tract, diaphragm, bone, muscle, arteries, veins'}
        self._organ_inserter = None

    def execute(self):
        """
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        """
        # Put your execute step code here before calling the '_doneExecution' method.

        self._organ_inserter = OrganInserter(self._port0_inputHostFile, self._port1_inputOrgansToEmbedFile,
                                             self._port3_inputTemplatesFile, self.get_common_trunk_keywords(),
                                             self.get_pass_through_keywords(), self._location)
        self._port2_output_marker_data_file = self._organ_inserter.get_output_file_name()

        self._doneExecution()

    def setPortData(self, index, dataIn):
        """
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.

        :param index: Index of the port to return.
        :param dataIn: The data to set for the port at the given index.
        """
        if index == 0:
            self._port0_inputHostFile = dataIn  # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location
        elif index == 1:
            self._port1_inputOrgansToEmbedFile = dataIn  # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location
        elif index == 3:
            self._port3_inputTemplatesFile = dataIn  # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location

    def getPortData(self, index):
        """
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.
        :param index: Index of the port to return.
        """
        files = []
        for file in self._port2_output_marker_data_file:
            files.append(os.path.realpath(os.path.join(self._location, file)))
        return files  # http://physiomeproject.org/workflow/1.0/rdf-schema#multiple_file_locations
        # return self._port2_output_marker_data_file  # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location

    def configure(self):
        """
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        """
        dlg = ConfigureDialog(self._main_window)
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)

        if dlg.exec_():
            self._config = dlg.getConfig()

        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        """
        The identifier is a string that must be unique within a workflow.
        """
        return self._config['identifier']

    def setIdentifier(self, identifier):
        """
        The framework will set the identifier for this step when it is loaded.
        """
        self._config['identifier'] = identifier

    def get_common_trunk_keywords(self):
        return self._config['common trunk keywords']

    def get_pass_through_keywords(self):
        return self._config['pass through keywords']

    def serialize(self):
        """
        Add code to serialize this step to string.  This method should
        implement the opposite of 'deserialize'.
        """
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        """
        Add code to deserialize this step from string.  This method should
        implement the opposite of 'serialize'.
        :param string: JSON representation of the configuration in a string.
        """
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()
