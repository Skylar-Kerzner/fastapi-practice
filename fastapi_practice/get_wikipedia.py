import wikipedia



def get_wikipedia_text(search_string: str):
    search_results = wikipedia.search(search_string)
    page_name = search_results[0]
    try:
        summary = wikipedia.summary(page_name)
    except wikipedia.exceptions.DisambiguationError as e:
        page_name = e.options[0]
    page = wikipedia.page(page_name)
    page_text = page.content
    return page_text

#This could be user input
search_string = "New York"
page_text = get_wikipedia_text(search_string)
print(len(page_text))
