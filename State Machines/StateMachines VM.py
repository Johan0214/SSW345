from abc import ABC, abstractmethod

class SM(ABC):
    state = 0
    startState = 0

    def start(self):
        self.state = self.startState

    # step returns the next output.
    # getNextValues returns (nextState, nextOutput)
    def step(self, inp):
        (s, o) = self.getNextValues(self.state, inp)
        self.state = s
        return o

    def transduce(self, inputs):
        self.start()
        return [self.step(inp) for inp in inputs]

    def run(self, n=10):
        return self.transduce([None] * n)

    # by default getNextValues assumes that
    # the output is the next state.
    def getNextValues(self, state, inp):
        nextState = self.getNextState(state, inp)
        return (nextState, nextState)

    @abstractmethod
    def getNextState(self, state, inp):
        pass

class Accumulator(SM):
    # predefine the startState to follow UML
    startState = 0

    def __init__(self, initialValue=0):
        self.startState = initialValue

#    state = 0
#    def getNextValues(self, state, inp):
#        return (state + inp,state + inp)

    def getNextState(self, state, inp):
        return state + inp


a = Accumulator()
print(f"{a.transduce([100,-3,4,-123,10])}")

class Gain(SM):
    def __init__(self, k):
      self.k = k

    def getNextState(self, state, inp):
        return inp * self.k


g = Gain(3)
print(f"{g.transduce([1.1, -2, 100, 5])}")

class UpDown(SM):
    startState = 0
    def getNextState(self, state, inp):
        if inp == 'u':
            return state + 1
        else:
            return state - 1

class Delay(SM):
    def __init__(self, v0):
        self.startState = v0

    def getNextState(self, state, inp):
        return 0

    def getNextValues(self, state, inp):
        return (inp, state)

d = Delay(7)
print(f"{d.transduce([3,1,2,5,9])}")

class Average2(SM):
    startState = 0
    def getNextValues(self, state, inp):
        return (inp, (inp + state) / 2.0)

    def getNextState(self, state, inp):
        return state + inp

a2 = Average2()
print(f"{a2.transduce([10,5,2,10])}")

class SimpleParkingGate(SM):
    startState = 'waiting'

    def generateOutput(self, state):
        if state == 'raising':
            return 'raise'
        elif state == 'lowering':
            return 'lower'
        else:
            return 'nop'

    def getNextValues(self, state, inp):
        (gatePosition, carAtGate, carJustExited) = inp
        if state == 'waiting' and carAtGate:
            nextState = 'raising'
        elif state == 'raising' and gatePosition == 'top':
            nextState = 'raised'
        elif state == 'raised' and carJustExited:
            nextState = 'lowering'
        elif state == 'lowering' and gatePosition == 'bottom':
            nextState = 'waiting'
        else:
            nextState = state
        return (nextState, self.generateOutput(nextState))

    def getNextState(self, state, inp):
        return state

gate = SimpleParkingGate()
# (gatePosition, carAtGate, carJustExited)
gateInput = [
    ('bottom', False, False),
    ('bottom', True, False),
    ('bottom', True, False),
    ('middle', True, False),
    ('middle', True, False),
    ('middle', True, False),
    ('middle', True, False),
    ('top', True, False),
    ('top', True, False),
    ('top', True, False),
    ('top', True, True),
    ('top', True, True),
    ('middle', True, False),
    ('middle', True, False),
    ('bottom', True, False),
    ('bottom', True, False)
]
print(f"{gate.transduce(gateInput)}")

class VendingMachine(SM):
    startState = 'waiting'
    drink_cost = 0.75

    def __init__(self):
        self.balance = 0.0

    def generateOutput(self, state):
        if state == 'dispensing':
            return f'Dispensing drink'
        elif state == 'cancelled':
            return f'Transaction cancelled. Returning {self.balance:.2f} dollars.'
        else:
            return f'Inserted {self.balance:.2f} dollars. Ready to dispense.'

    def getNextValues(self, state, inp):
        if inp is None:
            return (state, 'Waiting for money')
        
        if inp == 'cancel':
            return ('cancelled', self.generateOutput('cancelled'))
        
        if inp in [1.0, 0.25, 0.10, 0.05]:
            self.balance += inp
            
            if self.balance >= self.drink_cost:
                change = self.balance - self.drink_cost
                self.balance = 0.0
                return ('waiting', f'Inserted {self.balance + self.drink_cost:.2f} dollars. Dispensing drink Returning {change:.2f} dollars in change.')
            return ('waiting', self.generateOutput(state))
        
        return (state, 'Invalid input you can only insert nickels, dimes, quarters, or dollar bills.')

    def getNextState(self, state, inp):
        return state

vending_machine = VendingMachine()

scenario_a = vending_machine.transduce([0.25, 0.25, 0.25])
scenario_b = vending_machine.transduce([0.25, 'cancel'])
scenario_c = vending_machine.transduce([0.10, 1.00])

print(f"Scenario a: {scenario_a}") #User inputs three quarters
print(f"Scenario b: {scenario_b}") #User inputs one quarter and then cancels the transaction
print(f"Scenario c: {scenario_c}") #User inputs a dime and a dollar bill