#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing the important libraries
import numpy as np
import pandas as pd
# pd.set_option('display.max_colwidth', -1)
# pd.set_option('display.max_rows', None)


# In[2]:


#loading the datasets into a dataframe
korean = pd.read_csv('KoreanMovies.csv')
thailand = pd.read_csv('ThaiLandMovies.csv')
chinese = pd.read_csv('ChineseMovies.csv')
hongkong =pd.read_csv('HongKongMovies.csv')


# In[3]:


#concatenating all the dataframes since they have the same columns
asian_df = pd.concat([korean, thailand, chinese, hongkong])


# In[4]:


#checking out the first 5 rows of the dataframe
asian_df.head()


# In[5]:


#checking the shape of the dataframe
asian_df.shape


# In[6]:


#checking for null values in the dataframe
asian_df.isna().sum()


# In[7]:


#dropping duplicated values in the dataframe
asian_df = asian_df.drop_duplicates()
#checking the shape of the dataframe again
asian_df.shape


# In[8]:


#getting a column named episodes from the genre column and also cleaning the episodes column.
asian_df['Episodes'] = asian_df['Genre'].apply(lambda x: str(x).split('|')[-1])
asian_df['Genre'] = asian_df['Genre'].apply(lambda x: str(x).split('|')[0])
asian_df['Episodes'] = asian_df['Episodes'].replace(r'(\D)', '', regex=True)


# In[9]:


#getting the year column from the title column and also cleaning the year and title column
asian_df['Year'] = asian_df['Title'].apply(lambda x: str(x).split('(')[-1])
asian_df['Year'] = asian_df['Year'].apply(lambda x: str(x).split(')')[0])
asian_df['Title'] = asian_df['Title'].replace(r'(\d\d\d\d)', '', regex=True)
asian_df['Title']= asian_df['Title'].replace(r'(\(\))', '', regex=True)


# In[10]:


#cleaning the rating column by converting all the words to numbers
asian_df['Rating'] = asian_df['Rating'].replace(r'(\&)', '.5', regex=True)
asian_df['Rating'] = asian_df['Rating'].str.replace('Half', '')
asian_df['Rating'] = asian_df['Rating'].str.replace('Stars', '')
asian_df['Rating'] = asian_df['Rating'].str.replace('Star', '')
asian_df['Rating'] = asian_df['Rating'].str.replace('Three', '3')
asian_df['Rating'] = asian_df['Rating'].str.replace('Two', '2')
asian_df['Rating'] = asian_df['Rating'].str.replace('One', '1')
asian_df['Rating'] = asian_df['Rating'].str.replace('Four', '4')
asian_df['Rating'] = asian_df['Rating'].str.replace('Five', '5')
asian_df['Rating'] = asian_df['Rating'].str.replace(' ', '')
asian_df['Rating'] = asian_df['Rating'].str.replace('NotRated', '0')


# In[11]:


#checking for unique values in the rating column to ensure it is now clean.
asian_df['Rating'].unique()


# In[12]:


#replcing symbols with empty soace
asian_df['Casts'] = asian_df['Casts'].replace(r'(\\n)', ':', regex=True)
asian_df['Casts'] = asian_df['Casts'].replace(r"['\{|\}|\"|:]", '', regex=True)
#replacing the role each actor played & some unwanted values  with an empty string
asian_df.Casts = asian_df['Casts'].str.replace('Regular Member', '')
asian_df.Casts = asian_df['Casts'].str.replace('Guest', '')
asian_df.Casts = asian_df['Casts'].str.replace('Main Host', '')
asian_df.Casts = asian_df['Casts'].str.replace('supporting role', '')
asian_df.Casts = asian_df['Casts'].str.replace('main role', '')
asian_df.Casts = asian_df['Casts'].str.replace('role', '')
asian_df.Casts = asian_df['Casts'].str.replace('/', '')
asian_df.Casts = asian_df['Casts'].str.replace(r'(\(.*?\))', '', regex=True)
asian_df.Casts = asian_df['Casts'].str.replace(r'\[[^()]*\]', '', regex=True)


