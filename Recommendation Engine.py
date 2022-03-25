#!/usr/bin/env python
# coding: utf-8

# In[1]:


# lets import the basic Libraries
import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')


# In[2]:


#reading the cleaned data into a database
movies_df = pd.read_csv('cleanedmovies.csv')


# In[3]:


#printing the first 5 rows of the database
movies_df.head()


# In[4]:


#checking the types of the columns
movies_df.dtypes


# In[5]:


#checking for null values
movies_df.isna().sum()


# In[6]:


#filling the null values with an empty space
movies_df.fillna("", inplace =True)


# In[7]:


#checking out the columns of a dataframe
movies_df.columns


# In[8]:


#selecting the features to be used for building our recommendation system
features = ['Title', 'Description', 'Country','Genre1', 'Genre2', 'Genre3', 'Genre4', 'Genre5', 'Genre6', 'Cast1', 'Cast2', 'Cast3', 'Cast4', 'Cast5', 'Cast6']


# In[9]:


#concatenating the columns together
selected_features= movies_df['Title']+' '+ movies_df['Description']+' '+movies_df['Country']+' '+movies_df['Genre1']+' '+movies_df['Genre2']+' '+movies_df['Genre3']+' '+movies_df['Genre4']+' '+movies_df['Genre5']+' '+['Genre6']+' '+['Cast1']+' '+['Cast2']+' '+['Cast3']+' '+['Cast4']+' '+['Cast5']+' '+['Cast6']


# In[10]:


#checking out the concatenated columns
selected_features


# In[11]:


#initializing the tfidf vectorizer
vectorizer = TfidfVectorizer()


# In[12]:


#using the tfidf vectorizer on the selected features.
feature_vectors = vectorizer.fit_transform(selected_features)


# In[13]:


print(feature_vectors)


# In[14]:


#checking the similarity between the feature vectors
similarity = cosine_similarity(feature_vectors)


# In[15]:


print(similarity)


# In[16]:


print(similarity.shape)


# In[ ]:



movie_name = input('Enter your favorte movie:')


# In[ ]:


movies_df['Title'] = movies_df['Title'].str.rstrip()


# In[ ]:


list_of_all_title = movies_df['Title'].tolist()
print(list_of_all_title)


# In[ ]:


find_close_match = difflib.get_close_matches(movie_name, list_of_all_title)
print(find_close_match)


# In[ ]:


close_match = find_close_match[2]
print(close_match)


# In[ ]:


#find the index of the movie title
index_of_the_movie = movies_df[movies_df.Title == close_match].index.values[0]
print(index_of_the_movie)


# In[ ]:


sim_score = list(enumerate(similarity[index_of_the_movie]))


# In[ ]:


len(sim_score)


# In[ ]:


#sorting the movies based on their similarity score
sorted_similar_movies = sorted(sim_score, key = lambda x:x[1], reverse=True)
print(sorted_similar_movies[:10])


# In[ ]:


#print the name of similar movies based on the index

print("Movies suggested for you : \n")

i = 1

for movie in sorted_similar_movies:
    index = movie[0]
    title_from_index = movies_df[movies_df.index == index]['Title'].values[0]
    if i<30:
        print(i, '-', title_from_index)
        i += 1
    


# # Putting everything together in a function.

# In[ ]:


def movie_rec_system(movie_name):
    if movie_name in movies_df['Title']:
        list_of_all_title = movies_df['Title'].tolist()
        find_close_match = difflib.get_close_matches(movie_name, list_of_all_title)
        close_match = find_close_match[2]
        index_of_the_movie = movies_df[movies_df.Title == close_match].index.values[0]
        sim_score = list(enumerate(similarity[index_of_the_movie]))
        sorted_similar_movies = sorted(sim_score, key = lambda x:x[1], reverse=True)

        print("Movies suggested for you : \n")

        i = 1

        for movie in sorted_similar_movies:
            index = movie[0]
            title_from_index = movies_df[movies_df.index == index]['Title'].values[0]
            if i<15:
                print(i, '-', title_from_index)
                i += 1
    else:
         print("This movie is not found in our database. Please check out the following movies \n", movies_df[['Title', 'Country', 'Genre2']].sample(10).reset_index(drop=True))


# In[ ]:


movie_name = input('Enter your favorte movie:')
movie_rec_system(movie_name)


# In[ ]:




