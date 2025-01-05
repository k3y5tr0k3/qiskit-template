"""Application main entrypoint."""

import os

from src.utils.config import Config
from src.utils.logging import Logging

from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.exceptions import CircuitError
from qiskit.providers.exceptions import QiskitBackendNotFoundError
from qiskit_ibm_runtime.accounts.exceptions import AccountNotFoundError
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit_ibm_runtime.exceptions import (
    RuntimeJobFailureError,
    RuntimeJobMaxTimeoutError,
    RuntimeInvalidStateError,
)


logger = Logging.get_logger()

API_TOKEN = None
try:
    API_TOKEN = os.getenv("IBMQ_API_KEY")
    assert API_TOKEN is not None
except AssertionError:
    logger.error("IBMQ API Token is `None`")
    exit(100)


def setup_test():
    """Checks that the repository is setup and configured correctly."""
    result = None

    example_circuit = None
    try:
        example_circuit = QuantumCircuit(2)
        example_circuit.measure_all()
    except CircuitError:
        logger.exception(
            "Failed to instantiate QuantumCircuit. Either the circuit "
            "name, if given, is not valid, or both inputs and "
            "captures are given."
        )
        exit(101)

    simulate = Config.get("environment.simulate")

    if not simulate:
        try:
            service = QiskitRuntimeService(channel="ibm_quantum", token=API_TOKEN)
        except AccountNotFoundError:
            logger.exception(
                "Failed to instantiate Qiskit Runtime Service. Check that API"
                "token is set and is correct."
            )
            exit(102)

        else:
            try:
                backend = service.least_busy(operational=True, simulator=False)
            except QiskitBackendNotFoundError:
                logger.exception("No Qiskit backend found that matches the criteria.")
                exit(103)

            else:
                sampler = Sampler(backend)
                try:
                    job = sampler.run([example_circuit])
                except ValueError:
                    logger.exceptions("Invalid parameter passed to Sampler.run().")
                    exit(104)

                else:
                    logger.info(f"Job id: {job.job_id()}.")

                    try:
                        result = job.result()
                    except RuntimeJobFailureError as e:
                        logger.exception(f"{e}")
                    except RuntimeJobMaxTimeoutError as e:
                        logger.exception(f"{e}")
                    except RuntimeInvalidStateError as e:
                        logger.exception(f"{e}")

    else:
        backend = AerSimulator()
        job = backend.run(transpile(example_circuit, backend))
        result = job.result()

    return result


if __name__ == "__main__":
    result = setup_test()
    logger.info(f"Result: {result}")
