.PHONY: all clean

all: paper/paper.pdf

# Preprocessing: data wrangling and figures
output/figures/figure_5_2.png output/figures/figure_5_3.png: input/PaidSearch.csv code/preprocess.py
	python code/preprocess.py

# DID estimation
output/tables/did_table.tex: input/PaidSearch.csv code/did_analysis.py
	python code/did_analysis.py

# Paper compilation
paper/paper.pdf: paper/paper.tex output/figures/figure_5_2.png output/figures/figure_5_3.png output/tables/did_table.tex
	cd paper && pdflatex paper.tex && pdflatex paper.tex

clean:
	rm -f output/figures/*.png output/tables/*.tex paper/paper.pdf paper/paper.aux paper/paper.log
# =============================================================
# Dependency Graph Questions (Task 2)
# 1. Edit preprocess.py: Make rebuilds figures and paper.pdf.
#    It skips did_analysis.py and did_table.tex.
# 2. Edit did_analysis.py: Make rebuilds did_table.tex and paper.pdf.
#    It skips preprocess.py and the figures.
# 3. Edit paper.tex: Make only recompiles paper.pdf.
#    No Python scripts run at all.
#
# Reflection (Task 8)
# The Makefile makes explicit what run_all.sh left implicit.
# In run_all.sh the order of steps implied dependencies but never
# stated them directly. The Makefile declares exactly which files
# depend on which, so a new collaborator can immediately see the
# full dependency graph of the project. It also means only the
# necessary steps rerun when something changes, saving time and
# making the build process more reliable.
# =============================================================
