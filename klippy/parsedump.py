#!/usr/bin/env python
####################################
#项目名称：
#芯片类型: 
#功能: 
#研发人员：蓝才刚
#开发时间: 20230830
####################################


import os, sys, logging
import msgproto
####################################
#函数名称：
#输入参数：
#返 回 值:
#功能描述：蓝才刚-20230830
####################################
def read_dictionary(filename):
    dfile = open(filename, 'rb')
    dictionary = dfile.read()
    dfile.close()
    return dictionary
####################################
#函数名称：
#输入参数：
#返 回 值:
#功能描述：蓝才刚-20230830
####################################
def main():
    dict_filename, data_filename = sys.argv[1:]

    dictionary = read_dictionary(dict_filename)

    mp = msgproto.MessageParser()
    mp.process_identify(dictionary, decompress=False)

    f = open(data_filename, 'rb')
    fd = f.fileno()
    data = bytearray()
    while 1:
        newdata = os.read(fd, 4096)
        if not newdata:
            break
        data += bytearray(newdata)
        while 1:
            l = mp.check_packet(data)
            if l == 0:
                break
            if l < 0:
                logging.error("Invalid data")
                data = data[-l:]
                continue
            msgs = mp.dump(data[:l])
            sys.stdout.write('\n'.join(msgs[1:]) + '\n')
            data = data[l:]

if __name__ == '__main__':
    main()
