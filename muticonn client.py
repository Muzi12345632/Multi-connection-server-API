import socket
import selectors
import types

messages = [b'Message 1 from client',b'Message 2 from client']
sel = selectors.DefaultSelector()


##HOST = '127.0.0.1'
##PORT = 65432

def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print('started connection', connid, 'to', server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect_ex(server_addr)
        sock.setblocking(False)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
                      connid= connid, msg_total= sum(len(m)for m in messages),
                     recv_total= 0, messages= list(messages), outb=b'')

        sel.register(sock, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print('received ', repr(recv_data), 'from connection', data.connid)
            data.recv_total += len(recv_data)
            if not recv_data or data.recv_total == data.msg_total:
                print('closing conection', data.connid)
                sel.unregister(sock)
                sock.close()

    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
            if data.outb:
                print('sending to', repr(data.outb), 'from', data.connid )
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]


