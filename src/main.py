import os

from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler


api_token = os.getenv("IBMQ_API_KEY")

def setup_test():
    service = QiskitRuntimeService(
        channel="ibm_quantum", 
        token=api_token
    )

    backend = service.least_busy(operational=True, simulator=False)

    example_circuit = QuantumCircuit(2)
    example_circuit.measure_all()

    sampler = Sampler(backend)
    job = sampler.run([example_circuit])

    print(f"job id: {job.job_id()}")

    result = job.result()

    return result


if __name__ == "__main__":
    result = setup_test()
    print(result)
