"""
State of the Art Tree-Based Classification
with scikit-learn
"""
"""
from sklearn import tree
import graphviz

X = [[0,0],[1,1]]
Y = [0, 1]
clf = tree.DecisionTreeClassifier()  # clf for Classifier
clf = clf.fit(X, Y)
tree.plot_tree(clf)  # should plot but does not

dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("iris")
graph

"""

from sklearn.datasets import load_iris
from sklearn import tree
import graphviz

iris = load_iris()
X, y = iris.data, iris.target
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, y)
tree.plot_tree(clf)

dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("iris")