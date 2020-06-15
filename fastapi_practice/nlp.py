
from subprocess import call
# call('python -m spacy download en_core_web_sm', shell=True)
from get_wikipedia import get_wikipedia_text
from collections import Counter
import string
from spacy.lang.en import English, stop_words
import spacy
spacy_stopwords = stop_words.STOP_WORDS

#This could be user input
def get_most_common_words_tags_counts(search_string: str, top_num: int = 10):
    
    page_text, page_name = get_wikipedia_text(search_string)
    processed_page_text = page_text.lower().translate(str.maketrans('','', string.punctuation))

    nlp = spacy.load('en_core_web_sm')
    
    doc = nlp(processed_page_text)
    tagged_tokens = [(w.text, w.pos_) for w in doc if (w.is_alpha)] # (w.text not in spacy_stopwords) Need stopwords for zipf
    tokens, pos_tags = zip(*tagged_tokens)
    tags_counts = Counter(pos_tags)
    common_words_counts = {k:v for (k,v) in Counter(tokens).most_common(top_num)}
    total_words = len(tagged_tokens)
    return common_words_counts, tags_counts, page_name, total_words


# --- TEST ---
#search_string = "New York"
#common_words_counts, tags_counts, page_name = get_most_common_words_tags_counts(search_string)
#print(f"Page Name: {page_name}")
#print(f"Common Words: {common_words_counts}")

