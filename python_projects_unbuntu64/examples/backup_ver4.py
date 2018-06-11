#!/usr/bin/python
import os
import time
source = ['/home/luchenglin/tmp']
target_dir = '/home/luchenglin/backup/'
today = target_dir +  time.strftime('%Y%m%d')
now = time.strftime('%H%M%S')
comment = raw_input('Enter a comment -->')
if len(comment) == 0:
    target  = today + os.sep + now + '.zip'
else:
    target = today + os.sep + now +'_' + \
comment.replace(' ', '_') + '.zip'
if not os.path.exists(today):
    os.mkdir(today)
    print 'Sucessfully created directory', today
#zip_command = "zip  -qr '%s'  %s" % (target, ' '.join(source))
tar = 'tar -cvzf %s %s -X /home/luchenglin/tmp/test1.txt' % (target, ' '.join(source))
if os.system(tar) == 0:
    print 'Successful backup to', target
else:
    print 'Backup FAILED'
