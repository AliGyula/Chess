class pathFinding:
    def __init__(self,grid, startX, startY, endX, endY):
        self.grid=grid
        self.start=self.grid.tiles[startX][startY]
        self.end=self.grid.tiles[endX][endY]
        self.path=[]
        self.cameFrom=[]
        self.openSet=[]
        self.closedSet=[]
        self.solvegrid()

    def heuristic(self,current,goal):
        return abs(current.i-goal.i)+abs(current.j-goal.j)

    def makePath(self,current):
        self.path.append(current)

        while current.cameFrom!=None:
            current=current.cameFrom
            self.path.append(current)

    def lowestFScore(self):
        index=0
        minF=self.openSet[0].fScore
        for i in range(1,len(self.openSet)):
            if minF>self.openSet[i].fScore:
                minF=self.openSet[i].fScore
                index=i
        return index

    def solvegrid(self):
        self.openSet.append(self.start)
        self.start.gScore=0
        self.start.fScore=self.heuristic(self.start,self.end)

        while len(self.openSet)>0:
            current=self.openSet[self.lowestFScore()]

            if current.i == self.end.i and current.j == self.end.j:
                self.makePath(current)
                return
            
            self.openSet.remove(current)
            self.closedSet.append(current)

            neighbors = current.neighbors
            for neighbor in neighbors:
                if neighbor in self.closedSet:
                    continue

                tempGScore=current.gScore+1

                if neighbor not in self.openSet:
                    self.openSet.append(neighbor)
                elif tempGScore>=neighbor.gScore:
                    continue
                neighbor.cameFrom=current
                neighbor.gScore=tempGScore
                neighbor.fScore=neighbor.gScore+self.heuristic(neighbor,self.end)