#!/usr/bin/env python
# coding: utf-8

# <p style="text-align:center">
#     <a href="https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkML0101ENSkillsNetwork1047-2023-01-01">
#     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo"  />
#     </a>
# </p>
# 
# 
# # Classification with Python
# 
# 
# Estimated time needed: **25** minutes
#     
# 
# ## Objectives
# 
# After completing this lab you will be able to:
# 
# * Confidently create classification models
# 

# In this notebook we try to practice all the classification algorithms that we learned in this course.
# 
# We load a dataset using Pandas library, apply the following algorithms, and find the best one for this specific dataset by accuracy evaluation methods.
# 
# Let's first load required libraries:
# 

# In[6]:


import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
from sklearn import preprocessing
get_ipython().run_line_magic('matplotlib', 'inline')


# ### About dataset
# 

# This dataset is about the performance of basketball teams. The __cbb.csv__ data set includes performance data about five seasons of 354 basketball teams. It includes the following fields:
# 
# | Field          | Description                                                                           |
# |----------------|---------------------------------------------------------------------------------------|
# |TEAM |	The Division I college basketball school|
# |CONF|	The Athletic Conference in which the school participates in (A10 = Atlantic 10, ACC = Atlantic Coast Conference, AE = America East, Amer = American, ASun = ASUN, B10 = Big Ten, B12 = Big 12, BE = Big East, BSky = Big Sky, BSth = Big South, BW = Big West, CAA = Colonial Athletic Association, CUSA = Conference USA, Horz = Horizon League, Ivy = Ivy League, MAAC = Metro Atlantic Athletic Conference, MAC = Mid-American Conference, MEAC = Mid-Eastern Athletic Conference, MVC = Missouri Valley Conference, MWC = Mountain West, NEC = Northeast Conference, OVC = Ohio Valley Conference, P12 = Pac-12, Pat = Patriot League, SB = Sun Belt, SC = Southern Conference, SEC = South Eastern Conference, Slnd = Southland Conference, Sum = Summit League, SWAC = Southwestern Athletic Conference, WAC = Western Athletic Conference, WCC = West Coast Conference)|
# |G|	Number of games played|
# |W|	Number of games won|
# |ADJOE|	Adjusted Offensive Efficiency (An estimate of the offensive efficiency (points scored per 100 possessions) a team would have against the average Division I defense)|
# |ADJDE|	Adjusted Defensive Efficiency (An estimate of the defensive efficiency (points allowed per 100 possessions) a team would have against the average Division I offense)|
# |BARTHAG|	Power Rating (Chance of beating an average Division I team)|
# |EFG_O|	Effective Field Goal Percentage Shot|
# |EFG_D|	Effective Field Goal Percentage Allowed|
# |TOR|	Turnover Percentage Allowed (Turnover Rate)|
# |TORD|	Turnover Percentage Committed (Steal Rate)|
# |ORB|	Offensive Rebound Percentage|
# |DRB|	Defensive Rebound Percentage|
# |FTR|	Free Throw Rate (How often the given team shoots Free Throws)|
# |FTRD|	Free Throw Rate Allowed|
# |2P_O|	Two-Point Shooting Percentage|
# |2P_D|	Two-Point Shooting Percentage Allowed|
# |3P_O|	Three-Point Shooting Percentage|
# |3P_D|	Three-Point Shooting Percentage Allowed|
# |ADJ_T|	Adjusted Tempo (An estimate of the tempo (possessions per 40 minutes) a team would have against the team that wants to play at an average Division I tempo)|
# |WAB|	Wins Above Bubble (The bubble refers to the cut off between making the NCAA March Madness Tournament and not making it)|
# |POSTSEASON|	Round where the given team was eliminated or where their season ended (R68 = First Four, R64 = Round of 64, R32 = Round of 32, S16 = Sweet Sixteen, E8 = Elite Eight, F4 = Final Four, 2ND = Runner-up, Champion = Winner of the NCAA March Madness Tournament for that given year)|
# |SEED|	Seed in the NCAA March Madness Tournament|
# |YEAR|	Season
# 

# ### Load Data From CSV File  
# 

# Let's load the dataset [NB Need to provide link to csv file]
# 

# In[7]:


df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillsNetwork/labs/Module%206/cbb.csv')
df.head()


# In[8]:


df.shape


# ## Add Column
# Next we'll add a column that will contain "true" if the wins above bubble are over 7 and "false" if not. We'll call this column Win Index or "windex" for short. 
# 

# In[9]:


