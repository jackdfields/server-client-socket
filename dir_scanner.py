import os
import sys
import time
import datetime

def path_walker(path):
        current_time = datetime.datetime.now()
	count = 0
        while True:
                print("Current time is:" + str(current_time) +
                      "\n -----------------------------")
                for (files) in os.walk(path):
                        for filename in files:
				count += 1
                                print(count)
                                
if __name__ == '__main__':
        # place r before file path to convert into raw string
	path_walker(r'path for files')
