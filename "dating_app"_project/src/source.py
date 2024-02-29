import copy
import numpy as np

def onePerEach(weight, value, bagweight, person_limit):
    """
    Solves a variant of the 0/1 Knapsack problem optimized for a matchmaking context, where the goal is to select a subset of potential partners to maximize the sum of their match rates. This variant imposes two additional constraints: the total age difference between the selected partners must not exceed a specified limit (bagweight), and the number of partners chosen must not exceed a set limit (person_limit).
    
    Each potential partner is represented as an item with two attributes: an 'age difference' that contributes to the total weight and a 'match rate' that adds value. The function identifies the optimal combination of partners that provides the highest sum of match rates without the total age difference exceeding the bagweight and without choosing more than the person_limit number of partners.

    Args:
    weight (list of int): The weights representing the age difference of each potential partner.
    value (list of int): The values representing the match rate of each potential partner.
    bagweight (int): The maximum allowable total age difference between the selected partners.
    person_limit (int): The maximum number of potential partners to be selected.
    
    Returns:
    tuple: A tuple containing the maximum value that can be attained, the list of indices of chosen items, 
    and the list of values of the chosen items.
    """
    
    n = len(weight)  # Number of items
    # Initialize the dynamic programming table
    # The table will store tuples containing the total value and the list of chosen items
    dp = [[[[0, []] for _ in range(bagweight + 1)] for _ in range(person_limit + 1)] for _ in range(n + 1)]

    # Build the table bottom-up
    for i in range(1, n + 1):
        for k in range(1, person_limit + 1):
            for j in range(1, bagweight + 1):
                # If the current capacity is less than the item's weight, we can't include this item
                if j < weight[i - 1]:
                    dp[i][k][j] = copy.deepcopy(dp[i - 1][k][j])
                else:
                    # Compare the value of including and not including the current item
                    without_item = dp[i - 1][k][j]
                    with_item = dp[i - 1][k - 1][j - weight[i - 1]][:]
                    with_item[0] += value[i - 1]  # Increase the total value by the current item's value
                    # Add the current item to the list of chosen items
                    with_item[1] = copy.deepcopy(dp[i - 1][k - 1][j - weight[i - 1]][1]) + [i - 1]
                    # Store the option with the higher value
                    dp[i][k][j] = max(without_item, with_item, key=lambda x: x[0])

    # Retrieve the best value and combination for the exact person_limit and bagweight
    best_value, best_combination = dp[n][person_limit][-1]

    # Get the values for the chosen items based on the indices in best_combination
    chosen_values = [value[i] for i in best_combination]

    # Return the maximum value, the list of chosen item indices, and their corresponding values
    return best_value, best_combination, chosen_values



class RandomForestClassifier:
    def __init__(self, n_estimators=100, max_depth=None, min_samples_split=2, min_samples_leaf=1):
        """
        Random Forest Classifier.

        Parameters:
        - n_estimators (int): The number of decision trees in the forest.
        - max_depth (int): The maximum depth of each decision tree.
        - min_samples_split (int): The minimum number of samples required to split an internal node.
        - min_samples_leaf (int): The minimum number of samples required to be at a leaf node.
        """
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.trees = []

    def fit(self, X, y):
        """
        Train the Random Forest on the input features and target labels.

        Parameters:
        - X (numpy.ndarray): Input features.
        - y (numpy.ndarray): Target labels.
        """
        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)

        for _ in range(self.n_estimators):
            tree = DecisionTreeClassifier(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                min_samples_leaf=self.min_samples_leaf
            )
            bootstrap_indices = np.random.choice(len(X), len(X), replace=True)
            tree.fit(X[bootstrap_indices], y[bootstrap_indices])
            self.trees.append(tree)

    def predict(self, X):
        """
        Predict class labels for input samples.

        Parameters:
        - X (numpy.ndarray): Input samples.

        Returns:
        - numpy.ndarray: Predicted class labels.
        """
        probabilities = self.predict_proba(X)
        return np.argmax(probabilities, axis=1)

    def predict_proba(self, X):
        """
        Predict class probabilities for input samples.

        Parameters:
        - X (numpy.ndarray): Input samples.

        Returns:
        - numpy.ndarray: Predicted class probabilities.
        """
        predictions = np.zeros((len(X), self.n_classes_))

        for tree in self.trees:
            tree_predictions = tree.predict_proba(X)
            predictions += tree_predictions

        return predictions / self.n_estimators


