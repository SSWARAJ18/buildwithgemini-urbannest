"""Seed script to populate Firestore with sample UrbanNest property listings."""

import sys
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-6db14bebe7b8"
COLLECTION_NAME = "properties"

SAMPLE_PROPERTIES = [
    {
        "id": "listing-mission-1br",
        "title": "Sunny Modern 1BR in Mission District",
        "neighborhood": "Mission District",
        "price_per_month": 2950,
        "bedrooms": 1,
        "bathrooms": 1.0,
        "pet_policy": "Dogs and Cats OK",
        "amenities": ["in-unit laundry", "hardwood floors", "bike storage", "shared roof deck"],
        "square_feet": 720,
        "transit_score": 94,
        "description": "Sun-drenched top floor 1BR apartment with exposed brick, stainless steel appliances, and steps from Dolores Park and BART.",
    },
    {
        "id": "listing-soma-2br",
        "title": "Luxury 2BR Loft in SOMA",
        "neighborhood": "SOMA",
        "price_per_month": 4100,
        "bedrooms": 2,
        "bathrooms": 2.0,
        "pet_policy": "Small Dogs OK (< 25 lbs), Cats OK",
        "amenities": ["assigned parking", "fitness center", "in-unit laundry", "concierge", "private balcony"],
        "square_feet": 1150,
        "transit_score": 98,
        "description": "Sleek industrial loft with 14-foot concrete ceilings, chef's kitchen, floor-to-ceiling windows, and EV charging in building.",
    },
    {
        "id": "listing-hayes-studio",
        "title": "Chic Studio near Hayes Valley Green",
        "neighborhood": "Hayes Valley",
        "price_per_month": 2350,
        "bedrooms": 0,
        "bathrooms": 1.0,
        "pet_policy": "Cats only",
        "amenities": ["dishwasher", "walk-in closet", "secure entry", "heat included"],
        "square_feet": 480,
        "transit_score": 96,
        "description": "Quiet courtyard-facing studio in the heart of Hayes Valley boutiques and award-winning dining.",
    },
    {
        "id": "listing-pacheights-3br",
        "title": "Classic 3BR Victorian in Pacific Heights",
        "neighborhood": "Pacific Heights",
        "price_per_month": 5800,
        "bedrooms": 3,
        "bathrooms": 2.5,
        "pet_policy": "Dogs and Cats OK (no size restrictions)",
        "amenities": ["private garage", "in-unit laundry", "fireplace", "fenced yard", "bay views"],
        "square_feet": 1750,
        "transit_score": 86,
        "description": "Grand historic Victorian with modern chef upgrades, bay view dining room, restored period molding, and private landscaped garden.",
    },
    {
        "id": "listing-marina-2br",
        "title": "Bright 2BR Marina Apartment near Chestnut",
        "neighborhood": "Marina",
        "price_per_month": 3750,
        "bedrooms": 2,
        "bathrooms": 1.5,
        "pet_policy": "No pets",
        "amenities": ["hardwood floors", "garage parking", "dishwasher", "on-site laundry"],
        "square_feet": 980,
        "transit_score": 89,
        "description": "Light-filled corner flat one block from Chestnut Street shopping, Marina Green, and Golden Gate Bridge views.",
    },
    {
        "id": "listing-noe-2br",
        "title": "Charming 2BR Flat with Garden Patio in Noe Valley",
        "neighborhood": "Noe Valley",
        "price_per_month": 3600,
        "bedrooms": 2,
        "bathrooms": 1.0,
        "pet_policy": "Dogs and Cats OK",
        "amenities": ["garden patio", "in-unit washer/dryer", "stainless steel appliances", "storage space"],
        "square_feet": 920,
        "transit_score": 88,
        "description": "Quiet, sunny flat on a tree-lined street near 24th Street cafes, Whole Foods, and J-Church Muni line.",
    },
]


def seed_database():
    print(f"Connecting to Firestore with project '{PROJECT_ID}'...")
    db = firestore.Client(project=PROJECT_ID)
    collection_ref = db.collection(COLLECTION_NAME)

    print(f"Seeding {len(SAMPLE_PROPERTIES)} properties into '{COLLECTION_NAME}'...")
    for prop in SAMPLE_PROPERTIES:
        doc_id = prop["id"]
        doc_data = {k: v for k, v in prop.items() if k != "id"}
        collection_ref.document(doc_id).set(doc_data)
        print(f"  ✓ Seeded: {doc_id} - {prop['title']}")

    print("\n✅ Successfully seeded Firestore properties collection!")


if __name__ == "__main__":
    seed_database()
