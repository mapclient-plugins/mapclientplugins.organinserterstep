Organ Inserter Step
============================

Overview
--------

The **Organ Inserter** step is an interactive plugin for the MAP-Client.

The **Organ Inserter** currently inserts organ scaffold in the whole body scaffold via one of the three available modes: common trunk, pass through and default.

The *common trunk* mode adopts a trunk from a template scaffold file and uses the path of the template trunk to determine the path of the branches of an organ scaffold. The template scaffold has to be derived from the same subject from which the whole body scaffold was generated from. This mode is currently used for inserting subject-specific vagus scaffolds. It can potentially be used in future for handling airways, circulatory systems or other nerves.

The *pass through* mode handles organ scaffolds that have already been built or are derived from the same subject as the whole body scaffold. They should already be in the same coordinate system as the whole body scaffold and will not require any further processing for organ insertion, hence these scaffold files will be passed right through. Currently used for gastrointestinal tract, diaphragm, bone, muscle, arteries and veins.

The *default* mode performs a rigid body transformation to align fiducial markers in the organ scaffold to the same markers present in the whole body scaffold in order to achieve organ insertion. This mode will require at least 3 non-collinear markers for each organ to work.  This is currently used for inserting the brainstem, heart, lungs and bladder.

This tool takes a `Zinc` compatible whole body scaffold EX file as a first input, one or more `Zinc` compatible organ scaffold EX file as a second input and one or more `Zinc` compatible template organ scaffold EX file as an optional third input. The **Organ Inserter** step outputs a series of `Zinc` compatible EX files of the organ scaffolds with coordinates transformed to the same coordinate system as the whole body scaffold, effectively resulting in the insertion of the organs in the whole body scaffold.

Specification
-------------

Information on this plugin's specifications is available :ref:`here <mcp-organinserter-specification>`.


Configuration
-------------

Information on this plugin's configuration is available :ref:`here <mcp-organinserter-configuration>`.


Workflow Setup
--------------

Information on setting up a workflow with this plugin can be found :ref:`here <mcp-organinserter-workflow-setup>`.


Instructions
------------
This is a non-interactive step.


.. toctree::
   :maxdepth: 2
   :hidden:

   specification
   configuration
   workflow-setup
