import pygame
from config import Largura, Altura, FPS, tela, clock, font_alagard, SPRITE_Largura, SPRITE_Altura
from assets import mapas, player_spritesheet2, player_spritesheet3
from player import Player, atualizar_sprites
from collisions import colisoes_segundo_mapa, colisoes_mapa_torre, colisoes_primeiro_mapa

class Game:
    def __init__(self): # inicializa o jogo
        self.tela = tela
        pygame.display.set_caption("A Ordem dos Discretos") # nome do jogo
        self.clock = clock
        self.running = True
        self.mapa_atual = "primeiro mapa"
        self.player = Player(30, Altura // 2)

        # carrega os sprites dos coletaveis
        self.coletavel_img2 = pygame.transform.scale(pygame.image.load("bau_fechado.png"), (46, 36))
        self.coletavel_img3 = pygame.transform.scale(pygame.image.load("bau_aberto.png"), (46, 36))
        self.coletavel_img4 = pygame.transform.scale(pygame.image.load("Caveira_Com_Manto.png"), (100, 100))
        self.coletavel_img5 = pygame.transform.scale(pygame.image.load("Caveira_Sem_Manto.png"), (100, 100))

        # Coletáveis por mapa
        self.coletaveis = {
            "primeiro mapa": [],
            "segundo mapa": [
                {"pos": (200, 180), "coletado": False},
                {"pos": (750, 470), "coletado": False}
            ],
            "torre": []
        }

        # variaveis para a mensagem
        self.mensagem_tempo = 0
        self.mensagem_texto = ""

    # define a mensagem que sera mostrada na tela
    def mostrar_mensagem(self, texto, duracao):
        self.mensagem_texto = texto
        self.mensagem_tempo = duracao

    # desenha a mensagem na tela
    def desenhar_mensagem(self):
        if self.mensagem_tempo > 0:
            # Aumenta o tamanho da caixa para caber mensagens mais longas
            caixa_largura, caixa_altura = Largura // 1.5, Altura // 5  # Aumentei a largura
            caixa_x, caixa_y = (Largura - caixa_largura) // 2, Altura // 3  # Centraliza horizontalmente
            
            # Desenha uma caixa com borda arredondada e sombra
            # Sombra (mais escura)
            pygame.draw.rect(self.tela, (20, 20, 20), (caixa_x + 5, caixa_y + 5, caixa_largura, caixa_altura), border_radius=15)
            # Caixa principal com gradiente mais escuro
            surface_caixa = pygame.Surface((caixa_largura, caixa_altura), pygame.SRCALPHA)
            pygame.draw.rect(surface_caixa, (60, 60, 60, 230), (0, 0, caixa_largura, caixa_altura), border_radius=15)  # Fundo mais escuro
            # Borda dourada
            pygame.draw.rect(surface_caixa, (200, 180, 100), (0, 0, caixa_largura, caixa_altura), 3, border_radius=15)
            self.tela.blit(surface_caixa, (caixa_x, caixa_y))
            
            # Renderiza o texto com sombra
            texto_surface_sombra = font_alagard.render(self.mensagem_texto, True, (40, 40, 40))  # Sombra mais escura
            texto_surface = font_alagard.render(self.mensagem_texto, True, (255, 215, 0))  # Texto dourado
            texto_rect = texto_surface.get_rect(center=(caixa_x + caixa_largura // 2, caixa_y + caixa_altura // 2))
            self.tela.blit(texto_surface_sombra, (texto_rect.x + 2, texto_rect.y + 2))
            self.tela.blit(texto_surface, texto_rect)
            
            self.mensagem_tempo -= 1


    # def para a mensagem da tela inicial
    def tela_inicial(self):
        inicio_tempo = pygame.time.get_ticks()
        while pygame.time.get_ticks() - inicio_tempo < 3000: # 3 segundos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
            self.tela.fill((0, 0, 0)) # tela preta
            texto_surface = font_alagard.render("Bem-vindo a A Ordem dos Discretos!", True, (255, 255, 255))
            texto_rect = texto_surface.get_rect(center=(Largura // 2, Altura // 2))
            self.tela.blit(texto_surface, texto_rect) 
            pygame.display.update() # atualiza a tela
        return True

    # loop principal do jogo
    def game_loop(self):
        if not self.tela_inicial():
            return

        while self.running:
            self.clock.tick(FPS)
            self.tela.blit(mapas[self.mapa_atual], (0, 0))
            keys = pygame.key.get_pressed()
            
            # Define as colisões do mapa atual
            if self.mapa_atual == "segundo mapa":
                colisoes = colisoes_segundo_mapa
            if self.mapa_atual == "torre":
                colisoes = colisoes_mapa_torre
            if self.mapa_atual == "primeiro mapa":
                colisoes = colisoes_primeiro_mapa
            
        
            self.player.move(keys, colisoes)
            self.player.draw(self.tela)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Verifica colisão com coletáveis
            jogador_rect = pygame.Rect(self.player.x, self.player.y, SPRITE_Largura, SPRITE_Altura)
            for index, coletavel in enumerate(self.coletaveis[self.mapa_atual]):
                
                if not coletavel["coletado"]:
                    coletavel_rect_bau = self.coletavel_img2.get_rect(topleft=coletavel["pos"])
                    coletavel_rect_esq = self.coletavel_img4.get_rect(topleft=coletavel["pos"])
                    
                    if coletavel == self.coletaveis[self.mapa_atual][1]:
                        if jogador_rect.colliderect(coletavel_rect_bau) and self.coletaveis["segundo mapa"][0]["coletado"]:
                            coletavel["coletado"] = True
                            self.mostrar_mensagem("Cajado da Vacuidade coletado!", 120)
                            
                            # Troca o spritesheet do jogador com base no coletável
                            if index == 0: # Coletável [0]
                                atualizar_sprites(self.player, player_spritesheet2)
                            elif index == 1: # Coletável [1]
                                atualizar_sprites(self.player, player_spritesheet3)
                    else:
                        if jogador_rect.colliderect(coletavel_rect_esq):
                            coletavel["coletado"] = True
                            self.mostrar_mensagem("Manto da Sabedoria coletado!", 120)
                            
                            # Troca o spritesheet do jogador com base no coletável
                            if index == 0: # Coletável [0]
                                atualizar_sprites(self.player, player_spritesheet2)
                            elif index == 1: # Coletável [1]
                                atualizar_sprites(self.player, player_spritesheet3)

            # Desenha coletáveis não coletados
            for coletavel in self.coletaveis[self.mapa_atual]:
                if coletavel == self.coletaveis[self.mapa_atual][1]:
                    if not coletavel["coletado"]:
                        self.tela.blit(self.coletavel_img2, coletavel["pos"])
                    if coletavel["coletado"]:
                        self.tela.blit(self.coletavel_img3, coletavel["pos"])
                else:
                    if not coletavel["coletado"]:
                        self.tela.blit(self.coletavel_img4, coletavel["pos"])
                    if coletavel["coletado"]:
                        self.tela.blit(self.coletavel_img5, coletavel["pos"])

            # Transição dos mapas
            if self.mapa_atual == "primeiro mapa" and self.player.x >= 970: # transicao do primeiro para o segundo mapa
                self.mapa_atual = "segundo mapa"
                self.player.y = Altura // 2 + 35
                self.player.x = 15
                
            if self.mapa_atual == "segundo mapa": # transicoes do segundo mapa: volta para o primeiro mapa ou segue para a torre
                if self.player.x <= 5: # transicao para o primeiro mapa
                    self.mapa_atual = "primeiro mapa"
                    self.player.y = Altura // 2 - 20
                    self.player.x = 950
                elif 420 < self.player.x < 460 and self.player.y <= 225: # transicao para a torre
                    self.mapa_atual = "torre"
                    self.player.x = Largura // 2 - 30
                    self.player.y = 780
                    
            if self.mapa_atual == "torre":
                # Voltar para o segundo mapa ao descer pela porta
                if 415 < self.player.x < 600 and self.player.y >= 790:  # Ajustado para y >= 780 e x alinhado com a abertura
                    self.mapa_atual = "segundo mapa"
                    self.player.x = 440  # Centraliza na entrada da torre no segundo mapa
                    self.player.y = 225  # Posiciona logo abaixo da entrada da torre

            # Desenha a mensagem se houver
            self.desenhar_mensagem()
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.game_loop()