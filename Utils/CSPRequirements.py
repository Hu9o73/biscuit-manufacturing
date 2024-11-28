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
        
        if state in self.domain or state == "0" or state == None:   # Check if state is in the domain, or 0, or None (for u)
            self.state = state                                      # Assign domain
            pass
        else:
            pass # Do nothing...
    


class Constraint:
    '''Class used to define constraints. Scope are variables related to this constraint.'''

    def __init__(self, name, scope, function = lambda: True):
        self.name = "CONS_" + name  # Name of our constraint
        self.scope = list(scope)    # Scope of the constraint => Variables related to our constraint
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
    



class BiscuitProblem(CSP):
    def __init__(self, name, rollLength, defect_data, biscuit_thresholds):
        super().__init__(name=name, variables=[], constraints=[])
        self.defect_data = defect_data
        self.biscuit_thresholds = biscuit_thresholds
        self.roll = [None] * rollLength  # Initialize the roll list
        self.biscuit_start_pos = []
        
        # Create variables
        for i in range(len(self.roll)):
            self.variables.append(Variable(name=str(i), domain=[0, 1, 2, 3]))

        # Create Constraints
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
