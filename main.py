import pygame,sys,random

class Boxs:
    def __init__(self,screen:pygame.Surface,size=100):
        self.__screen = screen
        screen_width,screen_height = screen.get_size()
        self.__Boxs = []
        self.__botPos = {"start":None,"end":None}
        self.__size = size
        for low in range(0,screen_height,size):
            lowList = []
            for high in range(0,screen_width,size):
                lowList.append({"rect":pygame.Rect(high,low,size,size),"center":(high+size//2,low+size//2),"class":None,"perant":None,"g":0,"h":0,"f":0})
            self.__Boxs.append(lowList)
    @property
    def Boxs(self) -> list[list[dict]]:
        return self.__Boxs
    
    @property
    def botPos(self) -> dict:
        return self.__botPos
    
    @property
    def size(self) -> int:
        return self.__size
   
    def getBoxCenter(self,pos:tuple[int,int]) -> tuple[int,int]:
        """return center"""
        return self.__Boxs[pos[0]][pos[1]]["center"]
    def setBoxClass(self,pos:tuple[int,int],object = None):
        """start,end,wall"""
        self.__Boxs[pos[0]][pos[1]]["class"] = object
        if object in ["start","end"]:
            self.__botPos[object] = pos
    def getBoxClass(self,pos:tuple[int,int]):
        return self.__Boxs[pos[0]][pos[1]]['class']
    def getBoxINFO(self,pos:tuple[int,int],info=None):
        """g,h,f"""
        return self.__Boxs[pos[0]][pos[1]][info]
    def setBoxINFO(self,pos:tuple[int,int],info=None,value=None):
        """g,h,f"""
        self.__Boxs[pos[0]][pos[1]][info] = value
    def getBoxRect(self,pos:tuple[int,int]) -> pygame.Rect:
        """return rect"""
        return self.__Boxs[pos[0]][pos[1]]['rect']

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
        self.__grid = grid
        self.__bottomLeft = (screen.get_height()//grid.size-1,0)
        self.__topRight = (0,screen.get_width()//grid.size-1)
        print(self.__bottomLeft,self.__topRight)

        self.__start_pos:tuple[int,int] = grid.botPos["start"]
        self.__end_pos:tuple[int,int] = grid.botPos["end"]
        self.Open = [self.__start_pos]
        self.__cur = None
        self.Close = []
    
    def update(self):
        # print(self.Open,self.Close)
        self.__cur = self.Open[0]
        for i in range(len(self.Open)):
            if self.__grid.getBoxINFO(self.Open[i],"f") <= self.__grid.getBoxINFO(self.__cur,"f") and self.__grid.getBoxINFO(self.Open[i],"h") < self.__grid.getBoxINFO(self.__cur,"h"):
                self.__cur = self.Open[i]
        self.Open.remove(self.__cur)
        self.Close.append(self.__cur)

        if self.__cur == self.__end_pos:
            print ("영우 배달 완료!")
            return
        
        print(self.__cur,"---")
        cur_y ,cur_x= self.__cur
        self.OpenListadd(cur_x,cur_y-1)
        self.OpenListadd(cur_x+1,cur_y)
        self.OpenListadd(cur_x,cur_y+1)
        self.OpenListadd(cur_x-1,cur_y)
        
    def OpenListadd(self,checkX,checkY):
        print("함수 실행",checkY,checkX,self.__bottomLeft,self.__topRight,end=" ")
        if checkX >= self.__bottomLeft[1] and checkX < self.__topRight[1] and checkY <= self.__bottomLeft[0] and checkY >= self.__topRight[0] and not self.__grid.getBoxClass((checkY,checkX)) == "wall":
            # NeighborNode = (checkY-self.__bottomLeft[0],checkX-self.__bottomLeft[1])
            NeighborNode = (checkY,checkX)
            print("이웃노드 활성화",NeighborNode,end=" ")
            moveCost =self.__grid.getBoxINFO(self.__cur,'g') + (10 if self.__grid.getBoxRect(self.__cur).x - checkX==0 or self.__grid.getBoxRect(self.__cur).y - checkY==0 else 14)
            if moveCost < self.__grid.getBoxINFO(NeighborNode,'g') or self.Open not in NeighborNode:
                self.__grid.setBoxINFO(NeighborNode,'g',moveCost)
                self.__grid.setBoxINFO(NeighborNode,'h',(abs(NeighborNode[1] - self.__end_pos[1]) + abs(NeighborNode[0] - self.__end_pos[0])) * 10)
                self.__grid.setBoxINFO(NeighborNode,'perant',self.__cur)
                self.__grid.setBoxINFO(NeighborNode,'f',(self.__grid.getBoxINFO(NeighborNode,'g')+self.__grid.getBoxINFO(NeighborNode,'h')))
                self.Open.append(NeighborNode)
        print()
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 700))
        pygame.display.set_caption("영우 배달 게임")
        self.grid=Boxs(self.screen)
        
        # for _ in range(7):
        #     randomPos = (random.randrange(0,self.screen.get_height()//100-1),random.randrange(0,self.screen.get_width()//100-1))
        #     self.grid.setBoxClass(randomPos,"wall")
        set_wall = [(5,0),(4,0),(4,1),(4,3),(3,1),(3,3),(2,1),(1,2),(0,3),(6,2),(6,3)]
        for wall in set_wall:
            self.grid.setBoxClass(wall,"wall")
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