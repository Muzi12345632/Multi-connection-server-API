# Multi-connection-server-API
API for concurrency connections

difference between this server and the echo server is the call to lsock.setblocking(False) to configure the socket in non-blocking mode

sel.register() registers the socket to be monitored with sel.select() for the events 

For the listening socket, we want read events: selectors.EVENT_READ

data is used to store whatever arbitrary data you’d like along with the socket

use data to keep track of what’s been sent and received on the socket

sel.select(timeout=None) blocks until there are sockets ready for I/O.

If key.data is None, then we know it’s from the listening socket and we need to accept() the connection

If key.data is not None, then we know it’s a client socket that’s already been accepted, and we need to service it. service_connection() 

If the socket is ready for reading, then mask & selectors.EVENT_READ is true, and sock.recv() is called

Any data that’s read is appended to data.outb so it can be sent later

**MULTI CONNECTION CLIENT SIDE**

 it starts by initiating connections via start_connections()
 
 num_conns is read from the command-line, which is the number of connections to create to the server
 
 connect_ex() initially returns an error indicator, errno.EINPROGRESS, instead of raising an exception while the connection is in progress
 
 the data we want stored with the socket is created using the class types.SimpleNamespace
 
 messages the client will send to the server are copied using list(messages)
  
