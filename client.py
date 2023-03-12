#0608560
#CT30A3401 Distributed Systems
#Assignment 2
#Client part
#Help received:https://docs.python.org/3/library/xmlrpc.html, ChatGPT

import xmlrpc.client, datetime, pyfiglet

def main():
    print("--------")
    text = pyfiglet.figlet_format("Client side")
    print(text)
    # What user wants to do
    print("Send new note            --> [1]")
    print("Get old note             --> [2]")
    print("Get data from wikipedia  --> [3]")
    x = input("Choose number: ")
    
    if x == "1":
        addNote()
    elif x == "2":
        getNote()
    elif x == "3":
        getWiki()
    else:
        print("Wrong input")
    print("--------")
    
    

def addNote():
    print("")
    server_url = 'http://localhost:8000' # Server's URL
    server = xmlrpc.client.ServerProxy(server_url) #returns object that can be used to call methods on the server

    #Ask the user for data
    topic = input("Topic? : ")
    note = input("Note?  : ")
    text = input("Text?  : ")
    time = datetime.datetime.now()
    timestamp = time.strftime("%m/%d/%y - %H:%M:%S")

    #Send data to server
    try:
        result = server.addNote(topic, note, text, timestamp) 
    except Exception:
        print("Error")
        return
    
    print("")
    print("Result: " + result) # Print result that server gives
    


def getNote():
    print("")
    server_url = 'http://localhost:8000' # Server's URL
    server = xmlrpc.client.ServerProxy(server_url) #returns object that can be used to call methods on the server
    
    #Ask topic
    topic = input("Topic? : ")
    
    #Get data from the server
    try:
        result = server.getNote(topic)
    except Exception:
        print("Error")
        return
    print("")
    print("Result: " + result) # Print result
    
    
def getWiki():
    print("")
    server_url = 'http://localhost:8000' # Server's URL
    server = xmlrpc.client.ServerProxy(server_url) #returns object that can be used to call methods on the server
    
    #Ask topic
    term = input("Name search terms? : ")
    
    #get time
    time = datetime.datetime.now()
    timestamp = time.strftime("%m/%d/%y - %H:%M:%S")
    
    #Get data from the server
    try:
        result = server.getWiki(term, timestamp)
    except Exception:
        print("Error")
        return
    print("")
    print("Result: " + result) # Print result
    
main()