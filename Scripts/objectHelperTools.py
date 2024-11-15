import re


def name_to_key(name:str):
    return name.casefold().replace(" ", "_")


def regexSearch(query:str, searchList):
    query = name_to_key(query)
    regex = ".*" + query + ".*"
    item_list = "\n".join(searchList)
    return re.findall(regex, item_list)
