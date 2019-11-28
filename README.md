# dash.live.medianrtt

## Summary

   * This repository includes the following programs:
        1. cousteau.py --> creates DNS-measurements, changes can easily be made to the definitions
        2. renderlinegraph.py --> renders a line-graph for one or more nameservers between a specified timeperiod
        3. renderlive.py --> renders a live line-graph for on or more nameservers
        4. scatterrtt.py --> renders a scatter-plot for one nameserver between a specified timeperiod.
           Every timestamp in this timeperiod connects to all rtt-values in the resultfile from that time



   * Running any of the last tree programs does the following apart from rendering:
        1. Downloads and parses previously defined RIPE atlas DNS measurements.
        2. Produces a CSV file with the results from one or more specified NameServer/s, and enriches the results with probemetadata
        3. Produces a gz.file with probemetadata:
         * probe's country
         * probe's continent
         * probe's subregion
         * probe's firmware version
         * Probe's Coordinates


## Demo of json-result from Ripe Atlas
   * https://atlas.ripe.net/api/v2/measurements/23033112/results/?start=1571184000&stop=1571270399&format=json


## How-to run the programs and generate the plot

 ```bash

 #Clone the repository
 $ git clone https://github.com/NoraOdel/dash.live.medianrtt.git

 #Download requirements.txt
 $ cd dash.live.medianrtt/
 $ activate your virtualenv
 $ pip install -r requirements.txt


 #read to run:
 $ python3 cousteau.py OR
 $ python3 renderlinegraph.py OR
 $ python3 renderlive.py OR
 $ python3 scatterrtt.py

 #required arguments for renderlinegraph.py, renderlive.py and scatterrtt.py:
 $ firstlast --> timeperiod to plot in datetime format ie. yyy-mm-dd hh:mm:ss (start) and yyy-mm-dd hh:mm:ss (stop)

 #optional arguments:
 $ -ns --> choose which nameservers to plot, ex. a.ns.se4 (the last element refers to IPv, 4 or 6)
 $ -interval --> choose interval between result fetching, default is 10 minutes

 # EXAMPLE:
 $ python3 scatterrtt.py 2019-11-22 12:00:00 2019-11-23 12:00:00 -ns a.ns.se4 z.ns.se4 b.ns.se6 -interval 30
 $ This would create a scatter plot with a timeperiod between 2019-11-22 12:00:00 and 2019-11-23 12:00:00,
 $ for nameservers a.ns.se4, z.ns.se4  and b.ns.se6 with an interval of 30 minutes


  ```

### Output files on your local dir

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

   * MeasurementID file consisting of measurementIDs and connecting NameServers

   * These files will be continuously deleted, this can be changed in the script.
   * Changing this is NOT recommended since one or more files are created every 6 seconds if renderlive.py is run --> A LOT OF FILES

