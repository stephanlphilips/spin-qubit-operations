from pulse_templates.coherent_control.routines.instruction_builder import quasi_quasm_adder

from witnesses.witness_generator import optimal_witness, stabilizer_witness, mermin_witness
from witnesses.witness_compiler import witness_compiler

def generate_witness_operators(system, qubits, m_operator, witness_type='optimal', repeat = 2, verbose = True):
    '''
    Function that can be called to generate the different measurement operators for a certain witness experiment.
    
    Args:
        system (object) : system that has buildable object to generate the gates in the measurement list
        qubits_used (list<int>) : list with the number of the qubits that are used in the state
        m_operator (list<str>) : list of measurement operators measureable per qubit, in case of combined measurement, refer to the basis and other qubit number.
        witness_type (str) : type of witness to be used (optimal, stabilizer, mermin)
        repeat (int) : repeat the current experiment
        verbose (bool) : show the compiled output
    '''
    witness_generator = None
    if witness_type is 'optimal':
        witness_generator = optimal_witness
    elif witness_type is 'stabilizer':
        witness_generator = stabilizer_witness
    elif witness_type is 'mermin':
        witness_generator = mermin_witness
    else:
        raise ValueError('Witness type not recognized.')

    
    W = witness_generator(len(qubits))
    instruction_list = witness_compiler(W, qubits, m_operator).compile()

    if verbose == True:
        print(instruction_list)

    return quasi_quasm_adder(system, instruction_list, repeat = repeat)
