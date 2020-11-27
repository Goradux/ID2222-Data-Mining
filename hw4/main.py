import numpy as np
import scipy
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.cluster import KMeans

k = 4

# Read the data
graph = nx.read_edgelist("example1.dat", delimiter=",", nodetype=int, data=True, create_using=nx.MultiDiGraph)  # type: nx.MultiDiGraph
nx.draw(graph, node_size=10)
plt.show()

# 1. Form the affinity matrix
A = np.zeros([graph.number_of_nodes(), graph.number_of_nodes()])
for edge in graph.edges:
    A[edge[0] - 1, edge[1] - 1] = 1

# 2. Define D and L
D = np.diag(np.sum(A, axis=1))
D_inv = scipy.linalg.inv(scipy.linalg.sqrtm(D))
L = np.dot(np.dot(D_inv, A), D_inv)

# 3. Find eigenvectors
eigenvalues, eigenvectors = scipy.linalg.eigh(L)  # Gives eigenvectors in acceding order
# Take k largest eigenvectors and eigenvalues
X = eigenvectors[:, -k:]
X_values = eigenvalues[-k:]

# 4. Form matrix Y by renormalizing X
Y = np.zeros_like(X)
for i in range(k):
    square = X[i, :].dot(X[i, :])
    Y[i, :] = X[i, :] / np.sqrt(square)

# 5. Apply k-means cluster
labels = KMeans(n_clusters=k, init='random').fit(X).labels_

nx.draw(graph, node_size=10, node_color=labels)
plt.show()
