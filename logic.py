"""
logic.py — Business Logic for Sugar Management System
------------------------------------------------------
Contains all domain-specific calculation functions.
Kept separate from app.py for clean separation of concerns.
"""

from datetime import datetime, timedelta

# ─── Crop growth periods (months until harvest) ───────────────────────────────
CROP_GROWTH_MONTHS = {
    "Co 86032":      12,
    "CoM 0265":      14,
    "CoC 671":       12,
    "CoS 767":       10,
    "Co 419":        13,
    "CoJ 64":        12,
}

# ─── Soil yield multipliers (relative productivity) ──────────────────────────
SOIL_YIELD_MULTIPLIER = {
    "loamy":  1.0,   # Best for sugarcane — baseline
    "clay":   0.85,  # Good water retention but drainage issues
    "sandy":  0.70,  # Poor nutrient retention
}

# ─── Base yield per acre by crop type (in tons) ───────────────────────────────
CROP_BASE_YIELD = {
    "Co 86032":  35.0,
    "CoM 0265":  38.0,
    "CoC 671":   32.0,
    "CoS 767":   30.0,
    "Co 419":    34.0,
    "CoJ 64":    36.0,
}

# ─── Sugar extraction rate (%) from sugarcane by crop type ───────────────────
SUGAR_EXTRACTION_RATE = {
    "Co 86032":  0.105,   # 10.5%
    "CoM 0265":  0.115,   # 11.5%
    "CoC 671":   0.100,   # 10.0%
    "CoS 767":   0.095,   # 9.5%
    "Co 419":    0.108,   # 10.8%
    "CoJ 64":    0.112,   # 11.2%
}

# ─── Water usage (liters per acre per day) ────────────────────────────────────
# Standard sugarcane requires ~2000-2500 mm per year.
# 1 mm/acre ≈ 4046 liters.
# 2000 mm ≈ 8,000,000 liters per year.
# This works out to ~22,000 liters per day per acre.
# The previous value of 2000 was likely a placeholder or per-session value.
DAILY_WATER_PER_ACRE = 22000   


def calculate_water(land_area: float, irrigation_interval: int) -> float:
    """
    Calculate total water usage over one growing season.
    
    Total water should be based on the daily requirement over the growth period.
    The irrigation interval determines the frequency but the total need remains constant.
    """
    growing_days = 365           # Standard one-year crop cycle
    total_water = land_area * DAILY_WATER_PER_ACRE * growing_days
    return round(total_water, 2)


def estimate_yield(land_area: float, soil_type: str, crop_type: str) -> float:
    """
    Estimate sugarcane yield in metric tons.
    """
    base_yield   = CROP_BASE_YIELD.get(crop_type, 33.0)
    soil_factor  = SOIL_YIELD_MULTIPLIER.get(soil_type.lower(), 0.85)
    total_yield  = land_area * base_yield * soil_factor
    return round(total_yield, 2)


def calculate_sugar_output(yield_tons: float, crop_type: str) -> float:
    """
    Calculate final sugar output from harvested sugarcane.
    """
    extraction_rate  = SUGAR_EXTRACTION_RATE.get(crop_type, 0.10)
    sugar_kg         = yield_tons * 1000 * extraction_rate   # tons → kg first
    return round(sugar_kg, 2)


def get_harvest_date(planting_date: datetime, crop_type: str) -> datetime:
    """
    Calculate the expected harvest date based on crop variety.
    """
    months = CROP_GROWTH_MONTHS.get(crop_type, 12)
    days_to_harvest = int(months * 30.44)
    return planting_date + timedelta(days=days_to_harvest)
