class queue:
    items = {}

    def __init__(self, items):
        self.items = items

    def getQueueLength(self):
        return len(self.items)

    def removeItemByIndex(self, index):
        try:
            self.items.pop(index)
            self.updateItems()
            return True
        except:
            return False

    def updateItems(self):
        for i in range(len(self.items)):
            self.items[i].updateItem(i)

    def nextItem(self):
        try:
            return self.items[0]
        except:
            return None
        
    def createQueueItem(self, filename, url):
        index = self.getQueueLength()
        self.items[index] = queueItem(self, index, filename, url)
        return self.items[index]
    
    def isEmpty(self):
        return len(self.items) == 0
    
    def getItems(self):
        return self.items

class queueItem:
    queue = None
    index = 0
    title = ''
    length = ''
    filename = ''
    url = ''

    def __init__(self, queue, index, filename, url):
        self.queue = queue
        self.index = index
        #self.title = title
        #self.length = length
        self.filename = filename
        self.url = url

    def getTrackQueue(self):
        return self.queue
    
    def getTrackIndex(self):
        return self.index

    def getTrackName(self):
        return self.title
    
    def getTrackLength(self):
        return self.length
    
    def getTrackUrl(self):
        return self.url
    
    def getTrackFilename(self):
        return self.filename
    
    def updateItem(self, id):
        if self.index != id:
            self.index = id
