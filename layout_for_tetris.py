import pygame

pygame.init()

logo = pygame.image.load("tetris_logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Tetris Gosi")
screen = pygame.display.set_mode(size=(600, 600))

pygame.draw.rect(screen, (255, 255, 255), (30, 30, 360, 540), 5)
pygame.draw.rect(screen, (255, 255, 255), (420, 450, 150, 120), 5)
pygame.draw.rect(screen, (255, 255, 255), (420, 30, 150, 210), 5)


score_font = pygame.font.SysFont('Arial', 30)
score_text = score_font.render('Your score:', True, (255, 255, 255))
screen.blit(score_text, (430, 460))

score_font2 = pygame.font.SysFont('Arial', 40)
score_text2 = score_font2.render('123456', True, (255, 255, 255))
screen.blit(score_text2, (430, 505))

next_block_text = score_font.render('Next block:', True, (255, 255, 255))
screen.blit(next_block_text, (435, 40))

pygame.display.update()

def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == "__main__":
    main()
