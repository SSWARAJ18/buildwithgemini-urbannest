"""Financial and affordability calculation tools for UrbanNest."""

import json


def calculate_total_occupancy_cost(
    monthly_rent: int,
    has_pet: bool = False,
    needs_parking: bool = False,
    utilities_included: bool = False,
    annual_income: float = 0.0,
) -> str:
    """Calculate the estimated total monthly cost of living for an apartment and assess affordability.

    Args:
        monthly_rent: Base monthly rent in USD (e.g. 2950).
        has_pet: Whether the tenant has a pet (adds estimated pet rent).
        needs_parking: Whether a dedicated parking space is needed.
        utilities_included: Whether utilities (electric, gas, water, internet) are included in rent.
        annual_income: Optional tenant gross annual salary in USD to evaluate the 30% income rule.

    Returns:
        JSON string containing the itemized monthly expense breakdown, total monthly cost,
        recommended annual income, and affordability rating.
    """
    est_utilities = 0 if utilities_included else 150
    est_pet_rent = 60 if has_pet else 0
    est_parking = 250 if needs_parking else 0
    est_insurance = 25

    total_monthly = monthly_rent + est_utilities + est_pet_rent + est_parking + est_insurance
    recommended_annual = round((total_monthly * 12) / 0.30)

    result = {
        "breakdown": {
            "base_rent": monthly_rent,
            "estimated_utilities": est_utilities,
            "pet_rent": est_pet_rent,
            "parking_fee": est_parking,
            "renters_insurance": est_insurance,
        },
        "total_estimated_monthly_cost": total_monthly,
        "recommended_min_annual_income": recommended_annual,
    }

    if annual_income > 0:
        monthly_income = annual_income / 12
        ratio = round((total_monthly / monthly_income) * 100, 1)
        if ratio <= 30.0:
            verdict = f"Comfortable ({ratio}% of monthly income - within standard 30% guideline)"
        elif ratio <= 40.0:
            verdict = f"Moderate Stretch ({ratio}% of monthly income - slightly above 30% guideline)"
        else:
            verdict = f"High Burden ({ratio}% of monthly income - exceeds 40% of income)"
        result["income_analysis"] = {
            "annual_income": annual_income,
            "rent_to_income_percentage": f"{ratio}%",
            "verdict": verdict,
        }

    return json.dumps(result, indent=2)
