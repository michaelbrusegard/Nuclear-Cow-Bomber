import pygame

meny=True

white = (255,255,255)
black= (0,0,0)

lobbyvindu = pygame.display.set_mode((1000,707)) #dimensjonene til vinduet
pygame.display.set_caption("Soviet Run") #navn på vinduet
lobbyvindu.fill(black) # fyller hele vinduet med sort


"""
def Level1():
    lobbyvindu.fill((0,0,0))
    pygame.display.flip()
    import firstLevel

def Level2():
    lobbyvindu.fill((0,0,0))
    pygame.display.flip()
    import secondlevel

def Musikk():
    lobbyvindu.fill((0,0,0))
    pygame.display.flip()
    #En variabel som styrer lyd er lik false
"""
pygame.init() #starter pygame
pygame.font.init() #starter pygame.font

while meny:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Hvis du hendelsen er helt lik at du klikker på krysset 
            pygame.QUIT # Stopper pygame
            pygame.display.update() #Oppdaterer vinduet over at pygame har stoppet

    font = pygame.font.Font(pygame.font.get_default_font(), 40) # font med fonttype og størrelse
    font2 = pygame.font.Font(pygame.font.get_default_font(), 28) #font med samme fonttype og mindre størrelse
    
    stlv1 = font.render("Starter level 1!", False, (0,0,0)) #definerer variablen med tekst, "bold" eller ikke og farge, nå klar til å legges på skjermen
    
    stlv2 = font.render("Starter level 2!", False, (0,0,0)) #Samme som stlv1
    
    stlv3 = font.render("Starter Level 3!", False, (0,0,0)) #Samme som stlv1

    level1 = font.render("Level 1", False, (255,255,255))

    lobbyvindu.blit(level1,(350, 300)) #Setter funksjonen level 1 på vinduet

    level2 = font.render("Level 2", False, (255,255,255)) #Definerer tekst, om det skal være "bold" eller ikke og farge

    lobbyvindu.blit(level2,(550,300)) #Setter funksjonen level 2 på vinduet
    
    MP = font2.render(" Musikk:På", False, (255,255,255))
    
    MA= font2.render("Musikk:Av", False, (255,255,255))

    lobbyvindu.blit(MP,(430,400)) #Setter funksjonen MP på vinduet
       
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN: #Hvis den trykker ned musknapp og element 0 i listen pygame.get_pos er større eller lik og element 1 er større eller lik. 
            if pygame.mouse.get_pos()[0] >= 300 and pygame.mouse.get_pos()[1] >= 250: 
                if pygame.mouse.get_pos()[0] <= 400 and pygame.mouse.get_pos()[1] <= 350: #Skjekker om de er mindre enn noen variabler
                    lobbyvindu.fill(white) #Hvis begge If testene er sant så skal skjermen bli hvit og tekst stlv1 skal dukke opp og starte funksjonen Level1().
                    pygame.display.flip()
                    pygame.display.update()
                    lobbyvindu.blit(stlv1,(400,450))
                    #level1()
    

        if event.type == pygame.MOUSEBUTTONDOWN:  
            if pygame.mouse.get_pos()[0] >= 500 and pygame.mouse.get_pos()[1] >= 250:  #Hvis den trykker ned musknapp og element 0 i listen pygame.get_pos er større eller lik og element 1 er større eller lik. 
                if pygame.mouse.get_pos()[0] <= 600 and pygame.mouse.get_pos()[1] <= 350:#Skjekker om de er mindre enn noen variabler
                    lobbyvindu.fill(white)  #Hvis begge If testene er sant så skal skjermen bli hvit og tekst stlv2 skal dukke opp og starte funksjonen Level2().
                    pygame.display.update()
                    lobbyvindu.blit(stlv2,(400,450))
                    #level2()
               
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pos()[0] >= 400 and pygame.mouse.get_pos()[1] >= 350: #Hvis den trykker ned musknapp og element 0 i listen pygame.get_pos er større eller lik og element 1 er større eller lik. 
                if pygame.mouse.get_pos()[0] <= 460 and pygame.mouse.get_pos()[1] <= 450:#Skjekker om de er mindre enn noen variabler
                    musikk = False #Hvis begge If testene er sant så skal funksjon være False.

