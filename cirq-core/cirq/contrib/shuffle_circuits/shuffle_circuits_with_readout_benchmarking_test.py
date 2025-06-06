# Copyright 2025 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import itertools

import numpy as np
import pytest

import cirq
from cirq.experiments import (
    random_quantum_circuit_generation as rqcg,
    SingleQubitReadoutCalibrationResult,
)
from cirq.experiments.single_qubit_readout_calibration_test import NoisySingleQubitReadoutSampler
from cirq.study import ResultDict


def _create_test_circuits(qubits: list[cirq.Qid], n_circuits: int) -> list[cirq.Circuit]:
    """Helper function to generate circuits for testing."""
    if len(qubits) < 2:
        raise ValueError(
            "Need at least two qubits to generate two-qubit circuits."
        )  # pragma: no cover
    two_qubit_gates = [cirq.ISWAP**0.5, cirq.CNOT**0.5]
    input_circuits = []
    qubit_pairs = list(itertools.combinations(qubits, 2))
    num_pairs = len(qubit_pairs)
    for i in range(n_circuits):
        gate = two_qubit_gates[i % len(two_qubit_gates)]
        q0, q1 = qubit_pairs[i % num_pairs]
        circuits = rqcg.generate_library_of_2q_circuits(
            n_library_circuits=5, two_qubit_gate=gate, q0=q0, q1=q1
        )
        for circuit in circuits:
            circuit.append(cirq.measure(*qubits, key="m"))
        input_circuits.extend(circuits)
    return input_circuits


def test_shuffled_circuits_with_readout_benchmarking_errors_no_noise():
    """Test shuffled circuits with readout benchmarking with no noise from sampler."""
    qubits = cirq.LineQubit.range(5)

    # Generate random input circuits
    input_circuits = _create_test_circuits(qubits, 3)

    sampler = cirq.Simulator()
    circuit_repetitions = 1
    # allow passing a seed
    rng = 123
    readout_repetitions = 1000

    measurements, readout_calibration_results = (
        cirq.contrib.shuffle_circuits.run_shuffled_with_readout_benchmarking(
            input_circuits,
            sampler,
            circuit_repetitions,
            rng,
            num_random_bitstrings=100,
            readout_repetitions=readout_repetitions,
        )
    )

    for measurement in measurements:
        assert isinstance(measurement, ResultDict)

    for qlist, readout_calibration_result in readout_calibration_results.items():
        assert isinstance(qlist, tuple)
        assert all(isinstance(q, cirq.Qid) for q in qlist)
        assert isinstance(readout_calibration_result, SingleQubitReadoutCalibrationResult)

        assert readout_calibration_result.zero_state_errors == {q: 0 for q in qubits}
        assert readout_calibration_result.one_state_errors == {q: 0 for q in qubits}
        assert readout_calibration_result.repetitions == readout_repetitions
        assert isinstance(readout_calibration_result.timestamp, float)


def test_shuffled_circuits_with_readout_benchmarking_errors_with_noise():
    """Test shuffled circuits with readout benchmarking with noise from sampler."""
    qubits = cirq.LineQubit.range(6)

    # Generate random input circuits
    input_circuits = _create_test_circuits(qubits, 6)

    sampler = NoisySingleQubitReadoutSampler(p0=0.1, p1=0.2, seed=1234)
    circuit_repetitions = 1
    rng = np.random.default_rng()
    readout_repetitions = 1000

    measurements, readout_calibration_results = (
        cirq.contrib.shuffle_circuits.run_shuffled_with_readout_benchmarking(
            input_circuits,
            sampler,
            circuit_repetitions,
            rng,
            num_random_bitstrings=100,
            readout_repetitions=readout_repetitions,
        )
    )

    for measurement in measurements:
        assert isinstance(measurement, ResultDict)

    for qlist, readout_calibration_result in readout_calibration_results.items():
        assert isinstance(qlist, tuple)
        assert all(isinstance(q, cirq.Qid) for q in qlist)
        assert isinstance(readout_calibration_result, SingleQubitReadoutCalibrationResult)

        for error in readout_calibration_result.zero_state_errors.values():
            assert 0.08 < error < 0.12
        for error in readout_calibration_result.one_state_errors.values():
            assert 0.18 < error < 0.22
        assert readout_calibration_result.repetitions == readout_repetitions
        assert isinstance(readout_calibration_result.timestamp, float)


