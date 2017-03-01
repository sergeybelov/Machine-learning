# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 15:08:44 2017

@author: tehn-11
"""

#==============================================================================
#  Анализ текстов
#==============================================================================
from sklearn import datasets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

#==============================================================================
# Для начала вам потребуется загрузить данные. 
# В этом задании мы воспользуемся одним из датасетов, доступных в scikit-learn'е — 20 newsgroups. 
# Для этого нужно воспользоваться модулем datasets:
#==============================================================================
newsgroups = datasets.fetch_20newsgroups(
                    subset='all', 
                    categories=['alt.atheism', 'sci.space']
             )

#==============================================================================
# Вычислите TF-IDF-признаки для всех текстов. 
# Обратите внимание, что в этом задании мы предлагаем вам вычислить TF-IDF по всем данным. 
# При таком подходе получается, что признаки на обучающем множестве используют информацию из тестовой выборки — но такая ситуация вполне законна, 
# поскольку мы не используем значения целевой переменной из теста. 
# На практике нередко встречаются ситуации, когда признаки объектов тестовой выборки известны на момент обучения, 
# и поэтому можно ими пользоваться при обучении алгоритма.
#==============================================================================

#В Scikit-Learn это реализовано в классе 
#sklearn.feature_extraction.text.TfidfVectorizer. 
#Преобразование обучающей выборки нужно делать с помощью функции fit_transform, тестовой — с помощью transform.
y_train = newsgroups.target#Класс
X_train = newsgroups.data#Характеристики

#X_train = ["this is some food", "this is some drink", "this is some apple", "this is an orange", "this is an table"]
#y_train = [1,2,3,4,5]

vectorizer = TfidfVectorizer()
dataMatrix=vectorizer.fit_transform(X_train).toarray()#матрица объектов по словам, в ячейках веса слов

#idf = vectorizer.idf_
words=vectorizer.get_feature_names()
#tf_idf=dict(zip(words, idf))#токены с весами


#==============================================================================
# Подберите минимальный лучший параметр C из множества [10^-5, 10^-4, ... 10^4, 10^5] для SVM с линейным ядром (kernel='linear') 
# при помощи кросс-валидации по 5 блокам. Укажите параметр random_state=241 и для SVM, и для KFold. 
# В качестве меры качества используйте долю верных ответов (accuracy).
#==============================================================================

grid = {'C': np.power(10.0, np.arange(-5, 6))}
cv = KFold(n_splits=5, shuffle=True, random_state=241)
clf = SVC(kernel='linear', random_state=241)
gs = GridSearchCV(clf, grid, scoring='accuracy', cv=cv)
gs.fit(dataMatrix, y_train)

#записываем параметры в массив
params=gs.cv_results_['params']

validationTest={}
for a in gs.grid_scores_:
    validationTest[a.mean_validation_score]=a.parameters# — оценка качества по кросс-валидации и значения параметров
    
#==============================================================================
# Обучите SVM по всей выборке с оптимальным параметром C, найденным на предыдущем шаге.
#==============================================================================

#У GridSearchCV есть поле best_estimator_, 
#которое можно использовать, чтобы не обучать заново классификатор с оптимальным параметром.

#==============================================================================
# Найдите 10 слов с наибольшим абсолютным значением веса (веса хранятся в поле coef_ у svm.SVC). 
# Они являются ответом на это задание. Укажите эти слова через запятую или пробел, в нижнем регистре, в лексикографическом порядке.
# 
#==============================================================================
