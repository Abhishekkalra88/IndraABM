# Sandpile Model

last-updated: Nov 14, 2021

Nov 1, 2021
1602151 function calls (1567174 primitive calls) in 9.492 seconds

Oct 24, 2021
1628518 function calls (1593264 primitive calls) in 6.714 seconds


## Ten Slowest Functions in CProfiler

|ncalls | tottime | file | function |
| --- | --- | --- | --- |
| 373 | 0.063 | doccer.py | docformat(line:10) |
|3113 | 0.046 | sre_parse.py | _parse (line:493) |
| 2750 | 0.040 | inspect.py | cleandoc(626) |
| 168 | 0.039 | __init__.py |  \<module> (line:1) |
| 627 | 0.033 | sre_compile.py | _optimize_charset(line:276) |
| 1356 | 0.027 | inspect.py | _signature_from_function(line:2150) |
| 4076 | 0.025 | sre_compile.py | _compile(line:71) |
| 248 | 0.020 | traitlets.py | getmember(line:219) |
| 27880 | 0.019 | sre_parse.py | __next(line:233) |
| 42988 | 0.019 | sre_parse.py | __getitem__(line:164) |


## CProfiler thoughts
Most if not all the totime comes from built-in functions 
After taking a closer look, none of the methods that aren't built in come close to 0.01 seconds


## Running PyInstrument
Afterwards, to get a different view of the model, I ran a Statistical Profiler (pyinstrument) using the command:
`python -m pyinstrument -r html  sandpile.py > sandpile.profile`

to get the time by time leading to the 9+ seconds of time used to run the code and here are the things I found:


Recorded: 11/14/2021, 3:52:59 AM

Duration: 9.29     CPU time: 9.22

Program: sandpile.py

lib/actions.py - 0 -> 9.236 = 9.236 seconds

runpy.py - 9.236 -> 9.292 = 0.056 seconds

### More on the lib/actions.py

lib/display_methods.py:1 - mainly __init__ from many different libraries took 8.528 seconds
- seaborn/__init__.py:1 took 5.009 seconds
- pandas/__init__.py:1 took 1.628 seconds
- matplotlib/pyplot.py:1 took 1.042 seconds
- matplotlib/__init__.py:1 took 0.646 seconds
- matplotlib/__init__.py:1032 took 0.127 (actual usage of matplotlib in sandpile.py)

lib/agent.py - numpy __init__ took 0.672 seconds

## Thoughts and comparisons
Using pyinstrument will display time by time frames of what is being ran to give a different perspective of using a deterministic profiler. 
  
This is more useful than CProfile in this specific case since CProfile profiles too many details which makes it hard to organize and figure out lower-end times because it gets mixed with a lot of useless information.

CProfile however, is better to pick up outliers in terms of what takes the most time.
  
The best way to improve this code would be taking a look at what actions.py is calling and try to remove some initializations and importing

However after taking a closer look at the code and at the html generated by pyinstrument, not a lot of libraries can be removed as it inherits from model.py which is being used in other models.





