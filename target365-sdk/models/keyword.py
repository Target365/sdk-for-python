class Keyword:

    def fromDict(self, dictionnaryItem):
        self.keywordId = dictionnaryItem["keywordId"]
        self.shortNumberId = dictionnaryItem["shortNumberId"]
        self.keywordText = dictionnaryItem["keywordText"]
        self.mode = dictionnaryItem["mode"]
        self.forwardUrl = dictionnaryItem["forwardUrl"]
        self.enabled = dictionnaryItem["enabled"]
        self.created = dictionnaryItem["created"]
        self.lastModified = dictionnaryItem["lastModified"]
        self.tags = dictionnaryItem["tags"]
        self.customProperties = dictionnaryItem.get("customProperties", None)

    def fromResponseList(self, listOfKeywords):
        items = []
        for item in listOfKeywords:
            keyword = Keyword()
            keyword.fromDict(item)
            items.append(keyword)

        return items
