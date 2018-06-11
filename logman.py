import os
import sys 
import time
import netifaces as ni
import subprocess

class Watcher(object):
    running = True
    refresh_delay_secs = 1

    # Constructor
    def __init__(self, watch_file, call_func_on_change=None, *args, **kwargs):
        self._cached_stamp = 0
        self.filename = watch_file
        self.call_func_on_change = call_func_on_change
        self.args = args
        self.kwargs = kwargs

    # Look for changes
    def look(self):
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            # File has changed, so do something...
            # print('File changed')
            # -- edit as logged 
            if self.call_func_on_change is not None:
                self.call_func_on_change(*self.args, **self.kwargs)

    # Keep watching in a loop        
    def watch(self):
        while self.running: 
            try: 
                # Look for changes
                time.sleep(self.refresh_delay_secs) 
                self.look() 
            except KeyboardInterrupt: 
                print('\nDone') 
                break 
            except FileNotFoundError:
                # Action on file not found
                pass
            except: 
                print('Unhandled error: %s' % sys.exc_info()[0])

# Call this function each time a change happens
def custom_action(text):
    # print(text)
    print (text+" has changed -- "+ time.ctime())

    # get ip local from ni
    ip = ni.ifaddresses('en0')[ni.AF_INET][0]['addr']

    # convert ip to string
    ip = ip.encode('ascii','ignore')

    # get argument path source and dest
    file1 = (sys.argv[1])
    destination = (sys.argv[2])

    # create path
    path = destination+ip+"/"

    # create folder
    # os.system("mkdir -p "+ destination )

    # transfer file to another path
    # os.system("rsync -a " +source +" "+destination) 

    # sync file
    # os.system('rsync -a --rsync-path=\"mkdir -p '+path +"\" "+ file1+" "+path)
    args = "--rsync-path=%s" % (path)
    subprocess.Popen(["rsync", "-a", args, file1,path])

#watch_file = '/Users/rachen/Desktop/logman/log.txt'
watch_file1 = sys.argv[1]

# watcher = Watcher(watch_file)
watcher_file1 = Watcher(watch_file1, custom_action, text='file1')  # also call custom action function

# start the watch going
watcher_file1.watch()
