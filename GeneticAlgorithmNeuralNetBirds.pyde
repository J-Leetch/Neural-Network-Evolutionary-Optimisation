
###### Created: 29 May 2018 ###########################################################################################################################################################

"""Author: James Leetch"""

"""
A script to implement the creation of artificial neural networks which are used to play a simple game. The randomly generated
set of intial networks are developed by an evolutionary algorithm to find an improved network for playing the game.
"""

#######################################################################################################################################################################################

"""Network class to be the 'brain' of the birds"""

class NeuralNetwork():
    
    #initialising
    def __init__ (self, sizes = [5,4,3,1]):
        """
        Sizes is a list of the number of nodes  in each layer of the network; the
        first layer is the input layer. Weights and biases are initialised randomly.
        """
        self.num_layers = len(sizes)
        self.sizes = sizes
        
        #'neuronvalues' and biases referenced as neuron[layer][number]
        self.neuronvals = [[0 for neuron in range(self.sizes[layer])] for layer in range(self.num_layers)]
        self.biases = [[random(-1,1) for neuron in range(self.sizes[activelayer+1])] for activelayer in range(self.num_layers-1)]
        
        #weights referenced as 'synapse'[start layer][number of start neuron][number of finish neuron (in next layer)]
        self.weights = [[[random(-1,1) for fin in range(self.sizes[layer+1])] for strt in range(self.sizes[layer])] for layer in range(self.num_layers-1)] 
        
        
    def feedforward (self, input):
        #Checks if the input is compatible
        if len(input) == self.sizes[0]:
            
            #Calculating the ouput
            self.neuronvals[0] = input    #setting the input layer according to the input
            for layer in range(self.num_layers-1):    #iterates through each layer
                for i in range(self.sizes[layer+1]):    #iterates through the next layer
                    for s in range(self.sizes[layer]):     #iterates through the layer before
                        self.neuronvals[layer+1][i] += self.weights[layer][s][i] * self.neuronvals[layer][s]   #adds values*weights from the layer before to the next layer
                    self.neuronvals[layer+1][i] = sigmoid(self.neuronvals[layer+1][i] + self.biases[layer][i])    #sigmoid function applied to each neuron
            #Returns the output of the network
            return(self.neuronvals[self.num_layers-1])  
        else:
            print("The input list is not the correct length.")
        
#######################################################################################################################################################################################

"""Bird object class as the player in the game"""

