import socket
import pickle
import sys
import time
import numpy as np

t2 = time.time()

host = '127.0.0.1'
#host = '192.168.122.66'
port = '9999'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, int(port)))
s.listen(2)
print('Aguardando conexao')
conn, ender = s.accept()
print('conectado em', ender)

def montar(dados):
    arquivo = pickle.loads(b''.join(dados))
    return arquivo

data = []
data_list = []

invx = []
detx =[]
tempx = []

while True:
    #conn, ender = s.accept()
    #print("to no primeiro while")
    rec_data = conn.recv(2048)
    data.append(rec_data)
    if data[-1] == b'\x80\x04\x95\x13\x00\x00\x00\x00\x00\x00\x00\x8c\x0fPacote enviooou\x94.':
        data.pop(-1)
        data_ok = montar(data)
        invx = np.linalg.inv(data_ok['matrizes'])
        detx = np.linalg.det(invx)
        break


data_3 = dict()
data_3['inversa'] = invx
data_3['determinantes'] = detx

time1 = data_ok['tempo']
time2 = float(time1[0]) + time.time() - t2

data_3['tempo'] = time2

host2 = '127.0.0.1'
# host2 = '192.168.122.130'
port2 = 9000
d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
d.connect((host2, port2))

while True:

    pack = pickle.dumps(data_3)
    tam_bytes = sys.getsizeof(pack)
    qtd_pct = int(np.ceil(tam_bytes/1024))
    tam_pct = int(len(pack)/qtd_pct)
    tam_pct_b = sys.getsizeof(pack[:tam_pct])

    if qtd_pct == 1:
        data_list.append(pack)
        for i in data_list:
            d.sendall(i)
        time.sleep(0.1)
        d.sendall(pickle.dumps("Pacote enviooou"))
        print("se chegou essa msg os dados foram enviados")
        d.close()
    else:
        while tam_pct>1024:
              qtd_pct += 2
              tam_pct = int(len(pack)/qtd_pct)
              tam_pct_b = sys.getsizeof(pack[:tam_pct])

        for i in range(qtd_pct):  #Lista com os packs
             aux = pack[(i)*tam_pct:(i+1)*tam_pct]
             data_list.append(aux)

             if i==(qtd_pct-1) and (i+1)*tam_pct<len(pack): #Garantir que tudo esta dentro da lista
                aux=pack[(i+1)*tam_pct:]
                data_list.append(aux)
        for i in data_list:
            d.sendall(i)
        time.sleep(0.1)
        d.sendall(pickle.dumps("Pacote enviooou"))
        print("se chegou essa msg os dados foram enviados")
        d.close()
    break




