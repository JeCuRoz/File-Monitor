import time
import argparse
import pathlib
import sys
from queue import Queue, Empty
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from commands import Command


# Disk event handler
# Watching for file system events (creation of new files/folders only)
class FSEventHandler(FileSystemEventHandler):
    
    def __init__(self, callback):
        super(FSEventHandler, self).__init__()
        self.callback = callback  # callback will be executed when a new object (file or folder) is created

    def on_created(self, event):
        # This event is triggered when a new object is created in the monitored folder
        # src_path is the path of the new object
        # The callback will process the event
        self.callback(event.src_path)


# Watch folder and its events
class FolderMonitor(Observer):
    
    def launch(self, folder, callback):
        self.schedule(FSEventHandler(callback), path=folder)
        self.start()

    def halt(self, ):
        # stop and wait for the observer to finish
        self.stop()
        self.join()


class Application:
    # Monitor a folder

    def __init__(self, folder, command):
        
        # this queue communicates the monitor thread with the processor thread
        self.queue = Queue()

        self.folder = folder
        self.command = command

    def __enqueue(self, filename):
        # A new object has been created, we added it to the queue
        self.queue.put(filename)
        print(filename)

    def run(self):
        # start the app
        
        # This object monitors the folder and add the new objects to the queue
        folder_monitor = FolderMonitor()
        folder_monitor.launch(self.folder, self.__enqueue)

        try:        
            # We are using the application from the command line
            # There are no background threads
            # New objects will be processed in the foreground
            self.__process()

        except KeyboardInterrupt:
            # the user has stopped the app using the keyboard
            print('\nThe user has stopped the app')
            # stop and wait for the monitor
            folder_monitor.halt()
            sys.exit(0)

        except Exception as e:
            # unhandle exception
            raise e   
 
    def __process(self):
        # Here is where the hard work is done

        # delay to check the queue
        query_delay = 1
        
        while True:
            try:
                # get the path of the new object
                fileobject = self.queue.get_nowait()
                # execute the command for the new files
                if self.command:
                    cmd = Command(f'{self.command} "{fileobject}"')
                    print(f'Command to execute: {cmd.cmd}')
                    cmd.run()
                    print(f'Success: {cmd.success}')
                    print(f'Exit code: {cmd.returncode}')
                    print(f'Command output:')
                    print("\n".join(cmd.lines))
            except Empty:
                # the queue is empty, wait a moment
                time.sleep(query_delay)
            except Exception as e:
                # unhandle exception
                raise e   
  

def parse_args():
    # command line parameters management
    parser = argparse.ArgumentParser(
        description='Watch a folder for new files/folders and executes a command'
    )

    parser.add_argument(
        'folder',
        help='Monitored folder',
        type=pathlib.Path
    )

    parser.add_argument(
        '-c', '--command',
        required=True,
        help='Command to execute when a new file or folder is created'
    )

    # process and return the input parameters
    return  parser.parse_args()


def run_app():

    # process the CLI parameters
    args = parse_args()

    # start the app
    app = Application(args.folder, args.command)
    app.run()


if __name__ == '__main__':
    run_app()
