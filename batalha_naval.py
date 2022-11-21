from random import randint
import numpy as np
import time
import pandas as pd

class BatalhaNaval():
    def __init__(self, dificuldade='facil'):
        assert dificuldade in ['facil', 'normal', 'dificil']
        self.ordem = 10
        self.pontos = 0
        self.tentativas_restantes = 10
        self.dificuldade = dificuldade
        self.tabuleiro = self.gerar_tabuleiro_vazio()
        self.tabuleiro_gabarito = self.gerar_tabuleiro_vazio()
        self.navios_plotados = []
        self.popular_navios()

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

    def calcula_navios_restantes(self):
        self.navios_plotados = [ x for x in self.navios_plotados if x ]
        return len(self.navios_plotados)

    def escolher_coordenada(self):
        coordenada_string = input("Digite uma coordenada: ")
        x,y = self.converter_coordenadas(coordenada_string)
        if not self.atirar_em(x,y):
            inp = input("Digite uma coordenada: ")
            return self.escolher_coordenada(inp)

    def converter_coordenadas(self,coordenada):
        coordenada = coordenada.strip()
        print(len(coordenada), coordenada)
        if len(coordenada) not in [2,3]:
            print("Coordenada deve conter 1 letra e um numero\n")
            print(self.tabuleiro)
            inp = input("Digite uma coordenada: ")
            return self.converter_coordenadas(inp)
        
        letra = coordenada[0:1]
        numero = coordenada[1:]

        if letra.isnumeric() or not numero.isnumeric():
            print("Coordenada inválida: Primeiro letra, em segundo número\n")
            print(self.tabuleiro)
            inp = input("Digite uma coordenada: ")
            return self.converter_coordenadas(inp)
        
        if letra.lower() not in "abcdefghij" or int(numero) not in range(1,11):
            print("Coordenada inválida, range excedido\n")
            print(self.tabuleiro)
            inp = input("Digite uma coordenada: ")
            return self.converter_coordenadas(inp)

        y = 'abcdefghij'.find(letra.lower())
        x = int(numero)

        return x,y

    def atirar_em(self,x,y):

        dict_msgs_erro = {
            0: "\nAcertou a.........água :/. Tente de novo...\n",
            1: "\nUia! Quase mas não foi dessa vez...\n",
            2: "\nUm tiro torto... e munição perdida...\n"
        }

        dict_msgs_acerto = {
            0: "\nPOWWW! Acertou em cheio!!!\n",
            1: "\nAcertou!! Tiro, porrada e bomba!!\n",
            2: "\nDanificou o navio inimigo!! Isso aí!\n"
        }

        dict_msgs_afunda = {
            0: "\nE você afundou um navio inimigo!!\n",
            1: "\nHOMEM AO MAR!! Você conseguiu afundar o navio inimigo!\n",
            2: "\nMuito bem! Mandou o navio inimigo repousar no fundo do oceano...\n",
            3: "\n\"É um navio que não afunda\" disseram... Pois esse afundou!!\n"
        }
        
        if self.tabuleiro.iloc[y].at[x] in ['agua', 'NV', '[SP]']:
            print("Escolha outra coordenada, ponto já revelado!!\n")
            print(self.tabuleiro)
            return False

        self.animar_mira()

        if self.tabuleiro_gabarito.iloc[y].at[x] == '~^':
            self.animar_tiro()
            self.tabuleiro.iloc[y].at[x] = 'agua'
            msg_id = randint(0,2)
            print(dict_msgs_erro[msg_id])
            # print(f'Tentativa {self.tentativas_restantes}')

        elif self.tabuleiro_gabarito.iloc[y].at[x] != '[SP]':
            self.animar_tiro()
            self.tabuleiro.iloc[y].at[x] = 'NV'
            msg_id = randint(0,2)
            print(dict_msgs_acerto[msg_id])
            for navio in self.navios_plotados:
                if (y,x) in navio:
                    navio.remove((y,x))
                    if len(navio) < 1:
                        time.sleep(1)
                        msg_id = randint(0,3)
                        print(dict_msgs_afunda[msg_id])
        else:
            self.animar_sup()
        
        self.tentativas_restantes -= 1
        return True

    @staticmethod                
    def animar_mira():
        print("\n\nPreparar...\n")
        time.sleep(0.3)
        print("Apontar...\n")
        time.sleep(0.3)
        print("E...\n")
        # suspense
        print("..../----\....")
        print(".../      \....")
        print("...\      /....")
        print("....|    |....")
        print("....|    |....")
        print("....|____|....")
        time.sleep(2)

    @staticmethod
    def animar_tiro():
        print("..../\/\/\....")
        print("...< POOW >...")
        print("....\/\/\/....")
        time.sleep(0.5)
        print("       O      ")
        time.sleep(0.5)
        print("       O      ")
        time.sleep(0.5)
        print("       O      ")
        time.sleep(0.5)
        print("       O      ")
        time.sleep(0.5)
        print("       O      ")
        time.sleep(2)
        print("      ...     \n")

    def animar_sup(self):
        print("ALTO LÁ!")
        time.sleep(0.5)
        print("Você avista uma caixa muito chamativa boiando...")
        time.sleep(0.5)
        print("Uma caixa de munição!!\nQue conveniente\n")
        time.sleep(0.4)
        print("Você recebe mais 3 tentativas")
        self.tentativas_restantes+=3
        print(f"Tentativas restantes: {self.tentativas_restantes}")
        

    # Popular aleatoriamente o tabuleiro criado com navios (Porta-Aviões, Cruzador, Destroyer) 
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
                self.navios_plotados.append([(x-2,y),(x-1,y),(x,y),(x+1,y),(x+2,y)])
                
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
                self.navios_plotados.append([(x,y-2),(x,y-1),(x,y),(x,y+1),(x,y+2)])

            navios_restantes-=1
            sentido = "horizontal" if randint(0,1) else "vertical"
    
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
                self.navios_plotados.append([(x-1,y),(x,y),(x+1,y)])
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
                self.navios_plotados.append([(x,y-1),(x,y),(x,y+1)])

            navios_restantes-=1
            sentido = "horizontal" if randint(0,1) else "vertical"

    def popular_destroyer(self):
        # Sentido aleatorio
        sentido = "horizontal" if randint(0,1) else "vertical"
        # plotar um ponto aleatorio que caiba o navio
        navios_restantes = 1
        tentativas = 10
        while navios_restantes>0 and tentativas>0:
            if sentido == "vertical":
                # vertical
                x = randint(1, self.ordem-2)
                y = randint(1, self.ordem)
                if len(set([self.tabuleiro_gabarito.iloc[x-1].at[y],\
                           self.tabuleiro_gabarito.iloc[x].at[y]])) > 1:
                           tentativas-=1
                           continue
                self.tabuleiro_gabarito.iloc[x-1].at[y],\
                           self.tabuleiro_gabarito.iloc[x].at[y] = '/dest\\','\\royer/'
                self.navios_plotados.append([(x-1,y),(x,y)])
            else:
                # horizontal
                x = randint(0, self.ordem-1)
                y = randint(2, self.ordem-1)
                if len(set([self.tabuleiro_gabarito.iloc[x].at[y-1],\
                           self.tabuleiro_gabarito.iloc[x].at[y]])) > 1:
                           tentativas-=1
                           continue
                self.tabuleiro_gabarito.iloc[x].at[y-1],\
                           self.tabuleiro_gabarito.iloc[x].at[y] = ' <dest','royer>'
                self.navios_plotados.append([(x,y-1),(x,y)])

            navios_restantes-=1
            sentido = "horizontal" if randint(0,1) else "vertical"
    
    def popular_submarino(self):
        # plotar um ponto aleatorio que caiba o navio
        navios_restantes = 3
        tentativas = 10
        while navios_restantes>0 and tentativas>0:
            x = randint(0, self.ordem-1)
            y = randint(1, self.ordem)
            if self.tabuleiro_gabarito.iloc[x].at[y] != '~^':
                tentativas-=1
                continue
            self.tabuleiro_gabarito.iloc[x].at[y] = '(({O}))'
            self.navios_plotados.append([(x,y)])

        navios_restantes-=1
        
    def popular_municao(self):

        nivel = {
            'facil': 5,
            'normal': 3
        }

        municao_restante = nivel.get(self.dificuldade, 0)
        while municao_restante>0:
            x = randint(0, self.ordem-1)
            y = randint(1, self.ordem)
            if self.tabuleiro_gabarito.iloc[x].at[y] != '~^':
                continue
            self.tabuleiro_gabarito.iloc[x].at[y] = '[SP]'



    # def popular_destroyer() 2 quadrados
    # def popular 

    def popular_navios(self):
        self.popular_porta_avioes()
        self.popular_cruzador()
 
