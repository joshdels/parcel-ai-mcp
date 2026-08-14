import sys
import httpx
import smtplib
import os

from pathlib import Path
from mcp.server import MCPServer
from sqlalchemy.orm import Session
from email.message import EmailMessage
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))
BASE_DIR = Path(__file__).resolve().parents[2]

from app.db.database import engine
from app.service.queries import (
    get_parcels,
    get_parcel_by_prop_id,
    count_all_parcels,
)

load_dotenv(BASE_DIR / ".env")

print("SMTP USER:", os.getenv("SMTP_USERNAME"))
print("SMTP PASSWORD EXISTS:", bool(os.getenv("SMTP_PASSWORD")))

mcp = MCPServer("WilliamsonParcelBot")


@mcp.tool()
def list_parcels(
    min_acres: float | None = None,
    max_acres: float | None = None,
    min_value: float | None = None,
    max_value: float | None = None,
):
    """
    Retrieves the parcels

    Args:
        min_acres/max_acres: for the area.
        min_value/max_value: for market value in dollars.

    """

    try:
        with Session(engine) as session:
            parcels = get_parcels(
                session,
                min_acres,
                max_acres,
                min_value,
                max_value,
            )

            return [
                {
                    "property_id": parcel.prop_id,
                    "owner_name": parcel.owner_name,
                    "market_value": parcel.mkt_value,
                    "situs_address": parcel.situs_addr,
                    "area_acres": area_acres,
                }
                for parcel, area_acres, geojson in parcels
            ]

    except Exception as e:
        return {
            "error": "Failed to list parcels",
            "detail": str(e),
        }


@mcp.tool()
def find_parcel_by_prop_id(prop_id: str):
    """
    Retrives a single parcel

    Args:
        prod_id: str -> property id example R011094
    """

    with Session(engine) as session:
        result = get_parcel_by_prop_id(session, prop_id)

        if result is None:
            return {
                "found": False,
                "message": f"No parcel found with property ID '{prop_id}'.",
            }

        parcel, area_acres = result

        return {
            "found": True,
            "property_id": parcel.prop_id,
            "owner_name": parcel.owner_name,
            "market_value": parcel.mkt_value,
            "situs_address": parcel.situs_addr,
            "area_acres": area_acres,
        }


@mcp.tool()
def get_count_parcels():
    """Count all the present parcels"""

    with Session(engine) as session:
        count = count_all_parcels(session)

        return [{"parcel_count": count}]


@mcp.tool()
async def zoom_to_parcel(prop_id: str):
    """Zoom the map to a parcel by property ID."""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/map/command",
            json={
                "action": "zoom_to_parcel",
                "parcel_id": prop_id,
            },
        )

    response.raise_for_status()

    return f"Map zoom command sent for {prop_id}"


@mcp.tool()
def send_email(
    recipient: str,
    subject: str,
    message: str,
):
    """Send an email using SMTP."""

    sender = os.environ["SMTP_USERNAME"]
    password = os.environ["SMTP_PASSWORD"]

    email = EmailMessage()
    email["From"] = sender
    email["To"] = recipient
    email["Subject"] = subject
    email.set_content(message)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(sender, password)
            smtp.send_message(email)

        return {
            "success": True,
            "message": f"Email sent successfully to {recipient}",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
