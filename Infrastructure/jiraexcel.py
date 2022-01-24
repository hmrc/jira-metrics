import xlsxwriter


class excel_creator: 
    def __init__(self):# date_from, date_to):              
        self.workbook = xlsxwriter.Workbook('Metrics.xlsx')#from ' + date_from + ' to ' + date_to + '.xlsx')             
        #self.worksheet = self.workbook.add_worksheet()

    def create_report(self, jira_tickets, date_from, date_to):
        row = 0
        col = -1
        self.worksheet = self.workbook.add_worksheet('from ' + date_from + ' to ' + date_to)
        worksheet_columns = ["Ticket Id", "Summary", "Issue Type", "Waiting in Queue", "Cycle Time", "Lead Time", "Reopened (count)", 
                                "Blocked (count)", "Moved to Left (count)", "Dev Ready", "In Progress", "Dev Complete", "Closed"]

        for column_name in worksheet_columns:
            col += 1
            self.worksheet.write(row, col, column_name)
            #print ("Row: " + str(row) + " Col: " + str(col) + " Column Name " + column_name)
            
        row = 1
       
    
        for jt in jira_tickets:            
          
            col = 0
            self.worksheet.write(row, col, jt.key)
            col += 1
            self.worksheet.write(row, col, jt.summary)
            col += 1
            self.worksheet.write(row, col, jt.issue_type)
            col += 1
            self.worksheet.write(row, col, jt.waiting_in_queue)
            col += 1
            self.worksheet.write(row, col, jt.cycle_time)
            col += 1
            self.worksheet.write(row, col, jt.lead_time)
            col += 1
            self.worksheet.write(row, col, jt.reopened_count)
            col += 1
            self.worksheet.write(row, col, jt.timesBlocked)
            col += 1
            self.worksheet.write(row, col, jt.moves_to_left)
            col += 1
            self.worksheet.write(row, col, jt.status_dates.get("Dev Ready"))
            col += 1
            self.worksheet.write(row, col, jt.status_dates.get("In Progress"))
            col += 1
            self.worksheet.write(row, col, jt.status_dates.get("Dev Complete"))
            col += 1
            self.worksheet.write(row, col, jt.status_dates.get("Closed"))
            row += 1
    
    def close_workbook(self):
        self.workbook.close()
        