from functools import reduce
import numpy as np

class Slide:
    # where slide :: (id, {tags})
    def __init__(self, slides):
        self.slides = slides
        self.tagVec = []
        self.size = 0

    # returns in output-able format
    def getIds(self):
        ids = self.slides[0][0]
        for s in self.slides[1:]:
            ids = '{} {}'.format(ids, s[0])
        return ids
    
    def getTags(self):
        #return reduce(lambda acc, x: acc.union(x[1]), self.slides)
        tags = self.slides[0][1]
        for s in self.slides[1:]:
            tags = tags.union(s[1])
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
            if v2 != v and len(v[1].union(v2[1])) < 15:
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
    for i in range(0, len(notSat), 2):
        slides.append(Slide([notSat[i], notSat[i + 1]]))

def readIn(fileName):
    with open(fileName, 'r') as f:
        lines = f.read().split('\n')
        #lines = f.readlines()
        noPhotos = int(lines[0])

        for (idx, l) in enumerate(lines[1:]):
            parseLine(l.rstrip(), idx)

        minimiseVerts()
        pairNonSat()

        sort = sorted(slides, key=lambda x: len(x.getTags()))
        print(len(slides), 'slides')

        unique = reduce(lambda acc, x: acc.union(x.getTags()), sort, set())
        print('unique tags:', len(unique))

        for s in sort:
            tagVec = []
            for k in unique:
                if k in s.getTags():
                    tagVec.append(1)
                else:
                    tagVec.append(0)
            
            s.tagVec = np.array(tagVec)
            s.size = np.sqrt(s.tagVec.dot(s.tagVec))
        
        final = []
        for s in range(0, len(sort)):
            base = sort[s]
            for k in range(s + 1, len(sort)):
                comp = sort[k]
                if comp != base and comp not in final:
                    theta = np.dot(base.tagVec, comp.tagVec) / (base.size * comp.size)
                    if abs(theta - 0.7010678118) <= 0.8:
                        #final.append(base)
                        final.append(comp)
                        break
        print(len(final))
        print(len(sort))
        
        """ for i in range(1, int(len(sort) / 2) - 1):
            final.append(sort[i])
            final.append(sort[len(sort) - i]) """

        

        with open('{}.ans'.format(fileName.split('.')[0]), 'w') as f:
            f.write('{}\n'.format(len(final)))
            for s in final:
                f.write('{}\n'.format(s.getIds()))

#readIn('b_lovely_landscapes.txt')
readIn('b_lovely_landscapes.txt')
#readIn('c_memorable_moments.txt')
