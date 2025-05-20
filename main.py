import pygame,sys

class Boxs:
    def __init__(self,screen:pygame.Surface):
        self.__screen = screen
        screen_width,screen_height = screen.get_size()
        self.__Boxs = []
        for low in range(0,screen_height,100):
            lowList = []
            for high in range(0,screen_width,100):
                lowList.append({"rect":pygame.Rect(high,low,100,100),"center":(high+50,low+50)})
            self.__Boxs.append(lowList)
    @property
    def Boxs(self) -> list[list[dict]]:
        return self.__Boxs

    def update(self):
        for box in self.__Boxs:
            for inbox in box:
                pygame.draw.rect(self.__screen,(255,0,0),inbox["rect"],1)
                pygame.draw.circle(self.__screen,(0,255,0),inbox["center"],4)
class Game:
    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((500, 700))
        self.__grid=Boxs(self.__screen)

    def EventManager(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def updates(self):
        self.__screen.fill((255, 255, 255))
        self.__grid.update()

        pygame.display.update()

    def main(self):
        while True:
            self.EventManager()
            self.updates()

if __name__ == "__main__":
    Game().main()