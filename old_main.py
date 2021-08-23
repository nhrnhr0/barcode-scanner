
from evdev import InputDevice, categorize, ecodes,list_devices

import os,subprocess, time, threading


# exit all chromium windows and reopen the main page
def exit_chromium():
    print('killing chromium')
    cmd = 'sudo -u pi /home/pi/Desktop/barcode_scanner/chromiumn_main_page.sh &'
    os.system('pkill -o chromium')
    os.system(cmd)


# open a chromium product page
def handle_barcode(barcode):
    if barcode != None and barcode != '':
        cmd = 'sudo -u pi /home/pi/Desktop/barcode_scanner/chromiumn_product_page.sh ' + barcode + ' &'
        os.system(cmd)


# start listen to the barcode scanner and open chromium browsers
def main():


    # iterate all input devices and find the barcode scanner nad saved it as device
    devices = [InputDevice(path) for path in list_devices()]
    i = 0
    bar_device = None
    timer = None
    for device in devices:
        print(i, ') ',device.path, device.name, device.phys)
        i+=1
        if 'Barcode Reader' in device.name:
            bar_device = InputDevice(device.path)

    device = bar_device
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
    
    exit_chromium() # used in the start to open the first main page
    barcode = ''
    # wait for a key read from the barcode scanner
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            data = categorize(event)
            # Down events only
            if data.keystate == 1:  
                # get the key pressed
                key_lookup = scancodes.get(data.scancode) or u'UNKNOWN:{}'.format(data.scancode)  

                # if enter pressed
                if key_lookup == 'CRLF':

                    print('================================== new barcode scaned: ', barcode)

                    # a new barcode is scand:
                    # reset or first start the timer for closing the chromium window to prevent early closing
                    if timer != None:
                        timer.cancel()
                    timer = threading.Timer(20.0, exit_chromium)
                    timer.start()
                    print('============================= timer', timer)
                    handle_barcode(barcode, timer)
                    barcode = ''
                else:
                    barcode += key_lookup
if __name__ == '__main__':
    main()