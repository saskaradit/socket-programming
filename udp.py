import argparse
import socket

MAX_SIZE_BYTES = 65535  # Mazimum size of a UDP datagram


def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data


def server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = '127.0.0.1'
    s.bind((hostname, port))
    print('Listening at {}'.format(s.getsockname()))
    while True:
        data, clientAddress = s.recvfrom(MAX_SIZE_BYTES)
        message = data.decode('ascii')
        upperCaseMessage = message.upper()
        print('The client at {} says {!r}'.format(clientAddress, message))
        data = upperCaseMessage.encode('ascii')
        s.sendto(data, clientAddress)


def client(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hosts = []
    while True:
        host = input('Input host address:')
        hosts.append((host, port))
        message = input('Input lowercase sentence:')
        data = message.encode('ascii')
        s.sendto(data, (host, port))
        print('The OS assigned the address {} to me'.format(s.getsockname()))
        data, address = s.recvfrom(MAX_SIZE_BYTES)
        text = data.decode('ascii')
        if(address in hosts):
            print('The server {} replied with {!r}'.format(address, text))
            hosts.remove(address)
        else:
            print('The server {} replied with {!r}'.format(address, text))


if __name__ == '__main__':
    funcs = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='UDP client and server')
    parser.add_argument('functions', choices=funcs, help='client or server')
    parser.add_argument('-p', metavar='PORT', type=int, default=3000,
                        help='UDP port (default 3000)')
    args = parser.parse_args()
    function = funcs[args.functions]
    function(args.p)