def test_shuffled_circuits_with_readout_benchmarking_errors_with_noise_and_input_qubits():
    """Test shuffled circuits with readout benchmarking with noise from sampler and input qubits."""
    qubits = cirq.LineQubit.range(6)
    readout_qubits = qubits[:4]

    # Generate random input circuits
    input_circuits = _create_test_circuits(qubits, 6)

    sampler = NoisySingleQubitReadoutSampler(p0=0.1, p1=0.3, seed=1234)
    circuit_repetitions = 1
    rng = np.random.default_rng()
    readout_repetitions = 1000

    measurements, readout_calibration_results = (
        cirq.contrib.shuffle_circuits.run_shuffled_with_readout_benchmarking(
            input_circuits,
            sampler,
            circuit_repetitions,
            rng,
            num_random_bitstrings=100,
            readout_repetitions=readout_repetitions,
            qubits=readout_qubits,
        )
    )

    for measurement in measurements:
        assert isinstance(measurement, ResultDict)

    for qlist, readout_calibration_result in readout_calibration_results.items():
        assert isinstance(qlist, tuple)
        assert all(isinstance(q, cirq.Qid) for q in qlist)
        assert isinstance(readout_calibration_result, SingleQubitReadoutCalibrationResult)

        for error in readout_calibration_result.zero_state_errors.values():
            assert 0.08 < error < 0.12
        for error in readout_calibration_result.one_state_errors.values():
            assert 0.28 < error < 0.32
        assert readout_calibration_result.repetitions == readout_repetitions
        assert isinstance(readout_calibration_result.timestamp, float)


def test_shuffled_circuits_with_readout_benchmarking_errors_with_noise_and_lists_input_qubits():
    """Test shuffled circuits with readout benchmarking with noise from sampler and input qubits."""
    qubits_1 = cirq.LineQubit.range(3)
    qubits_2 = cirq.LineQubit.range(4)

    readout_qubits = [qubits_1, qubits_2]

    # Generate random input circuits and append measurements
    input_circuits = _create_test_circuits(qubits_1, 6) + _create_test_circuits(qubits_2, 4)

    sampler = NoisySingleQubitReadoutSampler(p0=0.1, p1=0.3, seed=1234)
    circuit_repetitions = 1
    rng = np.random.default_rng()
    readout_repetitions = 1000

    measurements, readout_calibration_results = (
        cirq.contrib.shuffle_circuits.run_shuffled_with_readout_benchmarking(
            input_circuits,
            sampler,
            circuit_repetitions,
            rng,
            num_random_bitstrings=100,
            readout_repetitions=readout_repetitions,
            qubits=readout_qubits,
        )
    )

    for measurement in measurements:
        assert isinstance(measurement, ResultDict)

    for qlist, readout_calibration_result in readout_calibration_results.items():
        assert isinstance(qlist, tuple)
        assert all(isinstance(q, cirq.Qid) for q in qlist)
        assert isinstance(readout_calibration_result, SingleQubitReadoutCalibrationResult)

        for error in readout_calibration_result.zero_state_errors.values():
            assert 0.08 < error < 0.12
        for error in readout_calibration_result.one_state_errors.values():
            assert 0.28 < error < 0.32
        assert readout_calibration_result.repetitions == readout_repetitions
        assert isinstance(readout_calibration_result.timestamp, float)


def test_can_handle_zero_random_bitstring():
    """Test shuffled circuits without readout benchmarking."""
    qubits_1 = cirq.LineQubit.range(3)
    qubits_2 = cirq.LineQubit.range(4)

    readout_qubits = [qubits_1, qubits_2]

    # Generate random input circuits and append measurements
    input_circuits = _create_test_circuits(qubits_1, 6) + _create_test_circuits(qubits_2, 4)

    sampler = NoisySingleQubitReadoutSampler(p0=0.1, p1=0.3, seed=1234)
    circuit_repetitions = 1
    rng = np.random.default_rng()
    readout_repetitions = 1000

    measurements, readout_calibration_results = (
        cirq.contrib.shuffle_circuits.run_shuffled_with_readout_benchmarking(
            input_circuits,
            sampler,
            circuit_repetitions,
            rng,
            num_random_bitstrings=0,
            readout_repetitions=readout_repetitions,
            qubits=readout_qubits,
        )
    )

    for measurement in measurements:
        assert isinstance(measurement, ResultDict)
    # Check that the readout_calibration_results is empty
    assert len(readout_calibration_results.items()) == 0


