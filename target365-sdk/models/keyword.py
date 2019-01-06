class Keyword:

    def from_dict(self, dictionaryItem):
        self.keywordId = dictionaryItem["keywordId"]
        self.shortNumberId = dictionaryItem["shortNumberId"]
        self.keywordText = dictionaryItem["keywordText"]
        self.mode = dictionaryItem["mode"]
        self.forwardUrl = dictionaryItem["forwardUrl"]
        self.enabled = dictionaryItem["enabled"]
        self.created = dictionaryItem["created"]
        self.lastModified = dictionaryItem["lastModified"]
        self.tags = dictionaryItem["tags"]
        self.customProperties = dictionaryItem.get("customProperties", None)

    def from_response_list(self, list_of_keywords):
        items = []
        for item in list_of_keywords:
            keyword = Keyword()
            keyword.from_dict(item)
            items.append(keyword)

        return items
