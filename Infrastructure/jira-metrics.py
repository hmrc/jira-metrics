import sys, getopt
import datetime as dt
from infraticket import InfraTicket as infra_ticket
from supticket import SupTicket as sup_ticket
from jiraexcel import excel_creator
import requests
import configparser

config = configparser.ConfigParser()
config.read("jira-metrics.ini")
credentials = config['credentials']

usageMessage = "dates.py -w <ammount of weeks> -d <from date>"
dateFormatMessage = "Date must be formatted D/M/YYYY, 31/12/2021"

headers = {
   "Accept": "application/json",
   "Content-Type": "application/json",
   "Authorization": "Bearer " + credentials.get('token')
   }

url = "https://jira.tools.tax.service.gov.uk/rest/api/2/search"

def execute_query(params):
   response = requests.request(
   "GET", 
   url,
   headers=headers,
   params = params)
   #print(response.json())
   #print(response.url)
   #print(response.text)
   if response.status_code == 400:
       print("Server returned bad request error (400)")
       sys.exit()
   return response.json()
   

def prepare_params (from_date, to_date):
    params = {"jql" : "project = SUP AND labels = infrastructure AND resolved >=  " 
                + from_date + "  AND resolved <= " + to_date + " " 
                "OR project = INFRA AND resolved >=  " 
                + from_date + "  AND resolved <= " + to_date 
                , "expand": "changelog"}
    #params = {"jql" : "key = SUP-12201 or key = SUP-12233", "expand": "changelog"}
    #print(params)
    return params

def read_json(json_response):
    list_jira_tickets = []
    records = json_response.get("total")     
    if records != None:
        print("Found: " + str(records)) 
        for json_jira_ticket in json_response['issues']:            
            jira_ticket = create_ticket(json_jira_ticket['key'], json_jira_ticket["fields"]["summary"], 
                                        json_jira_ticket["fields"]["issuetype"]["name"], 
                                        json_jira_ticket["fields"]["created"], 
                                        json_jira_ticket.get('changelog').get('histories'))    
            jira_ticket.process_histories() 
            list_jira_tickets.append(jira_ticket)                                                      
            
    return list_jira_tickets
                    
def create_ticket(key, summary, name, created_date, histories):
    if key.find("INFRA-") == 0:
        return infra_ticket(key, summary, name, created_date, histories)    
    if key.find("SUP-") == 0:
        return sup_ticket(key, summary, name, created_date,histories)   

def main(argv):
    weeks = None
    from_date = None
    try:
        opts, args = getopt.getopt(argv,"hw:d:",["weeks=","fromDate="])
    except getopt.GetoptError:
      print (usageMessage)
      sys.exit(2)
    if len(sys.argv) <= 3:    
        print (usageMessage)
        sys.exit()
    for opt, arg in opts:      
      
      if opt == '-h':
         print (usageMessage)
         sys.exit()         
      elif opt in ("-w", "--weeks"):
         weeks = arg    
      elif opt in ("-d", "--fromDate"):
          try:
            from_date = dt.datetime.strptime(arg, '%d/%m/%Y')
          except ValueError:            
            print(dateFormatMessage)
            sys.exit()
    
    excel = excel_creator()        
    for wn in range(int(weeks)):
        from_date = from_date - dt.timedelta(7) 
        params = prepare_params( from_date.strftime("%Y-%m-%d"), (from_date + dt.timedelta(7)).strftime("%Y-%m-%d"))        
        print("From " + from_date.strftime("%Y-%m-%d") + " To " + (from_date + dt.timedelta(7)).strftime("%Y-%m-%d"))
        json_response = execute_query(params)       
        list_tickets = read_json(json_response)                       
        excel.create_report(list_tickets, from_date.strftime("%Y-%m-%d"), (from_date + dt.timedelta(7)).strftime("%Y-%m-%d"))
    excel.close_workbook()    
if __name__ == "__main__":
   main(sys.argv[1:])

