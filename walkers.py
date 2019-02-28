from functools import reduce

class Slide:
    # where slide :: (id, {tags})
    def __init__(self, slides):
        self.slides = slides

    # returns in output-able format
    def getIds(self):
        ids = self.slides[0][0]
        for s in self.slides[1:]:
            ids += ' {}'.format(s[0])
        return ids
    
    def getTags(self):
        #return reduce(lambda acc, x: acc.union(x[1]), self.slides)
        tags = self.slides[0][1]
        for s in self.slides[1:]:
            tags = tags.intersection(s[1])
        return tags
    
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
notSat = []

# h -> add to slide
# v -> add to array
def parseLine(line, lineNo):
    sp = line.split(' ')

    idd = str(lineNo)
    tags = set(sp[2:])
    photo = (idd, tags)

    if sp[0] == 'H':
        # create slide with just one photo
        slides.append(Slide([photo]))
    elif sp[0] == 'V':
        vPhotos.append(photo)

def minimiseVerts():
    for v in vPhotos:
        for v2 in vPhotos:
            # find another vert. photo
            # which meets min. tag threshold
            if v2 != v and len(v[1].union(v2[1])) < 13:
                # met threshold -
                # create new slide w both
                slides.append(Slide([v, v2]))
                vPhotos.remove(v)
                vPhotos.remove(v2)
                break
        # if not met add to non. sat arr
        if v in vPhotos:
            notSat.append(v)
            vPhotos.remove(v)

def pairNonSat():
    for i in range(0, len(notSat) - 1, 2):
        slides.append(Slide([notSat[i], notSat[i + 1]]))

def readIn(fileName):
    with open(fileName, 'r') as f:
        lines = f.readlines()
        noPhotos = int(lines[0])

        for (idx, l) in enumerate(lines[1:]):
            parseLine(l.rstrip(), idx)
        minimiseVerts()
        pairNonSat()
        
        #print(len(slides))
        print(slides[501])
        print(slides[501].getTags())

        sort = sorted(slides, key=lambda x: len(x.getTags()))

        final = []
        for i in range(1, int(len(sort) / 2) - 1):
            final.append(sort[i])
            final.append(sort[len(sort) - i])

        with open('{}.ans'.format(fileName.split('.')[0]), 'w') as f:
            f.write('{}\n'.format(len(final)))
            for s in sort:
                f.write('{}\n'.format(s.getIds()))

readIn('b_lovely_landscapes.txt')
<<<<<<< HEAD
#readIn('c_memorable_moments.txt')
=======
#readIn('b_lovely_landscapes.txt')
#readIn('c_memorable_moments.txt')
>>>>>>> d176361c65135e8c712b12be13cb15db06db5480
