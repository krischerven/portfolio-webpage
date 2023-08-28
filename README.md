# README

## Installation
```bash
pip install -r requirements.txt
```

## Deployment

To run locally:
```bash
./main.py      # Unix
python main.py # Windows
```

To run remotely:
```bash
# install nginx
./create-nginx-symlinks
sudo ln -s "$PWD"/portfolio-webpage.service /etc/systemd/system
./create-download-hardlinks
sudo systemctl start portfolio-webpage
```