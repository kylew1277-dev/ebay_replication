# eBay Paid Search — Difference-in-Differences Replication

A reproducible replication package estimating the causal effect of eBay's paid search advertising on revenue, based on the natural experiment analyzed by Blake et al. (2014) and presented in Chapter 5 of Taddy (2019).

## Research Question

What is the effect of paid search (SEM) advertising on eBay's revenue?

## Data

The dataset contains daily revenue observations for 210 designated market areas (DMAs) from April to July 2012. In 65 treatment DMAs, eBay stopped bidding on Google AdWords on May 22, 2012. The remaining 145 DMAs serve as the control group.

## Repository Structure

ebay_replication/
|-- input/
|-- code/
|   |-- preprocess.py
|   +-- did_analysis.py
|-- output/
|   |-- figures/
|   +-- tables/
|-- paper/
|-- run_all.sh
+-- README.md

## Prerequisites

- Python 3 with pandas, numpy, matplotlib
- LaTeX (pdflatex) with graphicx, booktabs, and amsmath packages

## How to Reproduce

git clone git@github.com:kylew1277-dev/ebay_replication.git
cd ebay_replication
bash run_all.sh

This will run the preprocessing, estimation, and paper compilation. The final output is paper/paper.pdf.

## Results

The DID estimate suggests that turning off paid search reduced eBay revenue by approximately 0.66 percent. However, the 95 percent confidence interval includes zero, so the effect is not statistically significant at the 5 percent level. This replicates the main finding of Blake et al. (2014).
