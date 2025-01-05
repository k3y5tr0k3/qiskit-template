"""Application main entrypoint."""

import os

from src.utils.logging import Logging

from qiskit import QuantumCircuit
from qiskit.circuit.exceptions import CircuitError
from qiskit.providers.exceptions import QiskitBackendNotFoundError
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit_ibm_runtime.accounts.exceptions import AccountNotFoundError
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
    try:
        service = QiskitRuntimeService(channel="ibm_quantum", token=API_TOKEN)
    except AccountNotFoundError:
        logger.exception(
            "Failed to instantiate Qiskit Runtime Service. Check that API"
            "token is set and is correct."
        )
        exit(101)

    else:
        try:
            backend = service.least_busy(operational=True, simulator=False)
        except QiskitBackendNotFoundError:
            logger.exception("No Qiskit backend found that matches the criteria.")
            exit(102)

        else:
            try:
                example_circuit = QuantumCircuit(2)
                example_circuit.measure_all()
            except CircuitError:
                logger.exception(
                    "Failed to instantiate QuantumCircuit. Either the circuit "
                    "name, if given, is not valid, or both inputs and "
                    "captures are given."
                )
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

                    result = None
                    try:
                        result = job.result()
                    except RuntimeJobFailureError as e:
                        logger.exception(f"{e}")
                    except RuntimeJobMaxTimeoutError as e:
                        logger.exception(f"{e}")
                    except RuntimeInvalidStateError as e:
                        logger.exception(f"{e}")

                    return result


if __name__ == "__main__":
    result = setup_test()
    print(result)
