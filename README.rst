SkillMetrics Project
====================
This package contains a collection of functions for calculating the skill of model predictions against observations. It includes metrics such as root-mean-square-error (RMSE) difference, centered root-mean-square (RMS) difference, and skill score (SS), as well as a collection of functions for producing target and Taylor diagrams. The more valuable feature of the package are the plotting functions for target and Taylor diagrams and the ability to easily customize the diagrams.

Features
--------
- Statistical metrics such as root-mean-square-error (RMSE) difference, centered root-mean-square (RMS) difference, and skill score (SS)
- Functions to calculate statistical metrics for target & Taylor diagrams
- Target Diagrams
- Taylor Diagrams
- Options to control plot features such as color of labels and lines, width of lines, choice of markers, etc.
- Output of graphics to PNG format.

Installing
----------
To install the package simply use the pip command:
::

$ pip install SkillMetrics

If you are upgrading the package then include the upgrade option:
::

$ pip install SkillMetrics --upgrade

Examples
--------
A primer on Taylor diagrams as well as an "Examples" folder that contains a collection of example Python scripts showing how to produce target and Taylor diagrams in a variety of formats is available via a GitHub Wiki at  
https://github.com/PeterRochford/SkillMetrics/wiki. There are 6 examples for target diagrams and 7 examples for Taylor diagrams that successively progress from very simple to more customized figures. These series of examples provide an easy tutorial on how to use the various options of the target_diagram and taylor_diagram functions. They also provide a quick reference in future for how to produce the diagrams with specific features. The diagrams produced by each script are in Portable Network Graphics (PNG) format and have the same file name as the script with a "png" suffix. Examples of the diagrams produced can be found on the Wiki.

There is also a simple program "all_stats.py" available via the Wiki that provides examples of how to calculate the various skill metrics used or available in the package. All the calculated skill metrics are written to an Excel file for easy viewing and manipulation. The Python code is kept to a minimum.

Available Metrics
-----------------
Here is a list of currently supported metrics. Examples of how to obtain them can be found in the "all_stats.py" program.

.. list-table::
   :widths: 15 10
   :header-rows: 1

   * - Metric
     - Description
   * - bias
     - Mean error
   * - BS
     - Brier score
   * - BSS
     - Brier skill score
   * - r-square
     - Correlation coefficient
   * - CRMSD
     - centered root-mean-square error deviation
   * - RMSD
     - root-mean-square error deviation
   * - SS
     - Murphy's skill score
   * - STD
     - standard deviation
