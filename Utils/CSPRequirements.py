import copy
from Utils import ConstraintDefinition as cd

class Variable:
    '''Class used to define variables.'''
    def __init__(self, name, domain, state = None):
        self.name = "VAR_" + name           # Name of our constraint
        self.domain = list(domain)          # Values it can take
        self.state = state                  # Base state is None

    def __str__(self):
        return "Variable {} | State : {} | Domain : {}\n".format(self.name, self.state, self.domain)
    

    def setState(self, state):
        '''Function to set the state "properly". Verifying that the state passed as a parameter is in the domain.'''
        
        if state in self.domain or state == None:   # Check if state is in the domain, or 0, or None (for u)
            self.state = state                                      # Assign domain
            pass
        else:
            pass # Do nothing...
    


class Constraint:
    '''Class used to define constraints. Scope are variables related to this constraint.'''

    def __init__(self, name, scope, function = lambda: True):
        self.name = "CONS_" + name  # Name of our constraint
        if not isinstance(scope, CSP):
            self.scope = list(scope)  # Scope of the constraint => Variables related to our constraint
        else:
            self.scope = scope

        self.function = function    # Assigning the bool function that states if our constraint is respected or not. If nothing specified, we return True no matter what

    def __str__(self):
        return self.name

    
    def check(self):
        '''Check if constraint is respected by applying its associted function to its scope
        (= the variables related to the constraint.)'''
        if self.function(self.scope) == False:
                return False
        
        return True 
    

class CSP:
    '''Base class for Constraint Satisfaction Problem declaration.'''

    def __init__(self, name, variables, constraints):
        self.name = "CSP_" + name       # Name of the problem
        self.variables = variables      # Variables of the problem
        self.constraints = constraints  # Constraints of the problem. Each constraint has variables related to it. Make sure they're included inthe variables list.

    def __str__(self):
        return self.name
    
    def select_unassigned_variable(self):
        '''Select a variable that has not yet been assigned a value.'''
        for var in self.variables:
            if var.state is None:
                return var
        return None  # All variables are assigned
    
    
    



class BiscuitProblem(CSP):
    def __init__(self, name, rollLength, defect_data, biscuit_thresholds):
        super().__init__(name=name, variables=[], constraints=[])
        self.defect_data = defect_data
        self.biscuit_thresholds = biscuit_thresholds
        self.roll = [None] * rollLength  # Initialize the roll list
        self.biscuit_start_pos = []
        self.bestValue = 0
        self.bestRoll = []
        self.bestValues = []
        self.step = 0
        
        # Create variables
        for i in range(len(self.roll)):
            self.variables.append(Variable(name=str(i), domain=[0, 1, 2, 3]))

        # Create Constraints
        self.constraints.append(Constraint("noOverlap", self, cd.noOverlap))
        self.constraints.append(Constraint("defectsUnderThreshold", self, cd.defectsUnderThreshold))
        self.constraints.append(Constraint("fitOnRoll", self.variables, cd.biscuitsFitOnRoll))


    def assignBiscuitToSpot(self, x, biscuitType):
        biscuitLength = int(self.biscuit_thresholds[biscuitType]['size'])

        if x + biscuitLength > len(self.roll):
            return False

        for i in range(x, x+biscuitLength):
            if self.roll[i] is not None:
                return False

        for i in range(x, x+biscuitLength):
            self.roll[i] = biscuitType
            self.variables[i].setState(biscuitType)
        
        self.biscuit_start_pos.append(x)
        return True
    
    def removeBiscuitFromSpot(self, x):
        if x not in self.biscuit_start_pos:
            return False
        
        localBiscuitType = self.roll[x]
        localBiscuitLength = int(self.biscuit_thresholds[localBiscuitType]['size'])

        for i in range(x, x+localBiscuitLength):
            self.roll[i] = None
            self.variables[i].setState(None)

        self.biscuit_start_pos.remove(x)

        return True
    
    def next_free_spot(self):
        for i in range(len(self.roll)):
            if self.roll[i] is None:
                return i
        
        return None

    def computeRollValue(self):
        totalValue = 0
        for x in self.biscuit_start_pos:
            biscuitType = self.roll[x]
            totalValue += self.biscuit_thresholds[biscuitType]['value']

        return totalValue

    def is_complete(self):
        noneCount = 0
        for i in self.roll:
            if i is None:
                noneCount += 1

        if noneCount <= 2:
            return True
        else:
            return False

    def is_consistent(self, variable, value):
        '''Check if assigning `value` to `variable` is consistent with constraints.'''
        # Temporarily set the variable's state
        variable.setState(value)
        x_pos = int(variable.name[4:])  # Slice off the first 4 characters ("VAR_") and convert the remaining part to an integer.

        if(self.assignBiscuitToSpot(x_pos, value)):
            # Check all constraints
            for constraint in self.constraints:
                if not constraint.check():
                    variable.setState(None)  # Reset state
                    self.removeBiscuitFromSpot(x_pos)
                    return False
        else:
            variable.setState(None)  # Reset state
            return False
        
        variable.setState(None)  # Reset state
        return True

    def backtrack(self):
        '''Backtracking algorithm to solve the biscuit CSP.'''
        
        self.step +=1 

        #if(self.step%100000 == 0):
            #print("Current step: ", self.step)

        rollValue = self.computeRollValue()
        if rollValue > self.bestValue:
            self.bestValue = rollValue
            self.bestValues.append([rollValue, copy.deepcopy(self.step)])
            self.bestRoll = copy.deepcopy(self.roll)
        

        # Select an unassigned spot
        x_spot = self.next_free_spot()
        
        if x_spot is None:
            return None
        
        # Get the corresponding variable
        variable = self.variables[x_spot]
            

        # Try every value in the variable's domain
        for value in variable.domain:
            if self.is_consistent(variable, value):
                # Assign value to spot
                self.assignBiscuitToSpot(x_spot, value)
                
                # Recurse
                result = self.backtrack()

                if result is not None:
                    return result

                # Backtrack
                self.removeBiscuitFromSpot(x_spot)

        return None  # Failure to assign a value for this variable
