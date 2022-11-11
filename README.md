                      Lab 2 - ECE 358
---------------------------Task 1---------------------------
*notes
 - python 3 was used
 - the code runs on the eceubuntu server BUT could not be 
   tested with a client (such as postman) see piazza @453
 - URL: http://127.0.0.1:10000/HellowWorld.html

1. run "webserver.py" with "HelloWorld.html" in the same 
   direcotry OR in a directory below the one with 
   "webserver.py"
2. Open a client such as postman or a browser and use the 
   above URL to communicate with the webserver
3. Test for GET and HEAD requests, the server will reply
   with appropriate headers and data accordingly. 
   NOTE: 3 headers will be empty when testing for a file 
   name that is NOT present

---------------------------Task 2---------------------------
 - python 3 was used
 - code runs on server with 'python3 client.py' and 
   'python3 server.py'
 
1. open both server and client
2. input desired domain name into client (eg. 'google.com')
3. client will output requested data and server will 
   display the request and response in hex
4. if an unknown domain is entered, client will display 
   'Unknown domain name' and the server will not dispay 
   any response
5. if 'end' is entered into the client, the connection 
   will end. Server and client will stop
