import time
from datetime import datetime, timedelta
import os



data_hoje = datetime.today().strftime('%d/%m/%Y')
arquivos_placares = os.listdir(r"placar/")

if 'teste.txt' in arquivos_placares:
    # Carregar arquivo de placares
    with open(r"placar/teste.txt", 'r') as arquivo:
        try:

            placar = arquivo.readlines()
            placar_win = int(placar[0].split(',')[1])
            placar_semGale = int(placar[1].split(',')[1])
            placar_gale1 = int(placar[2].split(',')[1])
            placar_gale2 = int(placar[3].split(',')[1])
            placar_loss = int(placar[4].split(',')[1])
            placar_geral = int(placar_win) + int(placar_loss)
            asserividade = placar[5].split(',')[1]+"%"
        
        except:
            pass

        
else:
    # Criar um arquivo com a data atual
    with open(r"placar/teste.txt", 'w') as arquivo:
        arquivo.write("win,0\nsg,0\ng1,0\ng2,0\nloss,0\nass,0")

    
    with open(r"placar/teste.txt", 'r') as arquivo:
        try:

            placar = arquivo.readlines()
            placar_win = int(placar[0].split(',')[1])
            placar_semGale = int(placar[1].split(',')[1])
            placar_gale1 = int(placar[2].split(',')[1])
            placar_gale2 = int(placar[3].split(',')[1])
            placar_loss = int(placar[4].split(',')[1])
            placar_geral = int(placar_win) + int(placar_loss)
            asserividade = placar[5].split(',')[1]+"%"
        
        except:
            pass

    


print("📊 Placar Atual:\n\
        ==================\n\
        😍 WIN - "+str(placar_win)+"\n\
        🏆 WIN S/ GALE - "+str(placar_semGale)+"\n\
        🥇 WIN GALE1 - "+str(placar_gale1)+"\n\
        🥈 WIN GALE2 - "+str(placar_gale2)+"\n\
        😭 LOSS - "+str(placar_loss)+"\n\
        ==================\n\
        🎯 Assertividade "+ str(round(placar_win / placar_geral*100, 1)).replace('.0',"")+"%" if placar_win != 0 else "🎯 Assertividade - 0%")


print(placar_win, placar_semGale, placar_gale1, placar_gale2, placar_loss, placar_geral, asserividade)

#f'{data_hoje}.txt'