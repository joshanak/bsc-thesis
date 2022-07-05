class TrainStop:
    def __init__(self, name, duration, part_of, angle):
        self.name = name
        self.part_of = part_of
        self.duration = duration
        self.angle = angle
        self.Rect = list()

    # rect holds information about displaying the stop
    def setRect(self, location, height, width):
        self.Rect.append(location[0])
        self.Rect.append(location[1])
        self.Rect.append(height)
        self.Rect.append(width)

    def printTrainSpot(self):
        print(self.name, self.Rect, self.duration)


