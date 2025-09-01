"""
Common trunk inserter for inserting organs with a common trunk.  Currently implemented for inserting vagus scaffolds by
calling SSV tools to modify the trunk coordinates for insertion.
"""
import os

from cmlibs.zinc.context import Context
from mapclientplugins.organinserterstep.model.base_output_file import BaseOutputFile
from ssvtools.modify_coordinates import adopt_template_trunk_coordinates


class CommonTrunkInserter(BaseOutputFile):

    def __init__(self, organ_file, template_file, output_directory, trunk_group_name):
        super().__init__()

        context = Context("InsertCommonTrunk")
        region = context.getDefaultRegion()
        region.readFile(organ_file)
        fieldmodule = region.getFieldmodule()
        coordinates_field = fieldmodule.findFieldByName("coordinates").castFiniteElement()
        template_region = region.createRegion()
        template_region.readFile(template_file)
        template_fieldmodule = template_region.getFieldmodule()
        unit_conversion_factor = None

        template_coordinates_field = template_fieldmodule.findFieldByName("coordinates").castFiniteElement()
        adopt_template_trunk_coordinates(region, coordinates_field, template_region, template_coordinates_field,
                                         trunk_group_name, unit_conversion_factor)
        filename = os.path.splitext(os.path.basename(organ_file))[0]
        filenameNew = filename + '_transformed.exf'
        self._output_filename = os.path.join(output_directory, filenameNew)
        region.writeFile(self._output_filename)
