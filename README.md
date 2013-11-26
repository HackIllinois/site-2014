Development Setup Guide
----

This isn't meant to be an extensive guide, just a quick help for getting setup. If you don't understand something on the list, please ask for help. (Also, if someone wants to edit this and make it better, feel free!)

**Prereqs: ** Make sure Python is installed on your computer. Then install the [Google App Engine SDK for Python](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python).

***Setup*** (note that this is only tested on OS X, and other platforms may differ slightly. Feel free to edit this with changes.)

* Make sure you've satisfied the prereqs above.
* Clone this repository to your computer.
* Open the App Engine launcher (or figure out the command line tools on Linux).
    * Possibly only relevant to OS X: If this is your first time opening the launcher, go ahead and create the symlinks.
* Click and drag the website folder to the App Engine Launcher. It should autodetect the app and put it in the list with the name ``hackillinois``.
* Select the app and click Run. Once the web server has spun up (~10 seconds), you should have the website running on localhost, probably on port 8080 (http://localhost:8080). You can find the administrative console on port 8000.