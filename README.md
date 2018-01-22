# fog
Run scrapeprivate.py in order to migrate. Before that you should hardcode your ifttt credentials in the script.
The first time you run the script you must click the button on the bridge to acquire the token.

newlittlebits.ino is the arduino file that runs the littleBits demo.

after migrating run jsonserver.py to be able to perform the webrequests.
In the jsonserver.py you can perform the following actions:
Get all the lamps: /public/lamps -> http://localhost:8080/public/lamps
Get all the makers: /public/makers -> http://localhost:8080/public/makers
Get all the cloudbits: /public/cloudbits -> http://localhost:8080/public/cloudbits
Run a maker applet locally: /public/makers/(ifttt event keyword) -> http://localhost:8080/public/makers/onlights, http://localhost:8080/public/makers/offlights etc
Get all the applets that use a certain lamp (name): /public/appletbylamp/(.*) -> http://localhost:8080/public/appletbylamp/Door
Get all the applets that use a certain cloudbit (name): /public/appletbycloudbit/(.*) -> http://localhost:8080/public/appletbycloudbit/CBIT

makersniffer.py is the file that matches mutiple maker event.
For example if an applet uses Maker - Hue to turn on the lights with the keyword "onlights", running http://localhost:8080/public/makers/onlights
will turn on the lights. If another Maker - Maker applet sends the keyword "multiple" to receive back from IFTTT a web request with the keyword
"onlights", when you send to the local web server "multiple" (http://localhost:8080/public/makers/onlights) the lights will go on. 
If the event keyword to the local web server does not correspong to a migrated applet the request will be sent to IFTTT using that keyword.


For the shadow device implementation a worker that polls on the lamp state had to be implemented since Philips API does not provide an event subscriber to notify when the state changes.

Next steps on the project are to add more devices, import the application into a docker container since there are too many libraries that need to be installed to run out of the box, possibly replace some code with nodejs since it is more suitable for the parts that use multithreading, and more.