class Bird(NeuralNetwork):    #Bird inherits its 'brain' from the NeuralNetwork class
    
    def __init__(self):     #Initialises new instance when created
        NeuralNetwork.__init__(self)    #Creates the bird's random initial 'brain' - bird instance has all NeuralNetwork attributes and methods
        
        #Initialising attributes
        #Constants
        self.xPos = 100   #x-position in window
        self.diam = 15    #width of bird
        
        #Variables
        self.yPos = random(0,height)   #y-position in window
        self.ySpeed = 0    #y-speed
        self.crashed = False    #crashed boolean
        self.xDist = spacing    #x-distance to centre of next gap
        self.LoweryDist = 0    #y-distance to centre of bottom of next gap
        self.UpperyDist = 0    #y-distance to centre of top of next gap
        self.fitness = 0    #fitness attribute
        
        #Just for visuals
        self.timer = 0
        
        
    def think(self):
        """Method which allows a neural network instance to control the game by taking inputs and calculating its output as a 'decision'"""
        #Takes in game information
        self.getDistances()   #updates x and y distance to next gap
        
        #Decides whether to fly or not
        decision = self.feedforward([self.xDist, self.UpperyDist, self.LoweryDist, speed, self.ySpeed])[0]   #feeds the x and y distances into the bird's neural network to give a results between 0 and 1
        
        #Controls the bird in game
        if decision > 0.5:   
            self.fly()    #gives a simple way to allow the neural network to control the behaviour of the game through its output
    
    
    def getDistances(self):
        """Method to allow the bird instance to 'see' its environment in the game"""
        global activewall
        self.xDist = walls[activewall].gaploc - self.xPos    #calculates x-distance to the active (upcoming) wall
        self.UpperyDist = self.yPos - (walls[activewall].gaploc -  walls[activewall].gapwidth/2)   #calculates y-distance to the center of the active (upcoming) wall
        self.LoweryDist = self.yPos - (walls[activewall].gaploc +  walls[activewall].gapwidth/2)
    
    def fly(self):
        """Method to fly up"""
        if self.ySpeed>-5:   #if upwards speed is less than maximum value:
            self.ySpeed -= 3    #upwards speed is increased
    
    
    def fall(self):
        """Causes falling due to gravity"""
        if self.ySpeed<7:   #if downwards speed is less than maximum value:
            self.ySpeed += 0.7   #downwards speed is increased
        
        
    def move(self):
        """Updates position and fitness if not crashed"""
        if self.crashed==False:    #checks if the bird has crashed
            self.yPos += self.ySpeed    #updates y-position according to current y-speed
            
            #conditions for it the bird hits the top and bottom boundaries
            if self.yPos>height-self.diam/2:
                self.yPos = height - self.diam/2-0.1
                self.ySpeed = 0
                self.crashed = True
            if self.yPos<self.diam/2:
                self.yPos = self.diam/2+0.1
                self.ySpeed = 0
                self.crashed = True
                
            #updates fitness (distance travelled)
            self.fitness += speed
    
    
    def checkCollisions(self):
        """Method to check whether a bird instance has hit a wall"""
        global activewall
        wall = walls[activewall]    #gets the active wall to shorten next (long!) line
        if((wall.xPos-wall.depth/2-self.diam/2<self.xPos<wall.xPos+wall.depth/2+self.diam/2) and ((self.yPos<wall.gaploc-wall.gapwidth/2+self.diam)\
                or (self.yPos>wall.gaploc+wall.gapwidth/2-self.diam))):    #condition for having crashed
            self.crashed = True   #sets crashed attribute to True
    
    
    def draw(self):
        """Method to draw a bird instance"""
        if self.crashed==False:   #if the bird instance hasn't crashed
            """Drawing"""
            #Bird
            stroke(255)
            noFill()
            strokeWeight(2)
            rect(self.xPos-self.diam/2, self.yPos-self.diam/2, self.diam, self.diam, 5,5,5,5)
            
            #Sight line
            # global activewall
            # strokeWeight(1)
            # stroke(0,255,0)
            # line(self.xPos+self.diam/2, self.yPos, walls[activewall].xPos-5, walls[activewall].gaploc)
            stroke(255,0,0)
            # ellipse(walls[activewall].xPos,walls[activewall].gaploc,10,10)
            fill(255,0,0)
            ellipse(self.xPos+self.diam/4, self.yPos-self.diam/4,3,3)
            
        else:   #if the bird has crashed
            #Animates the bird's exit when crashed
            self.ySpeed = 0   #freezes
            self.xPos -= speed    #moves with walls
            
            #fades out
            if self.timer<20:   
                stroke(255)
                noFill()
                strokeWeight(2-self.timer*0.1)    #reducing line width with time
                rect(self.xPos-self.diam/2, self.yPos-self.diam/2, self.diam, self.diam)
                self.timer += 1
        
        
    def drawnet(self):
        """Method to draw the neural network of a bird instance"""
        for layer in range(len(self.sizes)):
            for i in range(self.sizes[layer]):
                noFill()
                stroke(255,255,255)
                
                if layer==len(self.sizes)-1 and self.neuronvals[layer][i] > 0.5:
                    fill(255,255,255)
                    
                strokeWeight(1)
                ellipse(width-50-layer*100, height-50-i*50,20,20)
                if layer<len(self.sizes)-1:
                    for z in range(self.sizes[layer+1]):
                        if self.weights[layer][i][z] < 0:
                            stroke(255,0,0)
                        else:
                            stroke(0,255,0)
                        strokeWeight(abs(self.weights[layer][i][z]))
                        line(width-40-(layer+1)*100, height-50-(z)*50,width-60-layer*100, height-50-i*50)
                    
            
######################################################################################################################################################################################
 
"""Wall object class for the walls in the game"""        
                                  
class Wall():
    
    def __init__(self, num):    #Initialises new instance when created        
        #Constants
        self.depth = 30   #thickness of wall
        
        #Variables
        self.gapwidth = height/3   #initial gap width
        self.gaploc = random(1+self.gapwidth/2, height-1-self.gapwidth/2)    #initial random gap center location
        self.passed = False    #initialising the passed boolean
        self.xPos = spacing + 300 + num*spacing    #initialising x-position according to input num (allows walls to created in a procession)
    
    
    def draw(self):
        """Method to draw a wall instance"""
        stroke(255)
        fill(255)
        rect(self.xPos-self.depth/2, 0, self.depth, self.gaploc-self.gapwidth/2)
        rect(self.xPos-self.depth/2, self.gaploc+self.gapwidth/2, self.depth, height-(self.gaploc+self.gapwidth/2))
    
    
    def checkPos(self):
        """Method to refresh position when a wall goes off screen and determine when a wall has been passed"""
        if(self.xPos < -self.depth/2):   #if off screen
            global num
            self.xPos += spacing*numwalls   #move to end of wall procession
            self.gaploc = random(1+self.gapwidth/2, height-1-self.gapwidth/2)   #allocates new random gap width
            self.gapwidth -= 2    #reduces gapwidth to increase difficulty gradually
            self.passed = False    #'new' wall has not been passed
            
        if(self.xPos < 100-self.depth/2-birds[0].diam and self.passed==False):   #if wall has gone past birds' x-position
            global activewall, speed, score
            self.passed = True   #wall instance passed attribute set to True
            
            #sets the active wall to the next wall in the procession
            activewall += 1  
            if activewall==numwalls:
                activewall = 0

            speed += 0.05   #increases speed to increase difficulty
            score += 1   #adds 1 to score


    def move(self):
        """Moves the walls/ moves the birds"""
        self.xPos -= speed    #updates wall instance x-position
        
