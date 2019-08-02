from collections import defaultdict
import socket, select, sys

def connectServer():
    TCP_IP = '0.0.0.0'
    TCP_PORT = 5000

    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, 5000))
    socket_list = [sys.stdin, s]
    na = nbboAnalyzer()
    while 1:
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for sock in read_sockets:
            # incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print('\nDisconnected from server')
                    sys.exit()
                else:
                    sys.stdout.write("\n")
                    na.analyze(data.decode())
            else:
                msg = sys.stdin.readline()
                s.send(bytes(msg))
                sys.stdout.write('<Me> ')
                sys.stdout.flush()

class nbboAnalyzer:
    exchange_map = {'NASDAQ': 0, 'BATS': 1}

    def __init__(self):
        self.data = defaultdict(list)

    def analyze(self, message):
        m = message.split('\n')
        print(m, self.data)
        for q in m:
            if q and q[0] == 'Q':
                splited_data = q.split('|')
                print(splited_data)
                if not splited_data[1] in self.data:
                    self.data[splited_data[1]].append([0.0] * len(nbboAnalyzer.exchange_map))
                    self.data[splited_data[1]].append([float('inf')] * len(nbboAnalyzer.exchange_map))
                    print(self.data[splited_data[1]])

                self.data[splited_data[1]][0][nbboAnalyzer.exchange_map[splited_data[2]]] = float(splited_data[3])
                self.data[splited_data[1]][1][nbboAnalyzer.exchange_map[splited_data[2]]] = float(splited_data[4])
                print(splited_data[1], max(self.data[splited_data[1]][0]), '@', min(self.data[splited_data[1]][1]))


def main():
    connectServer()

if __name__ == "__main__":
    main()
