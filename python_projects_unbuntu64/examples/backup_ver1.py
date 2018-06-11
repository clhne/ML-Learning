#!/usr/bin/python
import os
import time
#source = ['/home/luchenglin/tmp/test1.txt','/home/luchenglin/tmp/test2.txt']
source = ['/home/luchenglin/tmp']
target_dir = '/home/luchenglin/backup/'
target = target_dir + time.strftime('%Y%m%d%H%M%S') + '.zip'
zip_command = "zip  -qr '%s'  %s" % (target, ' '.join(source))
if os.system(zip_command) == 0:
    print 'Successful backup to', target
else:
    print 'Backup FAILED'