#######################################################################################################################################################################################

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

#######################################################################################################################################################################################

"""Other functions"""

def sigmoid(x):
    """Utility function for the NeuralNetwork class"""
    return (1/(1+exp(1)**-x))


def Key():
    """Gives manual control of a bird if Bird.think() is commented out"""
    if keyPressed==True:
        birds[0].fly()   #if a key is pressed, the fly method is called
        counter = 0
            
#######################################################################################################################################################################################

"""Running of the game"""

#Working constants/variables

#Walls
spacing = 200    #spacing between centers of each wall
numwalls = 3    #number of walls (enough to fill the screen loop, depending on spacing)
activewall = 0    #number of the wall which is next up for the birds
speed = 3   #speed at which the walls move
walls = []   #list to be filled with wall instances

#Birds
numbirds = 50    #number of birds in a generation
birds = []    #list to be filled with bird instances
numCrashed = 0     #number of crashed birds
#bestbird = Bird()

#Game
score = 0    #number of walls passed
running = True    #boolean to control whether the game is running
gen = 1    #generation number
maxscore = 0    #best score of previous generations

"""Display"""

def setup():    #setup runs once when programme starts
    size(500,400)    #creates window 500x400
    #frameRate(30)
    textSize(15)
    #keyPressed = False
    
    #creating an array of instances of the wall object 
    for i in range(numwalls):
        wall = Wall(i)    #creates a wall instance
        walls.append(wall)    #adds it to the array walls
        
    #creating an array of instances of the bird object 
    for i in range(numbirds):
        bird = Bird()    #creates a bird instance with its associated neural network
        birds.append(bird)   #adds it to the array birds


def draw():    #runs repeatedly until programme closed    
    #declaring necessary variables/constants as global
    global running, birds, score, numCrashed, gen, maxscore, speed, numbirds, activewall
    
    """Animating the game"""
    if running==True:    #executes if game is running
        #setting up the base graphics
        background(0)   #background colour
        fill(255)    #sets fill colour for shapes
        text(score, 10, 25)    #displays score
        text("Alive: " +str(numbirds-numCrashed), 50, 25)    #displays number of birds still alive
        text("Generation: " +str(gen), 150,25)    #displays generation number
        text("Best score: " +str(maxscore), width-150, 25)    #displays best score of previous generations

        
        Key()   #function for manual control- checks if an input has been made
        
        """Progressing through the game"""
        #walls
        for wall in walls:   #for each wall
            wall.draw()   #wall is drawn
            wall.checkPos()   #checks whether wall has been passed and refreshes position when wall goes off screen
            wall.move()   #moves wall position
        
        #birds 
        numCrashed = 0    #setting back to 0 for check
        for bird in birds:   #for each bird
            bird.think()   #neural network instance takes 
            bird.checkCollisions()    #checks if bird has crashed
            bird.draw()    #draws bird
            bird.fall()    #causes bird to fall
            bird.move()    #updates bird position
            #counts number of crashed birds
            if bird.crashed==True:
                numCrashed+=1
        #if all the birds have crashed the game stops running and moves to the evolution/reset routine
        if numCrashed==len(birds):
            running = False
        
        birds = sortbirds(birds)
        birds[0].drawnet()
        
    """Evolution/reset routine"""
    if running==False:
        background(0)    #blank window

        birds = CreateNextGeneration(birds)   #evolutionary algorithm updates birds to create new generation
        
        #Resetting the game for the next generation
        for bird in birds:    #for each new bird
            #resets variable game attributes
            bird.xPos = 100    #resets x-position
            bird.yPos = random(0,height)    #seeds bird at random height
            bird.ySpeed = 0    #at zero y-speed
            bird.crashed = False   #resets crashed boolean
            bird.xDist = spacing    #initial distance to next wall
            #bird.yDist = 0
            bird.fitness = 0    #resets fitness to zero
            bird.timer = 0    #resets animation for variable for when crashed
            
        for num in range(numwalls):    #for each wall
            #resets variable game attributes
            walls[num].gapwidth = height/3   #sets initial gap width
            walls[num].gaploc = random(1+walls[num].gapwidth/2, height-1-walls[num].gapwidth/2)    #allocates random gap location
            walls[num].passed = False    #each wall has not been passed initially
            walls[num].xPos = spacing + 300 + num*spacing    #sets x-position according to instance number
        
        #if the score achieved in the last generation was greater than the maximum previous score, the maximum score is updated
        if score>maxscore:
           maxscore = score
           bestbird = birds[0]
           
        #resets game parameters
        activewall = 0   #sets the upcoming wall for the birds as the first wall
        speed = 3    #resets speed
        numCrashed = 0    #no birds have crashed initially
        score = 0   #resets score to zero
        gen+=1   #generation number increased by 1
        running = True   #sets the next generation to run
        