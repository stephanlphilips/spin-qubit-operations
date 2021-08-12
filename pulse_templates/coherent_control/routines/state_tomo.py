from pulse_templates.coherent_control.routines.instruction_builder import quasi_quasm_adder

from routines.state_tomography.state_tomography_generator import state_tomography
from routines.state_tomography.state_tomography_compiler import compile_state_tomography

def generate_state_tomography_operators(system, qubits, m_operator, repeat = 2, verbose = True):
    '''
    Function that can be called to generate the different measurement operators for a certain witness experiment.
    
    Args:
        system (object) : system that has buildable object to generate the gates in the measurement list
        qubits_used (list<int>) : list with the number of the qubits that are used in the state
        m_operator (list<str>) : list of measurement operators measureable per qubit, in case of combined measurement, refer to the basis and other qubit number.
        repeat (int) : repeat the current experiment
        verbose (bool) : show the compiled output
    '''    
    W = state_tomography(len(qubits))
    instruction_list = compile_state_tomography(W, qubits, m_operator)

    if verbose == True:
        print(instruction_list)

    return quasi_quasm_adder(system, instruction_list, repeat = repeat)