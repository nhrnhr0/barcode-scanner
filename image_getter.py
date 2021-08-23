import convertapi
import secrects
import os
import time


last_modifed = os.path.getmtime("images/676525117969.png")
current_time = time.time()
print(current_time - last_modifed)
secounds_sense_modifed = current_time - last_modifed
expire_time_str = '00:04:23'
ftr = [3600,60,1]
expire_time_secounds = sum([a*b for a,b in zip(ftr, map(int,expire_time_str.split(':')))])

print(expire_time_str)
print(expire_time_secounds)
if secounds_sense_modifed > expire_time_secounds:
    print('rerequest image')






#convertapi.api_secret = secrects.api_secret
#convertapi.convert('png', {
#    'Url': 'http://3.136.112.72:8010/product/676525117969/'
#}, from_format = 'web').save_files('images/676525117969.png')