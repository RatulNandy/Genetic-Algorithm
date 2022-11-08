#!/usr/bin/env python
# coding: utf-8


import random
from numpy import *

"""
The function 'randomGenome' returns a random individual(genome) (bit string- 0 or 1) of a
given length. 
"""

def randomGenome(length):
    individual=[]
    i=0
    for i in range(length):
        individual.append(random.randint(0,2))
    return individual

"""
The function 'makePopulation' returns a new randomly created population of
the specified size, represented as a list of genomes of the specified length
"""

def makePopulation(size,length):
    population=[]
    i=0
    """
    Using randomGenome function to append new individuals to the population   
    """
    for i in range(size):
        population.append(randomGenome(length)) 
    return population

"""
The fitness function returns the fitness value of a genome
"""

def fitness(genome):
    return (sum(genome))

"""
The 'evaluateFitness' function returns four values. The average fitness of the
population as a whole, the fitness of the best individual in the population and the indexes
of two worst fit individual in the population
"""

def evaluateFitness(population):
    w1=0
    w2=0
    fit=0
    bestFitness=-1
    sumFit=0
    count=0
    worstFit=21
    worstFit2=21
    for count in range(len(population)):
        fit=fitness(population[count])
        sumFit+=fit
        if(fit>bestFitness):
            bestFitness=fit     #Generating the best fitness of the population            
        if(fit<worstFit2):
            worstFit2=fit
            w2=count
            if(fit<worstFit):
                worstFit2=worstFit
                worstFit=fit
                w2=w1         # w2 is the index of the second worst fit individual of the population
                w1=count      # w1 is the index of the worst fit individual of the population
            
    avgFitness=sumFit/(len(population)) #Generating the average fitness value of the population
    return avgFitness, bestFitness, w1, w2

"""
The function 'crossover' returns two new genomes produced by crossing
over the given genomes at a random crossover point. It also returns 1 
if crossover happens.
"""

def crossover(genome1,genome2,pcRate):           #pcRate is the crossover rate
    child1=genome1
    child2=genome2
    crossOverFlag=0
    if (random.random()<pcRate):                 #Generating the probability if crossover happens  
        crossOverFlag=1                          #Checking if crossover happens
        pt=random.randint(1,len(genome1)-2)      #Generating a random point for crossover
        child1=genome1[:pt]+genome2[pt:]         #Crossover taking place
        child2=genome2[:pt]+genome1[pt:]         #Crossover taking place
    return child1, child2, crossOverFlag

"""
The function 'mutate' returns a new mutated version of the given
genome.
"""


def mutate(genome,pmRate):                    #pmRate is the mutation rate
    i=0
    for i in range(len(genome)):
        if(random.random()<pmRate):           #Generating probability for mutation         
                genome[i]=1-int(genome[i])    #Flipping a random bit (0,1)
                break
    return genome

"""
The function 'selectPair' selects and returns two genomes from the given
population using fitness-proportionate selection
"""

def selectPair(population):
    i=0
    totalSumFitness=0
    for i in range(len(population)):
        totalSumFitness=int(totalSumFitness)+int(fitness(population[i]))        
    w=0    
    cummulativeWeight={}
    """
    Creating a dictionary cummulativeWeight to store details.
    cummulativeWeight[index,0] is the index of the individual
    cummulativeWeight[index,1] is the fitness value of the individual
    cummulativeWeight[index,2] is the proportional fitness value (fitness/total fitness of the population)
    
    cummulativeWeight[index,3] is used to store the range of the proportional fitness for any individual
    between 0 and 1. A random number will then be generated (between 0 and 1) to choose the fittest individual.
    The individual with higher proportional value will have larger range and hence higher probability of getting 
    chosen.
    Eg. If individual 1 has proportional fitness value of 0.3, it will hold the range (0,0.3).If the next individual 
    has proportional fitness of 0.5, it will hold the range (0.3,0.8).
    """
    for w in range(len(population)):
        cummulativeWeight[w,0]=w
        cummulativeWeight[w,1]=fitness(population[w])
        cummulativeWeight[w,2]=(fitness(population[w])/totalSumFitness)
        if w==0:
                cummulativeWeight[w,3]=0
        else:
                cummulativeWeight[w,3]=cummulativeWeight[(w-1),3]+cummulativeWeight[(w-1),2]    
    parent1=-1
    parentCount=0
    while(parentCount<2):                  #Looping to find two individuals
        r=random.random()                  #Generating random number 0-1
        p=0
        while(cummulativeWeight[p,3]<r):   #Looping to find the individual belonging to the random range
            p=p+1; 
            if(p>len(population)-1):
                break
        if(parentCount==0):                #This piece of code validates if same individual is not chosen twice. 
            parent1=p-1
            parentCount=parentCount+1
        elif((parentCount==1) and (parent1!=p-1)):     
            parent2=p-1
            parentCount=parentCount+1
    return population[parent1], population[parent2] 

"""
In the function 'replacement', the offsprings replace the genomes with the worst fitness in the
population. Replaces two worst fit genomes if crossover is performed or just the worst
fit genome if only mutation is performed.
"""

def replacement(child1,child2,cFlag,cPopulation,worstFitIndex1,worstFitindex2):
    bestChild=child1
    bestChild2=child2
    if(fitness(child2)>fitness(child1)):       #Selecting the best fit child 
        bestChild=child2
        bestChild2=child1
    cPopulation[worstFitIndex1]=bestChild      #Replace worstfit genome with best fit child    
    if(cFlag==1):
        #Replace second worstfit genome with second best fit child if crossover performed.
        cPopulation[worstFitindex2]=bestChild2 
    return cPopulation
        
"""*********Start of the Main Program*******************

Inputs-
    populationSize= Size of the population provided by user
    crossoverRate=  Crossover rate provided by the user
    mutaionRate = Mutation rate provided by the user
    fileName = filename of the file for logging ( Optional)

"""
    
populationSize,crossoverRate,mutationRate,*fileName=input("Enter Population Size, CrossOver Rate, Mutation Rate and File Name(Optional) with comma separation\n").split(', ')
fileName=fileName[0] if fileName else ''    #Checking if optional filename is provided

if (len(fileName)!=0):
    file=open(r'/Users/ratulnandy/Documents/MSAAI/'+fileName+'.txt',"w+") #Setting filepath
generation = 0
print("Population size : "+populationSize)
print("Genome length : 20")
currentPopulation=makePopulation(int(populationSize),20)    #Creating the initial population
targetFit=20                                                #Bestfit condition
bestFit=0

while((targetFit!=bestFit) and (generation<1000)):          #Generates the iterating next generations
    avgFit,bestFit,wf1,wf2=evaluateFitness(currentPopulation) #Evaluating the fitness of current population
    print("Generation    "+str(generation)+": average fitness "+str(avgFit)+", best fitness "+str(bestFit))
    str1=str(generation)+'  '+str(avgFit)+'  '+str(bestFit)+'\n'
    if (len(fileName)!=0):
        file.write(str1)                   #Logging in the file   
    p1,p2=selectPair(currentPopulation)    #Selecting the parent in the current population
    c1,c2,cF=crossover(p1,p2,float(crossoverRate))  #Creating children with crossover
    mc1=mutate(c1,float(mutationRate))              #Mutation of 1st child
    mc2=mutate(c2,float(mutationRate))              #Mutaion of 2nd child
    #Creating next generation replacing worstfit genomes in the population with fitter children
    currentPopulation=replacement(mc1,mc2,cF,currentPopulation,wf1,wf2)
    generation=generation+1
file.close()         #Closing the file


