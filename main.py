from evdev import InputDevice, categorize, ecodes,list_devices
import os
from pathlib import Path
import convertapi
import secrects
import time
import threading
import barcodenumber

convertapi.api_secret = secrects.api_secret
PRODUCTS_SERVER = 'http://3.136.112.72:8010/product/'

EXPIRE_TIME_STR = '48:00:00'
ftr = [3600,60,1]
EXPIRE_TIME_SECOUNDS = sum([a*b for a,b in zip(ftr, map(int,EXPIRE_TIME_STR.split(':')))])

IMAGE_DISPLAY_TIMEOUT = 10
def exit_images():
    print('killing images')
    cmd = 'pkill feh'
    os.system(cmd)

def reopen_chromium():
    print('killing chromium')
    cmd = 'sudo -u pi /home/pi/Desktop/barcode_scanner/chromiumn_main_page.sh &'
    os.system('pkill -o chromium')
    os.system(cmd)

def api_ask_for_image(barcode):
    print('WARNING: sending request to the api')
    convertapi.convert('png', {
        'Url': PRODUCTS_SERVER + barcode
    }, from_format = 'web').save_files(f'images/{barcode}.png')

# configre the scanner and yeild the scaned barcode
def get_barcode_input():
    devices = [InputDevice(path) for path in list_devices()]
    i = 0
    bar_device = None
    timer = None
    
    for device in devices:
        print(i, ') ',device.path, device.name, device.phys)
        i+=1
        if 'Barcode Reader' in device.name:
            bar_device = InputDevice(device.path)

    device = bar_device#devices[3]
    os.system('echo "selected device: ' + device.path + '"')


    scancodes = {
        # Scancode: ASCIICode
        0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
        10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
        20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
        30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
        40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
        50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
    }
    
    barcode = ''
    # wait for a key read from the barcode scanner
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            data = categorize(event)
            # Down events only
            if data.keystate == 1:  
                # get the key pressed
                key_lookup = scancodes.get(data.scancode) or ''#u'UNKNOWN:{}'.format(data.scancode)  

                # if enter pressed
                if key_lookup == 'CRLF':

                    #print('================================== new barcode scaned: ', barcode)

                    # a new barcode is scand:
                    yield barcode
                    barcode = ''
                else:
                    barcode += key_lookup

def get_product_image(barcode):
    if barcode == '': return

    barcode_image = Path(f"images/{barcode}.png")
    
    if barcode_image.exists():
        last_modifed = os.path.getmtime(f"images/{barcode}.png")
        current_time = time.time()
        secounds_sense_modifed = current_time - last_modifed
        print(f'file images/{barcode} found - secounds sense modifed: {secounds_sense_modifed}')
        if secounds_sense_modifed > EXPIRE_TIME_SECOUNDS:
            print('image is stale, redownload...')
            x = threading.Thread(target=api_ask_for_image, args=(barcode,))
            x.start()
        return barcode_image
    else:
        print(f'barcode {barcode} image file not found')
        if barcodenumber.check_code('UPCA',barcode):
            
            print(f'barcode {barcode} is valid')
            waiting_image = Path("loading.png")
            open_image_process(waiting_image)
            api_ask_for_image(barcode)
            #exit_image_process_after_timeout(p, 5)
            
            return get_product_image(barcode)
        else:
            print('error: scaned invalid barcode!')
        
import subprocess
#def exit_image_process(p):
#    p.kill()
#def exit_image_process_after_timeout(image_process, ptimeout):
#    threading.Thread(target=exit_image_thread, args=(image_process,ptimeout)).start()
    #time.sleep(IMAGE_DISPLAY_TIMEOUT)
    

#def exit_image_thread(image_process,ptimeout):
#    time.sleep(ptimeout)
#    exit_image_process(image_process)

def main():
    reopen_chromium()
    # listen to barcode scanner:
    #barcodes = ['676525117969', '676525116443', '676525117969']
    timer = None
    time.sleep(5)
    for barcode in get_barcode_input():
        print('new barcode scaned: ', barcode)
        image = get_product_image(barcode)
        print('got barcode image: ', image)
        open_image_process(image)
        #TODO: exit all images after timeout
        if timer != None:
            timer.cancel()
        timer = threading.Timer(20.0, exit_images)
        timer.start()

def open_image_process(image):
    cmd = 'sudo -u pi /home/pi/Desktop/barcode_scanner/open_image.sh ' + str(image) + ' &'
    os.system(cmd)
    #cmd= 'feh --auto-zoom --borderless --fullscreen --hide-pointer ' + str(image)
    #print('executing: ', cmd)
    #my_env = os.environ.copy()
    #my_env["DISPLAY"] = ":0"

    #p = subprocess.Popen(['feh', '--auto-zoom', '--borderless', '--fullscreen', '--hide-pointer', image], env=my_env)
    #return p

if __name__ == '__main__':
    main()