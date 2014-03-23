sudo apt-get install -y git python python-pip
sudo apt-get install -y redis-server
git clone git@bitbucket.org:hackillinois/hackillinois-website.git
cd hackillinois-website/backend_tasks
sudo pip install -r dependencies.txt
# dome wierd thing with the repos for this one so it's best to just do it separately
sudo pip install googledatastore
