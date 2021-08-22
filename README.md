# setup
cd /home/pi/Desktop
git clone https://github.com/nhrnhr0/barcode-scanner.git
sudo cp /home/pi/Desktop/barcode_scanner/bars.conf /etc/supervisor/conf.d/bars.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart barcode_scanner