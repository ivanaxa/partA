import time
import requests
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config_loader import Config


class Watcher:
    #DIRECTORY_TO_WATCH = "/Users/xai/rules/"
    directory=Config.paths('DIRECTORY_TO_MONITOR')
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(10)
        except:
            self.observer.stop()
            print ("Error in running program")

        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        
        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print ("new file created - %s." % event.src_path)
            #print(os.path.basename(event.src_path))
            p=os.path.basename(event.src_path)
            processFileEvent(p)
        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print ("file contents modified: %s." % event.src_path)
            #print(os.path.basename(event.src_path))
            p=os.path.basename(event.src_path)
            processFileEvent(p)
        elif event.event_type == 'moved':
            print ("file renamed: %s." % event.src_path)
            #print(os.path.basename(event.dest_path))
            p=os.path.basename(event.dest_path)
            processFileEvent(p)
        else:
            pass

def sendToPostEndpoint(fileName):
    directory = Config.paths('DIRECTORY_TO_MONITOR')
    user=Config.dev('USERNAME')
    password=Config.dev('PASSWORD')
    file=open(directory+fileName, 'rb')
    url='http://localhost:8080/postRule'
    files={'file':file}
    r=requests.post(url, files=files, auth=(user, password))
    print("uploaded: " +fileName+ "-- response from server: "+ str(r))


def processFileEvent(fileName):
    x = fileName.split('_')
    if (len(x)<=1 or len(x)>2):
        print(".")
    elif (x[0]==".DS" and x[1]=="Store"):
        print(".")
    elif (len(x) == 2 ):
        sendToPostEndpoint(fileName)
    else:
        print(".")
    
def initialRulesProcessing(fileArray):
    for fileName in fileArray:
        x = fileName.split('_')
        
        if (len(x)<=1 or len(x)>2):
            pass
        elif (x[0]==".DS" and x[1]=="Store") or ():
            pass
        elif (len(x) == 2 ):
            sendToPostEndpoint(fileName)
        else:
            pass
            
def main():

    #print (Config.paths('DIRECTORY_TO_MONITOR'))
    #print (Config.dev('USERNAME'))
    #print (Config.dev('PASSWORD'))

    print("starting reading of directory:"+ Config.paths('DIRECTORY_TO_MONITOR'))
    #initial scan of the local directory
    files =  os.listdir(Config.paths('DIRECTORY_TO_MONITOR'))
    initialRulesProcessing(files)

    #initiate watcher class instance and update database as changes are made
    w = Watcher()
    w.run()




if __name__ == '__main__':
    main()
