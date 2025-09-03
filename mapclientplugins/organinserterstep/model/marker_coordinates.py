"""
MarkerCoordinates class and functions for dealing with markers in 3D whole body and organ scaffolds.
"""
from cmlibs.utils.zinc.general import ChangeManager
from cmlibs.utils.zinc.field import findOrCreateFieldGroup, findOrCreateFieldCoordinates,\
    findOrCreateFieldStoredString
from cmlibs.zinc.context import Context
from cmlibs.zinc.field import Field
from cmlibs.zinc.node import Node
from cmlibs.zinc.result import RESULT_OK
from mapclientplugins.organinserterstep.model.base_output_file import BaseOutputFile

import os


class MarkerCoordinates(BaseOutputFile):
    def __init__(self, input_scaffold_file, output_directory):
        super().__init__()
        self._context = Context('markerBodyCoordinates')
        self._region = self._context.createRegion()
        self._region.setName('bodyRegion')
        self._field_module = self._region.getFieldmodule()
        self._scaffold_file = input_scaffold_file
        self._model_coordinates_field = None
        self._marker_region = None

        self._load()
        self._get_marker_coordinates()
        marker_region = self._get_marker_region()
        self._save(marker_region, output_directory)

    def _discover_coordinate_fields(self):
        field = None
        if self._model_coordinates_field:
            field = self._field_module.findFieldByName(self._model_coordinates_field)
        else:
            mesh = self._get_highest_dimension_mesh()
            element = mesh.createElementiterator().next()
            if element.isValid():
                field_cache = self._field_module.createFieldcache()
                field_cache.setElement(element)
                field_iter = self._field_module.createFielditerator()
                field = field_iter.next()
                while field.isValid():
                    if field.isTypeCoordinate() and (field.getNumberOfComponents() == 3) \
                            and (field.castFiniteElement().isValid()):
                        if field.isDefinedAtLocation(field_cache):
                            break
                    field = field_iter.next()
                else:
                    field = None
        if field:
            self._set_model_coordinates_field(field)

    def get_marker_fields(self):
        marker_group_names = []
        marker_name = False
        marker_location_name = False
        marker_group_name = False
        field_iter = self._field_module.createFielditerator()
        field = field_iter.next()
        while field.isValid():
            field_name = field.getName()
            if 'marker' in field_name.lower() and '_' in field_name.lower():
                marker_group_name = field_name
                marker_group_names.append(marker_group_name)
                if 'name' in field_name.lower():
                    marker_name = field_name
                elif 'location' in field_name.lower():
                    marker_location_name = field_name
            field = field_iter.next()
        if all([marker_name, marker_location_name, marker_group_names]):
            return marker_location_name, marker_name, marker_group_names
        else:
            raise AssertionError('Could not find marker fields')

    def _get_highest_dimension_mesh(self):
        for d in range(2, -1, -1):
            mesh = self._mesh[d]
            if mesh.getSize() > 0:
                return mesh
        return None

    def _load(self):
        result = self._region.readFile(self._scaffold_file)
        assert result == RESULT_OK, "Failed to load model file" + str(self._scaffold_file)
        self._mesh = [self._field_module.findMeshByDimension(d + 1) for d in range(3)]
        self._discover_coordinate_fields()

    def _save(self, region, output_directory):
        filename = os.path.basename(self._scaffold_file).split('.')[0] + '_marker_coordinates.exnode'
        path = output_directory
        self._output_filename = os.path.join(path, filename)
        region.writeFile(self._output_filename)

    def _get_marker_coordinates(self):
        field_cache = self._field_module.createFieldcache()
        nodes = self._field_module.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)

        marker_location_name, marker_name, marker_group_names = self.get_marker_fields()

        markerLocation = self._field_module.findFieldByName(marker_location_name)
        markerName = self._field_module.findFieldByName(marker_name)

        self._marker_region = self._region.createRegion()
        marker_fieldmodule = self._marker_region.getFieldmodule()
        temp_nodes = marker_fieldmodule.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
        marker_fieldCache = marker_fieldmodule.createFieldcache()
        marker_data_coordinates = findOrCreateFieldCoordinates(marker_fieldmodule, name="marker_data_coordinates",
                                                               components_count=3)
        marker_data_name = findOrCreateFieldStoredString(marker_fieldmodule, name="marker_data_name")
        marker_data_group = findOrCreateFieldGroup(marker_fieldmodule, name="marker")
        marker_data_nodesGroup = marker_data_group.createNodesetGroup(temp_nodes)

        markerTemplateInternal = temp_nodes.createNodetemplate()
        markerTemplateInternal.defineField(marker_data_name)
        markerTemplateInternal.defineField(marker_data_coordinates)
        markerTemplateInternal.setValueNumberOfVersions(marker_data_coordinates, -1, Node.VALUE_LABEL_VALUE, 1)

        for marker_group_name in marker_group_names:
            markerGroup = self._field_module.findFieldByName(marker_group_name)
            markerNodes = None
            if markerGroup.isValid():
                markerGroup = markerGroup.castGroup()
                markerNodes = markerGroup.getNodesetGroup(nodes)

            if markerLocation.isValid() and markerName.isValid():
                with ChangeManager(marker_fieldmodule):
                    marker_coordinates = self._field_module.createFieldEmbedded(self._model_coordinates_field,
                                                                                markerLocation)
                    nodeIter = markerNodes.createNodeiterator()
                    node = nodeIter.next()
                    while node.isValid():
                        marker_node = temp_nodes.createNode(node.getIdentifier(), markerTemplateInternal)
                        marker_data_nodesGroup.addNode(marker_node)

                        marker_fieldCache.setNode(marker_node)
                        field_cache.setNode(node)
                        result, x = marker_coordinates.evaluateReal(field_cache, 3)
                        result = marker_data_coordinates.setNodeParameters(marker_fieldCache, -1, Node.VALUE_LABEL_VALUE, 1, x)
                        if result == RESULT_OK:
                            name = markerName.evaluateString(field_cache)
                            if name:
                                marker_data_name.assignString(marker_fieldCache, name)
                        node = nodeIter.next()

    def _set_model_coordinates_field(self, model_coordinates_field: Field):
        finite_element_field = model_coordinates_field.castFiniteElement()
        assert finite_element_field.isValid() and (finite_element_field.getNumberOfComponents() == 3)
        self._model_coordinates_field = finite_element_field

    def _get_marker_region(self):
        return self._marker_region
