import random,pygame

class Node:
    def __init__(self,pos:tuple[int,int],scale):
        self.__y,self.__x = pos
        self.__g = 0
        self.__h = 0
        self.__perant = None
        self.__box_class = None
        self.GUIPos = (self.__x * scale, self.__y * scale)
        self.GUICenter = (self.GUIPos[0] + scale // 2, self.GUIPos[1] + scale // 2)

    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y
    @property
    def f(self):
        return self.__g + self.__h
    @property
    def g(self):
        return self.__g
    @property
    def h(self):
        return self.__h
    @property
    def perant(self):
        return self.__perant
    @property
    def box_class(self):
        return self.__box_class
    
    @g.setter
    def g(self,g:int):
        self.__g = g
    @h.setter
    def h(self,h:int):
        self.__h = h
    @perant.setter
    def perant(self,perant:tuple[int,int]):
        self.__perant = perant
    @box_class.setter
    def box_class(self,Class:str):
        self.__box_class = Class

class GridBox:
    def __init__(self,size:tuple[int,int],scale:int):
        self.__grid = [[Node((i,j),scale) for j in range(size[1])] for i in range(size[0])]
        self.__bottomLeft = {"y":size[0]-1,"x":0}
        self.__topRight = {"y":0,"x":size[1]-1}

    @property
    def BottomLeft(self) -> tuple[int,int]:
        return self.__bottomLeft
    
    @property
    def TopRight(self) -> tuple[int,int]:
        return self.__topRight
    
    def getAllGrid(self) -> list[list[Node]]:
        return self.__grid
      
    def getGrid(self,pos) -> Node:
        return self.__grid[pos[0]][pos[1]]
    
    def showGrid(self,detail=False):
        for i in self.__grid:
            for j in i:
                if not detail:
                    print("%5s"%j.box_class,end=" ")
                else:
                    print(f"({j.y},{j.x}) g:{j.g} h:{j.h} f:{j.f} perant:{j.perant} class:{j.box_class}",end=" | ")
            print()
        print("-" * 20)

    def setBoxClass(self,pos:tuple[int,int],Class:str):
        self.__grid[pos[0]][pos[1]].box_class = Class

    @property
    def getStartPos(self) -> tuple[int,int]:
        for i in self.__grid:
            for j in i:
                if j.box_class == "start":
                    return (j.y,j.x)
    @property
    def getEndPos(self) -> tuple[int,int]:
        for i in self.__grid:
            for j in i:
                if j.box_class == "end":
                    return (j.y,j.x)

class AStar:
    def __init__(self,size:tuple[int,int],end:tuple[int,int],start:tuple[int,int],scale:int,diagonal=False):
        self.grid = GridBox(size,scale)
        self.size = sorted(size,reverse=True)
        self.grid.setBoxClass(start,"start")
        self.grid.setBoxClass(end,"end")

        self.diagonal = diagonal
        self.openlist = [self.grid.getStartPos]
        self.closelist = []
        self.finallist = []
        self.cur = self.openlist[0]
    
    def getGrid(self):
        return self.grid.getAllGrid()


    def setWall(self,pos:tuple[int,int]):
        self.grid.setBoxClass(pos,"wall")
        
    def OpenListAdd(self,y,x):
        pos = (y,x)
        # print(self.openlist)
        if x >= self.grid.BottomLeft["x"] and x <= self.grid.TopRight["x"] and y <= self.grid.BottomLeft["y"] and y >= self.grid.TopRight["y"] and self.grid.getGrid(pos).box_class != "wall" and pos not in self.closelist:
            NegiborNode = pos
            MoveCost = self.grid.getGrid(self.cur).g + (10 if self.grid.getGrid(self.cur).y - y == 0 or self.grid.getGrid(self.cur).x - x == 0 else 14)

            if MoveCost < self.grid.getGrid(NegiborNode).g or NegiborNode not in self.openlist:
                self.grid.getGrid(NegiborNode).g = MoveCost
                self.grid.getGrid(NegiborNode).h = (abs(NegiborNode[1] - self.grid.getEndPos[1]) + abs(NegiborNode[0] - self.grid.getEndPos[0])) * 10
                self.grid.getGrid(NegiborNode).perant = self.cur
                self.openlist.append(NegiborNode)

    def findNode(self):
        try:
            while self.openlist:
                self.cur = self.openlist[0]
                for i in self.openlist:
                    if self.grid.getGrid(i).f <= self.grid.getGrid(self.cur).f and self.grid.getGrid(i).h < self.grid.getGrid(self.cur).h:
                        self.cur = i

                self.openlist.remove(self.cur)
                self.closelist.append(self.cur)

                if self.cur == self.grid.getEndPos:
                    TargetCur = self.grid.getEndPos
                    while TargetCur != self.grid.getStartPos:
                        self.finallist.append(TargetCur)
                        TargetCur = self.grid.getGrid(TargetCur).perant
                    self.finallist.append(self.grid.getStartPos)
                    self.finallist.reverse()
                    # for i in self.finallist:
                    #     print(i,end=" -> ")
                    # print("end")
                    return self.finallist
                
                if self.diagonal:
                    self.OpenListAdd(self.grid.getGrid(self.cur).y-1, self.grid.getGrid(self.cur).x-1)
                    self.OpenListAdd(self.grid.getGrid(self.cur).y-1, self.grid.getGrid(self.cur).x+1)
                    self.OpenListAdd(self.grid.getGrid(self.cur).y+1, self.grid.getGrid(self.cur).x+1)
                    self.OpenListAdd(self.grid.getGrid(self.cur).y+1, self.grid.getGrid(self.cur).x-1)

                self.OpenListAdd(self.grid.getGrid(self.cur).y-1, self.grid.getGrid(self.cur).x)
                self.OpenListAdd(self.grid.getGrid(self.cur).y, self.grid.getGrid(self.cur).x+1)
                self.OpenListAdd(self.grid.getGrid(self.cur).y+1, self.grid.getGrid(self.cur).x)
                self.OpenListAdd(self.grid.getGrid(self.cur).y, self.grid.getGrid(self.cur).x-1)
        except:
            print(f"{self.cur} -> {self.grid.getEndPos} 경로 없음")
            pass

class RandomPos:
    def __init__(self, size:tuple[int,int],num=5,start=None,end=None):
        self.__yMax,self.__xMax = size
        self.__ranPos = []
        if start:
            self.__ranPos.append(start)
        if end:
            self.__ranPos.append(end)
        for _ in range(num):
            ran = (random.randint(0,self.__yMax-1),random.randint(0,self.__xMax-1))
            while ran in self.__ranPos:
                ran = (random.randint(0,self.__yMax-1),random.randint(0,self.__xMax-1))
            self.__ranPos.append(ran)
        
    def getStartEnd(self):
        return self.__ranPos[0], self.__ranPos[1], self.__ranPos[2:]
class GUIAStar(AStar):
    def __init__(self,size:tuple[int,int],start:tuple[int,int],end:tuple[int,int],scale:int,diagonal=False):
        super().__init__(size, start, end,scale,diagonal)
        self.scale = scale
    def drawNode(self,screen,nodelist):
        try:
            for i in range(len(nodelist)-1):
                pygame.draw.line(screen,(0,255,0),self.grid.getGrid(nodelist[i]).GUICenter,self.grid.getGrid(nodelist[i+1]).GUICenter,5)
        except:
            pass

    def drawGrid(self,screen):
        for i in self.grid.getAllGrid():
            for j in i:
                if j.box_class == "wall":
                    pygame.draw.rect(screen,(255,0,0),pygame.Rect(j.GUIPos[0],j.GUIPos[1],self.scale,self.scale))
                elif j.box_class == "start":
                    pygame.draw.rect(screen,(0,255,0),pygame.Rect(j.GUIPos[0],j.GUIPos[1],self.scale,self.scale))
                elif j.box_class == "end":
                    pygame.draw.rect(screen,(0,0,255),pygame.Rect(j.GUIPos[0],j.GUIPos[1],self.scale,self.scale))
                else:
                    pygame.draw.rect(screen,(255,255,255),pygame.Rect(j.GUIPos[0],j.GUIPos[1],self.scale,self.scale),1)

def test(diagonal=False):
    start,end,walls = RandomPos((3,3),5).getStartEnd()
    node = AStar((3,3), end, start, 100,diagonal)
    for i in walls:
        node.setWall(i)
    node.grid.showGrid()
    nodelist = node.findNode()
    print("Final Path:",nodelist) 
    print("-" * 20)

def smaple_GUIAStar(screen,size,scale,WallCount,diagonal=False):
    start,end,wall = RandomPos(size,WallCount).getStartEnd()
    gu = GUIAStar(size, end, start, scale, diagonal)
    for i in wall:
        gu.setWall(i)
    gu.drawGrid(screen)
    gu.drawNode(screen, gu.findNode())
