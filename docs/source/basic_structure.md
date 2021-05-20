Basic structure
===============

The main idea of the pulse template library is the construct what is called a gates set with.
This is a set of gates that are commonly used in a quantum processor. One can think of this as commands that allow one to say:
```python
Q = my_qubit_system()

# add to the sequence in the qubit system a X180 pulse on qubit 4
Q.add(Q.q4.init)
Q.add(Q.q5.init)

Q.add(Q.q4.X90)
Q.add(Q.q56.CNOT12)

Q.add(Q.q4.read)
Q.add(Q.q5.read)
```

The code above should be sufficient to create a Bell state between qubit pair 4 and 5.

In the coming sections, it will be explained how to makes sets for
* readout / initialization
* single qubit gates
* two qubit gates

At the end we will also show how to bring everything together to get the the example shown above.