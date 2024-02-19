
def extractTilesfromImage(img, tiles=[]):
    imgs = []
    for pi in tiles:
            imgs.append(img.subsurface(pi))

    return imgs



class Animation :
    def __init__(self, images, aniSpeed=5, loop=True):
        self.images = images
        self.aniSpeed = aniSpeed
        self.loop = loop
        self.done = False
        self.frame = 0
    def copy (self):
        return Animation(self.images, self.aniSpeed, self.loop)
    def update(self, dt):
        self.frame += self.aniSpeed * dt
                 
        if self.frame >= len(self.images):
            if self.loop:
                self.frame=0
            else:
                self.frame = max(len(self.image)-1,0)
                self.done=True

    def img(self):
        return self.images[int(self.frame)]
    

    