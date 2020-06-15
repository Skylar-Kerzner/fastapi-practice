from models import Wikistats

def create_wikistats_entry(common_words_counts, page_name):
    wikistats_entry = Wikistats()
    wikistats_entry.page_name = page_name

    word_1_count = max(common_words_counts.values())

    for i, (word, count) in enumerate(common_words_counts.items()):
        exec('wikistats_entry.word_ranked_'+str(i+1)+' = word')
        exec('wikistats_entry.relative_frequency_'+str(i+1)+' = round(float(count)/word_1_count, 4)')
 
    return wikistats_entry