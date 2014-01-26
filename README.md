Development Setup Guide
----

This isn't meant to be an extensive guide, just a quick help for getting setup. If you don't understand something on the list, please ask for help. (Also, if someone wants to edit this and make it better, feel free!)

**Prereqs: ** Make sure Python is installed on your computer. Then install the [Google App Engine SDK for Python](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python).

**Setup: ** (note that this is only tested on OS X, and other platforms may differ slightly. Feel free to edit this with changes.)

* Make sure you've satisfied the prereqs above.
* Clone this repository to your computer.
* Open the App Engine launcher (or figure out the command line tools on Linux).
    * Possibly only relevant to OS X: If this is your first time opening the launcher, go ahead and create the symlinks.
* Click and drag the website folder to the App Engine Launcher. It should autodetect the app and put it in the list with the name ``hackillinois``.
* Select the app and click Run. Once the web server has spun up (~10 seconds), you should have the website running on localhost, probably on port 8080 (http://localhost:8080). You can find the administrative console on port 8000.

Git Deploy Setup Guide
============
**(Note: You obviously must have push permissions to do this.)**

Google has a process called [Push-to-Deploy](https://developers.google.com/appengine/docs/push-to-deploy) that allows you to add App Engine as a remote branch of the repo. It's a little buggy but makes managing dev/prod easy.

***Setup***:

* Follow the instructions [here](https://developers.google.com/appengine/docs/push-to-deploy) until you have the Git repo URL. There should already be a repository for both prod and dev.
* Following the above instructions, put the given authentication line in your `~/.netrc` file. (Instructions for Windows are on the page.)
* Copy the Git repo URL, and run `git remote add REMOTE_NAME PASTE_THE_URL_HERE` in the root directory of the Git repository. Replace `REMOTE_NAME` with either `prod` or `dev` depending on which one you're pushing.
* Running `git push prod master` pushes the master branch to prod. By the same token, running `git push dev master` pushes the master branch to dev. Running `git push` with no arguments still pushes to our Bitbucket, which is desired.

**When you push something, *especially prod*, make sure to commit it to the Bitbucket repo too so other people can push without reverting your changes.**