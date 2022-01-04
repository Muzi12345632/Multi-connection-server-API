# Multi-connection-server-API
API for concurrency connections

# Dependances

Install following libraries using pip
```
pip install selectors
pip install socket
pip install types


import selectors
import socket
import types
```
# Config


Difference between this server and the echo server is the call to lsock.setblocking(False) to configure the socket in non-blocking mode

sel.register() registers the socket to be monitored with sel.select() for the events 

 ```
 sel = selectors.DefaultSelector()

Isock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Isock.bind((HOST, PORT))
Isock.listen()
print('Listening on', (HOST, PORT))
Isock.setblocking(False)
sel.register(Isock, selectors.EVENT_READ, data=None)

 
 ```

For the listening socket, we want read events: selectors.EVENT_READ

Data is used to store whatever arbitrary data you’d like along with the socket

Use data to keep track of what’s been sent and received on the socket

sel.select(timeout=None) blocks until there are sockets ready for I/O.

If key.data is None, then we know it’s from the listening socket and we need to accept() the connection

```

def start_connections(host, port, num_conns):
    server_addr = (host, port)
```

If key.data is not None, then we know it’s a client socket that’s already been accepted, and we need to service it. service_connection()

```

def service_connection(key, mask ):
    sock = key.fileobj
    data = key.data

```

If the socket is ready for reading, then mask & selectors.EVENT_READ is true, and sock.recv() is called

Any data that’s read is appended to data.outb so it can be sent later

```
 if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]
```


# Multi connection client side

 it starts by initiating connections via start_connections()
 
 num_conns is read from the command-line, which is the number of connections to create to the server
 
 connect_ex() initially returns an error indicator, errno.EINPROGRESS, instead of raising an exception while the connection is in progress
 
 The data we want stored with the socket is created using the class types.SimpleNamespace
 
 ```
 
  data = types.SimpleNamespace(
                      connid= connid, msg_total= sum(len(m)for m in messages),
                     recv_total= 0, messages= list(messages), outb=b'')
 ```
 
 Messages the client will send to the server are copied using list(messages)
  