df['windex'] = np.where(df.WAB > 7, 'True', 'False')


# # Data visualization and pre-processing
# 
# 

# Next we'll filter the data set to the teams that made the Sweet Sixteen, the Elite Eight, and the Final Four in the post season. We'll also create a new dataframe that will hold the values with the new column.
# 

# In[10]:


df1 = df.loc[df['POSTSEASON'].str.contains('F4|S16|E8', na=False)]
df1.head()


# In[11]:


df1['POSTSEASON'].value_counts()


# 32 teams made it into the Sweet Sixteen, 16 into the Elite Eight, and 8 made it into the Final Four over 5 seasons. 
# 

# Lets plot some columns to underestand the data better:
# 

# In[12]:


# notice: installing seaborn might takes a few minutes
get_ipython().system('conda install -c anaconda seaborn -y')


# In[8]:


import seaborn as sns

bins = np.linspace(df1.BARTHAG.min(), df1.BARTHAG.max(), 10)
g = sns.FacetGrid(df1, col="windex", hue="POSTSEASON", palette="Set1", col_wrap=6)
g.map(plt.hist, 'BARTHAG', bins=bins, ec="k")

g.axes[-1].legend()
plt.show()


# In[9]:


bins = np.linspace(df1.ADJOE.min(), df1.ADJOE.max(), 10)
g = sns.FacetGrid(df1, col="windex", hue="POSTSEASON", palette="Set1", col_wrap=2)
g.map(plt.hist, 'ADJOE', bins=bins, ec="k")

g.axes[-1].legend()
plt.show()


# # Pre-processing:  Feature selection/extraction
# 

# ### Lets look at how Adjusted Defense Efficiency plots
# 

# In[10]:


bins = np.linspace(df1.ADJDE.min(), df1.ADJDE.max(), 10)
g = sns.FacetGrid(df1, col="windex", hue="POSTSEASON", palette="Set1", col_wrap=2)
g.map(plt.hist, 'ADJDE', bins=bins, ec="k")
g.axes[-1].legend()
plt.show()


# We see that this data point doesn't impact the ability of a team to get into the Final Four. 
# 

# ## Convert Categorical features to numerical values
# 

# Lets look at the postseason:
# 

# In[13]:


df1.groupby(['windex'])['POSTSEASON'].value_counts(normalize=True)


# 13% of teams with 6 or less wins above bubble make it into the final four while 17% of teams with 7 or more do.
# 

# Lets convert wins above bubble (winindex) under 7 to 0 and over 7 to 1:
# 

# In[14]:


df1['windex'].replace(to_replace=['False','True'], value=[0,1],inplace=True)
df1.head()


# ### Feature selection
# 

# Let's define feature sets, X:
# 

# In[15]:


X = df1[['G', 'W', 'ADJOE', 'ADJDE', 'BARTHAG', 'EFG_O', 'EFG_D',
       'TOR', 'TORD', 'ORB', 'DRB', 'FTR', 'FTRD', '2P_O', '2P_D', '3P_O',
       '3P_D', 'ADJ_T', 'WAB', 'SEED', 'windex']]
X[0:5]


# What are our lables? Round where the given team was eliminated or where their season ended (R68 = First Four, R64 = Round of 64, R32 = Round of 32, S16 = Sweet Sixteen, E8 = Elite Eight, F4 = Final Four, 2ND = Runner-up, Champion = Winner of the NCAA March Madness Tournament for that given year)|
# 

# In[16]:


y = df1['POSTSEASON'].values
y[0:5]


# ## Normalize Data 
# 

# Data Standardization gives data zero mean and unit variance (technically should be done after train test split )
# 

# In[17]:


X= preprocessing.StandardScaler().fit(X).transform(X)
X[0:5]


# ## Training and Validation 
# 

# Split the data into Training and Validation data.
# 

# In[18]:


# We split the X into train and test to find the best k
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=4)
print ('Train set:', X_train.shape,  y_train.shape)
print ('Validation set:', X_val.shape,  y_val.shape)


# # Classification 
# 

# Now, it is your turn, use the training set to build an accurate model. Then use the validation set  to report the accuracy of the model
# You should use the following algorithm:
# - K Nearest Neighbor(KNN)
# - Decision Tree
# - Support Vector Machine
# - Logistic Regression
# 
# 

# # K Nearest Neighbor(KNN)
# 
# <b>Question  1 </b> Build a KNN model using a value of k equals five, find the accuracy on the validation data (X_val and y_val)
# 

