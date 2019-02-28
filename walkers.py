from functools import reduce

class Slide:
    # where slide :: (id, tags)
    def __init__(self, slides):
        self.slides = slides
    
    def getTags(self):
        return reduce(lambda x, acc: acc.extend(x[1]), self.slides)
    
    def isComb(self):
        return len(self.slides) > 1
    
    def __repr__(self):
        ret = ''
        for s in self.slides:
            ret += '{}: {}'.format(s[0], s[1])
        return ret

noPhotos = 0
slides = []
vPhotos = []

# h -> add to slide
# v -> add to array
def parseLine(line):
    sp = line.split(' ')

    idd = sp[1]
    tags = sp[2:]
    photo = (idd, tags)

    if sp[0] == 'H':
        # create slide with just one photo
        slides.append(Slide([photo]))
    elif sp[0] == 'V':
        vPhotos.append(photo)


def readIn(fileName):
    with open(fileName) as f:
        lines = f.readlines()
        noPhotos = int(lines[0])

        for l in lines[1:]:
            parseLine(l.rstrip())
        
        print(len(slides))
        print(slides[10])

readIn('b_lovely_landscapes.txt')