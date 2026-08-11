"""LangGraph incident-response workflow."""

from langgraph.graph import END, START, StateGraph

from app.orchestration.nodes.rca_node import rca_node
from app.orchestration.nodes.recommendation_node import (
    recommendation_node,
)
from app.orchestration.nodes.severity_node import severity_node
from app.orchestration.state import IncidentState


def build_incident_graph():
    """Build and compile the incident-response workflow."""

    workflow = StateGraph(IncidentState)

    workflow.add_node(
        "severity_classifier",
        severity_node,
    )

    workflow.add_node(
        "rca_node",
        rca_node,
    )

    workflow.add_node(
        "recommendation_node",
        recommendation_node,
    )

    workflow.add_edge(
        START,
        "severity_classifier",
    )

    workflow.add_edge(
        "severity_classifier",
        "rca_node",
    )

    workflow.add_edge(
        "rca_node",
        "recommendation_node",
    )

    workflow.add_edge(
        "recommendation_node",
        END,
    )

    return workflow.compile()


incident_graph = build_incident_graph()