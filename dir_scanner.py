import os
import sys
import time
import datetime

def path_walker(path):
        while True:
                current_time = datetime.datetime.now()
                print("Current time is:" + str(current_time) +
                              "\n -----------------------------")
                # important: make sure count=0 to reset count every call
                count = 0
                for root, dirs, files in os.walk('C:\storeman\Office\XF001901'):
                    count += len(files)
                with open("pycache.txt", "w") as file:
                        file.write(f"num of files: {count}")
                time.sleep(10)

if __name__ == '__main__':
        path_walker(r'C:\storeman\Office\XE001901')
