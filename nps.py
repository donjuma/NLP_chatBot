import nltk
from random import shuffle, randint
from sklearn.svm import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.metrics import classification_report

class chatBot(object):

    def __init__(self):
        self.posts = nltk.corpus.nps_chat.xml_posts()
        self.categories = ['Emotion', 'ynQuestion', 'yAnswer', 'Continuer',
                'whQuestion', 'System', 'Accept', 'Clarify', 'Emphasis',
                'nAnswer', 'Greet', 'Statement', 'Reject', 'Bye', 'Other']
        self.mapper = [0, 2, 6, 3, 11, 5, 8, 1, 8, 3, 10, 11, 13, 13, 13]
        self.responses = {}
        self.featuresets = []
        self.train = []
        self.test = []
        self.testSet = []
        self.testSetClass = []
        self.classif = SklearnClassifier(LinearSVC())
        for i in range(0, 15):
            self.responses[i] = []
        for post in self.posts:
            self.featuresets.append((self.tokenize(post.text),self.categories.index(post.get('class'))))
            self.temp = self.responses[self.categories.index(post.get('class'))]
            self.temp.append(post.text)

    def tokenize(self, sentence):
        """
            Extracts a set of features from a message.
        """
        features = {}
        tokens = nltk.word_tokenize(sentence)
        for t in tokens:
            features['contains(%s)' % t.lower()] = True
        return features

    def talk(self):
        while 1:
            inp = raw_input("YOU: ")
            features = self.tokenize(inp)
            pp = self.classif.classify_many(features)
            pp = pp[0]
            pp = int(pp)
            m = self.mapper[pp]
            r = self.responses[m]
            val = randint(0, len(r))
            print("BOT: "+r[val])

    def trainSet(self):
        shuffle(self.featuresets)
        size = int(len(self.featuresets) * .1) # 10% is used for the test set
        self.train = self.featuresets[size:]
        self.test = self.featuresets[:size]
        self.classif.train(self.train)

        self.testSet = []
        self.testSetClass = []
        for i in self.test:
            self.testSet.append(i[0])
            self.testSetClass.append(i[1])
        self.batch = self.classif.classify_many(self.testSet)

    def statistics(self):
        print (classification_report(self.testSetClass, self.batch, labels=list(set(self.testSetClass)),target_names=self.categories))
