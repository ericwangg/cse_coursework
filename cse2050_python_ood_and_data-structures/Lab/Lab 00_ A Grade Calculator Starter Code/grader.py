def assigngrade(score, grades = ['A', 'B', 'C', 'D', 'F'],
                cutoffs = [90, 80, 70, 65, 0]):
                for x in range (len(cutoffs)):
                    if score >= cutoffs[x]:
                        return grades[x]

def droplowest(L):
    L.remove(min(L))

def average(L):
    return(sum(L) / len(L))
