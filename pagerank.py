#Python 3.0
import re
import os
import collections
import time
import numpy as np
#import other modules as needed

class inputFile:
    num_of_pages = 0
    num_of_links = 0
    graph = {}
    tpm = []
    adm = []
    pr_vector = []
    name = ""
    def __init__(self, num_of_pages, num_of_links):
      self.num_of_pages = num_of_pages
      self.num_of_links = num_of_links
      self.graph = {}
      
    def addGraphNode(self, from_link, to_link):
        if from_link in self.graph:
            self.graph[from_link].append(to_link)
        else:
            self.graph[from_link] = []
            self.graph[from_link].append(to_link)
    
    def calcAdjacencyMatrix(self):
        rows, cols = (self.num_of_pages, self.num_of_pages)
        adm = [[0 for i in range(cols)] for j in range(rows)]
        for x in range(rows):
            if x in self.graph:
                for y in range(cols):    
                    if y in self.graph[x]:
                        adm[x][y] = 1
        self.adm = adm
    
    def calcProbabilityMatrix(self, alpha, enable_teleportation):
        rows, cols = (self.num_of_pages, self.num_of_pages)
        tpm = [[0 for i in range(cols)] for j in range(rows)]
        for (adm_row, tpm_row) in zip(self.adm, tpm):
            num_of_ones = self.countOnes(adm_row)
            if num_of_ones == 0:
                for i in range(len(adm_row)):
                    tpm_row[i] = 1/len(adm_row)
            else:
                for i in range(len(adm_row)):
                    if adm_row[i] == 1:
                        tpm_row[i] = round(1/num_of_ones, 2)

        if enable_teleportation:
            for x in range(rows):
                for y in range(cols):
                    tpm[x][y] = round(tpm[x][y] * (1 - alpha), 2)
                    tpm[x][y] = round(tpm[x][y] + (alpha / self.num_of_pages),2)

        self.tpm = tpm
        
    
    def calcPageRankVector(self, max_iters, epsilon):
        r = [round(1/self.num_of_pages,2) for i in range(self.num_of_pages)]
        for i in range(max_iters):
            pr = r
            r = np.dot(self.tpm , r);
            diff = pr - r
            #print("diff", pr - r)
            if all(v < epsilon for v in diff):
                #r is page rank vector
                self.pr_vector = np.round(r, 4)
                print("Found page rank vector in "+str(i+1)+" iterations")
                break;
            
    
    def printPRVector(self):
        out = "\n"+ self.name + "\n"
        out += "page_id | page_rank\n"
        out += "-------------------\n"
        print(out)
        count = 0
        for idx, val in enumerate(self.pr_vector):
            r = "   "+str(idx+1)+"      "+ str(val)
            count += 1
            if count <= 9:
                print(r)
            out += r+"\n"
        out += "\n"
        return out

        
    def countOnes(self, row):
        count = 0
        for r in row:
            if r == 1:
                count += 1
        return count
    
    def print2dArr(self, arr):
        print(np.matrix(arr))
    
    def printTPM(self):
        self.print2dArr(self.tpm)
    
    def printADM(self):
        self.print2dArr(self.adm)
    
class pagerank:
    input_files = []
    alpha = 0.15
    def __init__(self, alpha):
        self.alpha = alpha
        
    def readInputFiles(self):
        for file in os.listdir("."):
            if file.endswith(".txt"):
                if file.startswith("out"):
                    continue
                with open(file) as f:
                    lines = f.readlines()
                    inf = inputFile(int(lines[0]), int(lines[1]))
                    inf.name = file
                    links = lines[2:]
                    for link in links:
                        inf.addGraphNode(int(link.split()[0]), int(link.split()[1]))
                    self.input_files.append(inf)
    
    def calculateAdjacencyMatrix(self):
        for input_file in self.input_files:
            input_file.calcAdjacencyMatrix()
            
    def calculateProbabilityMatrix(self, enable_teleportation):
        for input_file in self.input_files:
            input_file.calcProbabilityMatrix(self.alpha, enable_teleportation)
    
    def calculatePageRank(self, max_iters, epsilon):
        for input_file in self.input_files:
            input_file.calcPageRankVector(max_iters, epsilon)

    def printPageVector(self):
        all_out = ""
        for input_file in self.input_files:
            out = input_file.printPRVector()
            all_out += out + "\n"
        f = open("out.txt", "w")
        f.write(all_out)
        f.close()
            
    def printTPM(self):
        for input_file in self.input_files:
            input_file.printTPM()
            print("--------------------------------")
    
    def printADM(self):
        for input_file in self.input_files:
            input_file.printADM()
            print("--------------------------------")
	#def pagerank(self, input_file):
	#function to implement pagerank algorithm
	#input_file - input file that follows the format provided in the assignment description
	
alpha = 0.15
pr = pagerank(alpha)
pr.readInputFiles()
pr.calculateAdjacencyMatrix()
#pr.printADM()
pr.calculateProbabilityMatrix(True)
#pr.printTPM() 
pr.calculatePageRank(1000, 0.001)
pr.printPageVector()


