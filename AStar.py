import random

class Node:
    def __init__(self,pos:tuple[int,int]):
        self.__y,self.__x = pos
        self.__g = 0
        self.__h = 0
        self.__perant = None
        self.__box_class = None

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
    def __init__(self,size:tuple[int,int]):
        self.__grid = [[Node
        ((i,j)) for j in range(size[1])] for i in range(size[0])]
        self.__bottomLeft = {"y":size[1]-1,"x":0}
        self.__topRight = {"y":0,"x":size[0]-1}

    @property
    def BottomLeft(self) -> tuple[int,int]:
        return self.__bottomLeft
    
    @property
    def TopRight(self) -> tuple[int,int]:
        return self.__topRight
      
    def getGrid(self,pos) -> Node:
        return self.__grid[pos[0]][pos[1]]
    
    def showGrid(self,detail=False):
        if not detail:
            for i in self.__grid:
                for j in i:
                    print("%5s"%j.box_class,end=" ")
                print()
        else:
            for i in self.__grid:
                for j in i:
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
    def __init__(self,size:tuple[int,int],end:tuple[int,int],start:tuple[int,int]):
        self.grid = GridBox(size)
        self.grid.setBoxClass(start,"start")
        self.grid.setBoxClass(end,"end")

        self.openlist = [self.grid.getStartPos]
        self.closelist = []
        self.finallist = []
        self.cur = self.openlist[0]

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
                for i in self.finallist:
                    print(i,end=" -> ")
                print("end")
                return self.finallist
            self.OpenListAdd(self.grid.getGrid(self.cur).y-1, self.grid.getGrid(self.cur).x)
            self.OpenListAdd(self.grid.getGrid(self.cur).y, self.grid.getGrid(self.cur).x+1)
            self.OpenListAdd(self.grid.getGrid(self.cur).y+1, self.grid.getGrid(self.cur).x)
            self.OpenListAdd(self.grid.getGrid(self.cur).y, self.grid.getGrid(self.cur).x-1)




    # grid.showDetailGrid()

class TestAStar:
    def __init__(self,size=5):
        self.ranPos = []
        self.size = size
    def randomPos(self,start,end) -> int:
        ran = (random.randint(start,end),random.randint(start,end))
        while True:
            if ran not in self.ranPos:
                self.ranPos.append(ran)
                break
            else:
                ran = (random.randint(start,end),random.randint(start,end))

    def test(self):
        for _ in range(3):
            self.ranPos = []
            for i in range(self.size+2):
                self.randomPos(0,self.size-1)
            print(self.ranPos)
            node = AStar((self.size,self.size),self.ranPos[0],self.ranPos[1])
            for i in self.ranPos[2:]:
                node.setWall(i)
            node.grid.showGrid()
            nodelist = node.findNode()
            # print("Final Path:",nodelist) 
            print("-" * 20)



