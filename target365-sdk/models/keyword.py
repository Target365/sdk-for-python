class Keyword:

    def from_dict(self, dictionary_item):
        self.keywordId = dictionary_item["keywordId"]
        self.shortNumberId = dictionary_item["shortNumberId"]
        self.keywordText = dictionary_item["keywordText"]
        self.mode = dictionary_item["mode"]
        self.forwardUrl = dictionary_item["forwardUrl"]
        self.enabled = dictionary_item["enabled"]
        self.created = dictionary_item["created"]
        self.lastModified = dictionary_item["lastModified"]
        self.tags = dictionary_item["tags"]
        self.customProperties = dictionary_item.get("customProperties", None)

    # noinspection PyMethodMayBeStatic
    def from_response_list(self, list_of_keywords):
        items = []
        for item in list_of_keywords:
            keyword = Keyword()
            keyword.from_dict(item)
            items.append(keyword)

        return items
