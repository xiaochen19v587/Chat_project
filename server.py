from socket import *
import os, sys

ADDR = ('176.234.8.10', 7890)
info_dict = {}


def server_main():
    s = socket(AF_INET, SOCK_DGRAM)  # 创建UDP套接字
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 快速刷新端口
    s.bind(ADDR)  # 绑定地址
    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        while 1:
            msg = input('管理员消息:')
            msg = 'C 管理员消息 %s' % msg
            s.sendto(msg.encode(), ADDR)
    else:
        do_request(s)  # 处理客户端请求


def do_request(s):
    while 1:
        try:
            data, addr = s.recvfrom(1024)  # 接收客户端发送内容和客户端地址
            msg = data.decode().split(' ')

            if msg[0] == 'L':
                do_login(s, msg[1], addr)
            elif msg[0] == 'C':
                text = ' '.join(msg[2:])
                do_send(s, msg[1], text)
            elif msg[0] == 'Q':
                if msg[1] not in info_dict:
                    s.sendto('EXIT'.encode(), addr)
                    continue
                do_quit(s, msg[1])

        except KeyboardInterrupt:
            print('服务断关闭.')
            s.close()
            break


def do_login(s, name, addr):
    if name in info_dict or '管理员' in name:
        s.sendto('该用户已存在.'.encode(), addr)
        return
    s.sendto('OK'.encode(), addr)
    # 通知其他人
    msg = '欢迎%s进入聊天室.' % name
    for i in info_dict:
        s.sendto(msg.encode(), info_dict[i])
    # 将用户加入
    info_dict[name] = addr


def do_send(s, name, info):
    msg = '%s: %s' % (name, info)
    print('\r'+msg+'\n管理员消息:',end=' ')
    for i in info_dict:
        if i != name:
            s.sendto(msg.encode(), info_dict[i])


def do_quit(s, name):
    msg = '%s退出聊天室.' % name
    del info_dict[name]
    for i in info_dict:
        s.sendto(msg.encode(), info_dict[i])


if __name__ == '__main__':
    server_main()
