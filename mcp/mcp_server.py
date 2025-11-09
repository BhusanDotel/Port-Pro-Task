from fastmcp import FastMCP
from datetime import date
from pydantic import BaseModel
from typing import Dict, Any

mcp = FastMCP("Container MCP")

class FullContainerDetails(BaseModel):
    container: str
    status: str
    location: str
    size: str
    type: str
    holds: list[str]
    last_free_day: date

class AvailabilityResult(BaseModel):
    container: str
    available: bool
    reason: str | None = None

class LocationResult(BaseModel):
    container: str
    location: str
    vessel: str
    terminal: str

class HoldsResult(BaseModel):
    container: str
    holds: list[str]
    cleared: bool

class LastFreeDayResult(BaseModel):
    container: str
    last_free_day: date
    demurrage_start: date


def tool_full_container_details(container: str) -> FullContainerDetails:
    """Return a rich set of dummy details for a container."""
    return FullContainerDetails(
        container=container,
        status="In Yard",
        location="LOS ANGELES, CA",
        size="40",
        type="HC",
        holds=["CUSTOMS", "STEAMSHIP"],
        last_free_day=date.today(),
    )

def tool_check_availability(container: str) -> AvailabilityResult:
    """Return dummy availability."""
    available = hash(container) % 2 == 0
    reason = None if available else "Hold: CUSTOMS"
    return AvailabilityResult(container=container, available=available, reason=reason)

def tool_get_location(container: str) -> LocationResult:
    """Return dummy location info."""
    return LocationResult(
        container=container,
        location="Terminal T123 - Block B",
        vessel="MV Example Star",
        terminal="T123",
    )

def tool_check_holds(container: str) -> HoldsResult:
    """Return dummy holds."""
    holds = ["CUSTOMS"] if hash(container) % 3 == 0 else []
    return HoldsResult(container=container, holds=holds, cleared=len(holds) == 0)

def tool_get_last_free_day(container: str) -> LastFreeDayResult:
    """Return dummy last free day info."""
    lfd = date.today()
    return LastFreeDayResult(
        container=container,
        last_free_day=lfd,
        demurrage_start=lfd.replace(day=lfd.day + 1 if lfd.day < 28 else lfd.day),
    )


@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool()
def full_container_details(container: str) -> Dict[str, Any]:
    """Get full container details."""
    return tool_full_container_details(container).model_dump()

@mcp.tool()
def check_availability(container: str) -> Dict[str, Any]:
    """Check container availability."""
    return tool_check_availability(container).model_dump()

@mcp.tool()
def get_location(container: str) -> Dict[str, Any]:
    """Get container location."""
    return tool_get_location(container).model_dump()

@mcp.tool()
def check_holds(container: str) -> Dict[str, Any]:
    """Check holds on container."""
    return tool_check_holds(container).model_dump()

@mcp.tool()
def get_last_free_day(container: str) -> Dict[str, Any]:
    """Get last free day for container."""
    return tool_get_last_free_day(container).model_dump()

# fastmcp run my_server.py:mcp --transport http --port 8000
#fastmcp run mcp_server.py:mcp

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)