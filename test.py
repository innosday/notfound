# from AStar import test

# for i in range(10):
#     print(f"Test {i+1}:")
#     test(True)\

# class PygameTimer:
#     def __init__(self, interval):
#         self.__time = pygame.event.custom_type()
#         pygame.time.set_timer(self.__time, interval)
    
#     @property
#     def ID(self):
#         return self.__time

# import pygame

# pygame.init()
# pygame.display.set_caption("A* Pathfinding Visualizer")
# screen = pygame.display.set_mode((800, 600))

# src = PygameTimer(1000)
# mcsrc = PygameTimer(500)


# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()
#         elif event.type == src.ID:
#             print("Timer event triggered every second")
#         elif event.type == mcsrc.ID:
#             print("Timer event triggered every half second")

#     screen.fill((0, 0, 0))
#     pygame.display.flip()

# from AStar import AStar

# a = AStar((24,0),(0,14),(25,15),(20))

# try:
#     while True:
#         print(a.findNode())
# except KeyboardInterrupt:
#     pass

A = [1,2,3,4,5]
class test:
    def __init__(self,arr):
        self.arr:list = arr
    
    def add(self,num):
        self.arr.append(num)
    
    def remove(self):
        self.arr.pop(0)

print(A)
b = test(A)
b.add(6)
print(A)