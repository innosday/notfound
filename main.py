from AStar import GridBox,Entity,RandomPos
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


def main():
    size = (25,15)
    scale = 20
    window = (size[1] * scale, size[0] * scale)

    _,_,walls = RandomPos(size,50).getStartEndWalls()
    grid = GridBox(size,scale)
    for i in walls:
        grid.setBoxClass(i,"wall")

    pygame.init()
    screen = pygame.display.set_mode(window)
    pygame.display.set_caption("A* Pathfinding Visualizer")

    src = PYGTimer(250)
    test2 = Entity(grid,(24,0),(0,14),size,scale)
    test3 = Entity(grid,(14,0),(0,0),size,scale)

    while True:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # elif event.type == src.ID:
            #     test2.fin = test2.findNode()
            #     test3.fin = test3.findNode()
        grid.drawGrid(screen)
        test2.drawNode(screen)
        test3.drawNode(screen,(255,0,0))
        # print(f"test3 : {test3.fin}\ntest2 : {test2.fin}")
        pygame.display.flip()

if __name__ == "__main__":
    main()