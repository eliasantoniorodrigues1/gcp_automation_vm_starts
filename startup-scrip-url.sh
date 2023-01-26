echo "Startup script started"
sudo su
sudo apt update
sudo apt install -yq software-properties-common
sudo add-apt-repository -yq ppa:deadsnakes/ppa
sudo  apt-get install -y python3.9 python3.9-dev python3.9-venv
sudo apt-get install wget
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
cd /home
mkdir your-user
gsutil cp -r gs://your-bucket-goes-here/ /home/your-user/
cd /home/your-user/your-project-folder/sub-project-folder
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3.9 main.py
echo "Startup script ended"
