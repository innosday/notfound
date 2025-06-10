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

    pygame.init()
    screen = pygame.display.set_mode(window)
    pygame.display.set_caption("A* Pathfinding Visualizer")

    src = PYGTimer(250)
    
    walls = [
            [(11,i) for i in range(15) if not i in [3,12]],
            [(12,i) for i in range(15) if not i in [3,12]],
            [(13,i) for i in range(15) if not i in [3,12]]
        ]
    grid = GridBox(size,scale)
    for wall in walls:
        for w in wall:
            grid.setBoxClass(w,"wall")
    test2 = Entity((14,0),(0,0),grid)
    # test3 = Entity(grid,(14,0),(0,0),size,scale,True)
    while True:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == src.ID:
                test2.move()
        grid.drawGrid(screen)
        test2.drawNode(screen)
        # test3.drawNode(screen,(255,0,0))
        # print(f"test3 : {test3.fin}\ntest2 : {test2.fin}")
        pygame.display.flip()

if __name__ == "__main__":
    main()