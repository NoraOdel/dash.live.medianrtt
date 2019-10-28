# dash.try.live

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
 $ git clone https://github.com/NoraOdel/dash.try.live.git

 #Download requirements.txt and spatialindex
 $ cd dash.try.live/
 $ activate your virtualenv
 $ pip install -r requirements.txt
 $ brew install spatialindex

 #go to Files dir
 $ cd Files/

 #read to run:
 $ python3  ../chaos2countries/run.py

 #Optional argument input (if no arguments are defined the program refers to default values)
 $ -ns --> Choose one or more NameServers to visualize by typing -ns followed by wanted nameservers.
           Format = xy(z), where x is a specific letter and y either 4 or 6 depending on desired IPv.
           Letters to choose from: a, b

           If one desires to plot a map with both IPv4 and IPv6 use z aswell --> x46 or x64
           Choose multiple NameServers to plot by typing them all out with a space between each
           like so: -ns a4 b4 a46

 $ -time --> Choose measurements initiation by typing -time followed by desired time-of-initiation
             format = yyyy-mm-dd hh:mm:ss

 $ Default is a4 (which equals to a.ns.se IPv4) at current utc-time.

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

   * html-file to rendered visualization

   Each output file will be deleted from the project next time the program is run
   ie. files in each folder after execution will be those relevant to that exact run.
