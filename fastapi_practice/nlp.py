
from subprocess import call
# call('python -m spacy download en_core_web_sm', shell=True)
from get_wikipedia import get_wikipedia_text
from collections import Counter

from spacy.lang.en import English, stop_words
import spacy
spacy_stopwords = stop_words.STOP_WORDS

#This could be user input
def get_most_common_words_tags_counts(search_string: str, top_num: int = 10):
    
    page_text = get_wikipedia_text(search_string)

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(page_text.lower())
    tagged_tokens = [(w.text, w.pos_) for w in doc if (w.text not in spacy_stopwords) and (w.is_alpha)]
    tokens, pos_tags = zip(*tagged_tokens)
    tags_counts = Counter(pos_tags)
    common_words_counts = Counter(tokens).most_common(top_num)
    return common_words_counts, tags_counts

search_string = "New York"
common_words_counts, tags_counts = get_most_common_words_tags_counts(search_string)
print(common_words_counts)

