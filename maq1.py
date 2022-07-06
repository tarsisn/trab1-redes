import socket
import sys
import pickle
import time
import numpy as np

HOST = '127.0.0.1'
#HOST = '192.168.122.66'
PORT = 9999

matrix = []
detx = []
tempo = []
matriz = dict()
i = 0
t1 = time.time()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))
# print("conectado em --- ", HOST, PORT)
falha = 1

while falha:

    try:
        print(f"Tentando conectar ao endereço '{HOST}' pela porta {PORT}")
        s.connect((HOST, PORT))
    except:
        print(f"Endereço '{HOST}' não conectado!!")
        HOST = input("Por favor informe o endereço da Maquina G1 [enter = self]: ")
        if HOST == '':
            HOST = '127.0.0.1'
        PORT = int(input("Informe o numero do PORT CRIADO no Serviço B: "))
        falha = 1
    else:
        print(f"Endereço '{HOST}' conectado!!")
        falha = 0


while True:
    print("PROGRAMA QUE ENVIA MATRIZES")
    print("Digite a quantidade de matrizes que vc quer")
    qtd = int(input())
    print("Digite a ordem da matriz")
    tam = int(input())
    while i != qtd:
        m = np.random.randint(99, size=(tam, tam))
        print(m)
        #det = np.linalg.det(m)
        matrix.append(m)
        #detx.append(det)
        i = i + 1

    #print("passei aqui")
    tempo.append(t1)
    matriz['matrizes'] = matrix
    #matriz['det'] = detx
    matriz['tempo'] = tempo
    print("tempo inicial")
    print(matriz['tempo'])


    #print(f"esse é o tempooooooo ------------", tempo)

    pack1 = pickle.dumps(matriz)

    #tamanho aqui em bytes total de tudo
    tampct = sys.getsizeof(pack1)
    #agora vou dividir os pacotes pra ver a qtd pq cada pacote é de 1024
    qtd_pct = int(np.ceil(tampct/1024))
    #tamanho aqui do pacote
    tampct2 = int(len(pack1)/qtd_pct)
    tampct_bytes = sys.getsizeof(pack1[:tampct2])
    data = []
    if qtd_pct ==1:
        #s.sendall(pack1)
        data.append(pack1)
        for i in data:
            print(f"entrei no i {i}")
            s.sendall(bytes(i))
        time.sleep(0.1)
        s.sendall(pickle.dumps("Pacote enviooou"))
        print("matrizes e tempo enviados with sucess")
        s.close()

    else:
        print("entrei o no else")
        while tampct2 > 1024:
            qtd_pct +=2
            tampct2 = int(len(pack1)/qtd_pct)
            tampct_bytes = sys.getsizeof(pack1[:tampct2])

        for i in range(qtd_pct):
            aux = pack1[(i)*tampct2:(i+1)*tampct2]
            data.append(aux)

            if i==(qtd_pct-1) and (i+1)*tampct2<len(pack1):
                aux = pack1[(i+1)*tampct2]
                data.append(aux)
        for i in data:
            s.sendall(bytes(i))
            #s.sendall(data[i])
        time.sleep(0.1)
        s.sendall(pickle.dumps("Pacote enviooou"))
        #print("pacote enviou?")
        s.close()
    break
    # s.sendall(bytes(pack1))
    # time.sleep(1)
    # s.close()
    #break


