from pulse_templates.coherent_control.single_qubit_gates import single_qubit_gate_spec


class gate_descriptor:
    def __init__(self):
        self.label = None
        
    def __get__(self, instance, owner):
        print(self.label, instance, owner, 'bla')
        if instance.__dict__.get(self.label, None) is None:
            raise ValueError('Unable to get {}, gate undefined, please add it to the set.'.format(self.label))

        return instance.__dict__.get(self.label, None)
    
    def __set__(self, instance, value):
        if not isinstance(value, single_qubit_gate_spec):
            raise ValueError('please assign the correct type to the gate (single_qubit_gate_spec type), current type is {}'.format(str(type(value))))
        instance.__dict__[self.label] = value

class DescriptorOwner(type):
    def __new__(cls, name, bases, attrs):
        # find all descriptors, auto-set their labels
        for n, v in attrs.items():
            if isinstance(v, gate_descriptor):
                v.label = n
        return super(DescriptorOwner, cls).__new__(cls, name, bases, attrs)

class load_set_single_qubit:
    '''
    Make a set to generate all the clifford for the single qubit RB.

    Type for the gates : 
        pulse_templates.coherent_control.single_qubit_gates.single_qubit_gate_spec
    '''
    __metaclass__ = DescriptorOwner

    I = gate_descriptor()
    X = gate_descriptor()
    Y = gate_descriptor()
    Z = gate_descriptor()


class Descriptor(object):
    def __init__(self):
        #notice we aren't setting the label here
        self.label = None
        
    def __get__(self, instance, owner):
        return instance.__dict__.get(self.label, None)
    
    def __set__(self, instance, value):
        print(self.label)
        instance.__dict__[self.label] = value

        
class DescriptorOwner(type):
    def __new__(cls, name, bases, attrs):
        print(cls, name, bases, attrs)
        # find all descriptors, auto-set their labels
        for n, v in attrs.items():
            if isinstance(v, Descriptor):
                v.label = n
        return super(DescriptorOwner, cls).__new__(cls, name, bases, attrs)

        
class Foo(metaclass=DescriptorOwner):
    print("start foo")
    x = Descriptor()
    y = Descriptor()
    print("start foo")
    def __init_(self):
        print("start foo init")
    
f = Foo()
f.x = 10
print( f.x, f.y)