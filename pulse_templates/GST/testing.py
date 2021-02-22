import pygsti
from pygsti.objects import Circuit, Model, DataSet


c = Circuit( [('Gx',0),[('Gcnot',0,1),('Gy',1)]])

# c = Circuit( [('Gx',0),[('Gcnot',0,1),('Gy',3)],()])
# print(c)

# c = Circuit( ['Gx','Gy','Gi'] )
# print(c)


# c = Circuit( ['rho',('Gz',1),[('Gswap',0,1),('Gy',2)],'Mz'] , line_labels=[0,1,2])
# print(c)


mdl = pygsti.construction.build_explicit_model((0,1),
            [(),      ('Gx',0),    ('Gy',0),    ('Gx',1),    ('Gy',1),    ('Gcnot',0,1)],
            ["I(0,1)","X(pi/2,0)", "Y(pi/2,0)", "X(pi/2,1)", "Y(pi/2,1)", "CNOT(0,1)"])

# print("Preparations: ", ', '.join(map(str,mdl.preps.keys())))
# print("Measurements: ", ', '.join(map(str,mdl.povms.keys())))
# print("Layer Ops: ",    ', '.join(map(str,mdl.operations.keys())))

# c = Circuit( [('Gx',0),('Gcnot',0,1),('Gy',1)] , line_labels=[0,1])
# print(c)
# p = mdl.probs(c) # Compute the outcome probabilities of circuit `c`

    
# print("Probability_of_outcome(00) = ", p['00']) # p is like a dictionary of outcomes


circuit_list = pygsti.construction.circuit_list([ (), 
                                                  (('Gx',0),),
                                                  (('Gx',0),('Gy',1)),
                                                  (('Gx',0),)*4,
                                                  (('Gx',0),('Gcnot',0,1)),
                                                  (('Gx',0),('Gx',1),('Gy',0)) ], line_labels=(0,1))
ds_fake = pygsti.construction.generate_fake_data(mdl, circuit_list, nSamples=100,
                                                 sampleError='multinomial', seed=8675309)

print(ds_fake)