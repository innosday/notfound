import pygame,sys,random

class Boxs:
    def __init__(self,screen:pygame.Surface,size=100):
        self.__screen = screen
        screen_width,screen_height = screen.get_size()
        self.__Boxs = []
        self.__botPos = {"start":None,"end":None}
        for low in range(0,screen_height,size):
            lowList = []
            for high in range(0,screen_width,size):
                lowList.append({"rect":pygame.Rect(high,low,size,size),"center":(high+size//2,low+size//2),"class":None,"perant":None,"g":None,"h":None})
            self.__Boxs.append(lowList)
    @property
    def Boxs(self) -> list[list[dict]]:
        return self.__Boxs
    
    @property
    def botPos(self) -> dict:
        return self.__botPos
    
    def getBoxCenter(self,pos:tuple[int,int]) -> tuple:
        return self.__Boxs[pos[0]][pos[1]]["center"]
    def setBoxClass(self,pos:tuple[int,int],object = None):
        """start,end,wall"""
        self.__Boxs[pos[0]][pos[1]]["class"] = object
        if object in ["start","end"]:
            self.__botPos[object] = pos
    def getBoxClass(self,pos:tuple[int,int]):
        return self.__Boxs[pos[0]][pos[1]]['class']

    def update(self):
        for box in self.__Boxs:
            for inbox in box:
                if inbox["class"] == "wall":
                    pygame.draw.rect(self.__screen,(10,10,10),inbox["rect"])
                elif inbox["class"] == "start":
                    pygame.draw.rect(self.__screen,(255,0,0),inbox["rect"])
                elif inbox["class"] == "end":
                    pygame.draw.rect(self.__screen,(0,255,0),inbox["rect"])
                else:
                    pygame.draw.rect(self.__screen,(10,10,10),inbox["rect"],1)
                pygame.draw.circle(self.__screen,(0,0,255),inbox["center"],4)

class Bot:
    def __init__(self,screen:pygame.Surface,grid:Boxs):
        print("영우 배달 시작!")
        self.__screen = screen
        self.__Pos = grid.getBoxCenter(grid.botPos["start"])
    
    def update(self):
        pass

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 700))
        pygame.display.set_caption("영우 배달 게임")
        self.grid=Boxs(self.screen)
        
        for _ in range(7):
            randomPos = (random.randrange(0,self.screen.get_height()//100-1),random.randrange(0,self.screen.get_width()//100-1))
            self.grid.setBoxClass(randomPos,"wall")
        self.grid.setBoxClass((6,0),"start")
        self.grid.setBoxClass((0,4),"end")

        self.bot = Bot(self.screen,self.grid)

    def EventManager(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def updates(self):
        self.screen.fill((255, 255, 255))
        self.grid.update()
        self.bot.update()
        pygame.display.update()

    def main(self):
        while True:
            self.EventManager()
            self.updates()

if __name__ == "__main__":
    Game().main()