# You can use <code> accuracy_score</cdoe>
# 

# In[38]:


from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

k=5
neigh = KNeighborsClassifier(n_neighbors=k).fit(X_train, y_train)

print("Validation set accuraracy: ", accuracy_score(y_val, neigh.predict(X_val)))


# <b>Question  2</b> Determine and print the accuracy for the first 15 values of k on the validation data:
# 

# In[22]:


Ks = 16
mean_acc = np.zeros((Ks-1))
std_acc = np.zeros((Ks-1))

for n in range(1,Ks):
    neigh = KNeighborsClassifier(n_neighbors = n).fit(X_train,y_train)
    yhat=neigh.predict(X_val)
    mean_acc[n-1] = accuracy_score(y_val, yhat)

    std_acc[n-1]=np.std(yhat==y_val)/np.sqrt(yhat.shape[0])

mean_acc


# # Decision Tree
# 

# The following lines of code fit a <code>DecisionTreeClassifier</code>:
# 

# In[48]:


from sklearn.tree import DecisionTreeClassifier


# <b>Question  3</b> Determine the minumum   value for the parameter <code>max_depth</code> that improves results 
# 

# In[50]:


DecTree = DecisionTreeClassifier(criterion="entropy", max_depth=4)
DecTree.fit(X_train,y_train)

max_depth = 8
accuracy = []

for n in range(1,max_depth):
   
    DecTree_tmp = DecisionTreeClassifier(criterion="entropy", max_depth=n)
    DecTree_tmp.fit(X_train, y_train)
    
    score = DecTree_tmp.score(X_val, y_val)
    accuracy.append(score)

    
print(accuracy)
print("Min max_depth:", accuracy.index(min(accuracy))+1)


# # Support Vector Machine
# 

# <b>Question  4</b> Train the support  vector machine model and determine the accuracy on the validation data for each kernel. Find the kernel (linear, poly, rbf, sigmoid) that provides the best score on the validation data and train a SVM using it.
# 

# In[1]:


from sklearn import svm


# In[44]:


svmlinear = svm.SVC(kernel='linear')
svmlinear.fit(X_train, y_train)

yhatlinear = svmlinear.predict(X_val)

print('Linear accuracy: ', accuracy_score(y_val, yhatlinear))

svmrbf = svm.SVC(kernel='rbf')
svmrbf.fit(X_train, y_train)

yhatrbf = svmrbf.predict(X_val)

print('RBF accuracy: ', accuracy_score(y_val, yhatrbf))

svmpoly = svm.SVC(kernel='poly')
svmpoly.fit(X_train, y_train)

yhatpoly = svmpoly.predict(X_val)

print('Poly accuracy: ', accuracy_score(y_val, yhatpoly))

svmsig = svm.SVC(kernel='sigmoid')
svmsig.fit(X_train, y_train)

yhatsig = svmsig.predict(X_val)

print('Sigmoid accuracy: ', accuracy_score(y_val, yhatsig))

print('Poly model is best')


# # Logistic Regression
# 

# <b>Question 5</b> Train a logistic regression model and determine the accuracy of the validation data (set C=0.01)
# 

# In[26]:


from sklearn.linear_model import LogisticRegression


# In[45]:


LR = LogisticRegression(C=0.01, solver='liblinear').fit(X_train,y_train)
yhat = LR.predict(X_val)
accuracy_score(y_val, yhat)


# # Model Evaluation using Test set
# 

# In[33]:


from sklearn.metrics import f1_score
# for f1_score please set the average parameter to 'micro'
from sklearn.metrics import log_loss


# In[34]:


def jaccard_index(predictions, true):
    if (len(predictions) == len(true)):
        intersect = 0;
        for x,y in zip(predictions, true):
            if (x == y):
                intersect += 1
        return intersect / (len(predictions) + len(true) - intersect)
    else:
        return -1


# <b>Question  5</b> Calculate the  F1 score and Jaccard score for each model from above. Use the Hyperparameter that performed best on the validation data. **For f1_score please set the average parameter to 'micro'.**
# 

# ### Load Test set for evaluation 
# 

# In[35]:


test_df = pd.read_csv('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0120ENv3/Dataset/ML0101EN_EDX_skill_up/basketball_train.csv',error_bad_lines=False)
test_df.head()


# In[36]:


