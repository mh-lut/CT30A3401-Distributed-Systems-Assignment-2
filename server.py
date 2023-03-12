#0608560
#CT30A3401 Distributed Systems
#Assignment 2
#Server part
#help received: https://docs.python.org/3/library/xmlrpc.html, ChatGPT, https://www.mediawiki.org/wiki/API:Opensearch, https://docs.python.org/3/library/xml.etree.elementtree.html, https://requests.readthedocs.io/en/master/

import xmlrpc.server, socketserver, requests
import xml.etree.ElementTree as ET

# create XML data structure
data = ET.Element('data')


def main():
    print("Server running...")
    
    class ThreadedXMLRPCServer(socketserver.ThreadingMixIn, xmlrpc.server.SimpleXMLRPCServer): # "ThreadingMixIn" to enable handling of multiple requests concurrently
        pass
    
    server = ThreadedXMLRPCServer(('localhost', 8000)) #server adress
    
    #server functions
    server.register_introspection_functions()
    server.register_function(addNote)
    server.register_function(getNote)
    server.register_function(getWiki)

    #start server
    server.serve_forever()
    

def addNote(topicClient, noteClient,  textClient, timestapClient):
    
    old = 0 #if stay 0 make new topic
    
    #check if old exist
    for topic in data.findall('topic'):
        if topic.get('name') == topicClient:
            old = 1
            
            note = ET.SubElement(topic, 'note')
            note.set('name', noteClient)
            
            text = ET.SubElement(note, 'text')
            text.text = textClient
            
            timestamp = ET.SubElement(note, 'timestamp')
            timestamp.text = timestapClient
            
            tree = ET.ElementTree(data)
            tree.write('db.xml')
            print("File updated!")
            
            return str("ok (old found)")

    #create new
    if(old == 0):
        topic = ET.SubElement(data, 'topic')
        topic.set('name', topicClient)
        
        note = ET.SubElement(topic, 'note')
        note.set('name', noteClient)

        text = ET.SubElement(note, 'text')
        text.text = textClient

        timestamp = ET.SubElement(note, 'timestamp')
        timestamp.text = timestapClient
        
    tree = ET.ElementTree(data)
    tree.write('db.xml')
    print("File updated!")
    
    return str("ok (new created)")




def getNote(topicClient):
        
    for topic in data.findall('topic'):
        if topic.get('name') == topicClient:
            return (ET.tostring(topic).decode())
    
    return str("not topic with name '" + topicClient + "'")

def getWiki(term, timestamp):
    # Make a request to the Wikipedia API to get the page data
    params = {
        "action": "query",
        "format": "json",
        "titles": term,
        "prop": "extracts",
        "exintro": "",
        "explaintext": "",
    }
    response = requests.get("https://en.wikipedia.org/w/api.php", params=params)

    # Parse the response JSON and extract the page data
    data = response.json()
    print(data)
    pages = data["query"]["pages"]
    page_id = next(iter(pages))
    if(page_id == "-1"):
        return str("No info found")
    page = pages[page_id]
    title = page["title"]
    summary = page["extract"]

    result = addNote(term, title, summary, timestamp)
    return result
main()