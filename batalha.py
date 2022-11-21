from batalha_naval import BatalhaNaval

# Inicia Jogo
jogo = BatalhaNaval()
jogo.popular_navios()

def main():
    while (jogo.tentativas_restantes > 0 or jogo.calcula_navios_restantes() >0):
        print('Quantidade de Tentativas: ', jogo.tentativas_restantes)
        print('Navios Restantes: ', jogo.calcula_navios_restantes())
        # print(jogo.tabuleiro_gabarito)
        print(jogo.tabuleiro)
        coordenada = input('Digite as coordenadas: ')
        x,y = jogo.converter_coordenadas(coordenada)
        jogo.atirar_em(x, y)

    if jogo.quantidade_navios <=0:
        print('VOCÊ VENCEU!!!')

    if jogo.tentativas_restantes <= 0:
        print('Você perdeu :/, tente outra vez!')

    novo = input('Gostaria de começar um novo jogo?[s] ou [n]\n')
    
    if novo.lower() == 's':
        print("Vamos para mais uma! Derrote a frota inimiga!")
        return main()
    print("Nos vemos em breve, marujo!")
    

if __name__ == '__main__':

    main()
    


    

