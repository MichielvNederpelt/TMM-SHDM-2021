import pandas as pd
import numpy as np
#import nltk
#nltk.download('averaged_perceptron_tagger')
#from nltk.stem import WordNetLemmatizer
#nltk.download('wordnet')
from sklearn.feature_extraction import DictVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import csv

from sklearn import metrics

trainfile = 'data/SEM-2012-SharedTask-CD-SCO-training-simple.v2.features.conll'
#testfile = 'data/SEM-2012-SharedTask-CD-SCO-dev-simple.v2.features.conll'
testfile = 'data/bioscope.clinical.columns.features.conll'
training_path_opt ='data/SEM-2012-SharedTask-CD-SCO-training-simple.v2.features.conll'
dev_path_opt = 'data/SEM-2012-SharedTask-CD-SCO-dev-simple.v2.features.conll'

def create_vectorizer_and_classifier(features, labels):
    '''
    Function that takes feature-value pairs and gold labels as input and trains a logistic regression classifier
    
    :param features: feature-value pairs
    :param labels: gold labels
    :type features: a list of dictionaries
    :type labels: a list of strings
    
    :return svm_classifier: a trained SVM classifier
    :return vec: a DictVectorizer to which the feature values are fitted. 
    '''
    
    vec = DictVectorizer()
    #fit creates a mapping between observed feature values and dimensions in a one-hot vector, transform represents the current values as a vector 
    tokens_vectorized = vec.fit_transform(features)
    svm_classifier = LinearSVC()   
    svm_classifier.fit(tokens_vectorized, labels)
    
    return svm_classifier, vec

def print_confusion_matrix(predictions, goldlabels):
    '''
    Function that prints out a confusion matrix
    
    :param predictions: predicted labels
    :param goldlabels: gold standard labels
    :type predictions, goldlabels: list of strings
    ''' 
    
    #based on example from https://datatofish.com/confusion-matrix-python/ 
    data = {'Gold':    goldlabels[1:], 'Predicted': predictions[1:]    }
    df = pd.DataFrame(data, columns=['Gold','Predicted'])

    confusion_matrix = pd.crosstab(df['Gold'], df['Predicted'], rownames=['Gold'], colnames=['Predicted'])
    print (confusion_matrix)


def print_precision_recall_fscore(predictions, goldlabels):
    '''
    Function that prints out precision, recall and f-score
    
    :param predictions: predicted output by classifier
    :param goldlabels: original gold labels
    :type predictions, goldlabels: list of strings
    '''
    
    precision = metrics.precision_score(y_true=goldlabels,
                        y_pred=predictions,
                        average='macro')

    recall = metrics.recall_score(y_true=goldlabels,
                     y_pred=predictions,
                     average='macro')


    fscore = metrics.f1_score(y_true=goldlabels,
                 y_pred=predictions,
                 average='macro')

    print('P:', precision, 'R:', recall, 'F1:', fscore)
    
#vectorizer and lr_classifier are the vectorizer and classifiers created in the previous cell.
#it is important that the same vectorizer is used for both training and testing: they should use the same mapping from values to dimensions
# predictions, goldlabels = get_predicted_and_gold_labels_token_only(testfile, vectorizer, lr_classifier)
# print_confusion_matrix(predictions, goldlabels)

# the functions with multiple features and analysis

#defines the column in which each feature is located (note: you can also define headers and use csv.DictReader)
#feature_to_index = {'TOKEN': 0, 'POS': 1, 'LEMMA': 2, 'PUNCTUATION': 3, 'STARTSWITH_CAPITAL_LETTER': 4, 'IS_STOPWORD': 5}


def extract_features_and_gold_labels(conllfile, selected_features):
    '''Function that extracts features and gold label from preprocessed conll (here: tokens only).
    
    :param conllfile: path to the (preprocessed) conll file
    :type conllfile: string
    
    
    :return features: a list of dictionaries, with key-value pair providing the value for the feature `token' for individual instances
    :return labels: a list of gold labels of individual instances
    '''
    if conllfile.startswith('SEM'):
        
        feature_to_index = {'Token': 3 , 'Pre-token': 5, 'Next-token': 6, 'Lemma':7 , 'Pre-lemma':8 , 'Next-lemma':9, 'POS':10, 'Pre-POS':11 , 'Next-POS':12 , 'POS_classified':13 , 'Punctuation_python': 14, 'MatchesNegExp': 15, 'HasNegAffix':16, 'Negated event':17, 'NegAffix':18}
        features = []
        labels = []
        conllinput = open(conllfile, 'r')
        #delimiter indicates we are working with a tab separated value (default is comma)
        #quotechar has as default value '"', which is used to indicate the borders of a cell containing longer pieces of text
        #in this file, we have only one token as text, but this token can be '"', which then messes up the format. We set quotechar to a character that does not occur in our file
        csvreader = csv.reader(conllinput, delimiter='\t',quotechar='|')
        next(csvreader, None)
        for row in csvreader:
            #I preprocessed the file so that all rows with instances should contain 6 values, the others are empty lines indicating the beginning of a sentence
            if len(row) > 0:
                #structuring feature value pairs as key-value pairs in a dictionary
                #the first column in the conll file represents tokens
                feature_value = {}
                for feature_name in selected_features:
                    row_index = feature_to_index.get(feature_name)
                    feature_value[feature_name] = row[row_index]
                features.append(feature_value)
                #The last column provides the gold label (= the correct answer). 
                labels.append(row[4])
                
    else:
        
        feature_to_index = {'Token': 3 , 'Pre-token': 6, 'Next-token': 7, 'Lemma':8 , 'Pre-lemma':9 , 'Next-lemma':10, 'POS':11, 'Pre-POS':12 , 'Next-POS':13 , 'POS_classified':14 , 'Punctuation_python': 15, 'MatchesNegExp': 16, 'HasNegAffix':17, 'Negated event':18, 'NegAffix':19}
        features = []
        labels = []
        conllinput = open(conllfile, 'r')
        #delimiter indicates we are working with a tab separated value (default is comma)
        #quotechar has as default value '"', which is used to indicate the borders of a cell containing longer pieces of text
        #in this file, we have only one token as text, but this token can be '"', which then messes up the format. We set quotechar to a character that does not occur in our file
        csvreader = csv.reader(conllinput, delimiter='\t',quotechar='|')
        next(csvreader, None)
        for row in csvreader:
            #I preprocessed the file so that all rows with instances should contain 6 values, the others are empty lines indicating the beginning of a sentence
            if len(row) > 0:
                #structuring feature value pairs as key-value pairs in a dictionary
                #the first column in the conll file represents tokens
                feature_value = {}
                for feature_name in selected_features:
                    row_index = feature_to_index.get(feature_name)
                    feature_value[feature_name] = row[row_index]
                features.append(feature_value)
                #The last column provides the gold label (= the correct answer). 
                labels.append(row[4])
                
    
    return features, labels
    
    

