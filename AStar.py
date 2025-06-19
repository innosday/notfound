import random,pygame,copy

class Node:
    def __init__(self,pos:tuple[int,int],scale):
        self.__y,self.__x = pos
        self.__g = 0
        self.__h = 0
        self.__perant = None
        self.__box_class = None
        self.__sub_class = None
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
    @property
    def sub_class(self):
        return self.__sub_class
    
    @sub_class.setter
    def sub_class(self,sub_class:str):
        self.__sub_class = sub_class

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
    def __init__(self,size:tuple[int,int],scale:int,target):
        self.__target = target
        self.scale = scale
        self.__size = size
        self.__grid = [[Node((i,j),self.scale) for j in range(self.__size[1])] for i in range(self.__size[0])]
        self.__bottomLeft = {"y":size[0]-1,"x":0}
        self.__topRight = {"y":0,"x":size[1]-1}

    @property
    def size(self):
        return self.__size
    @property
    def target(self):
        return self.__target
    @property
    def BottomLeft(self) -> tuple[int,int]:
        return self.__bottomLeft
    @property
    def TopRight(self) -> tuple[int,int]:
        return self.__topRight
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

    def resetStartEnd(self):
        for i in self.__grid:
            for l in i:
                if l.box_class in ["start","end"]:
                    l.box_class = None
    
    def getAllGrid(self) -> list[list[Node]]:
        return self.__grid
      
    def getGrid(self,pos) -> Node:
        return self.__grid[pos[0]][pos[1]]

    def drawGrid(self,screen,curlist):
        for i in self.__grid:
            for j in i:
                # if j.box_class == "wall" and j.sub_class not in ["river"]:
                #     pygame.draw.rect(screen,(255,255,0),pygame.Rect(j.GUIPos[0],j.GUIPos[1],self.scale,self.scale))
                if j.sub_class == "river":
                    pygame.draw.rect(screen,(0,0,255),pygame.Rect(j.GUIPos[0],j.GUIPos[1],self.scale,self.scale))
                elif j.sub_class == "tower":
                    pygame.draw.rect(screen,(125,125,125),pygame.Rect(j.GUIPos[0],j.GUIPos[1],self.scale,self.scale))
                elif j.sub_class == "breaktower":
                    pygame.draw.rect(screen,(100,100,100),pygame.Rect(j.GUIPos[0],j.GUIPos[1],self.scale,self.scale))
                else:
                    pygame.draw.rect(screen,(255,255,255),pygame.Rect(j.GUIPos[0],j.GUIPos[1],self.scale,self.scale),1)
        # print(args)
        for i in curlist:
            # print(self.getGrid(i).GUIPos[0],self.getGrid(i).GUIPos[1],self.scale,self.scale)
            pygame.draw.rect(screen,(255,0,0),(self.getGrid(i).GUIPos[0],self.getGrid(i).GUIPos[1],self.scale,self.scale))

    def setBoxClass(self,pos:tuple[int,int],Class:str):
        self.__grid[pos[0]][pos[1]].box_class = Class
    
    def setSubClass(self,pos:tuple[int,int],Class:str):
        self.__grid[pos[0]][pos[1]].sub_class = Class

    def getGridPos(self,mousePos) -> tuple[int,int]:
        for i in self.__grid:
            for j in i:
                if j.GUIPos[0] <= mousePos[0] <= j.GUIPos[0] + self.scale and j.GUIPos[1] <= mousePos[1] <= j.GUIPos[1] + self.scale:
                    return (j.y,j.x)

