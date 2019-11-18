# dash.live.medianrtt

## Summary

   * These programs does the following:
      1. Downloads and parses previously defined RIPE atlas DNS measurements.
      2. Produces a CSV file with the results from one or more specified NameServer/s, and enriches the results with:
         * probe's country
         * probe's continent
         * probe's subregion
         * probe's firmware version
         * Probe's Coordinates
      3. renderlive.py plots a live line-graph based on RTTs from result file. The graph is updated every 4 seconds
      4. renderlinegraph.py plots a line-graph based on RTTs from result file. The interval can be change in the code
      5. cousteau.py creates measurements based on our needs along with a file filled with connecting measurementIDs



## Demo
   * https://atlas.ripe.net/api/v2/measurements/23033112/results/?start=1571184000&stop=1571270399&format=json


## How-to running the program and generating the plot

 ```bash

 #Clone the repository
 $ git clone https://github.com/NoraOdel/dash.live.medianrtt.git

 #Download requirements.txt
 $ cd dash.live.medianrtt/
 $ activate your virtualenv
 $ pip install -r requirements.txt


 #read to run:
 $ python3  renderlive.py (alternatively renderlinegraph.py or cousteau.py)

  ```

### Output files
    The demo will produce the following output files on your local dir.

   * Results file similar to this: ``a4-20191016-1571205731-1571206331-atlas-results.csv``
      * Different components are:
         *  ``measurementID=a4``
         *  ``date=20191016``
         *  ``start=1571184000``
         *  ``stop=1571270399``
              (each measurement has a duration of 10 min)

   * Probemetadata --> ``20191016-probemetadata.json.gz``
     * This includes information (listed above in 'this program does the following')
       about Ripe-Atlas probes

   * These files will be continuously deleted, this can be changed in the script.
   * Changing this is NOT recommended since 3 files are created every 4 seconds if renderlive.py is run --> A LOT OF FILES

   * MeasurementID file consisting of measurementIDs and connecting NameServers

