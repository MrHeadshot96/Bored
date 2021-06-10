import os
file_code = "code.txt"
analized = {}

def decode():
    text =""
    file_c = open(file_code)
    file_decode = open("decoded.txt")
    data_c = file_c.read()
    data_t = file_decode.read()
    data_t = eval(data_t)
    data_c = list(data_c.split(" "))
    leng = 0
    while leng < len(data_c):
        symb = data_c[leng]
        if symb in data_c:
           text += str(data_t.get(symb))
        leng +=1
    text = str(text)
    text.replace("b"," ")
    file_end = open("end.txt",'w')
    file_end.write(str(text))
    file_end = open("end.txt")
    text = file_end.read()
    print(text)
decode()