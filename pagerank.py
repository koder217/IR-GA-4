#Python 3.0
import re
import os
import collections
import time
#import other modules as needed

class inputFile:
    num_of_pages = 0
    num_of_links = 0
    graph = []
    def __init__(self, num_of_pages, num_of_links):
      self.num_of_pages = num_of_pages
      self.num_of_links = num_of_links
      self.graph = []
    def addGraphItem(self, from_link, to_link):
        self.graph.append([from_link, to_link])

class pagerank:
    input_files = []
    
    def readInputFiles(self):
        for file in os.listdir("."):
            if file.endswith(".txt"):
                with open(file) as f:
                    lines = f.readlines()
                    inf = inputFile(int(lines[0]), int(lines[1]))
                    links = lines[2:]
                    for link in links:
                        inf.addGraphItem(int(link.split()[0]), int(link.split()[1]))
                    self.input_files.append(inf)
                    
                    
	#def pagerank(self, input_file):
	#function to implement pagerank algorithm
	#input_file - input file that follows the format provided in the assignment description
	
pr = pagerank()
pr.readInputFiles()
for file in pr.input_files:
    print(file.graph)