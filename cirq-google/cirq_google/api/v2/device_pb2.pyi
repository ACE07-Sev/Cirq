"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class DeviceSpecification(google.protobuf.message.Message):
    """This contains information about a device that includes the
    qubits on the device, supported gates, connections, and timing.
    This message specifies information that is needed when sending a
    Program message to the device.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALID_GATE_SETS_FIELD_NUMBER: builtins.int
    VALID_GATES_FIELD_NUMBER: builtins.int
    VALID_QUBITS_FIELD_NUMBER: builtins.int
    VALID_TARGETS_FIELD_NUMBER: builtins.int
    DEVELOPER_RECOMMENDATIONS_FIELD_NUMBER: builtins.int
    developer_recommendations: builtins.str
    """Additional recommendations, caveats, and soft requirements that
    are advice to users of the device, specified in English text
    For instance, "All Z gates are converted to VirtualZ gates".
    """
    @property
    def valid_gate_sets(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___GateSet]:
        """A list of allowed gatesets for programs submitted to this processor
        Language.gate_set should be one of these values to be valid.
        """

    @property
    def valid_gates(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___GateSpecification]:
        """The device gateset.
        Contains the list of gates allowed in programs submitted to this processor.
        """

    @property
    def valid_qubits(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """A list of allowed ids for qubits within the Program.
        Any programs with ids not in this list will be rejected.
        If empty, all qubit values are allowed (e.g. in a simulator)
        Only grid qubits are supported. Strings must be in the form '<int>_<int>'.
        Single-qubit gates can be applied to all qubits.
        Measurement and wait gates can be applied to all subset of qubits.
        """

    @property
    def valid_targets(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___TargetSet]:
        """A list of targets that gates can use."""

    def __init__(
        self,
        *,
        valid_gate_sets: collections.abc.Iterable[global___GateSet] | None = ...,
        valid_gates: collections.abc.Iterable[global___GateSpecification] | None = ...,
        valid_qubits: collections.abc.Iterable[builtins.str] | None = ...,
        valid_targets: collections.abc.Iterable[global___TargetSet] | None = ...,
        developer_recommendations: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["developer_recommendations", b"developer_recommendations", "valid_gate_sets", b"valid_gate_sets", "valid_gates", b"valid_gates", "valid_qubits", b"valid_qubits", "valid_targets", b"valid_targets"]) -> None: ...

global___DeviceSpecification = DeviceSpecification

@typing.final
class GateSpecification(google.protobuf.message.Message):
    """This contains information about a single device gate.
    Replaces `GateDefinition`.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class Sycamore(google.protobuf.message.Message):
        """Gate types available to Google devices.
        Future gates may have parameter constraints that are frequently updated.
        In such cases, the gate message will contain additional fields to specify
        those constraints.
        """

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        def __init__(
            self,
        ) -> None: ...

    @typing.final
    class SqrtISwap(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        def __init__(
            self,
        ) -> None: ...

    @typing.final
    class SqrtISwapInv(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        def __init__(
            self,
        ) -> None: ...

    @typing.final
    class CZ(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        def __init__(
            self,
        ) -> None: ...

    @typing.final
    class PhasedXZ(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        def __init__(
            self,
        ) -> None: ...

    @typing.final
    class VirtualZPow(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        def __init__(
            self,
        ) -> None: ...

    @typing.final
    class PhysicalZPow(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        def __init__(
            self,
        ) -> None: ...

    @typing.final
    class CouplerPulse(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        def __init__(
            self,
        ) -> None: ...

    @typing.final
    class Measurement(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        def __init__(
            self,
        ) -> None: ...

    @typing.final
    class Wait(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        def __init__(
            self,
        ) -> None: ...

    @typing.final
    class FSimViaModel(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        def __init__(
            self,
        ) -> None: ...

    @typing.final
    class CZPowGate(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        def __init__(
            self,
        ) -> None: ...

    @typing.final
    class InternalGate(google.protobuf.message.Message):
        """This gate gets mapped to the internal representation corresponding
        to <gate_module.gate_name>.
        """

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        def __init__(
            self,
        ) -> None: ...

    @typing.final
    class Reset(google.protobuf.message.Message):
        """This gate resets qubit to its |0> state."""

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        def __init__(
            self,
        ) -> None: ...

    GATE_DURATION_PICOS_FIELD_NUMBER: builtins.int
    SYC_FIELD_NUMBER: builtins.int
    SQRT_ISWAP_FIELD_NUMBER: builtins.int
    SQRT_ISWAP_INV_FIELD_NUMBER: builtins.int
    CZ_FIELD_NUMBER: builtins.int
    PHASED_XZ_FIELD_NUMBER: builtins.int
    VIRTUAL_ZPOW_FIELD_NUMBER: builtins.int
    PHYSICAL_ZPOW_FIELD_NUMBER: builtins.int
    COUPLER_PULSE_FIELD_NUMBER: builtins.int
    MEAS_FIELD_NUMBER: builtins.int
    WAIT_FIELD_NUMBER: builtins.int
    FSIM_VIA_MODEL_FIELD_NUMBER: builtins.int
    CZ_POW_GATE_FIELD_NUMBER: builtins.int
    INTERNAL_GATE_FIELD_NUMBER: builtins.int
    RESET_FIELD_NUMBER: builtins.int
    gate_duration_picos: builtins.int
    """This defines the approximate duration to run the gate on the device,
    specified as an integer number of picoseconds.
    """
    @property
    def syc(self) -> global___GateSpecification.Sycamore: ...
    @property
    def sqrt_iswap(self) -> global___GateSpecification.SqrtISwap: ...
    @property
    def sqrt_iswap_inv(self) -> global___GateSpecification.SqrtISwapInv: ...
    @property
    def cz(self) -> global___GateSpecification.CZ: ...
    @property
    def phased_xz(self) -> global___GateSpecification.PhasedXZ: ...
    @property
    def virtual_zpow(self) -> global___GateSpecification.VirtualZPow: ...
    @property
    def physical_zpow(self) -> global___GateSpecification.PhysicalZPow: ...
    @property
    def coupler_pulse(self) -> global___GateSpecification.CouplerPulse: ...
    @property
    def meas(self) -> global___GateSpecification.Measurement: ...
    @property
    def wait(self) -> global___GateSpecification.Wait: ...
    @property
    def fsim_via_model(self) -> global___GateSpecification.FSimViaModel: ...
    @property
    def cz_pow_gate(self) -> global___GateSpecification.CZPowGate: ...
    @property
    def internal_gate(self) -> global___GateSpecification.InternalGate: ...
    @property
    def reset(self) -> global___GateSpecification.Reset: ...
    def __init__(
        self,
        *,
        gate_duration_picos: builtins.int = ...,
        syc: global___GateSpecification.Sycamore | None = ...,
        sqrt_iswap: global___GateSpecification.SqrtISwap | None = ...,
        sqrt_iswap_inv: global___GateSpecification.SqrtISwapInv | None = ...,
        cz: global___GateSpecification.CZ | None = ...,
        phased_xz: global___GateSpecification.PhasedXZ | None = ...,
        virtual_zpow: global___GateSpecification.VirtualZPow | None = ...,
        physical_zpow: global___GateSpecification.PhysicalZPow | None = ...,
        coupler_pulse: global___GateSpecification.CouplerPulse | None = ...,
        meas: global___GateSpecification.Measurement | None = ...,
        wait: global___GateSpecification.Wait | None = ...,
        fsim_via_model: global___GateSpecification.FSimViaModel | None = ...,
        cz_pow_gate: global___GateSpecification.CZPowGate | None = ...,
        internal_gate: global___GateSpecification.InternalGate | None = ...,
        reset: global___GateSpecification.Reset | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["coupler_pulse", b"coupler_pulse", "cz", b"cz", "cz_pow_gate", b"cz_pow_gate", "fsim_via_model", b"fsim_via_model", "gate", b"gate", "internal_gate", b"internal_gate", "meas", b"meas", "phased_xz", b"phased_xz", "physical_zpow", b"physical_zpow", "reset", b"reset", "sqrt_iswap", b"sqrt_iswap", "sqrt_iswap_inv", b"sqrt_iswap_inv", "syc", b"syc", "virtual_zpow", b"virtual_zpow", "wait", b"wait"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["coupler_pulse", b"coupler_pulse", "cz", b"cz", "cz_pow_gate", b"cz_pow_gate", "fsim_via_model", b"fsim_via_model", "gate", b"gate", "gate_duration_picos", b"gate_duration_picos", "internal_gate", b"internal_gate", "meas", b"meas", "phased_xz", b"phased_xz", "physical_zpow", b"physical_zpow", "reset", b"reset", "sqrt_iswap", b"sqrt_iswap", "sqrt_iswap_inv", b"sqrt_iswap_inv", "syc", b"syc", "virtual_zpow", b"virtual_zpow", "wait", b"wait"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["gate", b"gate"]) -> typing.Literal["syc", "sqrt_iswap", "sqrt_iswap_inv", "cz", "phased_xz", "virtual_zpow", "physical_zpow", "coupler_pulse", "meas", "wait", "fsim_via_model", "cz_pow_gate", "internal_gate", "reset"] | None: ...

global___GateSpecification = GateSpecification

@typing.final
class GateSet(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    VALID_GATES_FIELD_NUMBER: builtins.int
    name: builtins.str
    """The name of the gate set corresponding to Language.gate_set"""
    @property
    def valid_gates(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___GateDefinition]:
        """A list of valid gates permitted by this gate set"""

    def __init__(
        self,
        *,
        name: builtins.str = ...,
        valid_gates: collections.abc.Iterable[global___GateDefinition] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["name", b"name", "valid_gates", b"valid_gates"]) -> None: ...

global___GateSet = GateSet

@typing.final
class GateDefinition(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    NUMBER_OF_QUBITS_FIELD_NUMBER: builtins.int
    VALID_ARGS_FIELD_NUMBER: builtins.int
    GATE_DURATION_PICOS_FIELD_NUMBER: builtins.int
    VALID_TARGETS_FIELD_NUMBER: builtins.int
    id: builtins.str
    """The name for the gate.  This must match the Gate.id in your program."""
    number_of_qubits: builtins.int
    """If unset or set to zero, any number of qubits is allowed."""
    gate_duration_picos: builtins.int
    """This defines the approximate amount of time for each gate,
    specified as an integer number of picoseconds.
    """
    @property
    def valid_args(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ArgDefinition]:
        """The name of the arguments that should be specified for
        an operation of this gate
        """

    @property
    def valid_targets(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Valid targets that this gate can use.
        Values in this list correspond to the name of the TargetSet
        If unset, all combinations with number_of_qubits target are allowed.
        """

    def __init__(
        self,
        *,
        id: builtins.str = ...,
        number_of_qubits: builtins.int = ...,
        valid_args: collections.abc.Iterable[global___ArgDefinition] | None = ...,
        gate_duration_picos: builtins.int = ...,
        valid_targets: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["gate_duration_picos", b"gate_duration_picos", "id", b"id", "number_of_qubits", b"number_of_qubits", "valid_args", b"valid_args", "valid_targets", b"valid_targets"]) -> None: ...

global___GateDefinition = GateDefinition

@typing.final
class ArgDefinition(google.protobuf.message.Message):
    """A description of an argument to an operation."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _ArgType:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _ArgTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[ArgDefinition._ArgType.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        UNSPECIFIED: ArgDefinition._ArgType.ValueType  # 0
        FLOAT: ArgDefinition._ArgType.ValueType  # 1
        REPEATED_BOOLEAN: ArgDefinition._ArgType.ValueType  # 2
        STRING: ArgDefinition._ArgType.ValueType  # 3

    class ArgType(_ArgType, metaclass=_ArgTypeEnumTypeWrapper):
        """Note: This should be kept in sync with the ArgValue proto"""

    UNSPECIFIED: ArgDefinition.ArgType.ValueType  # 0
    FLOAT: ArgDefinition.ArgType.ValueType  # 1
    REPEATED_BOOLEAN: ArgDefinition.ArgType.ValueType  # 2
    STRING: ArgDefinition.ArgType.ValueType  # 3

    NAME_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    ALLOWED_RANGES_FIELD_NUMBER: builtins.int
    name: builtins.str
    """The name of the argument
    This corresponds to the valid key values for the
    map value of Operation.args
    """
    type: global___ArgDefinition.ArgType.ValueType
    """The type of the argument.
    This should correspond to the legal assignment
    of the Arg.arg oneof for this argument
    """
    @property
    def allowed_ranges(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ArgumentRange]:
        """This should only be populated for type FLOAT.
        If not set, all float values are allowed.
        """

    def __init__(
        self,
        *,
        name: builtins.str = ...,
        type: global___ArgDefinition.ArgType.ValueType = ...,
        allowed_ranges: collections.abc.Iterable[global___ArgumentRange] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["allowed_ranges", b"allowed_ranges", "name", b"name", "type", b"type"]) -> None: ...

global___ArgDefinition = ArgDefinition

@typing.final
class ArgumentRange(google.protobuf.message.Message):
    """Minimum value is inclusive and maximum value is exclusive.
    If minimum and maximum values are the same, only a single value is allowed.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MINIMUM_VALUE_FIELD_NUMBER: builtins.int
    MAXIMUM_VALUE_FIELD_NUMBER: builtins.int
    minimum_value: builtins.float
    maximum_value: builtins.float
    def __init__(
        self,
        *,
        minimum_value: builtins.float = ...,
        maximum_value: builtins.float = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["maximum_value", b"maximum_value", "minimum_value", b"minimum_value"]) -> None: ...

global___ArgumentRange = ArgumentRange

@typing.final
class TargetSet(google.protobuf.message.Message):
    """A list of targets that are valid for a set of gates.
    For instance, all qubit pairs that can be acted on by a 2-qubit gate
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _TargetOrdering:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _TargetOrderingEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[TargetSet._TargetOrdering.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        UNSPECIFIED: TargetSet._TargetOrdering.ValueType  # 0
        SYMMETRIC: TargetSet._TargetOrdering.ValueType  # 1
        """Symmetric gates, any id order within each target is valid.
        Two-qubit gates can be applied to all two-element targets in a TargetSet
        of this type.
        """
        ASYMMETRIC: TargetSet._TargetOrdering.ValueType  # 2
        """Asymmetric gates, the order of ids in each target is important.
        Only the order specified in each target is valid.
        Deprecated: Unused
        """
        SUBSET_PERMUTATION: TargetSet._TargetOrdering.ValueType  # 3
        """All targets in this TargetSet should contain only a single qubit id.
        Gates using this TargetSet can be applied to any subset of these targets
        in any order.
        For example, this could be the case for measurement gates that can
        measure any subset of qubits at once.
        Deprecated: Measurement gate can be applied to all subset of qubits.
        """

    class TargetOrdering(_TargetOrdering, metaclass=_TargetOrderingEnumTypeWrapper): ...
    UNSPECIFIED: TargetSet.TargetOrdering.ValueType  # 0
    SYMMETRIC: TargetSet.TargetOrdering.ValueType  # 1
    """Symmetric gates, any id order within each target is valid.
    Two-qubit gates can be applied to all two-element targets in a TargetSet
    of this type.
    """
    ASYMMETRIC: TargetSet.TargetOrdering.ValueType  # 2
    """Asymmetric gates, the order of ids in each target is important.
    Only the order specified in each target is valid.
    Deprecated: Unused
    """
    SUBSET_PERMUTATION: TargetSet.TargetOrdering.ValueType  # 3
    """All targets in this TargetSet should contain only a single qubit id.
    Gates using this TargetSet can be applied to any subset of these targets
    in any order.
    For example, this could be the case for measurement gates that can
    measure any subset of qubits at once.
    Deprecated: Measurement gate can be applied to all subset of qubits.
    """

    NAME_FIELD_NUMBER: builtins.int
    TARGET_ORDERING_FIELD_NUMBER: builtins.int
    TARGETS_FIELD_NUMBER: builtins.int
    name: builtins.str
    """The name of the target list.
    This will be referenced in the GateDefinition to denote
    which targets are valid.
    """
    target_ordering: global___TargetSet.TargetOrdering.ValueType
    """The type of ordering of the ids within each target in this set.
    For instance, if the ids within each target are symmetric.
    """
    @property
    def targets(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Target]:
        """A list of targets that are valid"""

    def __init__(
        self,
        *,
        name: builtins.str = ...,
        target_ordering: global___TargetSet.TargetOrdering.ValueType = ...,
        targets: collections.abc.Iterable[global___Target] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["name", b"name", "target_ordering", b"target_ordering", "targets", b"targets"]) -> None: ...

global___TargetSet = TargetSet

@typing.final
class Target(google.protobuf.message.Message):
    """A description of a valid target of a multi-qubit gate operation
    For most Google devices, this will be a pair of qubit ids.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    IDS_FIELD_NUMBER: builtins.int
    @property
    def ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """A list of qubit ids that form a valid gate target."""

    def __init__(
        self,
        *,
        ids: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["ids", b"ids"]) -> None: ...

global___Target = Target
