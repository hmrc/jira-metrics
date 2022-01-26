from ticketbase import Ticket
import dateutil.parser as parser

class SupTicket(Ticket):
    
    def __init__(self, key, summary, issue_type, created_date, histories):
        super().__init__(key, summary, issue_type, created_date, histories)
        self.status_open = "Open"
        self.status_next = "Next"
        self.status_dev_ready = "Dev Ready"
        self.status_in_progress = "In Progress"
        self.status_assigned = "Assigned"
        self.status_blocked = "Blocked"
        self.status_dev_complete = "Dev Complete"
        self.status_resolved = "Resolved"
        self.status_closed = "Closed"
        
        self.status_values = {        
            self.status_open : 1,
            self.status_next : 2,
            self.status_dev_ready : 3,
            self.status_in_progress : 4,
            self.status_assigned : None,
            self.status_blocked : 1,
            self.status_dev_complete : 5,
            self.status_resolved : 6,
            self.status_closed : 6  
        }
        
        self.status_dates  = {
            self.status_open : None,
            self.status_next : None,
            self.status_dev_ready : None,
            self.status_in_progress : None,
            self.status_assigned : None,
            self.status_blocked : None,
            self.status_dev_complete : None,
            self.status_resolved : None,
            self.status_closed : None            
        }                            
        
        self.status_dates[self.status_open] =  parser.parse(created_date).strftime('%d/%m/%Y')    
        
    def process_ticket_status_change(self, item_from_status, item_to_status,  status_date):                        
        self.changed_status(item_to_status,  status_date)   
        
        
        if item_from_status == "Blocked":
            delta = self.delta_dates(item_from_status, item_to_status)        
            self.daysBlocked = self.daysBlocked + delta
        
                                                                
        if item_to_status == self.status_in_progress and item_from_status != self.status_in_progress:
            #print('Started Work ')            
            if self.status_dates[self.status_dev_ready] != None:
                delta = self.delta_dates(self.status_dev_ready, self.status_in_progress)                
                    
                if self.waiting_in_queue != 0:
                    self.waiting_in_queue = self.waiting_in_queue + delta
                else:
                    self.waiting_in_queue = delta                                

        elif item_to_status == self.status_blocked:
            self.timesBlocked = self.timesBlocked  + 1
        
        elif item_to_status == self.status_dev_complete:
            #print("Ready to demo")                                    
            if self.status_dates[self.status_in_progress] != None:
                delta = self.delta_dates(self.status_in_progress, self.status_dev_complete)
                
                if self.cycle_time != 0:                    
                    self.cycle_time = self.cycle_time + delta
                else:
                    self.cycle_time = delta
        
        elif item_to_status == self.status_resolved:
            #print("Ready to demo")                                    
            if self.status_dates[self.status_in_progress] != None and self.status_dates[self.status_dev_complete] == None:
                delta = self.delta_dates(self.status_in_progress, self.status_resolved)
                
                if self.cycle_time != 0:                    
                    self.cycle_time = self.cycle_time + delta
                else:
                    self.cycle_time = delta             
        
             
        elif item_to_status == self.status_closed:            
                from_status = None
                if self.status_dates[self.status_dev_ready] != None:
                    from_status = self.status_dev_ready
                elif self.status_dates[self.status_open] != None:
                    from_status = self.status_open    
                
                if from_status != None:              
                    self.lead_time = self.delta_dates(from_status, self.status_closed)   