from batalha_naval import BatalhaNaval

# Inicia Jogo
jogo = BatalhaNaval()
jogo.popular_navios()


while (jogo.tentativas_restantes != 0 or jogo.quantidade_navios !=0):
    print('Quantidade de Tentativas: ', jogo.tentativas_restantes)
    print('Navios Restantes: ', jogo.quantidade_navios)
    print(jogo.tabuleiro_gabarito)
    print(jogo.tabuleiro)
    coordenada = input('Digite as coordenadas: ')
    x,y = jogo.converter_coordenadas(coordenada)
    jogo.atirar_em(x, y)
    if jogo.tentativas_restantes == 0:
        print('Você perdeu :/, tente outra vez!')
        break
    if jogo.quantidade_navios == 0:
        print('Você venceu')
        break

