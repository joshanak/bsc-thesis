class RailwayElements:
    def __init__(self):
        self.arcs = list()
        self.lines = list()

    # arc is a dictionary
    def addArc(self, arc):
        self.arcs.append(arc)

    # line is also a dictionary
    def addLine(self, line):
        self.lines.append(line)

    def returnDict(self):
        returndict = dict()
        returndict['arc'] = self.arcs
        returndict['line'] = self.lines
        return returndict

    def printRailElements(self):
        print(self.returnDict()['line'])