# In[13]:


#converting all description, casts entries to lowercase
asian_df['Description'] = asian_df['Description'].astype(str).apply(lambda x: x.lower())
asian_df['Casts'] = asian_df['Casts'].astype(str).apply(lambda x: x.lower())
asian_df['Genre'] = asian_df['Genre'].astype(str).apply(lambda x: x.lower())
asian_df['Country'] = asian_df['Country'].astype(str).apply(lambda x: x.lower())
#removing punctuations from the description column
asian_df['Description'] = asian_df['Description'].replace(r'[^\w\s\$]', '', regex=True)


# In[14]:


asian_df.loc[(asian_df.Casts == "not available")]


# In[15]:


#replacing the not available column with null values
asian_df.loc[(asian_df.Casts == 'not available'), 'Casts'] = ''
asian_df.loc[(asian_df.Casts == "not available")]


# In[16]:


asian_df['Year'].unique()


# In[17]:


asian_df['Year'] = asian_df['Year'].replace(('Hall of Comedy - The Beginning', 'Views', 'Upcoming Dramas', 'Legend of The Raiders', 'Little Bird'),
                                    (np.nan, np.nan, np.nan, np.nan, np.nan))


# In[18]:


#filling the year column with 2021 and converting to integer. 2021 is the max year
asian_df['Year'].fillna('2021', inplace=True)
#converting the numeric column to their right datatype
asian_df['Rating'] = pd.to_numeric(asian_df['Rating'])
#asian_df['Episodes'] = asian_df['Episodes'].astype(int)
asian_df['Year'] = asian_df['Year'].astype(int)


# In[19]:


#checking out the first 5 rows of the dataframe
asian_df.head()


# In[20]:


asian_df.fillna("", inplace=True)


# In[21]:


asian_df.dtypes


# In[22]:


asian_df.isna().sum()


# In[23]:


asian_df['Genre'] = asian_df['Genre'].str.split(',')
asian_df['Genre1'] = asian_df['Genre'].apply(lambda x: x[0])

# Some of the movies have only one genre. In such cases, assign the same genre to 'genre_2' as well
asian_df['Genre2'] = asian_df['Genre'].apply(lambda x: x[1] if len(x) > 1 else x[0])
asian_df['Genre3'] = asian_df['Genre'].apply(lambda x: x[2] if len(x) > 2 else x[0])
asian_df['Genre4'] = asian_df['Genre'].apply(lambda x: x[3] if len(x) > 3 else x[0])
asian_df['Genre5'] = asian_df['Genre'].apply(lambda x: x[4] if len(x) > 4 else x[0])
asian_df['Genre6'] = asian_df['Genre'].apply(lambda x: x[5] if len(x) > 5 else x[0])


# In[24]:


asian_df.head()


# In[25]:


asian_df['Casts'] = asian_df['Casts'].str.lstrip(',')


# In[26]:


asian_df.head()


# In[27]:


asian_df['Casts'] = asian_df['Casts'].str.split(',')
asian_df['Cast1'] = asian_df['Casts'].apply(lambda x: x[0])

# Some of the movies have only one genre. In such cases, assign the same genre to 'genre_2' as well
asian_df['Cast2'] = asian_df['Casts'].apply(lambda x: x[1] if len(x) > 1 else x[0])
asian_df['Cast3'] = asian_df['Casts'].apply(lambda x: x[2] if len(x) > 2 else x[0])
asian_df['Cast4'] = asian_df['Casts'].apply(lambda x: x[3] if len(x) > 3 else x[0])
asian_df['Cast5'] = asian_df['Casts'].apply(lambda x: x[4] if len(x) > 4 else x[0])
asian_df['Cast6'] = asian_df['Casts'].apply(lambda x: x[5] if len(x) > 5 else x[0])


# In[28]:


asian_df.isna().sum()


# In[29]:


asian_df.drop(['Release year', 'Casts', 'Genre'], inplace=True, axis=1)


# In[30]:


#saving to a new csv file
asian_df.to_csv("cleanedmovies.csv", index=False)


# In[ ]:




