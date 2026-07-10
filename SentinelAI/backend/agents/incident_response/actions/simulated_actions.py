"""Concrete simulated incident response actions."""

from agents.incident_response.actions.base import SimulatedResponseAction
from agents.incident_response.constants import (
    ACTION_BLOCK_IP,
    ACTION_DISABLE_USER,
    ACTION_DISCONNECT_DEVICE,
    ACTION_KILL_PROCESS,
    ACTION_SNAPSHOT_VM,
)


class DisableUserAction(SimulatedResponseAction):
    """Simulate disabling a user account."""

    action_name = ACTION_DISABLE_USER

    def build_message(self, *, target: str, context: dict) -> str:
        return f"Simulated user disablement for account '{target}'. No identity provider changes were made."


class BlockIPAction(SimulatedResponseAction):
    """Simulate blocking an IP address."""

    action_name = ACTION_BLOCK_IP

    def build_message(self, *, target: str, context: dict) -> str:
        return f"Simulated firewall block for IP '{target}'. No firewall or network controls were changed."


class KillProcessAction(SimulatedResponseAction):
    """Simulate killing a process."""

    action_name = ACTION_KILL_PROCESS

    def build_message(self, *, target: str, context: dict) -> str:
        host = context.get("device_id", "unknown-device")
        return f"Simulated process termination for '{target}' on '{host}'. No endpoint action was performed."


class DisconnectDeviceAction(SimulatedResponseAction):
    """Simulate disconnecting a device."""

    action_name = ACTION_DISCONNECT_DEVICE

    def build_message(self, *, target: str, context: dict) -> str:
        return f"Simulated device isolation for '{target}'. No EDR or network isolation was performed."


class SnapshotVMAction(SimulatedResponseAction):
    """Simulate creating a VM snapshot."""

    action_name = ACTION_SNAPSHOT_VM

    def build_message(self, *, target: str, context: dict) -> str:
        return f"Simulated VM snapshot for '{target}'. No cloud or hypervisor snapshot was created."


ACTION_REGISTRY = {
    ACTION_DISABLE_USER: DisableUserAction(),
    ACTION_BLOCK_IP: BlockIPAction(),
    ACTION_KILL_PROCESS: KillProcessAction(),
    ACTION_DISCONNECT_DEVICE: DisconnectDeviceAction(),
    ACTION_SNAPSHOT_VM: SnapshotVMAction(),
}
