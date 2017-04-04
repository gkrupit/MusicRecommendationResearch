from sklearn import datasets
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import LinearSVC
iris = datasets.load_iris()
data = [[1,1,1,1],[2,2,2,1],[3,3,3,1],[4,4,4,1],[1,1,1,2],[1,1,1,3],[1,1,1,4]]
classes = [1,1,1,1,2,3,4]
X, y = iris.data, iris.target
classifier = OneVsOneClassifier(LinearSVC(random_state=0))
print X
print y
classifier.fit(X,y)
while True:
    to_predict = raw_input('Enter 4 numbers to predict: ')
    lst = to_predict.split()
    print lst
    new_lst = []
    for num in lst:
        new_lst.append(float(num))
    print classifier.predict([new_lst])
