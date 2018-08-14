#pypyodbc connection to SQL

import pypyodbc
import csv

class PySQLTrans():
    """ send client data to database """
    def __init__(self, comp_name, num_of_files):
        self.comp_name = comp_name
        self.num_of_files = num_of_files

        
    def sql_db_upload(self):    
        #Insert Values to the Database
        #establish connection
        cxcn = pypyodbc.connect('Driver={SQL Server};'
                                'Server=CASHLAB-001901\LOCSMS;'
                                'Database=STORESQL;'
                                'Trusted_Connection=yes;')

        #create cursor
        cursor = cxcn.cursor()

        SQLCommand = ("SP_PYTHONSAMPLE  ?,?")
        Values = [self.comp_name, self.num_of_files]

        cursor.execute(SQLCommand, Values)

        #save to DB
        cxcn.commit()
        #close connection
        cxcn.close()

    def sql_db_dowload(self):
        # Retrieve Values from DB
        #EST new connection
        cxcn = pypyodbc.connect('Driver={SQL Server};'
                                'Server=CASHLAB-001901\LOCSMS;'
                                'Database=STORESQL;'
                                'Trusted_Connection=yes;')

        #create cursor
        cursor = cxcn.cursor()
        
        SQLCommand = ('SELECT ComputerName, NumOfFiles, Tran_Date FROM CLIENT_MONITOR')

        cursor.execute(SQLCommand)
        #Fetch results
        results = cursor.fetchall()

        #Write to a file
        with open('report_dialogue.txt', 'w') as file:
            for row in results:
               C_name, N_files, T_date = row
               actual_time,removed = str(T_date).split('.')
               report_dialogue = (C_name , N_files, actual_time) 
               file.write('<p>'+C_name + " " +  N_files + " " + actual_time+'<p>''\n')

           

        #close connection
        cxcn.close()
