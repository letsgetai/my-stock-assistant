from camel.toolkits import SearchToolkit
toolkit = SearchToolkit()
tools   = toolkit.get_tools()

search_wiki = tools[0]
if __name__ == "__main__":
    print(tools)