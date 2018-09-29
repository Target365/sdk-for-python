class Keyword:

    def fromDict(self, dict):
        self.keywordId = dict["keywordId"]
        self.shortNumberId = dict["shortNumberId"]
        self.keywordText = dict["keywordText"]
        self.mode = dict["mode"]
        self.forwardUrl = dict["forwardUrl"]
        self.enabled = dict["enabled"]
        self.created = dict["created"]
        self.lastModified = dict["lastModified"]
        self.customProperties = dict["customProperties"]
        self.tags = dict["tags"]

    def fromResponseList(self, listOfKeywords):
        items = []
        for item in listOfKeywords:
            keyword = Keyword()
            keyword.fromDict(item)
            items.append(item)

        return items
