Skill Metrics Project
--------------------
This package contains a collection of functions for calculating the skill of model predictions against observations. It includes metrics such as root-mean-square-error (RMSE) difference, centered root-mean-square (RMS) difference, and skill score (SS), as well as a collection of functions for producing target and Taylor diagrams. The more valuable feature of the package are the plotting functions for target and Taylor diagrams and the ability to easily customize the diagrams.

Features
---------------------
- Statistical metrics such as root-mean-square-error (RMSE) difference, centered root-mean-square (RMS) difference, and skill score (SS)
- Functions to calculate statistical metrics for target & Taylor diagrams
- Target Diagrams
- Taylor Diagrams
- Options to control plot features such as color of labels and lines, width of lines, choice of markers, etc.
- Output of graphics to any supported matplotlib format (default PNG).

Installation
---------------------
To install the package simply use the pip3 command:

`% pip3 install SkillMetrics`

If you are upgrading the package then include the upgrade option:

`% pip3 install SkillMetrics --upgrade`

Note that the SkillMetrics package now only supports Python 3 because Python 2 has been depricated. Use of pip may not successfully install the latest version of the package.

Example Scripts
---------------------
A primer on Taylor diagrams is provided as well as a 6-page description of target and Taylor diagrams as visual tools to aid in the analysis of model predictive skill. The figures used in the latter were generated with the SkillMetrics package. There is also an "Examples" folder that contains a collection of example Python scripts showing how to produce target and Taylor diagrams in a variety of formats on the [Wiki Home page](http://github.com/PeterRochford/SkillMetrics/wiki). There are multiple examples for target and Taylor diagrams that successively progress from very simple to more customized figures. These series of examples provide an easy tutorial on how to use the various options of the target_diagram and taylor_diagram functions. They also provide a quick reference in future for how to produce the diagrams with specific features. 

There is also a simple program [all_stats.py](http://github.com/PeterRochford/SkillMetrics/blob/master/Examples/all_stats.py) available via the [Wiki](http://github.com/PeterRochford/SkillMetrics/wiki#all-statistics) that provides examples of how to calculate the various skill metrics used or available in the package. All the calculated skill metrics are written to a spreadsheet file for easy viewing and manipulation: Excel for a Windows operating system, Comma Separated Value (CSV) for a Macintosh operating system (MacOS). The Python code is kept to a minimum.

Example Diagrams
---------------------
The diagrams produced by the example scripts are in Portable Network Graphics (PNG) format and have the same file name as the script with a `.png` suffix. The PNG files created can be viewed by following the links shown below. This is a useful starting point for users looking to identify the best example from which to begin creating a diagram for their specific need by modifying the accompanying Python script.

[Target Diagrams](http://github.com/PeterRochford/SkillMetrics/wiki/Target-Diagram-Examples)

[Taylor Diagrams](http://github.com/PeterRochford/SkillMetrics/wiki/Taylor-Diagram-Examples)

Here is a sample of the target and Taylor diagrams you'll find in the above examples:

| | |
| :-------------------------:|:-------------------------: |
| target diagram ![](https://github.com/PeterRochford/SkillMetrics/blob/master/Examples/target7_example.png) | Taylor diagram ![](https://github.com/PeterRochford/SkillMetrics/blob/master/Examples/taylor9_example.png) |

FAQ
---------------------
A list of Frequently Asked Questions ([FAQ](http://github.com/PeterRochford/SkillMetrics/wiki/FAQ)) is maintained on the Wiki. Users are encouraged to look there for solutions to problems they may encounter when using the package. 

Available Metrics
---------------------
Here is a list of currently supported metrics. Examples of how to obtain them can be found in the [all_stats.py](http://github.com/PeterRochford/SkillMetrics/blob/master/Examples/all_stats.py) program. A far more extensive list of statistical metrics can be calculated using the [SeqMetrics](https://pypi.org/project/SeqMetrics) package.

| Metric      | Description |
| ----------- | ----------- |
| bias        | Mean error  |
| BS          | Brier score |
| BSS         | Brier skill score |
| CRMSD       | centered root-mean-square error deviation |
| KGE09       | Kling-Gupta efficiency 2009 |
| KGE12       | Kling-Gupta efficiency 2012 |
| NSE         | Nash-Sutcliffe efficiency |
| r           | Correlation coefficient |
| RMSD        | root-mean-square error deviation |
| SDEV        | standard deviation |
| SS          | Murphy's skill score |

How to cite SkillMetrics
---------------------
Peter A. Rochford (2016) SkillMetrics: A Python package for calculating the skill of model predictions against observations, http://github.com/PeterRochford/SkillMetrics

```
  @misc{rochfordskillmetrics, 
    title={SkillMetrics: A Python package for calculating the skill of model predictions against observations}, 
    author={Peter A. Rochford}, 
    year={2016}, 
    url={http://github.com/PeterRochford/SkillMetrics}, 
```

Guidelines to contribute
---------------------
1. In the description of your Pull Request (PR) explain clearly what it implements/fixes and your changes. Possibly give an example in the description of the PR. 
2. Give your pull request a helpful title that summarises what your contribution does. 
3. Write unit tests for your code and make sure the existing [backward compatibility tests](http://github.com/PeterRochford/SkillMetrics/wiki/Backward-Compatibility-Testing) pass. 
4. Make sure your code is properly commented and documented. Each public method needs to be documented as the existing ones.
