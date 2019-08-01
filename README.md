# Neural Network Evolutionary Optimisation
A fun attempt at optimising a neural network for playing a simple game similar to 'flappy bird'- a classic example seen on YouTube. I created the game in Processing (python) and used just simple python code to implement the learning algorithms.

## Screenshot
![alt text](https://github.com/J-Leetch/Neural-Network-Evolutionary-Optimisation/blob/master/screenshot.png)!

It was a challenge for myself done in a little bit of spare time after 1st year exams to test out my new programming skills. It gave surprisingly good results considering its simplicity and that it was a first attempt, starting from zero knowledge and without using any machine learning libraries etc.

Give it a look and/or a run... it's satisfying to watch if nothing else!

## The network
- The network has a fully connected 4-layer structure with [5,4,3,1] nodes in each layer going from the input layer to the output node.
- The 'decision' of the network to jump or not jump for every frame cycle is interpreted by whether or not the output node's value is above 0.5 (on a scale of 0-1 given by the sigmoid function applied on each node). 

## The optimisation algorithm
The learning algorithm uses these ideas from evolution:
- ranking according to fitness (how well each 'bird' in the population does in the game)
- breeding or 'crossover' of properties between instances to create 'offspring' (better instances get to breed with the other best ones)
- mutation to create greater variety

Starting from an initial, randomly generated population which plays the game until all instances have crashed, these evolutionary processes are combined to produce a subsequent new (and hopefully improved) generation so that, across multiple generations, the AI becomes very effective at playing the game.
