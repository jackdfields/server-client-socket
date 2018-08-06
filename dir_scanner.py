import os
import sys
import time
import datetime

def path_walker(path):
        current_time = datetime.datetime.now()
        while True:
                print("Current time is:" + str(current_time) +
                      "\n -----------------------------")
                for (root, dirs, files) in os.walk(path):
                        for filename in files:
                                print(filename)
                print("\n")
                                
if __name__ == '__main__':
        # place r before file path to convert into raw string
	path_walker(r'C:\storeman\office\XF001901')
