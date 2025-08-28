"""
OrganTransformer class and functions for aligning markers from organ scaffolds to markers in whole body scaffold.
"""
import os

from PySide6 import QtCore, QtWidgets

from mapclientplugins.organinserterstep.model.base_output_file import BaseOutputFile
from scaffoldfitter.fitter import Fitter
from scaffoldfitter.fitterstepalign import FitterStepAlign
# from scaffoldfitter.fitterstepfit import FitterStepFit

class OrganTransformer(BaseOutputFile):

    def __init__(self, input_zinc_model_file, input_zinc_data_file, output_directory):
        super().__init__()
        self._fitter = Fitter(input_zinc_model_file, input_zinc_data_file)
        self._fitter.load()
        self.set_model_coordinates_field()

        file_basename = os.path.basename(input_zinc_model_file).split('.')[0]
        filename = file_basename + '_transformed'
        path = output_directory
        self._output_filename = os.path.join(path, filename)

        self._currentFitterStep = FitterStepAlign()
        self._fitter.addFitterStep(self._currentFitterStep)  # Future: , lastFitterStep
        self._currentFitterStep.setAlignMarkers(True)
        self._currentFitterStep.run(modelFileNameStem=self._output_filename)

        # Previous fit step added by Elias
        # self._currentFitterStep = FitterStepFit()
        # self._fitter.addFitterStep(self._currentFitterStep)  # Future: , lastFitterStep
        # self._currentFitterStep.setGroupStrainPenalty(None, [0.001])
        # self._currentFitterStep.setGroupCurvaturePenalty(None, [200.0])
        # self._currentFitterStep.setGroupDataWeight(None, 1000.0)

        print("Transforming organ ({}) via default mode... It may take a minute".format(file_basename))
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        # self._currentFitterStep.run(modelFileNameStem=self._output_filename)
        # self._output_filename = self._output_filename + '_fit1.exf'
        self._output_filename = self._output_filename + '_align.exf'
        QtWidgets.QApplication.restoreOverrideCursor()
        print('Transformation is done')

    def set_model_coordinates_field(self):
        field_module = self._fitter.getFieldmodule()
        modelCoordinatesFieldName = "coordinates"
        field = field_module.findFieldByName(modelCoordinatesFieldName)
        if field.isValid():
            self._fitter.setModelCoordinatesFieldByName(modelCoordinatesFieldName)
