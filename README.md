# Pytorch Code for "Regression Privacy: When Label Differential Privacy Meets Linear Programming"

## Brief Summary
With the wide application of machine learning techniques in practice, privacy preservation has gained increasing attention. Protecting user privacy with minimal accuracy loss is a fundamental task in the data analysis and mining community. In this paper, we focus on regression tasks under $\epsilon$-label differential privacy guarantees. Some existing methods for regression with $\epsilon$-label differential privacy, such as the RR-On-Bins mechanism and its variant, discretized the output space into finite bins and then applied randomized response (RR) algorithms. To efficiently determine these finite bins, the authors rounded the original responses down to integer values. However, such operations does not align well with real-world scenarios. To overcome these limitations, we model both original and randomized responses as *continuous* random variables, avoiding discretization entirely. Our novel approach estimates an optimal interval for randomized responses and introduces new algorithms designed for scenarios where a prior is either known or unknown. Additionally, we  prove that our algorithm, RPWithPrior, guarantees $\epsilon$-label differential privacy. Numerical results demonstrate that our approach outperforms the Gaussian, Laplace, Staircase, and RRonBins mechanisms on the Communities and Crime, Criteo Sponsored Search Conversion Log, and California Housing datasets.  

## The Criteo Sponsored Search Conversion Log Dataset
The Criteo Sponsored Search Conversion Log dataset is an open access dataset, you can download from https://ailab.criteo.com/criteo-sponsored-search-conversion-log-dataset/

## The Communities and Crime dataset
For the Communities and Crime dataset, you can download from https://archive.ics.uci.edu/ml/datasets/communities+and+crime

## The California Housing Dataset
This California Housing dataset was derived from the 1990 U.S. census, which can be obtained from the StatLib repository https://www.dcc.fc.up.pt/~ltorgo/Regression/cal_housing.html or import through the command  *fetch\_california\_housing* https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html\#sklearn.datasets.fetch_california_housing in sklearn.datasets. 