class AStar:
    def __init__(self,start,end,grid:GridBox = None,diagonal=False):
        # self.grid = copy.deepcopy(grid)
        self.grid = grid
        # self.size = sorted(size,reverse=True)
        self.start = start
        self.end = end

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
        if x >= self.grid.BottomLeft["x"] and x <= self.grid.TopRight["x"] and y <= self.grid.BottomLeft["y"] and y >= self.grid.TopRight["y"] and self.grid.getGrid(pos).box_class != "wall" and self.grid.getGrid(pos).box_class != "start" and  pos not in self.closelist:
            if self.diagonal:
                if self.grid.getGrid((y,self.grid.getGrid(self.cur).x)).box_class == "wall" and self.grid.getGrid((self.grid.getGrid(self.cur).y,x)).box_class == "wall" and self.grid.getGrid((y,self.grid.getGrid(self.cur).x)).box_class == "start" and self.grid.getGrid((self.grid.getGrid(self.cur).y,x)).box_class == "start":
                    return
            
            NegiborNode = pos
            MoveCost = self.grid.getGrid(self.cur).g + (10 if self.grid.getGrid(self.cur).y - y == 0 or self.grid.getGrid(self.cur).x - x == 0 else 14)

            if MoveCost < self.grid.getGrid(NegiborNode).g or NegiborNode not in self.openlist:
                self.grid.getGrid(NegiborNode).g = MoveCost
                self.grid.getGrid(NegiborNode).h = (abs(NegiborNode[1] - self.grid.getEndPos[1]) + abs(NegiborNode[0] - self.grid.getEndPos[0])) * 10
                self.grid.getGrid(NegiborNode).perant = self.cur
                self.openlist.append(NegiborNode)

    def findNode(self):
        # Reset lists before each search
        self.grid.setBoxClass(self.start,"start")
        self.grid.setBoxClass(self.end,"end")
        self.openlist = [self.grid.getStartPos]
        self.closelist = []
        self.finallist = []
        self.cur = self.openlist[0]
        
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
                    sorted(self.finallist,reverse=True)
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
            # print(f"{self.cur} -> {self.grid.getEndPos} 경로 없음")
            pass
class RandomPos:
    def __init__(self, size:tuple[int,int],num=5,start=None,end=None):
        self.__yMax,self.__xMax = size
        self.__ranPos = []
        if start:
            self.__ranPos.append(start)
        if end:
            self.__ranPos.append(end)
        for _ in range(num-len(self.__ranPos)):
            ran = (random.randint(0,self.__yMax-1),random.randint(0,self.__xMax-1))
            while ran in self.__ranPos:
                ran = (random.randint(0,self.__yMax-1),random.randint(0,self.__xMax-1))
            self.__ranPos.append(ran)
        
    def getStartEndWalls(self):
        return self.__ranPos[0], self.__ranPos[1], self.__ranPos[2:]

class Entity(AStar):
    def __init__(self,lastCur,grid:GridBox,towerInfo,diagonal=False):
        self.diagonal = diagonal
        winCenter = grid.size[1]//2
        self.towerInfo = towerInfo
        self.rotation = "left" if lastCur[1] < winCenter else "right"
        if self.towerInfo[self.rotation] <=0:
            self.rotation = "center"
        target = grid.target[self.rotation]
        super().__init__(lastCur,target,grid,diagonal)
        self.__path = None
    def drawNode(self,screen,color=(0,255,0)):
        if self.__path:
            centerNode = list(map(lambda x: self.grid.getGrid(x).GUICenter,self.__path))
            pygame.draw.lines(screen,color,False,centerNode,5)

    @property
    def Cur(self):
        return self.start
            
    def move(self):
        if self.start == self.end:
            return True
        else:
            if self.towerInfo[self.rotation] <=0:
                self.rotation = "center"
            self.end = self.grid.target[self.rotation]

            self.grid.resetStartEnd()
            if self.__path:
                # print(self.__path.index(self.start)-1)
                self.start = self.__path[self.__path.index(self.start)-1]
            self.__path = self.findNode()
        return False
        
class multipleAStar:
    def __init__(self,size:tuple[int,int],scale:int,target:dict[str,tuple[int,int]]):
        self.entitys:list[Entity] = []
        self.grid = GridBox(size,scale,target)
        self.target = target 

    def getMousePos(self,mousePos:pygame.mouse.get_pos) -> tuple[int,int]:
        return self.grid.getGridPos(mousePos)


    def add(self,start:tuple[int,int],targethealth,diagonal=False):
        self.entitys.append(Entity(start,self.grid,targethealth,diagonal))

    def draw(self,screen,drawNode=False):
        self.grid.drawGrid(screen,list(map(lambda x: x.start, self.entitys)))
        if drawNode:
            for e in self.entitys:
                e.drawNode(screen)
    def move(self,damage= 10):
        for e in self.entitys:
            if e.move():
                self.entitys.remove(e)
                e.towerInfo[e.rotation] -= damage
                
    def setWall(self,walls,wallname):
        for name in wallname:
            for wall in walls[name]:
                for pos in wall:
                    self.grid.setBoxClass(pos, "wall")
                    if name == "river":
                        self.grid.setSubClass(pos, "river")
                    elif name in ["left","right","center"]:
                        self.grid.setSubClass(pos, "tower")
