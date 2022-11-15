from random import randint
import numpy as np

class BatalhaNaval():
    def __init__(self, ordem, dificuldade='facil'):
        assert type(ordem)==int and (ordem>1 and ordem<=10)
        assert dificuldade in ['facil', 'normal', 'dificil']
        self.ordem = ordem+1
        self.pontos = 0
        self.tentativas_restantes = ordem
        self.dificuldade = dificuldade
        self.tabuleiro = np.array(self.gerar_tabuleiro_vazio())
        self.tabuleiro_gabarito = np.array(self.gerar_tabuleiro_vazio())
        self.popular_navios()

    # Geração do tabuleiro em branco (apenas "água")
    def gerar_tabuleiro_vazio(self):
        return [['~'] * self.ordem for i in range(self.ordem)]

    # Popular aleatoriamente o tabuleiro criado com os navios
    def popular_navios(self):
        navios_restantes = 0
        if self.dificuldade == 'facil':
            navios_restantes = self.ordem*self.ordem//3
        while navios_restantes:
            x = randint(0, self.ordem-1)
            y = randint(0, self.ordem-1)
            if self.tabuleiro_gabarito[x][y] == '~':
                self.tabuleiro_gabarito[x][y] = 'N'
                navios_restantes-=1
        return self.tabuleiro_gabarito
            

#game = BatalhaNaval(10)
#game.popular_navios()