class DecisionTreeClassifier:
    def __init__(self, max_depth=None, min_samples_split=2, min_samples_leaf=1):
        """
        Decision Tree Classifier.

        Parameters:
        - max_depth (int): The maximum depth of the tree.
        - min_samples_split (int): The minimum number of samples required to split an internal node.
        - min_samples_leaf (int): The minimum number of samples required to be at a leaf node.
        """
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf

    def fit(self, X, y):
        """
        Train the Decision Tree on the input features and target labels.

        Parameters:
        - X (numpy.ndarray): Input features.
        - y (numpy.ndarray): Target labels.
        """
        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)
        self.tree = self._build_tree(X, y, depth=0)

    def _build_tree(self, X, y, depth):
        """
        Recursively build the decision tree.

        Parameters:
        - X (numpy.ndarray): Input features.
        - y (numpy.ndarray): Target labels.
        - depth (int): Current depth in the tree.

        Returns:
        - dict: Tree node.
        """
        num_samples, num_features = X.shape
        unique_classes, class_counts = np.unique(y, return_counts=True)

        if len(unique_classes) == 1:
            # If only one class is present, return a leaf node
            return {'class': unique_classes[0], 'count': class_counts[0]}

        if depth == self.max_depth or num_samples < self.min_samples_split:
            # If max depth is reached or minimum samples for split is not met, return a leaf node
            majority_class = unique_classes[np.argmax(class_counts)]
            return {'class': majority_class, 'count': class_counts[0]}

        # Find the best split
        best_split = self._find_best_split(X, y)

        if best_split is None:
            # Unable to find a split, return a leaf node
            majority_class = unique_classes[np.argmax(class_counts)]
            return {'class': majority_class, 'count': class_counts[0]}

        # Split the data
        left_indices = X[:, best_split['feature']] <= best_split['threshold']
        right_indices = ~left_indices

        # Recursively build the left and right subtrees
        left_subtree = self._build_tree(X[left_indices], y[left_indices], depth + 1)
        right_subtree = self._build_tree(X[right_indices], y[right_indices], depth + 1)

        return {'feature': best_split['feature'], 'threshold': best_split['threshold'],
                'left': left_subtree, 'right': right_subtree}

    def _find_best_split(self, X, y):
        """
        Find the best split for a node.

        Parameters:
        - X (numpy.ndarray): Input features.
        - y (numpy.ndarray): Target labels.

        Returns:
        - dict or None: Best split information or None if no suitable split is found.
        """
        num_samples, num_features = X.shape
        parent_gini = self._calculate_gini(y)

        best_split = None
        best_gini_reduction = 0.0

        for feature in range(num_features):
            feature_values = np.unique(X[:, feature])
            for threshold in feature_values:
                left_indices = X[:, feature] <= threshold
                right_indices = ~left_indices

                if np.sum(left_indices) < self.min_samples_leaf or np.sum(right_indices) < self.min_samples_leaf:
                    # Skip splits that don't meet the minimum samples for leaf nodes
                    continue

                left_gini = self._calculate_gini(y[left_indices])
                right_gini = self._calculate_gini(y[right_indices])

                gini_reduction = parent_gini - (len(y[left_indices]) / num_samples * left_gini +
                                                len(y[right_indices]) / num_samples * right_gini)

                if gini_reduction > best_gini_reduction:
                    best_gini_reduction = gini_reduction
                    best_split = {'feature': feature, 'threshold': threshold}

        return best_split

    def _calculate_gini(self, y):
        """
        Calculate Gini impurity for a set of labels.

        Parameters:
        - y (numpy.ndarray): Target labels.

        Returns:
        - float: Gini impurity.
        """
        _, class_counts = np.unique(y, return_counts=True)
        class_probabilities = class_counts / len(y)
        gini = 1.0 - np.sum(class_probabilities ** 2)
        return gini

    def predict_proba(self, X):
        """
        Predict class probabilities for input samples.

        Parameters:
        - X (numpy.ndarray): Input samples.

        Returns:
        - numpy.ndarray: Predicted class probabilities.
        """
        predictions = np.zeros((len(X), self.n_classes_))
        for i in range(len(X)):
            predictions[i] = self._predict_sample(X[i], self.tree)
        return predictions

    def _predict_sample(self, sample, node):
        """
        Recursively predict class probabilities for a single sample.

        Parameters:
        - sample (numpy.ndarray): Input sample.
        - node (dict): Current tree node.

        Returns:
        - numpy.ndarray: Predicted class probabilities.
        """
        if 'class' in node:
            # If it's a leaf node, return class probabilities
            return np.array([1.0 if c == node['class'] else 0.0 for c in self.classes_])

        if sample[node['feature']] <= node['threshold']:
            return self._predict_sample(sample, node['left'])
        else:
            return self._predict_sample(sample, node['right'])
