# setup
    cd /home/pi/Desktop
    git clone https://github.com/nhrnhr0/barcode_scanner.git
    cd barcode_scanner/
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    TODO: add file 'secrects.py' with the values:
        api_secret='<secret api key>'
    sudo cp /home/pi/Desktop/barcode_scanner/bars.conf /etc/supervisor/conf.d/bars.conf
    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl restart barcode_scanner
