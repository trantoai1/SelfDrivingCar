import pygame


class KeyBoardModule():
    def __init__(self):
        pygame.init()
        win = pygame.display.set_mode((100,100))

    def getKey(self,keyName):
        ans = False
        for eve in pygame.event.get():pass
        keyInput = pygame.key.get_pressed()
        myKey = getattr(pygame,'K_{}'.format(keyName))
        if keyInput [myKey]:
            ans = True
        pygame.display.update()

        return ans

    def main(self):
        if self.getKey('LEFT'):
            print('Key Left was pressed')
        if self.getKey('RIGHT'):
            print('Key Right was pressed')

if __name__ == '__main__':
    key = KeyBoardModule()
    while True:
        key.main()