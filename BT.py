from threading import Lock, Thread
from time import sleep

from bluetooth import *


class BT:
    last_frame = []
    mutex = Lock()

    def loop(self):
        print("Init loop")
        while 1:
            try:
               server_sock = BluetoothSocket(RFCOMM)
               server_sock.bind(("", PORT_ANY))
               server_sock.listen(1)
               port = server_sock.getsockname()[1]
               uuid = "f21b7d92-bf0c-4cd5-8f45-bcf24fc3e088"
               advertise_service(server_sock, "SampleServer",
                                 service_id=uuid,
                                 service_classes=[uuid, SERIAL_PORT_CLASS],
                                 profiles=[SERIAL_PORT_PROFILE],
                                 #                   protocols = [ OBEX_UUID ]
                                 )

               print("Waiting for connection on RFCOMM channel %d" % port)
               client_sock, client_info = server_sock.accept()
               print("Accepted connection from ", client_info)
               try:
                   while True:
                       sleep(0.1)
                       data = client_sock.recv(16)
                       if len(data) == 0: break
                       print("received [%s]" % data)
                       self.mutex.acquire()
                       self.last_frame = data
                       self.mutex.release()
               except IOError:
                   pass
               print("disconnected")
               client_sock.close()
               server_sock.close()
               print("all done")
            except:
                pass

    def get_left_right(self):
        self.mutex.acquire()
        if self.last_frame and len(self.last_frame)==16:
            left = self.last_frame[0:4]
            right = self.last_frame[4:8]
            iterator = self.last_frame[8:16]
        self.mutex.release()
        left = left.decode("utf-8")
        right = right.decode("utf-8")
        iterator = iterator.decode("utf-8")
        return [int(left),int(right),int(iterator)]

bt = BT()

t = Thread(target = bt.loop)
t.start()
t.join()

while True:
    print("none")

