# Importing modules
# regex library
import re
# import libraries from sk-learn for LDA model
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
# wordcloud library
from wordcloud import WordCloud
# All get data frame functions can be found in utilities.py
import utilities
 
'''
--- Helper Functions ---
'''

# prints Wordcloud of permit text
def wordcloud_permit_text(permits):
    # join permit text together
    long_string = ','.join(list(permits['DESC_OF_WORK'].values))
    # create word cloud
    wordcloud = WordCloud(background_color="white", max_words=100, contour_width=3, w='firebrick')
    # create visual
    wordcloud.generate(long_string)
    wordcloud.to_image()

# Finds top topics in LDA
def LDA_find_top_topics(permits):
    # use english stop words in vectorizer
    count_vectorizer = CountVectorizer(stop_words='english')
    
    # transform descriptions
    count_data = count_vectorizer.fit_transform(permits['DESC_OF_WORK'])
    
    number_topics = 5
    number_words = 10
    
    # create/fit model
    lda = LDA(n_components=number_topics)
    lda.fit(count_data)
    
    # print topics found...
    print("Topics found via LDA:")
    print_topics(lda, count_vectorizer, number_words)

# Prints each Topic taking in LDA_model, vectorizer, and num of words to find
def print_topics(model, count_vectorizer, n_top_words):
    words = count_vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(model.components_):
        print("\nTopic #%d:" % topic_idx)
        print(" ".join([words[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

# get and clean up permit text further
def get_clean_permit_text(year):
    # Read data into permits
    if year == 2018:
        permits = utilities.getPermits2018()
    if year == 2010:
        permits = utilities.getPermits2010()

    # only keep relevant columns
    permits = permits[['OBJECTID', 'PERMIT_ID', 'PERMIT_TYPE_NAME' ,'DESC_OF_WORK', 'NEIGHBORHOODCLUSTER', 'FEES_PAID', 'OWNER_NAME', 'FEE_TYPE', 'PERMIT_APPLICANT', 'PERMIT_SUBTYPE_NAME']]
    
    # remove rows with 'nan' and punctuation then convert to lower case
    permits.drop(permits[permits['DESC_OF_WORK'] == 'nan'].index, inplace=True)
    permits['DESC_OF_WORK'] = permits['DESC_OF_WORK'].map(lambda x: re.sub('[,\.!?]', '', x))
    permits['DESC_OF_WORK'] = permits['DESC_OF_WORK'].map(lambda x: x.lower())
    return permits


def main(): 
    permits2010 = get_clean_permit_text(2010)
    permits2018 = get_clean_permit_text(2018)
    print('--- 2010 ---')
    wordcloud_permit_text(permits2010)
    LDA_find_top_topics(permits2010)
    print('--- 2018 ---')
    wordcloud_permit_text(permits2018)
    LDA_find_top_topics(permits2018)

if __name__ == "__main__":
    main()



