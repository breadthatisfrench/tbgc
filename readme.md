## tbgc

Used to generate graphs for sprints and backlog

# Usage Instructions

```
---Help and Program Info---

tbgc - Time Box Graph Creator
Usage: python tbgc.py [OPTION] [ARGS]
Options:
  -h     print help (This message)
  -e     enter in graph data through console prompts
  -f     read in graph data from a file; takes an argument of the filename
         Example Usage of -f: python tbgc.py -f mydatafile.txt
         Example file layout for use with tbgc (Numbers on the left are line numbers
         and do not need to be written)

         1 Name for Graph
         2 [ideal val 1] [ideal val 2] [ideal val 3] ... [ideal val n]
         3 [actual val 1] [actual val 2] [actual val 3] ... [actual val n]

```

> This help message can be displayed in the console by running tbgc.py without arguments or with the *-h* option