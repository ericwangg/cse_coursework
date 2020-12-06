class Pattern:
    def __init__(self, pattern, wildcard = None):
        self.pat = pattern
        self.wild = wildcard
        self.case = False

    def set_case_sensitive(self, case):
        if case is True:
            self.case = True

    def remove_dupe(self, l):
        for element in l:
            n = l.index(element)
            for dupe in l[n+1:]:
                if dupe == element:
                    l.remove(dupe)
            for element in l:
                if element == -1:
                    l.remove(element)
        return l

    def findMatch(self, text, start = 0):
        i = start
        while i < len(text):
            ind = 0
            if len(self.pat) > (len(text) - i):
                return -1
            while ind < len(self.pat):
                if self.pat[ind] == text[i + ind] or self.pat[ind] == self.wild:
                    ind += 1
                else:
                    break
            if ind == len(self.pat):
                return i
            i += 1

    def findMatches(self, text):
        if self.case is False:
            text = text.lower()
        list = [self.findMatch(text)]
        for i in range(list[0],len(text)):
            if (self.findMatch(text, start = i) != -1):
                list.append(self.findMatch(text, start = i))
            else:
                break
        return self.remove_dupe(list)

    def __str__(self):
        if self.case == True and self.wild != None:
            return "The case sensitive pattern is %s and the wildcard is %s" % (self.pat, self.wild)
        elif self.case == True and self.wild == None:
            return "The case sensitive pattern is %s" % (self.pat)
        elif self.wild != None:
            return "The pattern is %s and the wildcard is %s" % (self.pat, self.wild)
        else:
            return "The pattern is %s" % (self.pat)
