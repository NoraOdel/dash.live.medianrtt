# dash.live.medianrtt

## Summary

   * This program does the following:
      1. Downloads and parses previously defined RIPE atlas DNS measurements.
      2. Produces a CSV file with the results from one or more specified NameServer/s, and enriches the results with:
         * probe's country
         * probe's continent
         * probe's subregion
         * probe's firmware version
         * Probe's Coordinates
      3. Plots a live line-graph based on RTTs from result file. The graph is updated every 4 seconds



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

 #go to Files dir
 $ cd Main/

 #read to run:
 $ python3  render.py

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
   * Changing this is NOT recommended since 3 files are created every 4 seconds --> A LOT OF FILES

