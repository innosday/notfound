from AStar import GridBox,multipleAStar
import pygame,sys
class PYGTimer:
    id = 0
    def __init__(self, interval):
        self.__time = pygame.event.custom_type()
        pygame.time.set_timer(self.__time, interval)
        PYGTimer.id += 1
    
    @property
    def ID(self):
        return self.__time
class HoldButton:
    def __init__(self):    
        self.old = False
    
    def active(self,mouseClick:bool):
        bt = mouseClick
        if self.old != bt:
            if bt:
                self.old = True
                return True
            else:
                self.old = False
                return False
        else:
            return False
        
def main():
    size = (25,15)
    scale = 20
    window = (size[1] * scale, size[0] * scale)

    pygame.init()
    screen = pygame.display.set_mode(window)
    pygame.display.set_caption("A* Pathfinding Visualizer")

    src = PYGTimer(250)
    bt =HoldButton()
    me = multipleAStar(size,scale,{"left":(5,3),"right":(5,11),"center":(4,7)})
    
    towersHealth = {
        "left": 100,
        "right": 100,
        "center": 100
    }
    walls ={
        "river" :[
            [(11,i) for i in range(15) if not i in [3,12]],
            [(12,i) for i in range(15) if not i in [3,12]],
            [(13,i) for i in range(15) if not i in [3,12]],
        ],
        "left" :[
            [(2,2),(2,3),(2,4)],[(3,2),(3,3),(3,4)],[(4,2),(4,3),(4,4)]
        ],
        "right" :[
            [(2,12),(2,11),(2,10)],[(3,12),(3,11),(3,10)],[(4,12),(4,11),(4,10)]
        ],
        "center" :[
            [(1,6),(1,7),(1,8)],[(2,6),(2,7),(2,8)],[(3,6),(3,7),(3,8)]
        ]
    }
    me.setWall(walls,["river","left","right","center"])
    

    while True:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == src.ID:
                me.move()
                        
    
        me.draw(screen)
        if bt.active(pygame.mouse.get_pressed()[0]):
            me.add(me.getMousePos(pygame.mouse.get_pos()),towersHealth,diagonal=True)
        print(towersHealth)
        for i in towersHealth.keys():
            if towersHealth[i] <= 0:
                for a in walls[i]:
                    for b in a:
                        me.grid.setSubClass(b,"breaktower")

        pygame.display.flip()

if __name__ == "__main__":
    main()