test_df['windex'] = np.where(test_df.WAB > 7, 'True', 'False')
test_df1 = test_df[test_df['POSTSEASON'].str.contains('F4|S16|E8', na=False)]
test_Feature = test_df1[['G', 'W', 'ADJOE', 'ADJDE', 'BARTHAG', 'EFG_O', 'EFG_D',
       'TOR', 'TORD', 'ORB', 'DRB', 'FTR', 'FTRD', '2P_O', '2P_D', '3P_O',
       '3P_D', 'ADJ_T', 'WAB', 'SEED', 'windex']]
test_Feature['windex'].replace(to_replace=['False','True'], value=[0,1],inplace=True)
test_X=test_Feature
test_X= preprocessing.StandardScaler().fit(test_X).transform(test_X)
test_X[0:5]


# In[37]:


test_y = test_df1['POSTSEASON'].values
test_y[0:5]


# KNN
# 

# In[47]:


print('KNN F1 score: ', f1_score(test_y, neigh.predict(test_X), average='micro'))
print('KNN Jaccard index: ', jaccard_index(neigh.predict(test_X), test_y))


# Decision Tree
# 

# In[51]:


print('Dec Tree F1 score: ', f1_score(test_y, DecTree.predict(test_X), average='micro'))
print('Dec Tree Jaccard index: ', jaccard_index(DecTree.predict(test_X), test_y))


# SVM
# 

# In[52]:


print('SVM Poly F1 score: ', f1_score(test_y, svmpoly.predict(test_X), average='micro'))
print('SCM Poly Jaccard index: ', jaccard_index(svmpoly.predict(test_X), test_y))


# Logistic Regression
# 

# In[53]:


print('Log Reg F1 score: ', f1_score(test_y, LR.predict(test_X), average='micro'))
print('Log Reg Jaccard index: ', jaccard_index(LR.predict(test_X), test_y))


# # Report
# You should be able to report the accuracy of the built model using different evaluation metrics:
# 

# | Algorithm          | Accuracy | Jaccard  | F1-score  | LogLoss |
# |--------------------|----------|----------|-----------|---------|
# | KNN                |     ?    |     ?    |     ?     | NA      |
# | Decision Tree      |     ?    |     ?    |     ?     | NA      |
# | SVM                |     ?    |     ?    |     ?     | NA      |
# | LogisticRegression |     ?    |     ?    |     ?     |     ?   |
# 

# Something to keep in mind when creating models to predict the results of basketball tournaments or sports in general is that is quite hard due to so many factors influencing the game. Even in sports betting an accuracy of 55% and over is considered good as it indicates profits.
# 

# <h2>Want to learn more?</h2>
# 
# IBM SPSS Modeler is a comprehensive analytics platform that has many machine learning algorithms. It has been designed to bring predictive intelligence to decisions made by individuals, by groups, by systems – by your enterprise as a whole. A free trial is available through this course, available here: <a href="https://www.ibm.com/analytics/spss-statistics-software?utm_source=Exinfluencer&utm_content=000026UJ&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkML0101ENSkillsNetwork1047-2023-01-01&utm_medium=Exinfluencer&utm_term=10006555">SPSS Modeler</a>
# 
# Also, you can use Watson Studio to run these notebooks faster with bigger datasets. Watson Studio is IBM's leading cloud solution for data scientists, built by data scientists. With Jupyter notebooks, RStudio, Apache Spark and popular libraries pre-packaged in the cloud, Watson Studio enables data scientists to collaborate on their projects without having to install anything. Join the fast-growing community of Watson Studio users today with a free account at <a href="https://www.ibm.com/cloud/watson-studio?utm_source=Exinfluencer&utm_content=000026UJ&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkML0101ENSkillsNetwork1047-2023-01-01&utm_medium=Exinfluencer&utm_term=10006555">Watson Studio</a>
# 
# 

# ### Thank you for completing this lab!
# 
# 
# ## Author
# 
# Saeed Aghabozorgi
# 
# 
# ### Other Contributors
# 
# <a href="https://www.linkedin.com/in/joseph-s-50398b136/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkML0101ENSkillsNetwork1047-2023-01-01">Joseph Santarcangelo</a>
# 
# 
# 
# 
# ## Change Log
# 
# 
# |  Date (YYYY-MM-DD) |  Version | Changed By  |  Change Description |
# |---|---|---|---|
# |2021-04-03   | 2.1  | Malika Singla| Updated the Report accuracy |
# | 2020-08-27  | 2.0  | Lavanya  |  Moved lab to course repo in GitLab |
# |   |   |   |   |
# |   |   |   |   |
# 
# 
# ## <h3 align="center"> © IBM Corporation 2020. All rights reserved. <h3/>
# 
