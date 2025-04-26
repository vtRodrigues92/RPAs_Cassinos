txt = open("canais.txt", "r")

free = txt.readlines(1)
vip = txt.readlines(2)
ids = txt.readlines(3)

for canal in free:
    free=canal.split(' ')
    free = free[1]
    print(free)

for canal in vip:
    vip=canal.split(' ')
    vip = vip[1]
    print(vip)

for id in ids:
    id_usuario = id.split(' ')
    id_usuario = id_usuario[1]
    print(id_usuario)

if '1476864285' in id_usuario:
    print('Está aqui')
