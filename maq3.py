import socket
import pickle
import time

t3 = time.time()

def montar(dados):
    arquivo = pickle.loads(b''.join(dados))
    return arquivo

host = '127.0.0.1'
#host = '192.168.122.130'
port = '9000'
e = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
e.bind((host, int(port)))
e.listen(5)
print('Aguardando conexao')
conn, ender = e.accept()
print('conectado em', ender)

data = []
data_list = []

while True:
    rec_data = conn.recv(2048)
    data.append(rec_data)
    if data[-1] == b'\x80\x04\x95\x13\x00\x00\x00\x00\x00\x00\x00\x8c\x0fPacote enviooou\x94.':
        data.pop(-1)
        data_ok = montar(data)
        break

determinante = data_ok['determinantes']
inversa = data_ok['inversa']
time2 = data_ok['tempo']

print("Matriz inversa: ")
print(inversa, '\n')
print("Determinante da  inversa: ")
print(determinante, '\n')

time2 = round(time2,4)
t_final = time2 + time.time() - t3

print("o tempo total em milissegundos foi o exibido abaixo")
print(round(t_final,2))








