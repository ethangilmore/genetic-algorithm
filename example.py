from matplotlib import pyplot as plt
import genetic
import numpy as np

'''
an example of a genetic algorithm optimizing the parameters of a linear equation to find the
line of best fit for given points

there are only two parameters that are being optimized, but is easily scaleable;
    slope(flaot): between -10 and 10 --- this may need to be changed if the best fit line has a more extreme slope

    y-int(flaot): between -10 and 10 --- may also need to be changed depending on the location of the data

feel free to modify/add points or number of generations evolved

ethan gilmore
10/17/19
'''

x_points = [1, 1.5, 1.9, 2.1, 2.75, 4]
y_points = [5, 4.3, 2.4, 3.7, 2.5, 1]

'''
this is the structure for defining a set of parameters, or "gene_structure"

your parameters will be represented inside a dictionary with the keys named what the values represent
the value for each pair will be a 3-tuple

if you want your value to be a
    float: (float, min, max)
        float defines the type, but replace the min and the max fo set the bounds for the variable

    int: (int, min, max)
        int defines the type, replace min and max to set bounds

    list: (list, length, type)
        a list is a little different. the first element will be list to define it as a list
        second is the length, or number of things in the list
        third is the type of variable in the list - a float or an int
        
        example:
            {"my_list": (list, 10, (int, 1, 10))}
            this will create a paramter called my_list which is a list of length 10 filled with ints between 1 and 10
'''
parameters = {"slope": (float, -10, 10), "y-int": (float, -10, 10)}

'''
this is the structure for a fitness function

a fitness function is what determines how good a set of parameters (reffered to as an organism) is.
your fitness function should consist of;

Args:
    parameters / genes(dict): the actual values of an organism, modeled to your predefined structure

Returns:
    (int or float): returns a value specifying how good a set of paramters performed

    keep in mind that organisms (sets of parameters) with the HIGHEST RETURN VALUE when passed through 
    this function are the ones kept and chosen to reproduce
'''

def loss(parameters):
    mean_squared_error = 0
    #find the total error of the line and the points
    for i, x in enumerate(x_points):
        #find the error between the actual y and the y of the function built with slope and y-int
        error = y_points[i] - (x * parameters['slope'] + parameters['y-int'])
        #decrease the mean squared error, because i want the set of parameters with the least difference to be greater
        #i.e. those with a greater error will be have a more negative fitness score
        mean_squared_error -= error**2
    return mean_squared_error

#create a population of size 20 with the paremeters and loss function we created
pop = genetic.Population(20, parameters, loss)
[pop.evolve() for i in range(10000)]

#set the slope and y-int to the organism with the best fitness
slope = pop.organisms[-1]['slope']
y_int = pop.organisms[-1]['y-int']

#used to plot points and the corrosponding line of best fit
plt.plot(x_points, y_points, 'ro')
x = np.linspace(-5,5,100)
y = slope*x+y_int
plt.plot(x, y)
plt.show()