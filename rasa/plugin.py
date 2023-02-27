import argparse
import functools
import sys
from typing import Any, List, Optional, TYPE_CHECKING, Text, Tuple

import pluggy

from rasa.cli import SubParsersAction

if TYPE_CHECKING:
    from rasa.core.tracker_store import TrackerStore
    from rasa.utils.endpoints import EndpointConfig


hookspec = pluggy.HookspecMarker("rasa")


@functools.lru_cache(maxsize=2)
def plugin_manager() -> pluggy.PluginManager:
    """Initialises a plugin manager which registers hook implementations."""
    _plugin_manager = pluggy.PluginManager("rasa")
    _plugin_manager.add_hookspecs(sys.modules["rasa.plugin"])
    _discover_plugins(_plugin_manager)

    return _plugin_manager


def _discover_plugins(manager: pluggy.PluginManager) -> None:
    try:
        # rasa_plus is an enterprise-ready version of rasa open source
        # which extends existing functionality via plugins
        import rasa_plus

        rasa_plus.init_hooks(manager)
    except ModuleNotFoundError:
        pass


@hookspec  # type: ignore[misc]
def refine_cli(
    subparsers: SubParsersAction,
    parent_parsers: List[argparse.ArgumentParser],
) -> None:
    """Customizable hook for adding CLI commands."""


@hookspec  # type: ignore[misc]
def get_version_info() -> Tuple[Text, Text]:
    """Hook specification for getting plugin version info."""


@hookspec  # type: ignore[misc]
def configure_commandline(cmdline_arguments: argparse.Namespace) -> Optional[Text]:
    """Hook specification for configuring plugin CLI."""


@hookspec  # type: ignore[misc]
def init_telemetry(endpoints_file: Optional[Text]) -> None:
    """Hook specification for initialising plugin telemetry."""


@hookspec  # type: ignore[misc]
def read_endpoints_and_set_env_vars(endpoints_file: Optional[Text]) -> None:
    """Hook specification for reading endpoints and setting env vars."""


@hookspec  # type: ignore[misc]
def load_manager() -> Optional[Any]:
    """Hook specification for loading endpoint manager."""


@hookspec  # type: ignore[misc]
def update_endpoint_config(
    endpoint_config: "EndpointConfig", manager: Optional[Any]
) -> "EndpointConfig":
    """Hook specification for updating endpoint config."""


@hookspec  # type: ignore[misc]
def get_auth_retry_wrapper(tracker_store: "TrackerStore") -> "TrackerStore":
    """Hook specification for wrapping with AuthRetryTrackerStore."""
