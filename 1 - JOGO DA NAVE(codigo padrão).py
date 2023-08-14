import pygame
import os
from random import randint

#iniciando e colocando variaveis da tela
pygame.init()      
TELA_LARGURA = 1280
TELA_ALTURA = 720


#ADICIONANDO BARULHO DE FUNDO E COLISÃO
'''pygame.mixer.music.load('IMG NAVE ESPEC/BoxCat Games - Victory.mp3')
pygame.mixer.music.play(-1)'''
#colisao_barulho = pygame.mixer.Sound('IMG NAVE ESPEC/smw_thud.wav')


# 1 - colocando o tamanho da tela de jogo
# 2 - nome na tela de jogo
screen = pygame.display.set_mode((TELA_LARGURA,TELA_ALTURA))                
pygame.display.set_caption('ESPAÇO DESTRUIDOR')                              


# 1 - colocando a imagem de fundo
# 2 - adequando a imagem na tela
paisagem = pygame.image.load('IMG NAVE ESPEC/cidade.jpg').convert_alpha()    
paisagem = pygame.transform.scale(paisagem,(TELA_LARGURA,TELA_ALTURA)) 


#adicionando a imagem do alien
alienDestruir = pygame.image.load('IMG NAVE ESPEC/spaceship.png')
alienDestruir = pygame.transform.scale(alienDestruir, (50, 50))


# posição iniciail  do alien
posição_inicial_alien_x = 500                                      
posição_inicial_alien_y = 360


# 1 - adicionando a nave
# 2 - adequando ela a tela
# 3 - girando ela em 90 graus 
nave = pygame.image.load('IMG NAVE ESPEC/space.png')                
nave = pygame.transform.scale(nave, (50,50))
nave = pygame.transform.rotate(nave, -90) 


#posição inicial da nave
posição_inicial_nave_x = 200
posição_inicial_nave_y = 300


# 1 - adicionando o missil
# 2 - adequando ele a tela
# 3 - girando ele em 45 graus 
missil_nave = pygame.image.load('IMG NAVE ESPEC/missile.png').convert_alpha()    
missil_nave = pygame.transform.scale(missil_nave, (25,25))
missil_nave = pygame.transform.rotate(missil_nave, -45)


#POSIÇÃO E VELOCIDADE DO MISSIL
velocidade_missil = 0           
posição_missilX = 200
posição_missilY = 300
#condição falsa pra o missil só atirar quando for True
atirar = False


#função pra quando o alien ultrapassar a tela
def reaparecer():                           
    x = 1350
    y = randint(1, 640)
    return[x, y]


# função para a nave atirar mais de uma vez
def tiros_missil():                       
    atirar = False
    tiros_missil_x = posição_inicial_nave_x
    tiros_missil_y = posição_inicial_nave_y
    velocidade_missil = 0
    return[tiros_missil_x, tiros_missil_y, atirar, velocidade_missil]


#criando a função de colisão
pontos = 3
def colisão():
    global pontos
    if nave_retangulo.colliderect(alien_retangulo) or alien_retangulo.x == 60: #condição se a nave tocou no alien ou se passou da nave
        pontos = pontos - 1
        return True
    elif missil_retangulo.colliderect(alien_retangulo):
        pontos = pontos + 1
        return True
    else:
        return False


#transformando imagens em reatangulos para a colisão
nave_retangulo = nave.get_rect()
alien_retangulo = alienDestruir.get_rect()
missil_retangulo = missil_nave.get_rect()


#adicionar texto
fonte = pygame.font.SysFont('arial', 50)


#abrindo a tela de jogo e a opção sair
rodando = True              
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    
    #adicionando o fundo ao jogo
    screen.blit(paisagem,(0,0))


    #MOVENDO A TELA DE FUNDO
    largura_relativa = TELA_LARGURA % paisagem.get_rect().width              
    screen.blit(paisagem, (largura_relativa - paisagem.get_rect().width, 0)) 
    if largura_relativa < 1280:
        screen.blit(paisagem, (largura_relativa, 0))

    #manuseio do fundo(rápido ou devagar)
    TELA_LARGURA = TELA_LARGURA - 2     


    #adicionando a função LIMITE, e criando o looping pra quando passar da tela voltar novamente
    if posição_inicial_alien_x == -50:           
        posição_inicial_alien_x = reaparecer()[0]
        posição_inicial_alien_y = reaparecer()[1]

    #movimentando o alien(mais rápido ou mais devagar)
    posição_inicial_alien_x -= 1.5


    #adicionando teclas pra mover a nave
    movendo_nave = pygame.key.get_pressed()                          
    if movendo_nave[pygame.K_UP] and posição_inicial_nave_y > 1:
        posição_inicial_nave_y -= 3
        #aqui coloca a posição do missil junto com a posição da nave para o missil não ficar bugado
        if not atirar:                         
            posição_missilY -= 3
    if movendo_nave[pygame.K_DOWN] and posição_inicial_nave_y < 665:
        posição_inicial_nave_y += 3
        #aqui faz a mesma coisa de colocar o missil na posição da nave
        if not atirar:
            posição_missilY += 3

    
    # adicionando a tecla pra atirar o missil
    if movendo_nave[pygame.K_SPACE]:         
        atirar = True
        velocidade_missil = 4

    #trazendo a função tiros_missil e colocando no while pra atirar varias vezes 
    if posição_missilX == 1300:            
        posição_missilX, posição_missilY, atirar, velocidade_missil = tiros_missil()

    posição_missilX += velocidade_missil


    #adicionando os objetos ao looping/jogo
    pygame.draw.rect(screen, (0, 12, 105), nave_retangulo, 1)
    pygame.draw.rect(screen, (0, 12, 105), alien_retangulo, 1)
    pygame.draw.rect(screen, (0, 12, 105), missil_retangulo, 1)


    #alinhando os retangulos as respectivas imagens
    nave_retangulo.x = posição_inicial_nave_x
    nave_retangulo.y = posição_inicial_nave_y

    alien_retangulo.x = posição_inicial_alien_x
    alien_retangulo.y = posição_inicial_alien_y

    missil_retangulo.x = posição_missilX
    missil_retangulo.y = posição_missilY 


    #trazendo a função colisão e fazendo o alien sumir ao ocorrer a colisão
    if posição_inicial_alien_x == -50 or colisão():
        posição_inicial_alien_x = reaparecer()[0]
        posição_inicial_alien_y = reaparecer()[1]
       # colisao_barulho.play()


    #adicionando pontos no jogo
    mensagem = f'Pontos: {int(pontos)}'                 
    texto_formatado = fonte.render(mensagem, True, (255,255,255)) 
    screen.blit(texto_formatado, (50, 50))

    #condição de perder o jogo
    if pontos < 0:
        rodando = False


    #adicionando as imagens no jogo
    screen.blit(alienDestruir, (posição_inicial_alien_x, posição_inicial_alien_y))    
    screen.blit(missil_nave, (posição_missilX, posição_missilY))
    screen.blit(nave, (posição_inicial_nave_x, posição_inicial_nave_y))


    pygame.display.update()