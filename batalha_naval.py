from random import randint
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

    def __str__(self):
        return  "\n"*80+\
                "\n========================================="+\
               "\n                TABULEIRO                \n"+\
                "=========================================\n"+\
                str(self.tabuleiro)+\
                "\n=========================================\n"

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
            print(self)
            print("Coordenada deve conter 1 letra e um numero\n")
            inp = input("Digite uma coordenada: ")
            return self.converter_coordenadas(inp)
        
        letra = coordenada[0:1]
        numero = coordenada[1:]

        if letra.isnumeric() or not numero.isnumeric():
            print(self)
            print("Coordenada inválida: Primeiro letra, em segundo número\n")
            inp = input("Digite uma coordenada: ")
            return self.converter_coordenadas(inp)
        
        if letra.lower() not in "abcdefghij" or int(numero) not in range(1,11):
            print(self)
            print("Coordenada inválida, range excedido\n")
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
        
        if self.tabuleiro.iloc[y].at[x] in ['ag', 'NV', '[SP]']:
            print(self)
            print("Escolha outra coordenada, ponto já revelado!!\n")
            time.sleep(5)
            return False

        self.animar_mira()

        if self.tabuleiro_gabarito.iloc[y].at[x] == '~^':
            self.animar_tiro()
            self.tabuleiro.iloc[y].at[x] = 'ag'
            msg_id = randint(0,2)
            print("X"*(len(dict_msgs_erro[msg_id])-2)+dict_msgs_erro[msg_id]+"X"*(len(dict_msgs_erro[msg_id])-2))
            self.tentativas_restantes -= 1

        elif self.tabuleiro_gabarito.iloc[y].at[x] != '[SP]':
            self.animar_tiro()
            self.tabuleiro.iloc[y].at[x] = 'NV'
            msg_id = randint(0,2)
            print("*"*(len(dict_msgs_acerto[msg_id])-2)+dict_msgs_acerto[msg_id]+"*"*(len(dict_msgs_acerto[msg_id])-2))
            print("+ 1 PONTO")
            self.pontos+=1
            for navio in self.navios_plotados:
                if (y,x) in navio:
                    navio.remove((y,x))
                    if len(navio) < 1:
                        self.pontos+=3
                        time.sleep(1)
                        msg_id = randint(0,3)
                        print("*"*(len(dict_msgs_afunda[msg_id])-2)+dict_msgs_afunda[msg_id]+"*"*(len(dict_msgs_afunda[msg_id])-2))
                        print(f'Voce AFUNDOU UM NAVIO. Navios restantes: {self.calcula_navios_restantes()}')
                        print("+ 3 PONTOS")

        else:
            self.tabuleiro.iloc[y].at[x] = '[SP]'
            self.animar_sup()
        time.sleep(4)
        return True

    @staticmethod                
    def animar_mira():
        print("\n\nPreparar...")
        time.sleep(0.5)
        print("Apontar...")
        time.sleep(0.5)
        print("E...\n")
        # suspense
        print(" "*10+"      ..      ")
        print(" "*10+"     ....     ")
        print(" "*10+"  ..........  ")
        print(" "*10+"..............")
        print(" "*10+"..............")
        print(" "*10+"..../----\....")
        print(" "*10+".../      \...")
        print(" "*10+"...\      /...")
        print(" "*10+"....|    |....")
        print(" "*10+"....|    |....")
        print(" "*10+"....|____|....")
        print(" "*10+"  ..........  ")

        time.sleep(3)

    @staticmethod
    def animar_tiro():
        print(" "*10+"  ../\/\/\..  ")
        print(" "*10+"   < POOW >   ")
        print(" "*10+"    \/\/\/    ")
        time.sleep(0.5)
        print(" "*10+"       O      ")
        time.sleep(0.3)
        print(" "*10+"       O      ")
        time.sleep(0.3)
        print(" "*10+"       O      ")
        time.sleep(0.3)
        print(" "*10+"       O      ")
        time.sleep(0.3)
        print(" "*10+"       O      ")
        time.sleep(0.3)
        print(" "*10+"       O      ")
        time.sleep(0.3)
        print(" "*10+"       O      ")
        time.sleep(0.3)
        print(" "*10+"       O      ")
        time.sleep(0.3)
        print(" "*10+"       O      ")
        print(" "*10+"      ...     \n\n")
        time.sleep(2)
        

    def animar_sup(self):
        dict_msg_mun = {
            0: "\nIsso é munição!!! Que conveniente\n",
            1: "\nUma caixa de munição no meio do oceano? Suspeito... Mas e daí, ela é sua agora!\n",
            2: "\nHoje é seu dia de sorte! Uma caixa de munição toda para você!\n"
        }
        print(" "*10+"    ......    ")
        print(" "*10+">>>ALTO LÁ!<<<\n")
        time.sleep(1)
        print("Você avista uma caixa muito chamativa boiando...\n")
        time.sleep(2)
        msg_id = randint(0,2)
        print("*"*(len(dict_msg_mun[msg_id])-2)+dict_msg_mun[msg_id]+"*"*(len(dict_msg_mun[msg_id])-2))
        print(" "*10+".......................")
        print(" "*10+".....============......")
        print(" "*10+"....||          ||.....")
        print(" "*10+"....||  MUNIÇÃO ||.....")
        print(" "*10+"....||          ||.....")
        print(" "*10+".....============......")
        print(" "*10+".......................\n")


        time.sleep(1)
        print("Você recebe mais 3 tentativas!!")
        self.tentativas_restantes+=3

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
        navios_restantes = 5
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
        navios_restantes = 2
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
        navios_restantes = 5
        tentativas = 10
        while navios_restantes>0 and tentativas>0:
            x = randint(0, self.ordem-1)
            y = randint(1, self.ordem)
            if self.tabuleiro_gabarito.iloc[x].at[y] != '~^':
                tentativas-=1
                continue
            self.tabuleiro_gabarito.iloc[x].at[y] = '({O})'
            self.navios_plotados.append([(x,y)])
            navios_restantes-=1

    def popular_municao(self):

        nivel = {
            'facil': 8,
            'normal': 4
        }

        municao_restante = nivel.get(self.dificuldade, 0)
        while municao_restante>0:
            x = randint(0, self.ordem-1)
            y = randint(1, self.ordem)
            if self.tabuleiro_gabarito.iloc[x].at[y] != '~^':
                continue
            self.tabuleiro_gabarito.iloc[x].at[y] = '[SP]'
            municao_restante-=1



    # def popular_destroyer() 2 quadrados
    # def popular 

    def popular_navios(self):
        self.popular_porta_avioes()
        self.popular_cruzador()
        self.popular_destroyer()
        self.popular_submarino()
        self.popular_municao()
 
