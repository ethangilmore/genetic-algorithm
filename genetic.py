import random

'''
    a simple but versitile class to help with genetic algorithms - a method of optimizaiton that takes
    inspiration from natural processes - to be used in future personal projects

    ethan gilmore
    10/16/19

'''

class Population:
    def __init__(self, size, gene_structure, fitness_function, mutation_rate = 0.0125):
        self.size = size
        self.organisms = []
        self.structure = gene_structure
        self.fitness_function = fitness_function
        self.mutation_rate = mutation_rate
        self.populate()

    def val_from_structure(self, gene):
        '''
        translates a gene name into a value using the specefied gene structure

        Args:
            gene(string): the name of the parameter (the key) in the gene structure dictionary

        Returns:
            a value within the rules specified in the given gene structure

        '''
        #get the type, min, and max from the gene structure
        settings = self.structure[gene]

        #if the gene structure says float give it a float between max and min
        if(settings[0] == float):
            value = random.uniform(settings[1], settings[2])
        #basically same but an int
        elif(settings[0] == int):
            value = random.randint(settings[1], settings[2])
        elif(settings[0] == list):
            if(settings[2][0] == int):
                #if a list if given of type int, return a list of ints between min and max
                value = [random.randint(settings[2][1], settings[2][2]) for i in range(settings[1])]
            elif(settings[2][0] == float):
                #same for floats
                value = [random.uniform(settings[2][1], settings[2][2]) for i in range(settings[1])]
        else:
            value = None
        return value

    def populate(self):
        '''
        populates self.organisms according to the gene structure given when Population is initialized

        valid gene structure is a dict where the keys are the names of the parameters (referred to as genes), and paired values are a tuple
        consisting of first: the primitive type of the paramter, and second: another tuple containing the min and max of the parameter

        Args:
            size(int): the number of organisms to be added to self.organisms

        Returns:
            None
        '''

        for i in range(self.size):
            organism = {}
            for gene in self.structure:
                organism[gene] = self.val_from_structure(gene)
            self.organisms.append(organism)

    def breed(self, parents):
        '''
        used to produce a single new organism with values for genes selected randomly from each parent

        Args:
            parents(tuple): a tuple containing two parents to be bred

        Return:
            dict: returns a new dict representing a child organism with values randomly chosen between parents
        '''
        child = {}
        for gene in parents[0]:
            #dont pass down the fitness score because it will need to be recalculated anywyas
            if(gene == 'fitness_score'):
                continue

            #for basic primitive types
            if(self.structure[gene][0] != list):
                #pick a value from a random parent
                if(random.randint(0, 1)):
                    child[gene] = parents[0][gene]
                else:
                    child[gene] = parents[1][gene]

            #for lists
            else:
                new_list = []
                for i in range(self.structure[gene][1]):
                    #go through every index of list and pick a value from a random parents list
                    if(random.randint(0, 1)):
                        new_list.append(parents[0][gene][i])
                    else:
                        new_list.append(parents[1][gene][i])
                #set the new list of values from both parents to the child
                child[gene] = new_list

        return child

    def mutate(self, organism, mutation_rate=0.0125):
        '''
        will sometimes mutate a parameter in the given organism based on the gene structure given during initializion

        Args:
            organism(dict): a dict which represents a single organism

        Returns:
            (dict): returns a dict representing the mutated organism
        '''
        for gene in organism:
            #dont mutate the fitness score
            if(gene == 'fitness_score'):
                continue

            #for primitive types
            if(self.structure[gene][0] != list):
                #on random occasion change the type
                if(random.random() < self.mutation_rate):
                    organism[gene] = self.val_from_structure(gene)
            #for lists
            else:
                settings = self.structure[gene]
                #go through every item in list
                for i in range(self.structure[gene][1]):
                    if(random.random() < self.mutation_rate):
                        #on random occasion change the value with same type and range
                        if(settings[2][0] == int):
                            organism[gene][i] = random.randint(settings[2][1], settings[2][2])
                        elif(settings[2][0] == float):
                            organism[gene][i] = random.uniform(settings[2][1], settings[2][2])
        return organism

    def set_fitnesses(self):
        '''
        sets the fitness score of each organism based on the fitness function given during initialization

        Args:
            None
        Returns:
            None
        '''
        for organism in self.organisms:
            #use the fitness function given in init to set fitnesses
            organism["fitness_score"] = self.fitness_function(organism)

    def sort_by_fitness(self):
        '''
        sorts the organisms based on their fitness score

        Args:
            None
        Returns:
            None
        '''
        self.organisms = sorted(self.organisms, key=lambda k: k["fitness_score"])

    def keep_fittest(self):
        '''
        discards the organisms with fitness scores below the median

        Args:
            None
        Returns:
            None
        '''
        self.sort_by_fitness()
        mid = int(len(self.organisms)/2)
        #only keep the best half
        self.organisms = self.organisms[mid:]

    def repopulate(self):
        '''
        refills the population to the size specified in initialization by breeding the most fit 

        Args:
            None
        Returns:
            None
        '''

        children = []
        #calculate how many children need to be made
        missing = self.size - len(self.organisms)
        for i in range(missing):
            #get random tuple of parents
            parents = random.choice(self.organisms), random.choice(self.organisms)
            child = self.breed(parents)
            #breed and add to list
            children.append(child)
        #add children to the total list
        self.organisms += children

    def evolve(self):
        '''
        call this method to have the population undergo one generation of evolution

        Args:
            None
        Returns:
            dict: returns a dict representing the most fit after the evolution
        '''

        #basically calls internal methods in correct order to undergo one evolution
        self.set_fitnesses()
        self.keep_fittest()
        self.repopulate()
        for i in range(len(self.organisms)):
            self.organisms[i] = self.mutate(self.organisms[i])
        self.set_fitnesses()
        return self.organisms[-1]



