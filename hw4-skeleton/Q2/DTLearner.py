"""  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
A simple wrapper for linear regression.  (c) 2015 Tucker Balch  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
Atlanta, Georgia 30332  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
All Rights Reserved  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
Template code for CS 4646/7646  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
and other users of this template code are advised not to share it with others  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
or to make it available on publicly viewable websites including repositories  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
or edited.  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
We do grant permission to share solutions privately with non-students such  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
as potential employers. However, sharing with other current or future  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
GT honor code violation.  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
-----do not edit anything above this line---  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
"""

import numpy as np

class DTLearner(object):

    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = []
        pass # move along, these aren't the drones you're looking for

    def author(self):
        return 'zpatwary3' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        @summary: Add training data to learner  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        @param dataX: X values of data to add  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        @param dataY: the Y training values  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        """
        # slap on 1s column so linear regression finds a constant term
        # newdataX = np.ones([dataX.shape[0],dataX.shape[1]+1])
        # newdataX[:,0:dataX.shape[1]]=dataX
        dataY = dataY[:, None]
        data = np.concatenate((dataX,dataY), axis=1)

        # build and save the model
        self.tree = self.build_tree(data)
        if len(self.tree.shape) == 1:
            self.tree = np.expand_dims(self.tree, axis=0)
        if self.verbose:
            print(">>>> Decision Tree built")
#        self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY, rcond=None)

    def build_tree(self, data):
        num_rows = data.shape[0]
        leaf = np.array([["Leaf", np.mean(data[:, -1]), "NA", "NA"]], dtype=object)
        if num_rows <= self.leaf_size:
            return leaf
        if np.unique(data[:, -1]).shape[0] == 1:
            return leaf
        else:
            i = self.best_feature(data[:, 0:-1], data[:, -1])
            split_value = np.median(data[:, i])
            df = data[data[:, i] <= split_value]
            if np.array_equal(df, data):
                return leaf
            left_tree = self.build_tree(df)
            right_tree = self.build_tree(data[data[:, i] > split_value])
            root = np.array([[i, split_value, 1, left_tree.shape[0] + 1]], dtype=object)
            return np.concatenate((root, left_tree, right_tree), axis=0)

    def best_feature(self,dataX,dataY):
        num_features = dataX.shape[1]
        abs_corr = 0
        index = 0
        for i in range(num_features):
            if np.correlate(dataX[:, i], dataY) > abs_corr:
                abs_corr = np.correlate(dataX[:, i], dataY)
                index = i
        return index

    def query(self,dataX):
        """  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        @summary: Estimate a set of test points given the model we built.  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        @param points: should be a numpy array with each row corresponding to a specific query.  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        @returns the estimated values according to the saved model.  		  	   		     			  		 			 	 	 		 		 	 		 		 	 		  	 	 			  	 
        """
        num_row = dataX.shape[0]
        self.Y = []
        for i in range(num_row):
            self.searching_tree(dataX[i], 0)
        return np.array(self.Y)
#        return (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1]

    def searching_tree(self, dataX, index):
        node = self.tree[index, :]
        if node[0] == 'Leaf':
            self.Y.append(node[1])
            pass
        elif dataX[node[0]] <= node[1]:
            self.searching_tree(dataX, index + node[2])
        elif dataX[node[0]] > node[1]:
            self.searching_tree(dataX, index + node[3])


if __name__=="__main__":
    print("the secret clue is 'zzyzx'")
