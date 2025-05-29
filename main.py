from AStar import AStar
import pygame,sys

class BoxGrid:
    def __init__(self, size: tuple[int, int],scale:int):
        self.grid = [[{"pos": (j*scale, i*scale), "center": (j*scale+scale//2,i*scale+scale//2)} for i in range(size[0])] for j in range(size[1])]

def main():
    node = AStar((6,3),(5,0),(0,2)) 
    node.grid.showGrid(detail=False)
    scale = 100
    print(node.size)
    window = (scale * node.size[0], scale * node.size[1])
    
    boxGrid = BoxGrid(node.size, scale)

    pygame.init()
    screen = pygame.display.set_mode(window)
    pygame.display.set_caption("A* Pathfinding Visualizer")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # node.grid.showGrid(detail=False)
        pygame.display.flip()

if __name__ == "__main__":
    main()