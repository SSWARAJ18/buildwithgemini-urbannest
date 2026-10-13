"""Firestore backend for UrbanNest property listings and tour bookings."""

import json
from google.cloud import firestore

# Hardcoded project ID as required for Agent Platform compatibility
PROJECT_ID = "qwiklabs-gcp-04-6db14bebe7b8"
PROPERTIES_COLLECTION = "properties"
TOURS_COLLECTION = "tours"

_db = None


def get_firestore_client() -> firestore.Client:
    """Return a singleton Firestore client with the hardcoded project ID."""
    global _db
    if _db is None:
        _db = firestore.Client(project=PROJECT_ID)
    return _db


def search_properties(
    neighborhood: str = "",
    max_price: int = 0,
    min_bedrooms: int = 0,
    pets_allowed: bool = False,
) -> str:
    """Search available apartment and housing listings in the Firestore database.

    Args:
        neighborhood: Optional neighborhood to filter by (e.g. 'Mission District', 'SOMA', 'Hayes Valley', 'Marina', 'Pacific Heights').
        max_price: Optional maximum monthly rent in USD (e.g. 3500). Pass 0 for no limit.
        min_bedrooms: Optional minimum number of bedrooms (e.g. 1, 2, 3). Pass 0 for any.
        pets_allowed: If True, only returns listings that allow dogs or cats.

    Returns:
        JSON string containing the list of matching property listings.
    """
    db = get_firestore_client()
    docs = db.collection(PROPERTIES_COLLECTION).stream()

    results = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id

        if neighborhood and neighborhood.lower() not in data.get("neighborhood", "").lower():
            continue
        if max_price > 0 and data.get("price_per_month", 0) > max_price:
            continue
        if min_bedrooms > 0 and data.get("bedrooms", 0) < min_bedrooms:
            continue
        if pets_allowed:
            policy = data.get("pet_policy", "").lower()
            if "no pets" in policy or "not allowed" in policy:
                continue

        results.append(data)

    if not results:
        return json.dumps({"message": "No listings matched your criteria.", "results": []})
    return json.dumps({"count": len(results), "results": results}, indent=2)


def get_property_details(property_id: str) -> str:
    """Get complete details and specs for a specific property listing by ID.

    Args:
        property_id: The unique ID of the property listing (e.g. 'listing-mission-1br').

    Returns:
        JSON string containing the property details or error message if not found.
    """
    db = get_firestore_client()
    doc_ref = db.collection(PROPERTIES_COLLECTION).document(property_id)
    doc = doc_ref.get()
    if not doc.exists:
        return json.dumps({"error": f"Property listing with ID '{property_id}' not found."})
    data = doc.to_dict()
    data["id"] = doc.id
    return json.dumps(data, indent=2)


def add_property_listing(
    title: str,
    neighborhood: str,
    price_per_month: int,
    bedrooms: int,
    bathrooms: float,
    pet_policy: str,
    amenities: list[str],
    square_feet: int,
    description: str = "",
) -> str:
    """Add a new apartment or property listing to the Firestore database.

    Args:
        title: Title of the property (e.g. 'Bright 1BR Flat near Park').
        neighborhood: Neighborhood name (e.g. 'Mission District', 'Noe Valley').
        price_per_month: Monthly rent in USD (e.g. 3100).
        bedrooms: Number of bedrooms (e.g. 1).
        bathrooms: Number of bathrooms (e.g. 1.0 or 1.5).
        pet_policy: Pet rules (e.g. 'Dogs and Cats OK', 'Cats only', 'No pets').
        amenities: List of amenities (e.g. ['in-unit laundry', 'parking', 'balcony']).
        square_feet: Size in square feet (e.g. 750).
        description: Detailed summary of features and location.

    Returns:
        JSON string confirming addition with the generated listing ID.
    """
    db = get_firestore_client()
    doc_ref = db.collection(PROPERTIES_COLLECTION).document()
    data = {
        "title": title,
        "neighborhood": neighborhood,
        "price_per_month": price_per_month,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "pet_policy": pet_policy,
        "amenities": amenities,
        "square_feet": square_feet,
        "description": description,
    }
    doc_ref.set(data)
    return json.dumps({
        "status": "success",
        "listing_id": doc_ref.id,
        "message": f"Successfully created listing '{title}' with ID {doc_ref.id}."
    })


def schedule_tour(
    property_id: str,
    visitor_name: str,
    tour_date: str,
    visitor_contact: str = "",
) -> str:
    """Schedule an in-person apartment tour appointment in Firestore.

    Args:
        property_id: The ID of the property to tour (e.g. 'listing-mission-1br').
        visitor_name: Name of the prospective tenant scheduling the tour.
        tour_date: Requested date and time (e.g. '2026-10-20 at 2:00 PM').
        visitor_contact: Phone number or email for confirmation.

    Returns:
        JSON string confirming tour appointment with booking details.
    """
    db = get_firestore_client()
    prop_doc = db.collection(PROPERTIES_COLLECTION).document(property_id).get()
    prop_title = prop_doc.to_dict().get("title", property_id) if prop_doc.exists else property_id

    tour_ref = db.collection(TOURS_COLLECTION).document()
    tour_data = {
        "property_id": property_id,
        "property_title": prop_title,
        "visitor_name": visitor_name,
        "tour_date": tour_date,
        "visitor_contact": visitor_contact,
        "status": "confirmed",
    }
    tour_ref.set(tour_data)
    return json.dumps({
        "status": "confirmed",
        "confirmation_code": tour_ref.id,
        "property": prop_title,
        "visitor": visitor_name,
        "scheduled_time": tour_date,
        "message": f"Tour confirmed for {visitor_name} at {prop_title} on {tour_date}."
    })
