sudo apt-get install -y git python python-pip gcc python-dev python-setuptools libffi-dev
sudo apt-get install -y redis-server apache2
sudo rm /var/www/index.html
cd /var/www/
read -p "Enter serve directory of the backend tasks: " dir
sudo ln -s $dir
git clone git@bitbucket.org:hackillinois/hackillinois-website.git
cd hackillinois-website/backend_tasks
sudo pip install -r dependencies.txt
sudo pip install googledatastore
export PYTHONPATH=${PYTHONPATH}:$HOME/gsutil:\
$HOME/gsutil/third_party/boto:\
$HOME/gsutil/third_party/retry-decorator:\
$HOME/gsutil/third_party/socksipy-branch:\
$HOME/gsutil/third_party/httplib2/python2:\
$HOME/gsutil/third-party/httplib2/python2/httplib2:\
$HOME/gsutil/third_party/google-api-python-client:\
$HOME/gsutil/third_party/google-api-python-client/oauth2client
gsutil config