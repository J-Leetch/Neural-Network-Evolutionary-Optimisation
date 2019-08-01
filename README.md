
# Neural Network Evolutionary Optimisation
A fun attempt at optimising a neural network for playing a simple game similar to 'flappy bird'- a classic example seen on YouTube. I created the game in Processing (python) and used just simple python code to implement the learning algorithms.

## Screenshot
![alt text](https://github.com/J-Leetch/Neural-Network-Evolutionary-Optimisation/blob/master/screenshot.png)!

It was a challenge for myself done in a little bit of spare time after 1st year exams to test out my new programming skills. It gave surprisingly good results considering its simplicity and that it was a first attempt, starting from zero knowledge and without using any machine learning libraries etc.

Give it a look and/or a run... it's satisfying to watch if nothing else! GeneticAlgorithmNeuralNetBirds.pyde holds all of the necessary code - all that you need is an installation of Processing 3 with the python mode.

## The network
- The network has a fully connected 4-layer structure with [5,4,3,1] nodes in each layer going from the input layer to the output node although many different shapes and sizes seem to work just fine.
- The inputs (what the AI can 'see') are:
  - the horizontal distance to the next gap
  - the vertical distance to the top and bottom of the next gap (the gaps become narrower as more gaps have been passed)
  - the horizontal speed of the game (which increases with each gap passed to make it get harder)
  - the velocity at which the 'bird' itself is moving vertically
- The 'decision' of the network to flap upwards or not flap for every frame cycle is interpreted by whether or not the output node's value is above 0.5 (on a scale of 0-1 given by the sigmoid function applied on each node). 

## The optimisation algorithm
The learning algorithm uses these ideas from evolution:
- ranking according to fitness (how well each 'bird' in the population does in the game)
- breeding or 'crossover' of properties between instances to create 'offspring' (better instances get to breed with the other best ones)
- mutation to create greater variety

Starting from an initial, randomly generated population which plays the game until all instances have crashed, these evolutionary processes are combined to produce a subsequent new (and hopefully improved) generation so that, across multiple generations, the AI becomes very effective at playing the game.

The most interesting section of the code to implement these general ideas, written by me with almost no research (and so admittedly basic but also transparent and simple): 

```python
"""Functions to implement an evolutionary algorithm in order to develop the birds"""
        
def sortbirds(birds):
    """Sorts the birds into order from best fitness to worst"""
    fitnesses = [bird.fitness for bird in birds]   #creates a list of each bird's fitness
    sortedbirds = list(sorted(zip(fitnesses, birds), key=lambda elem: elem[0], reverse=True))    #sorts the birds using the list of fitnesses as a key
    sortedbirds = [b[1] for b in sortedbirds]    #removes fitnesses to give a list of just bird instances
    return sortedbirds    #returns the list of birds sorted according to fitness


def crossover(bird1, bird2):
    """Takes two 'parent' bird instances as input and implements an algorithm to combine features from each of them and produce a 'child' bird"""
    newbird = Bird()   #creates new bird instance to be returned with specified neural network attributes
    
    #for each weight value >>>
    for layer in range(len(bird1.sizes)-1):
        for strt in range(bird1.sizes[layer]):
            for fin in range(bird1.sizes[layer+1]):
                
                #the weight is assigned its value from one parent or the other at random
                if random(1)>0.5:   #randomises allocation
                    newbird.weights[layer][strt][fin] = bird2.weights[layer][strt][fin]    #weight from parent 2
                else:
                    newbird.weights[layer][strt][fin] = bird1.weights[layer][strt][fin]    #weight from parent 1
                       
    #for each bias value >> 
    for layer in range(len(bird1.sizes)-1):
        for neuron in range(bird1.sizes[layer+1]):
            
            #the bias is assigned its value from one parent or the other at random
            if random(1)>0.5:   #randomises allocation
                newbird.biases[layer][neuron] = bird2.biases[layer][neuron]    #bias from parent 2
            else:
                newbird.biases[layer][neuron] = bird2.biases[layer][neuron]    #bias from parent 1
    
    return newbird    #returns child bird
                
   
def mutation(bird):
    """For each weight and bias, sometimes (at random) allocates the weight/bias a random value between -1 and 1"""
    newbird = Bird()     #creates new bird instance to be returned with mutated neural network attributes
    
    #for each weight value >>>
    for layer in range(len(newbird.sizes)-1):
        for strt in range(newbird.sizes[layer]):
            for fin in range(newbird.sizes[layer+1]):
                
                if random(1)<0.05:   #specifies probability of mutation
                    newbird.weights[layer][strt][fin] = random(-1,1)   #new bird assigned a random weight
                else:
                    newbird.weights[layer][strt][fin] = bird.weights[layer][strt][fin]    #new bird assigned original weight
    
    #for each bias value >>
    for layer in range(len(newbird.sizes)-1):
        for neuron in range(newbird.sizes[layer+1]):
            
            if random(1)<0.01:    #specifies probability of mutation
                newbird.biases[layer][neuron] = random(-1,1)    #new bird assigned a random bias
            else:
                newbird.biases[layer][neuron] = bird.biases[layer][neuron]    #new bird assigned original bias
   
    return newbird   #returns mutated bird

    
def CreateNextGeneration(birds): 
    """Calls sortbirds(), crossover() and mutation() to create a new generation of birds"""   
    sortedbirds = sortbirds(birds)   #birds are sorted
        
    newbirds = sortedbirds   #creates a copy list of birds to be modified by the evolution functions
    
    #retains the best two birds and then iterates through to modify the other birds
    for i in range(int(numbirds)-2): 
        if i <numbirds/2:   #first half of remainder undergo crossover
            newbirds[i+2] = crossover(sortedbirds[i], sortedbirds[i+1])   #next new bird is a cross of two from last generation
        else:
            newbirds[i+2] = mutation(sortedbirds[i-int(numbirds/2)])   #next new bird is a mutation of a bird from last generation
   
    return newbirds   #reuturns a list of the new generation of birds
   
