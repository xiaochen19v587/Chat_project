from socket import *
import os, sys

ADDR = ('176.234.8.10', 7890)


def client_main():
    '''
     客户端
    :return:
    '''

    s = socket(AF_INET, SOCK_DGRAM)
    do_request(s)  # 处理信息


def do_request(s):
    while 1:
        name = input('输入姓名:')
        msg = 'L ' + name
        s.sendto(msg.encode(), ADDR)
        # 等待回应
        data, addr01 = s.recvfrom(1024)
        if data.decode() == 'OK':
            print('您已进入聊天室.')
            break
        else:
            print(data.decode())
    pid = os.fork()
    if pid < 0:
        sys.exit('Error!')
    elif pid == 0:
        send_msg(s, name)
    else:
        recv_msg(s)


def recv_msg(s):
    while 1:
        data, addr01 = s.recvfrom(1024)
        # 服务端发送EXIT表示让客户端退出
        if data.decode() == 'EXIT':
            sys.exit()
        print('\r' + data.decode() + '\n请输入内容:', end=' ')


def send_msg(s, name):
    while 1:
        try:
            content = input('请输入内容:')
        except KeyboardInterrupt:
            content = 'quit'
        if content == 'quit':
            msg = 'Q ' + name
            s.sendto(msg.encode(), ADDR)
            sys.exit('退出聊天室')
        msg = 'C %s %s' % (name, content)
        s.sendto(msg.encode(), ADDR)


if __name__ == '__main__':
    client_main()
