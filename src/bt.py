import os
import glob
import time
from bluetooth import *

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service(server_sock, "AquaPiServer",
                  service_id=uuid,
                  service_classes=[uuid, SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE],
                  #                  protocols = [ OBEX_UUID ]
                  )
while True:
    print("Waiting for connection on RFCOMM channel %d" % port)

    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)

    try:
        data = client_sock.recv(1024)
        if len(data) == 0:
            break
        print("received [%s]" % data)
        data = 'Hello!'
        client_sock.send(data)
        print("sending [%s]" % data)

    except IOError:
        pass

    except KeyboardInterrupt:
        print("disconnected")
        client_sock.close()
        server_sock.close()
        print("all done")
        break
