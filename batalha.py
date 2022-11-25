from batalha_naval import BatalhaNaval
import time
import criar_tabela
import sqlite3
# Inicia Jogo

def verifica_e_atualiza_records(pontuacao_feita):

    connection = sqlite3.connect('records.db')
    cursor = connection.cursor()

    record_query = 'SELECT * FROM records WHERE pontos>?'
    result = cursor.execute(record_query, (pontuacao_feita,)) 
    row = result.fetchone()
    if row:
        connection.close()
        return False
    else:
        insert_query = 'INSERT INTO records VALUES (NULL,?)'
        cursor.execute(insert_query, (pontuacao_feita,))
        connection.close()
        return pontuacao_feita

def main():
    dict_msgs = {
        'facil': 'Saindo uma batalha mamão com açúcar para o marinheiro de primeira viagem...',
        'normal': 'Uma batalha equilibrada...Vamos começar!',
        'dificil': 'Gosta de desafio então? Mar calmo nunca fez bom marinheiro...'
    }
    print("\nBEM VINDO MARUJO!!\nAntes de começar a batalha...\n")
    time.sleep(1)
    print("\nVamos às REGRAS:")
    time.sleep(2)
    print("\n1) Você inicia o jogo com 10  TENTATIVAS.\n2) ERRAR um tiro consome 1 TENTATIVA.\n3) ACERTOS não gastam TENTATIVA\n4) Você vence se derrubar COMPLETAMENTE toda a frota inimiga\n5) Há caixas de munição escondidas que dão BONUS de 3 TENTATIVAS (exceto no nivel dificil!)\n6) \'~^\'=DESCONHECIDO, NV=navio, ag=tiro na agua, SP=municao\n7) Acertar= 1 ponto, Afundar navio = 3 pontos\n8) Voce perde se esgotarem suas TENTATIVAS, havendo ao menos 1 navio\n9) DIVIRTA-SE :)")
    time.sleep(5)
    print("Sem mais delongas...\n")
    time.sleep(1)
    nivel = input("Para começar a batalha, DIGITE UM NIVEL DE DIFICULDADE:\nfacil, normal ou dificil:\n")
    while nivel.lower() not in ['facil', 'normal', 'dificil']:
        nivel = input("Nivel inválido, cabeça de bagre! Escolhe entre\n facil, normal ou dificil:\n")
    time.sleep(1)
    print("\n"+dict_msgs[nivel])
    jogo = BatalhaNaval(dificuldade=nivel.lower())
    time.sleep(3)
    print("PARTIDA COMEÇA EM...\n")
    time.sleep(0.8)
    print("3...")
    time.sleep(0.8)
    print("2...")
    time.sleep(0.8)
    print("1...")
    time.sleep(1)
    while (jogo.tentativas_restantes > 0 and jogo.calcula_navios_restantes() >0):
        # print(jogo.tabuleiro_gabarito)
        print(jogo)
        print('SCORE: ', jogo.pontos)
        print('Quantidade de Tentativas: ', jogo.tentativas_restantes)
        print('Navios Restantes: ', jogo.calcula_navios_restantes())
        coordenada = input('Digite as coordenadas: ')
        x,y = jogo.converter_coordenadas(coordenada)
        jogo.atirar_em(x, y)

    if jogo.calcula_navios_restantes() <=0:
        print('VITORIAAAA!!!\nO mar é todo seu agora, capitão!')
        time.sleep(1)
        if verifica_e_atualiza_records(jogo.pontos):
            print(f"\n\nE VOCÊ BATEU UM RECORD!!! Com {jogo.pontos} PONTOS!\nNavegar é preciso, mas deixar seu LEGADO é essencial!!!\nParabéns!!!\n\n")
            time.sleep(1)
        time.sleep(1)

    elif jogo.tentativas_restantes <= 0:
        print('G A M E   O V E R !')
        print('VOCE PERDEU :(')
        time.sleep(3)

    novo = input('Gostaria de começar uma nova batalha?[s] ou [n]\n')
    
    if novo.lower() == 's':
        print("Vamos para mais uma! Derrote a frota inimiga!")
        return main()
    print("Nos vemos em breve, marujo!")
    

if __name__ == '__main__':

    main()
    


    