def get_predicted_and_gold_labels(testfile, vectorizer, classifier, selected_features):
    '''
    Function that extracts features and runs classifier on a test file returning predicted and gold labels
    
    :param testfile: path to the (preprocessed) test file
    :param vectorizer: vectorizer in which the mapping between feature values and dimensions is stored
    :param classifier: the trained classifier
    :type testfile: string
    :type vectorizer: DictVectorizer
    :type classifier: LogisticRegression()
    
    
    
    :return predictions: list of output labels provided by the classifier on the test file
    :return goldlabels: list of gold labels as included in the test file
    '''
    
    #we use the same function as above (guarantees features have the same name and form)
    features, goldlabels = extract_features_and_gold_labels(testfile, selected_features)
    #we need to use the same fitting as before, so now we only transform the current features according to this mapping (using only transform)
    test_features_vectorized = vectorizer.transform(features)
    predictions = classifier.predict(test_features_vectorized)
    
    return predictions, goldlabels


def find_best_parameters(trainfile, selected_features):
    """
    Function to find the best parameters for the classifier.
    """
    training_opt = pd.read_csv(training_path_opt, encoding ='utf-8', sep='\t')
    
    x_train_opt, _ = extract_features_and_gold_labels(training_path_opt, selected_features)
    
    # Transforming the features to vectors:
    vec = DictVectorizer()
    x_train_opt_vec = vec.fit_transform(x_train_opt)
    # Adding labels to a seperate list:
    y_train_opt = training_opt.Label.to_list()
    
    classifier = LinearSVC()
    parameters = dict(
        C = (0.01,0.1,1.0),
        loss = ('hinge','squared_hinge'),
        tol = (1e-4,1e-3,1e-2,1e-1))

    grid = GridSearchCV(estimator = classifier, param_grid=parameters, cv=5, scoring='f1_macro')
    grid.fit(x_train_opt_vec, y_train_opt)
    classifier = grid.best_estimator_
    print('Best parameters:',grid.best_params_)


#define which from the available features will be used (names must match key names of dictionary feature_to_index)
all_features = ['Token', 'Pre-token', 'Next-token', 'Lemma', 'Pre-lemma', 'Next-lemma', 'POS', 'Pre-POS', 'Next-POS', 'POS_classified', 'Punctuation_python', 'MatchesNegExp', 'HasNegAffix', 'Negated event', 'NegAffix']

print('confusion matrix and classification report for all features:')

sparse_feature_reps, labels = extract_features_and_gold_labels(trainfile, all_features)
#we can use the same function as before for creating the classifier and vectorizer
svm_classifier, vectorizer = create_vectorizer_and_classifier(sparse_feature_reps, labels)
#when applying our model to new data, we need to use the same features
predictions, goldlabels = get_predicted_and_gold_labels(testfile, vectorizer, svm_classifier, all_features)
print_confusion_matrix(predictions, goldlabels)
print_precision_recall_fscore(predictions, goldlabels)
report = classification_report(goldlabels,predictions,digits = 7, zero_division=0)
print(report)


print('confusion matrix and classification report for selected features:')

#define which from the available features will be used (names must match key names of dictionary feature_to_index)
selected_features = ['Token', 'Pre-token', 'Next-token', 'Pre-lemma', 'POS', 'Negated event', 'NegAffix', 'HasNegAffix']

feature_values, labels = extract_features_and_gold_labels(trainfile, selected_features)
#we can use the same function as before for creating the classifier and vectorizer
svm_classifier, vectorizer = create_vectorizer_and_classifier(feature_values, labels)
#when applying our model to new data, we need to use the same features
predictions, goldlabels = get_predicted_and_gold_labels(testfile, vectorizer, svm_classifier, selected_features)
print_confusion_matrix(predictions, goldlabels)
print_precision_recall_fscore(predictions, goldlabels)
report = classification_report(goldlabels,predictions,digits = 7, zero_division=0)
print(report)

find_best_parameters(trainfile, selected_features)
