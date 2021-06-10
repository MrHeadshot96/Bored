import os
file_code = "code.txt"
file_tran = "translated.txt"
analized = {}

def analize():
    file_c = open(file_code, "r", encoding='ANSI')
    data_c = file_c.read()
    file_c.close()
    data_c = data_c.split()
    leng = len(data_c) -1
    file_t = open(file_tran, "r", encoding='ANSI')
    data_t = str(file_t.read())
    file_t.close()
    leng2 = len(data_t)
    print (leng,leng2)
    while leng > 0:
        if data_c[leng] in analized:
            pass
        else:
            analized.update({ data_c[leng] : data_t[leng]})
        leng -=1
    for key, value in analized.items():
        print( key, ' : ', value)
    file_decode = open("decoded.txt",'w')
    file_decode.write(str(analized))
analize()