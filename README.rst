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

Example Scripts
---------------
A primer on Taylor diagrams is provided as well as a 6-page description of target and Taylor diagrams as visual tools to aid in the analysis of model predictive skill. The figures used in the latter were generated with the SkillMetrics package. There is also an "Examples" folder that contains a collection of example Python scripts showing how to produce target and Taylor diagrams in a variety of formats on the 
`Wiki Home page <https://github.com/PeterRochford/SkillMetrics/wiki>`_. There are multiple examples for target and Taylor diagrams that successively progress from very simple to more customized figures. These series of examples provide an easy tutorial on how to use the various options of the target_diagram and taylor_diagram functions. They also provide a quick reference in future for how to produce the diagrams with specific features. 

There is also a simple program "all_stats.py" available via the Wiki that provides examples of how to calculate the various skill metrics used or available in the package. All the calculated skill metrics are written to a spreadsheet file for easy viewing and manipulation: Excel for a Windows operating system, Comma Separated Value (CSV) for a Macintosh operating system (MacOS). The Python code is kept to a minimum.

Example Diagrams
----------------
The diagrams produced by th example scripts are in Portable Network Graphics (PNG) format and have the same file name as the script with a "png" suffix. The PNG files created can be viewed by following the links shown below. This is a useful starting point for users looking to identify the best example from which to begin creating a diagram for their specific need by modifying the accompanying Python script.

`Target Diagrams <https://github.com/PeterRochford/SkillMetrics/wiki/Target-Diagram-Examples>`_

`Taylor Diagrams <https://github.com/PeterRochford/SkillMetrics/wiki/Taylor-Diagram-Examples>`_

FAQ
---
A list of Frequently Asked Questions (`FAQ <https://github.com/PeterRochford/SkillMetrics/wiki/FAQ>`_) is maintained on the Wiki. Users are encouraged to look there for solutions to problems they may encounter when using the package. 

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
   * - r
     - Correlation coefficient
   * - CRMSD
     - centered root-mean-square error deviation
   * - KGE09
     - Kling-Gupta efficiency 2009
   * - KGE09
     - Kling-Gupta efficiency 2012
   * - NSE
     - Nash-Sutcliffe efficiency
   * - RMSD
     - root-mean-square error deviation
   * - SS
     - Murphy's skill score
   * - SDEV
     - standard deviation

How to cite SkillMetrics
------------
Peter A. Rochford (2016) SkillMetrics: A Python package for calculating the skill of model predictions against observations, https://github.com/PeterRochford/SkillMetrics

::

  @misc{rochfordskillmetrics, 
    title={SkillMetrics: A Python package for calculating the skill of model predictions against observations}, 
    author={Peter A. Rochford}, 
    year={2016}, 
    url={https://github.com/PeterRochford/SkillMetrics}, 
  }

Guidelines to contribute
---------------------
1. In the description of your Pull Request (PR) explain clearly what it implements/fixes and your changes. Possibly give an example in the description of the PR. 
2. Give your pull request a helpful title that summarises what your contribution does. 
3. Write unit tests for your code and make sure the existing `backward compatibility tests <https://github.com/PeterRochford/SkillMetrics/wiki/Backward-Compatibility-Testing>`_ pass. 
4. Make sure your code is properly commented and documented. Each public method needs to be documented as the existing ones.
