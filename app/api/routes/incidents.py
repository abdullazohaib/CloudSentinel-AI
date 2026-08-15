"""Incident management API routes."""

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.database import get_connection


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


VALID_SEVERITIES = {
    "Critical",
    "High",
    "Medium",
    "Low",
}

VALID_STATUSES = {
    "Investigating",
    "Analyzing",
    "Monitoring",
    "Resolved",
}


class IncidentCreate(BaseModel):
    """Request model for creating an incident."""

    service_name: str = Field(
        min_length=1,
        max_length=100,
    )
    severity: str = Field(
        min_length=1,
    )
    description: str = Field(
        min_length=1,
        max_length=5000,
    )
    logs: str = Field(
        default="",
        max_length=20000,
    )

    @classmethod
    def validate_values(cls, values):
        """Validate required text fields."""
        for field_name in ("service_name", "severity", "description"):
            value = values.get(field_name)

            if isinstance(value, str):
                values[field_name] = value.strip()

        return values


class IncidentStatusUpdate(BaseModel):
    """Request model for updating an incident's status."""

    status: str = Field(
        min_length=1,
    )

    @classmethod
    def validate_values(cls, values):
        """Normalize status text."""
        value = values.get("status")

        if isinstance(value, str):
            values["status"] = value.strip()

        return values


def utc_now() -> str:
    """Return the current UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


def row_to_dict(row: Any) -> dict[str, Any]:
    """Convert a SQLite row to a dictionary."""

    return dict(row)


@router.get("")
async def list_incidents(
    search: str | None = Query(default=None),
    severity: str | None = Query(default=None),
    status: str | None = Query(default=None),
) -> dict[str, Any]:
    """Return incidents with optional filtering."""

    connection = get_connection()

    try:
        query = """
            SELECT
                id,
                incident_id,
                service_name,
                severity,
                status,
                description,
                logs,
                created_at,
                updated_at
            FROM incidents
            WHERE 1 = 1
        """

        parameters: list[str] = []

        if search:
            query += """
                AND (
                    incident_id LIKE ?
                    OR service_name LIKE ?
                    OR description LIKE ?
                )
            """

            search_value = f"%{search}%"

            parameters.extend(
                [
                    search_value,
                    search_value,
                    search_value,
                ]
            )

        if severity and severity in VALID_SEVERITIES:
            query += " AND severity = ?"
            parameters.append(severity)

        if status and status in VALID_STATUSES:
            query += " AND status = ?"
            parameters.append(status)

        query += " ORDER BY id DESC"

        rows = connection.execute(
            query,
            parameters,
        ).fetchall()

        incidents = [
            row_to_dict(row)
            for row in rows
        ]

        return {
            "count": len(incidents),
            "incidents": incidents,
        }

    finally:
        connection.close()


@router.get("/summary")
async def incident_summary() -> dict[str, Any]:
    """Return incident dashboard statistics."""

    connection = get_connection()

    try:
        total = connection.execute(
            "SELECT COUNT(*) FROM incidents"
        ).fetchone()[0]

        active = connection.execute(
            """
            SELECT COUNT(*)
            FROM incidents
            WHERE status != 'Resolved'
            """
        ).fetchone()[0]

        critical = connection.execute(
            """
            SELECT COUNT(*)
            FROM incidents
            WHERE severity = 'Critical'
              AND status != 'Resolved'
            """
        ).fetchone()[0]

        resolved = connection.execute(
            """
            SELECT COUNT(*)
            FROM incidents
            WHERE status = 'Resolved'
            """
        ).fetchone()[0]

        return {
            "total": total,
            "active": active,
            "critical": critical,
            "resolved": resolved,
        }

    finally:
        connection.close()


@router.get("/{incident_id}")
async def get_incident(
    incident_id: str,
) -> dict[str, Any]:
    """Return one incident."""

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                id,
                incident_id,
                service_name,
                severity,
                status,
                description,
                logs,
                created_at,
                updated_at
            FROM incidents
            WHERE incident_id = ?
            """,
            (incident_id,),
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Incident not found",
            )

        return row_to_dict(row)

    finally:
        connection.close()


@router.post("", status_code=201)
async def create_incident(
    request: IncidentCreate,
) -> dict[str, Any]:
    """Create a new incident."""

    if request.severity not in VALID_SEVERITIES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid severity. "
                "Use Critical, High, Medium, or Low."
            ),
        )

    timestamp = utc_now()

    connection = get_connection()

    try:
        next_number = (
            connection.execute(
                "SELECT COALESCE(MAX(id), 0) + 1 FROM incidents"
            ).fetchone()[0]
        )

        incident_id = f"INC-{next_number:04d}"

        connection.execute(
            """
            INSERT INTO incidents (
                incident_id,
                service_name,
                severity,
                status,
                description,
                logs,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                incident_id,
                request.service_name,
                request.severity,
                "Investigating",
                request.description,
                request.logs,
                timestamp,
                timestamp,
            ),
        )

        connection.commit()

        row = connection.execute(
            """
            SELECT
                id,
                incident_id,
                service_name,
                severity,
                status,
                description,
                logs,
                created_at,
                updated_at
            FROM incidents
            WHERE incident_id = ?
            """,
            (incident_id,),
        ).fetchone()

        return row_to_dict(row)

    finally:
        connection.close()


@router.patch("/{incident_id}/status")
async def update_incident_status(
    incident_id: str,
    request: IncidentStatusUpdate,
) -> dict[str, Any]:
    """Update an incident's status."""

    if request.status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid status. "
                "Use Investigating, Analyzing, "
                "Monitoring, or Resolved."
            ),
        )

    timestamp = utc_now()

    connection = get_connection()

    try:
        existing = connection.execute(
            """
            SELECT incident_id
            FROM incidents
            WHERE incident_id = ?
            """,
            (incident_id,),
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="Incident not found",
            )

        connection.execute(
            """
            UPDATE incidents
            SET status = ?,
                updated_at = ?
            WHERE incident_id = ?
            """,
            (
                request.status,
                timestamp,
                incident_id,
            ),
        )

        connection.commit()

        row = connection.execute(
            """
            SELECT
                id,
                incident_id,
                service_name,
                severity,
                status,
                description,
                logs,
                created_at,
                updated_at
            FROM incidents
            WHERE incident_id = ?
            """,
            (incident_id,),
        ).fetchone()

        return row_to_dict(row)

    finally:
        connection.close()