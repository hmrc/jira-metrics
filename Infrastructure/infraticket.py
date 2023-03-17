from ticketbase import Ticket
import dateutil.parser as parser

class InfraTicket(Ticket):    
    
    
    def __init__(self, key, summary, issue_type, created_date, histories):
        super().__init__(key, summary, issue_type, created_date ,histories)
        
        self.status_open = "Open"
        self.status_product_backlog = "Product Backlog"
        self.status_todo = "To Do"
        self.status_reopened = "Reopened"
        self.status_dev_ready = "Dev Ready"
        self.status_next = "Next"
        self.status_triage = "Triage"
        self.status_in_progress = "In Progress"
        self.status_needs_more_info = "Needs more info"
        self.status_blocked = "Blocked"
        self.status_dev_complete = "Dev Complete"
        self.status_resolved = "Resolved"
        self.status_closed = "Closed"    
        self.flaggedImpediment = "Impediment"
        self.unflaggedImpediment = ""
        
        self.status_dates = {
                self.status_open : None,
                self.status_product_backlog : None,
                self.status_todo : None,
                self.status_reopened : None,
                self.status_dev_ready : None,
                self.status_next : None,
                self.status_triage : None,
                self.status_in_progress : None,
                self.status_needs_more_info : None,
                self.status_blocked : None,
                self.status_dev_complete : None,
                self.status_resolved : None,
                self.flaggedImpediment : None,
                self.unflaggedImpediment : None                                         
        }
        
        self.status_values = {        
                self.status_open : 1,
                self.status_product_backlog : 1,
                self.status_todo : 1,
                self.status_reopened : 1,
                self.status_dev_ready : 2,
                self.status_next : 2,
                self.status_triage : 2,
                self.status_in_progress : 3,
                self.status_needs_more_info : 3,
                self.status_blocked : 3,
                self.status_dev_complete : 4,
                self.status_resolved : 4,
                self.status_closed : 5
        }   
        
        self.status_dates[self.status_open] =  parser.parse(created_date).strftime('%d/%m/%Y')     
    
    def process_history_item (self, field, item_from_status, item_to_status, item_status_date): 
        super(InfraTicket,self).process_history_item(field, item_from_status, item_to_status, item_status_date)     
        if field == 'Flagged':                        
            self.process_impediment(item_from_status, item_to_status, item_status_date)
    
     
    def process_impediment(self, status_from, status_to, status_date):
        print("Flagged " + status_to)     
        if status_to == self.flaggedImpediment:
            self.changed_status(self.flaggedImpediment,  status_date)
            self.timesBlocked += 1
        if status_from == self.flaggedImpediment:
            self.changed_status(self.unflaggedImpediment, status_date)
            self.daysBlocked = self.daysBlocked + self.delta_dates(self.flaggedImpediment, self.unflaggedImpediment) 
    
    
    def process_ticket_status_change(self, item_from_status, item_to_status,  status_date):                
        self.changed_status(item_to_status,  status_date)                                                                        
        if item_from_status != item_to_status:   
            
            if item_to_status == self.status_in_progress:
                #print('Started Work ')            
                if self.status_dates[self.status_dev_ready] != None:
                    delta = self.delta_dates(self.status_dev_ready, self.status_in_progress)
                    
                    if self.waiting_in_queue != 0:
                        self.waiting_in_queue = self.waiting_in_queue + delta
                    else:
                        self.waiting_in_queue = delta
            
            elif item_to_status == self.status_dev_complete:
                #print("Ready to demo")                                    
                if self.status_dates[self.status_in_progress] != None:
                    delta = self.delta_dates(self.status_in_progress, self.status_dev_complete)
                                    
                    if self.cycle_time != 0:
                        self.cycle_time = self.cycle_time + delta
                    else:
                        self.cycle_time = delta
        
            elif item_to_status == self.status_resolved:               
                if self.status_dates[self.status_in_progress] != None and self.status_dates[self.status_dev_complete] == None:
                    delta = self.delta_dates(self.status_in_progress, self.status_resolved)            
                    if self.cycle_time != 0:
                        self.cycle_time = self.cycle_time + delta
                    else:
                        self.cycle_time = delta             
            
                                        
            elif item_to_status == self.status_reopened:                        
                self.reopened_count = self.reopened_count  + 1
            
            elif item_to_status == self.status_closed:            
                from_status = None
                if self.status_dates[self.status_dev_ready] != None:
                    from_status = self.status_dev_ready
                elif self.status_dates[self.status_open] != None:
                    from_status = self.status_open    
                
                if from_status != None:              
                    self.lead_time = self.delta_dates(from_status, self.status_closed)                            