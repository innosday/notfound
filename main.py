from AStar import GUIAStar,RandomPos
import pygame,sys
class PygameTimer:
    def __init__(self, interval):
        self.__time = pygame.event.custom_type()
        pygame.time.set_timer(self.__time, interval)
    
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

    src = PygameTimer(1000)
    Gnode = GUIAStar(size,(24,0),(0,14),scale, diagonal=True)
    finlist = []
    while True:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == src.ID:
                print("Timer event triggered every second")
                start,end,walls = RandomPos(size,50,(24,0),(0,14)).getStartEnd()
                Gnode = GUIAStar(size,start,end,scale, diagonal=True)
                for i in walls:
                    Gnode.setWall(i)
                finlist = Gnode.findNode()
                print("상태 : ", "정상" if finlist else "경로 없음")
                
        Gnode.drawGrid(screen)
        Gnode.drawNode(screen, finlist)
        pygame.display.flip()

if __name__ == "__main__":
    main()