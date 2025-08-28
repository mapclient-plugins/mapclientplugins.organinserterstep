"""
OrganInserter class for analysing organ filenames and determining which mode to use for inserting organ into 3D whole
body. It is possible to insert using 3 modes:
(1) common trunk mode: Uses the trunk from a template file to determine the path of the organ trunk and branches.
    Currently used for vagus nerves scaffold. Potential use for airway, circulatory system or other nerves.
(2) pass-through mode: In this mode, the organ scaffold has already been built in the 3D whole body geometric
    coordinates and will not require addition work for insertion in the whole body. Currently used for GI tract organs.
(3) default mode: Suitable for organ scaffolds that have at least 3 non-collinear markers. The same markers need to be
    present in the 3D whole body for this to work. This mode aligns the markers in the scaffold to the position in the
    3D whole body for insertion purposes. Currently used for brainstem, bladder, heart, and lungs.
"""
from cmlibs.utils.zinc.general import ChangeManager
from cmlibs.zinc.context import Context
from mapclientplugins.organinserterstep.model.common_trunk_inserter import CommonTrunkInserter
from mapclientplugins.organinserterstep.model.marker_coordinates import MarkerCoordinates
from mapclientplugins.organinserterstep.model.organ_transformer import OrganTransformer

# import csv
import logging
import os
import re


logger = logging.getLogger(__name__)


class OrganInserter(object):
    def __init__(self, input_model_file, input_data_files, template_files, common_trunk_keywords, pass_through_keywords,
                 output_directory):

        self._input_data_files = input_data_files
        marker_coordinates = MarkerCoordinates(input_model_file, output_directory)

        # Convert keywords into regex patterns
        if pass_through_keywords:
            pass_through_patterns = [re.compile(keyword.strip(), re.IGNORECASE) for keyword in
                                     pass_through_keywords.split(',')]
        if common_trunk_keywords:
            common_trunk_patterns = [re.compile(keyword.strip(), re.IGNORECASE) for keyword in
                                     common_trunk_keywords.split(',')]

        # self.write_annotations(output_directory)
        self._output_filenames = []
        for file in input_data_files:
            filename = os.path.splitext(os.path.basename(file))[0]

            if pass_through_keywords and any(p.search(filename) for p in pass_through_patterns):
                print("Passing organ ({}) through".format(filename))
                self._output_filenames.append(file)
                self.add_organ_group(file)

            elif common_trunk_keywords and any(p.search(filename) for p in common_trunk_patterns):
                for pattern in common_trunk_patterns:
                    if re.search(pattern, filename):
                        if re.search(r'[r]\d{3}', filename, re.IGNORECASE):
                            logger.warning('organ_inserter: SSV from CASE will not be inserted at this stage.')
                            return
                        for template_file in template_files:
                            template_filename = os.path.splitext(os.path.basename(template_file))[0]
                            if re.search(pattern, template_filename):
                                print("Inserting organ ({}) via common trunk mode".format(filename))
                                trunk_group_name = "left vagus nerve" if "left" in filename else "right vagus nerve"
                                common_trunk_inserter = \
                                    CommonTrunkInserter(file, template_file, output_directory, trunk_group_name)
                                self._output_filenames.append(common_trunk_inserter.output_filename())
                                self.add_organ_group(common_trunk_inserter.output_filename())
            else:
                organ_transformer = OrganTransformer(file, marker_coordinates.output_filename(), output_directory)
                self._output_filenames.append(organ_transformer.output_filename())
                self.add_organ_group(organ_transformer.output_filename())

    def get_output_file_name(self):
        return self._output_filenames

    def get_organ_name(self, filename):
        organsList = ['lung', 'heart', 'brainstem', 'bladder']
        filename_base = os.path.basename(filename).split('.')[0]
        for organ_name in organsList:
            if organ_name in filename_base.lower():
                return organ_name
        else:
            return filename_base

    # def write_annotations(self, output_directory):
    #     DOI = ["https://doi.org/10.26275/yibc-wyu2", "https://doi.org/10.26275/dqpf-gqdt",
    #            "https://doi.org/10.26275/rets-qdch", "https://doi.org/10.26275/dqpf-gqdt",
    #            "https://doi.org/10.26275/yum2-z4uf", "https://doi.org/10.26275/xq3h-ba2b", "colon"]
    #     organ_names = ['whole-body']
    #     for filename in self._input_data_files:
    #         organ_names.append(self.get_organ_name(filename))
    #
    #     annotation_file = os.path.join(output_directory, 'organinserter_annotations.csv')
    #     with open(annotation_file, 'w', newline='') as fout:
    #         writer = csv.writer(fout)
    #         writer.writerow(['Organ name', 'Source', 'File name', 'Transformed file name'])
    #         writer.writerow([organ_names[0], DOI[0], 'whole_body.exf', 'whole_body.exf'])
    #         for c, filename in enumerate(self._input_data_files):
    #             filenamebase = os.path.basename(filename)
    #             writer.writerow([organ_names[c+1], DOI[c+1], filenamebase, filenamebase.split('.')[0]+'_transformed_fit1.exf'])

    def add_organ_group(self, filename):
        context = Context('organGroup')
        region = context.createRegion()
        region.readFile(filename)
        field_module = region.getFieldmodule()
        mesh = field_module.findMeshByDimension(3)
        with ChangeManager(field_module):
            field_group = field_module.createFieldGroup()
            organ_name = self.get_organ_name(filename)
            field_group.setName(organ_name)
            field_group.setSubelementHandlingMode(field_group.SUBELEMENT_HANDLING_MODE_FULL)
            mesh_group = field_group.createMeshGroup(mesh)
            is_organ = field_module.createFieldConstant(1)
            mesh_group.addElementsConditional(is_organ)
            sir = region.createStreaminformationRegion()
            srm = sir.createStreamresourceMemory()
            sir.setResourceGroupName(srm, organ_name)
            # sir.setResourceFieldNames(srm, fieldNames)
            region.write(sir)
            region.writeFile(filename)
