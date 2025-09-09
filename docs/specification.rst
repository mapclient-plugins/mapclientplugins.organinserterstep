.. _mcp-organinserter-specification:

Ports
-----

This plugin:

* **uses**:

 * *http://physiomeproject.org/workflow/1.0/rdf-schema#file_location*
 * *http://physiomeproject.org/workflow/1.0/rdf-schema#file_location*
 * *http://physiomeproject.org/workflow/1.0/rdf-schema#file_location*


and

* **provides**:

 * *http://physiomeproject.org/workflow/1.0/rdf-schema#file_location*

The first **uses** port imports a `Zinc` EX file containing a 3D whole body scaffold.
The second **uses** port imports one or multiple `Zinc` EX files consisting of individual organ scaffolds to be inserted into the whole body scaffold.
The third **uses** port imports one or multiple `Zinc` EX files consisting of template organ scaffolds that are previously derived from the whole body scaffold. This is an optional input port but is required when the organs are to be inserted using the common trunk mode.
The **provides** port outputs a series of `Zinc` EX files containing organ scaffolds inserted into the whole body.
