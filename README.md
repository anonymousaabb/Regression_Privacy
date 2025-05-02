# Pytorch Code for "Regression Privacy: When Label Differential Privacy Meets Linear Programming"

## Brief Summary
With the wide application of machine learning techniques in practice, privacy preservation has gained increasing attention. Protecting user privacy with minimal accuracy loss is a fundamental task in the data analysis and mining community. In this paper, we focus on regression tasks under $\epsilon$-label differential privacy guarantees. Existing methods for regression with $\epsilon$-label differential privacy, such as the RR-On-Bins mechanism and its variant, discretize the output space into finite bins and applying randomized response (RR) algorithms. To efficiently determine these finite bins, the authors discretized the labels by rounding the original responses down to integer values. However, such operations does not align well with real-world scenarios. To overcome these limitations, we propose treating the response as a {\it continuous} random variable without discretizing. Our novel approach selects optimal intervals for randomized responses and introduces new algorithms designed for scenarios where the global prior is either known or unknown. Additionally, we provide a theoretical analysis and prove that our algorithm, RPWithPrior, guarantees $\epsilon$-label differential privacy. Numerical results demonstrate that our approach outperforms the Gaussian, Laplace, Staircase, and RRonBins mechanisms on the Communities and Crime, Criteo Sponsored Search Conversion Log, and California Housing datasets. 

## The Criteo Sponsored Search Conversion Log Dataset
The Criteo Sponsored Search Conversion Log Dataset is an open access dataset, you can download from https://ailab.criteo.com/criteo-sponsored-search-conversion-log-dataset/

## The Communities and Crime dataset
For The Communities and Crime dataset, you can download from https://archive.ics.uci.edu/ml/datasets/communities+and+crime

