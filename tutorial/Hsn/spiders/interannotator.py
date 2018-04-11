
# coding: utf-8

# In[653]:


import pandas as pd
import numpy as np
import re

data = pd.read_csv("training.csv")
data.head()
data2=[]
# 11 categories are as follows 'Beauty', 'Coins & Collectibles', 'Toys & Games', 'Home',
#'Fan Shop', 'Kitchen & Food', 'Health & Fitness', 'Electronics', 'Jewelry', 'Crafts & Sewing', 'Fashion'

print(data.shape)

baseline_acc = 9544/len(data)
print("Baseline accuracy = " + str(len(data)))

# clean up by removing punctuations and non eng characters
def clean_text(string):
    return re.sub('[^A-Za-z0-9]+', ' ', string)

for index, i in data.iterrows():
    i["Item Name"] = clean_text(i["Item Name"])





X = data["Item Name"]
y = data["Category"] 

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=1)

# check if train and test datasets are the right shape
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)


# In[663]:


# count vectorizer
from sklearn.feature_extraction.text import CountVectorizer
vect = CountVectorizer(stop_words='english')
X_train_dtm = vect.fit_transform(X_train)
X_test_dtm = vect.transform(X_test)

# each row is a message
# every column is a feature with its count
print(X_train_dtm.shape)
print(X_test_dtm.shape)


# ### Naive Bayes
# 

# In[684]:


from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

nb = MultinomialNB()
get_ipython().run_line_magic('time', 'nb.fit(X_train_dtm, y_train)')


# In[685]:


from sklearn import metrics

# test model accuracy
y_pred_class = nb.predict(X_test_dtm)
accuracy = metrics.accuracy_score(y_test, y_pred_class)
print("Test accuracy for Naive Bayes = " + str(accuracy))


# In[683]:


from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

sns.heatmap(confusion_matrix(y_test, y_pred_class), annot=True, fmt="2.0f")
plt.show()


# ### Logistic Regression

# In[680]:


from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression()
get_ipython().run_line_magic('time', 'logreg.fit(X_train_dtm, y_train)')


# In[681]:


y_pred_class = logreg.predict(X_test_dtm)
accuracy = metrics.accuracy_score(y_test, y_pred_class)
print("Test accuracy for Logistic Regression = " + str(accuracy))


# In[669]:


sns.heatmap(confusion_matrix(y_test, y_pred_class), annot=True, fmt="2.0f")
plt.show()


# ### Random Forest

# In[678]:


from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=15)
get_ipython().run_line_magic('time', 'rf.fit(X_train_dtm, y_train)')


# In[679]:


y_pred_class = rf.predict(X_test_dtm)
print("Test accuracy for Random Forest = ", metrics.accuracy_score(y_test, y_pred_class))


# In[672]:


sns.heatmap(confusion_matrix(y_test, y_pred_class), annot=True, fmt="2.0f")
plt.show()


# ### Decision Trees

# In[673]:


from sklearn.tree import DecisionTreeClassifier

tree = DecisionTreeClassifier()
get_ipython().run_line_magic('time', 'tree.fit(X_train_dtm, y_train)')


# In[674]:


y_pred_class = tree.predict(X_test_dtm)
print("Test accuracy for Decision Tree = ", metrics.accuracy_score(y_pred_class, y_test))


# In[675]:


sns.heatmap(confusion_matrix(y_test, y_pred_class), annot=True, fmt="2.0f")
plt.show()

