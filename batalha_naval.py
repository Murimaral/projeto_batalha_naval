from random import randint
import numpy as np
import pandas as pd

class BatalhaNaval():
    def __init__(self, dificuldade='facil'):
        assert dificuldade in ['facil', 'normal', 'dificil']
        self.ordem = 10
        self.pontos = 0
        self.tentativas_restantes = 5
        self.dificuldade = dificuldade
        self.tabuleiro = self.gerar_tabuleiro_vazio()
        self.tabuleiro_gabarito = self.gerar_tabuleiro_vazio()


    # Geração do tabuleiro em branco (apenas "água")
    def gerar_tabuleiro_vazio(self):
        array_agua = ['~^'] * self.ordem
        coordenadas_letras = "ABCDEFGHIJ"
        dict_coordenadas = {}
        for letra in coordenadas_letras:
            dict_coordenadas[letra]=array_agua
        
        tabuleiro = pd.DataFrame.from_dict(dict_coordenadas, \
                    orient="index", columns= list(range(1,11)))
        return tabuleiro


    # Popular aleatoriamente o tabuleiro criado com os navios
    def popular_navios(self):
        navios_restantes = 0
        if self.dificuldade == 'facil':
            navios_restantes = self.ordem*self.ordem//3
        while navios_restantes:
            x = randint(0, self.ordem-1)
            y = randint(0, self.ordem-1)
            if self.tabuleiro_gabarito.iloc[x].at[y] == '~~':
                self.tabuleiro_gabarito.iloc[x].at[y] = 'NN'
                navios_restantes-=1
        return self.tabuleiro_gabarito
            
    def popular_porta_avioes(self):
        # Sentido aleatorio
        sentido = "horizontal" if randint(0,1) else "vertical"
        # plotar um ponto aleatorio que caiba o navio
        navios_restantes = 3
        tentativas = 10
        while navios_restantes>0 and tentativas>0:
            if sentido == "vertical":
                # vertical
                x = randint(2, self.ordem-3)
                y = randint(1, self.ordem)
                if len(set([self.tabuleiro_gabarito.iloc[x-2].at[y],\
                           self.tabuleiro_gabarito.iloc[x-1].at[y],\
                           self.tabuleiro_gabarito.iloc[x].at[y],\
                           self.tabuleiro_gabarito.iloc[x+1].at[y],\
                           self.tabuleiro_gabarito.iloc[x+2].at[y]]))>1:
                           tentativas-=1
                           continue
                self.tabuleiro_gabarito.iloc[x-2].at[y],\
                           self.tabuleiro_gabarito.iloc[x-1].at[y],\
                           self.tabuleiro_gabarito.iloc[x].at[y],\
                           self.tabuleiro_gabarito.iloc[x+1].at[y],\
                           self.tabuleiro_gabarito.iloc[x+2].at[y] = 'TT','||','PA','||','YY'
                
            else:
                # horizontal
                x = randint(0, self.ordem-1)
                y = randint(3, self.ordem-2)
                if len(set([self.tabuleiro_gabarito.iloc[x].at[y-2],\
                           self.tabuleiro_gabarito.iloc[x].at[y-1],\
                           self.tabuleiro_gabarito.iloc[x].at[y],\
                           self.tabuleiro_gabarito.iloc[x].at[y+1],\
                           self.tabuleiro_gabarito.iloc[x].at[y+2]]))>1:
                           tentativas-=1
                           continue
                self.tabuleiro_gabarito.iloc[x].at[y-2],\
                           self.tabuleiro_gabarito.iloc[x].at[y-1],\
                           self.tabuleiro_gabarito.iloc[x].at[y],\
                           self.tabuleiro_gabarito.iloc[x].at[y+1],\
                           self.tabuleiro_gabarito.iloc[x].at[y+2] = ' <','==','PA','==','> '
            navios_restantes-=1
            sentido = "horizontal" if randint(0,1) else "vertical"
        return self.tabuleiro_gabarito
    
    def popular_cruzador(self):
        # Sentido aleatorio
        sentido = "horizontal" if randint(0,1) else "vertical"
        # plotar um ponto aleatorio que caiba o navio
        navios_restantes = 6
        tentativas = 10
        while navios_restantes>0 and tentativas>0:
            if sentido == "vertical":
                # vertical
                x = randint(1, self.ordem-2)
                y = randint(1, self.ordem)
                if len(set([self.tabuleiro_gabarito.iloc[x-1].at[y],\
                           self.tabuleiro_gabarito.iloc[x].at[y],\
                           self.tabuleiro_gabarito.iloc[x+1].at[y]])) > 1:
                           tentativas-=1
                           continue
                self.tabuleiro_gabarito.iloc[x-1].at[y],\
                           self.tabuleiro_gabarito.iloc[x].at[y],\
                           self.tabuleiro_gabarito.iloc[x+1].at[y] = 'TT','||','YY'
            else:
                # horizontal
                x = randint(0, self.ordem-1)
                y = randint(2, self.ordem-1)
                if len(set([self.tabuleiro_gabarito.iloc[x].at[y-1],\
                           self.tabuleiro_gabarito.iloc[x].at[y],\
                           self.tabuleiro_gabarito.iloc[x].at[y+1]])) > 1:
                           tentativas-=1
                           continue
                self.tabuleiro_gabarito.iloc[x].at[y-1],\
                           self.tabuleiro_gabarito.iloc[x].at[y],\
                           self.tabuleiro_gabarito.iloc[x].at[y+1] = ' <','==','> '
            navios_restantes-=1
            sentido = "horizontal" if randint(0,1) else "vertical"
        return self.tabuleiro_gabarito




#game = BatalhaNaval(10)
#game.popular_navios()