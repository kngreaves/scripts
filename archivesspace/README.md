# archivesspace
These scripts export data from ArchivesSpace in a variety of formats.

## Requirements
*   Python
*   Requests module
*   ConfigParser
*   Some of these scripts require `agentarchives`, a Python library for working with the ArchivesSpace API. Detailed installation instructions are available at [the repository](https://github.com/artefactual-labs/agentarchives/)

## Installation

Download [Python](https://www.python.org/downloads/) (must be 2.7 or higher).

If using Python 3 or higher, note that URLLib2 and ConfigParser have been renamed. Please see [here](http://stackoverflow.com/questions/16597865/is-there-a-library-for-urllib2-for-python-which-we-can-download) for support for URLLib2 and [here](http://stackoverflow.com/questions/14087598/python-3-3-importerror-no-module-named-configparser) for support for ConfigParser.

For further instructions on including Python in your PATH variable see [here](https://docs.python.org/2/using/windows.html).
For instructions on installing Python on Linux, see [here](http://docs.python-guide.org/en/latest/starting/install/linux/).

For further instructions on installing the Requests module through easy_install, see [here](http://stackoverflow.com/questions/17309288/importerror-no-module-named-requests).

Save `asExport-associatedMets.py`, `asExport-ead.py`, `asExport-mets.py`, and `asPublish.py` to your Python installation directory.

Some of these scripts require a local configurations file, which should be created in the same directory as the script and named `local_settings.cfg`. A sample file looks like this:

    [ArchivesSpace]
    # the base URL of your ArchivesSpace installation
    baseURL:http://localhost:8089
    # the id of your repository
    repository:2
    # the username to authenticate with
    user:admin
    # the password for the username above
    password:admin

    [Logging]
    filename = log.txt
    format = %(asctime)s %(name)s %(levelname)s %(message)s
    datefmt = %a, %d %b %Y %H:%M:%S
    level = DEBUG

    [Export]
    # a list of resource IDs to publish
    publishIDs = ["FA001", "FA002","FA003"]

    [Destinations]
    # export destinations
    dataDestination = /path/to/location
    EADdestination = /path/to/location
    METSdestination = /path/to/location
    MODSdestination = /path/to/location
    PDFdestination = /path/to/location

You can use the `config_settings.py` file found [here] (https://github.com/RockefellerArchiveCenter/templates/blob/master/config_setup.py) to automatically create a `local_settings.cfg` file.

## Usage
In the console or terminal, navigate to the directory containing the script you want and execute the script.
*   On Windows this will be something like `python asExport-ead.py`
*   On Mac or Linux systems you can simply type `./asExport-ead.py`

## advancedNoteEdit.py

Finds matching note content and type and replaces it with user-entered note content. (Python)

## archivalObjectNotes.py

Searches for specific words in a notes of archival objects, and writes each instance to a comma-separated file. (Python)

## asAutoReplaceContainers.py

Replaces duplicate top containers in a resource record based on whether barcodes have periods (".") or if they are empty. Only works for resources in which the box number does not restart. Finds all archival objects attached to an AS resource record through the resource id (database id), then loops through all instances in each archival object. Will pass over any digital object instances. Creates two dictionaries of "correct" and "incorrect" barcodes; any barcode with a '.' or empty will be considered incorrect and matched and then replaced with a correct barcode from a matching container indicator.

## asCSV-accessions.py

Exports accessions data in a comma-separated file format. (Python)

## asCSV-archivalObjects.py

Prompts user for resource identifier and then writes the title, display_string, dateexpression, begindate, enddate, refid, accessrestrict to a CSV file named `CatReports.csv`. (Python)

## asCSV-locations.py

Exports locations data in a comma-separated file format. (Python)

## asCSV-notes.py

Exports content from user-defined note types in a comma-separated file format. (Python)

## asCSV-titles.py

Exports titles from children of a user-defined resource in a comma-separated file format. (Python)

## asDeleteOrphanContainers.py

Searches all top containers in your ArchivesSpace database and looks for the collection link is greater than zero. If not, it deletes them. This removes any top containers not linked to a resource or archival object. (Python)

## asDeleteOrphanLocations.py

Reads locations from a csv file and deletes them as listed. (Python)

## asExport-associatedMets.py

Exports METS files from digital object records associated with a given resource. (Python)

## asExport-ead.py

Creates EAD files from resource records. Export can be scoped to specific records by using an optional argument to match against the resource ID. (Python)

## asExport-mets.py

Exports METS files from all digital object records. (Python)

## asExportAllFA.py

Exports all resource records containing "FA" in the identifier.

## asNotes.py

Matches accessrestrict notes to user-input text, checks every archival object in your ArchivesSpace database, deletes any accessrestrict notes with content exactly matching the user input content, and then posts the archival object back without the note.

## asPublish.py

Compares resource record IDs against a list, then publishes those which are present and unpublishes those which are not. (Python)

## asReplaceContainers.py

Loops over archival objects that are children of a given resource record and replaces container URIs for duplicate top containers. Relies on a comma-separated values (CSV) file named `containers.csv` with pairs of top container URIs, the second of which is a URI to replace, and the first of which is the URI with which the second should be replaced:

    /repositories/2/top_containers/15456,/repositories/2/top_containers/15457
    /repositories/2/top_containers/15461,/repositories/2/top_containers/15463
    /repositories/2/top_containers/15462,/repositories/2/top_containers/15451
    /repositories/2/top_containers/15454,/repositories/2/top_containers/15464
    /repositories/2/top_containers/15469,/repositories/2/top_containers/15477
    /repositories/2/top_containers/15478,/repositories/2/top_containers/15479

## asReplaceLocations.py

Loops over all top containers and replaces location URIs. Relies on a comma-separated values (CSV) file named `locations.csv` with pairs of location URIs, the second of which is a URI to replace, and the first of which is the URI with which the second should be replaced:

      /locations/15456,/locations/15457
      /locations/15461,/locations/15463
      /locations/15462,/locations/15451
      /locations/15454,/locations/15464
      /locations/15469,/locations/15477
      /locations/15478,/locations/15479

## post_objects.py
Posts archival objects based on existing JSON data. (Python)

## resourceNotes.py
Searches notes in all AS resources for the following terms: 'obsolete','digital','special format','equipment'. Then stores the full note content and writes it to a CSV. (Python)