def test_empty_input_circuits():
    """Test that the input circuits are empty."""
    with pytest.raises(ValueError, match="Input circuits must not be empty."):
        cirq.contrib.shuffle_circuits.run_shuffled_with_readout_benchmarking(
            [],
            cirq.ZerosSampler(),
            circuit_repetitions=10,
            rng_or_seed=np.random.default_rng(456),
            num_random_bitstrings=5,
            readout_repetitions=100,
        )


def test_non_circuit_input():
    """Test that the input circuits are not of type cirq.Circuit."""
    q = cirq.LineQubit(0)
    with pytest.raises(ValueError, match="Input circuits must be of type cirq.Circuit."):
        cirq.contrib.shuffle_circuits.run_shuffled_with_readout_benchmarking(
            [q],
            cirq.ZerosSampler(),
            circuit_repetitions=10,
            rng_or_seed=np.random.default_rng(456),
            num_random_bitstrings=5,
            readout_repetitions=100,
        )


def test_no_measurements():
    """Test that the input circuits don't have measurements."""
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.H(q))
    with pytest.raises(ValueError, match="Input circuits must have measurements."):
        cirq.contrib.shuffle_circuits.run_shuffled_with_readout_benchmarking(
            [circuit],
            cirq.ZerosSampler(),
            circuit_repetitions=10,
            rng_or_seed=np.random.default_rng(456),
            num_random_bitstrings=5,
            readout_repetitions=100,
        )


def test_zero_circuit_repetitions():
    """Test that the circuit repetitions are zero."""
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.H(q), cirq.measure(q))
    with pytest.raises(ValueError, match="Must provide non-zero circuit_repetitions."):
        cirq.contrib.shuffle_circuits.run_shuffled_with_readout_benchmarking(
            [circuit],
            cirq.ZerosSampler(),
            circuit_repetitions=0,
            rng_or_seed=np.random.default_rng(456),
            num_random_bitstrings=5,
            readout_repetitions=100,
        )


def test_mismatch_circuit_repetitions():
    """Test that the number of circuit repetitions don't match the number of input circuits."""
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.H(q), cirq.measure(q))
    with pytest.raises(
        ValueError,
        match="Number of circuit_repetitions must match the number of" + " input circuits.",
    ):
        cirq.contrib.shuffle_circuits.run_shuffled_with_readout_benchmarking(
            [circuit],
            cirq.ZerosSampler(),
            circuit_repetitions=[10, 20],
            rng_or_seed=np.random.default_rng(456),
            num_random_bitstrings=5,
            readout_repetitions=100,
        )


def test_zero_num_random_bitstrings():
    """Test that the number of random bitstrings is smaller than zero."""
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.H(q), cirq.measure(q))
    with pytest.raises(ValueError, match="Must provide zero or more num_random_bitstrings."):
        cirq.contrib.shuffle_circuits.run_shuffled_with_readout_benchmarking(
            [circuit],
            cirq.ZerosSampler(),
            circuit_repetitions=10,
            rng_or_seed=np.random.default_rng(456),
            num_random_bitstrings=-1,
            readout_repetitions=100,
        )


def test_zero_readout_repetitions():
    """Test that the readout repetitions is zero."""
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.H(q), cirq.measure(q))
    with pytest.raises(
        ValueError, match="Must provide non-zero readout_repetitions for readout" + " calibration."
    ):
        cirq.contrib.shuffle_circuits.run_shuffled_with_readout_benchmarking(
            [circuit],
            cirq.ZerosSampler(),
            circuit_repetitions=10,
            rng_or_seed=np.random.default_rng(456),
            num_random_bitstrings=5,
            readout_repetitions=0,
        )


def test_rng_type_mismatch():
    """Test that the rng is not a numpy random generator or a seed."""
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit(cirq.H(q), cirq.measure(q))
    with pytest.raises(ValueError, match="Must provide a numpy random generator or a seed"):
        cirq.contrib.shuffle_circuits.run_shuffled_with_readout_benchmarking(
            [circuit],
            cirq.ZerosSampler(),
            circuit_repetitions=10,
            rng_or_seed="not a random generator or seed",
            num_random_bitstrings=5,
            readout_repetitions=100,
        )
