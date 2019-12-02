# dash.live.medianrtt

## Summary

   * This repository includes the following programs:
        1. measurement_creation.py --> creates user-defined DNS-measurement in Ripe Atlas
        2. renderlinegraph.py --> renders a line-graph for one or more nameservers between a specified timeperiod
        3. renderlive.py --> renders a live line-graph for on or more nameservers
        4. renderscatterplot.py --> renders a scatter-plot for one nameserver between a specified timeperiod
           Every timestamp in this timeperiod connects to all rtt values in the resultfile from that time



   * Running any of the last tree programs does the following apart from rendering:
        1. Downloads and parses previously defined RIPE atlas DNS measurements
        2. Produces a CSV file with the results from one or more specified NameServer/s, and enriches the results with probemetadata
        3. Produces a .gz.file with probe meta data:
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
 $ python3 measurement_creation.py (or)
 $ python3 renderlinegraph.py (or)
 $ python3 renderlive.py (or)
 $ python3 renderscatterplot.py

 #required arguments for renderlinegraph.py and renderscatterplot.py:
 $ first
   --> initial start time in datetime format ie. yyy-mm-dd hh:mm:ss

 #optional arguments:
 $ -ns  (option for renderlive.py aswell)
   --> choose which nameservers to plot, ex. a.ns.se4 (the last element refers to IPv, 4 or 6)
    renderlive.py, default is 'all4' which equals to every nameserver and its IPv4 traffic
 
 $ -interval  
   --> interval between result fetching, default is 10 minutes

 $ -numberofintervals
   --> number of intervals which defines the timeperiod for plot, default is 144. If numberofintervals is 144 and interval is 10 the timeperiod will be:
       144*10 = 1440 minutes --> 24h

 # EXAMPLE:
 $ python3 renderscatterplot.py 2019-11-22 12:00:00 2019-11-23 12:00:00 -ns a.ns.se4 z.ns.se4 b.ns.se6 -interval 30

   This would create a scatter plot with a timeperiod between 2019-11-22 12:00:00 and 2019-11-23 12:00:00,
   for nameservers a.ns.se4, z.ns.se4  and b.ns.se6 with an interval of 30 minutes


  ```

### Output files on your local dir

   * Results file similar to this: ``a.ns.se4-20191016-1571205731-1571206331-atlas-results.csv``
      * Different components are:
         *  ``measurementID for a.ns.se IPv4``
         *  ``date=20191016``
         *  ``start=1571184000``
         *  ``stop=1571270399`` (each measurement has a duration of 10 min)

   * Probe meta data file similar to this: ``20191016-probemetadata.json.gz``
     * This includes information (listed above in 'this program does the following')
       about relevant Ripe-Atlas probes

   * ``Running measurement_creation.py`` --> MeasurementID file consisting of measurementIDs and connecting NameServers

    Result and probe meta data files will be continuously deleted. 
    This CAN be changed in the script however, ir is NOT recommended since one or more files 
    are created every 6 seconds if renderlive.py is run --> A LOT OF FILES.

