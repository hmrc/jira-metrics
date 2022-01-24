import dateutil.parser as parser
import datetime as dt
import numpy as np


class Ticket(object):                        
    def __init__(self, key, summary, issue_type, created_date, histories):
        self.key = key
        self.summary = summary
        self.issue_type = issue_type
        self.open_date = 0        
        self.lead_time = 0
        self.cycle_time = 0
        self.waiting_in_queue = 0
        self.timesBlocked = 0
        self.daysBlocked = 0
        self.reopened_count = 0            
        self.moves_to_left = 0                         
        self.histories = histories     
        self.status_dates = None
        self.status_values = None   

    def process_histories(self):      
        print ("Key " + self.key) 
        for history in self.histories:        
            for item in history.get('items'):
                field = item.get('field')
                item_to_status = item.get('toString')
                item_from_status = item.get('fromString')                 
                self.process_history_item(field, item_from_status, item_to_status, history.get('created'))     
                
    
    def process_history_item (self, field, item_from_status, item_to_status, item_status_date):              
        if field == 'status':                                    
            self.count_moved_to_left(item_from_status, item_to_status)
            self.process_ticket_status_change(item_from_status, item_to_status, item_status_date)
    
    def count_moved_to_left (self, status_from, status_to):
        if self.status_values == None:
            raise NotImplementedError        
        if (self.status_values[status_from] > self.status_values[status_to]):
            self.moves_to_left += 1
    
    def changed_status(self, status, date_time_str):
        self.status_dates[status] = parser.parse(date_time_str).strftime('%d/%m/%Y')
        print ("Changed Status " + status + " Date " +  self.status_dates[status])
    
    def delta_dates(self, dateStatusFrom, dateStatusTo):
        try:
            fromDate = dt.datetime.strptime(self.status_dates[dateStatusFrom], '%d/%m/%Y')
            toDate = dt.datetime.strptime(self.status_dates[dateStatusTo] , '%d/%m/%Y')
            toDate += dt.timedelta(days=1)      
            diff = np.busday_count(fromDate.date(), toDate.date())            
        except TypeError:            
            return -1
        return diff
    
    def process_ticket_status_change(self , item_from_status, item_to_status, status_date ):
        """Define logic based on workflow specific to project"""
        raise NotImplementedError  