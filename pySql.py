# pypyodbc connection to SQL

import pypyodbc
import csv
import datetime

class PySQLTrans():
    """ send client data to database """
    def __init__(self, comp_name, num_of_files):
        self.comp_name = comp_name
        self.num_of_files = num_of_files
        
    def sql_db_upload(self):    
        # Insert Values to the Database
        # establish connection
        cxcn = pypyodbc.connect('Driver={SQL Server};'
                                'Server=CASHLAB-001901\LOCSMS;'
                                'Database=STORESQL;'
                                'Trusted_Connection=yes;')

        #create cursor
        cursor = cxcn.cursor()

        SQLCommand = ("SP_PYTHONSAMPLE  ?,?")
        Values = [self.comp_name, self.num_of_files]

        cursor.execute(SQLCommand, Values)

        # save to DB
        cxcn.commit()
        # close connection
        cxcn.close()

    def sql_db_dowload(self):
        # Retrieve Values from DB
        # EST new connection
        cxcn = pypyodbc.connect('Driver={SQL Server};'
                                'Server=CASHLAB-001901\LOCSMS;'
                                'Database=STORESQL;'
                                'Trusted_Connection=yes;')

        # create cursor
        cursor = cxcn.cursor()

        # Order the DB results by ABC order AND most recently updated
        SQLCommand = ('SELECT ComputerName, NumOfFiles, Tran_Date FROM CLIENT_MONITOR\n'+
                      'ORDER BY ComputerName ASC, Tran_Date DESC;')

        cursor.execute(SQLCommand)
        # Fetch results
        results = cursor.fetchall()

        # Write to a file
        with open('report_dialogue.txt', 'w') as file:
            for row in results:
               Comp_name, Num_files, T_date = row

               # get time from DB and convert it ms for difference
               db_milliseconds = int(round(T_date.timestamp() * 1000))
               now_milliseconds = int(round(datetime.datetime.now().timestamp() * 1000))
               current_time_lapse = now_milliseconds - db_milliseconds
               # convert to datetime
               time_since_checkin = round(current_time_lapse/60000)
               
               updated_time = str(datetime.datetime.fromtimestamp(db_milliseconds/1000).strftime('%Y-%m-%d %H:%M:%S'))

               # Notice a lack of check-in 
               if time_since_checkin > 5:
                   file.write('  <tr>\n' +
                              '\t<td align=center>' +
                              Comp_name +
                              '</td>\n' +
                              '\t<td align=center>' +
                              Num_files +
                              '</td>\n' +
                              '\t<td align=center>' +
                              updated_time +
                              '</td>\n' +
                              '\t<td bgcolor=#FF0000; align=center>' +
                              str(time_since_checkin) +
                              ' minutes </td>\n</tr>\n')
                   
               # check if files aren't updating
               elif int(Num_files) > 10:
                   file.write('  <tr>\n' +
                              '\t<td align=center>' +
                              Comp_name +
                              '</td>\n' +
                              '\t<td align=center>' +
                              Num_files +
                              '</td>\n' +
                              '\t<td bgcolor=#FF0000; align=center>' +
                              updated_time +
                              '</td>\n' +
                              '\t<td align=center>' +
                              str(time_since_checkin) +
                              ' minutes </td>\n</tr>\n')
                   
               # check if files and check-in are not coming in
               elif int(Num_files) > 10 and time_since_checkin > 5:
                   file.write('  <tr>\n' +
                              '\t<td align=center>' +
                              Comp_name +
                              '</td>\n' +
                              '\t<td align=center>' +
                              Num_files +
                              '</td>\n' +
                              '\t<td bgcolor=#FF0000; align=center>' +
                              updated_time +
                              '</td>\n' +
                              '\t<td bgcolor=#FF0000; align=center>' +
                              str(time_since_checkin) +
                              ' minutes </td>\n</tr>\n')

               # write normally
               else:
                   file.write('  <tr>\n' +
                              '\t<td align=center>' +
                              Comp_name +
                              '</td>\n' +
                              '\t<td align=center>' +
                              Num_files +
                              '</td>\n' +
                              '\t<td align=center>' +
                              updated_time +
                              '</td>\n' +
                              '\t<td align=center>' +
                              str(time_since_checkin) +
                              ' minutes </td>\n</tr>\n')
                    
        # close connection
        cxcn.close()
