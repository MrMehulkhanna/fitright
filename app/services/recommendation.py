"""Size recommendation engine with return-feedback adjustment."""

import math
from app.models import SizeChart, Order, Return
from app import db
from sqlalchemy import func

# Ordered size ladder for shift operations
SIZE_ORDER = ["XS", "S", "M", "L", "XL", "XXL"]

# Threshold: if >30% of size-related returns say too_small or too_large, shift
SHIFT_THRESHOLD = 0.30


def _euclidean_distance(sc: SizeChart, chest: float, waist: float, hip: float) -> float:
    """Euclidean distance between user measurements and a size chart entry."""
    return math.sqrt(
        (sc.chest - chest) ** 2 + (sc.waist - waist) ** 2 + (sc.hip - hip) ** 2
    )


def _get_return_bias(product_id: int, raw_size: str) -> int:
    """
    Return +1 if >30% of returns for this product say 'too_small' (shift up),
    -1 if >30% say 'too_large' (shift down), else 0.
    """
    # Count returns for this product with size-related reasons
    size_return_count = (
        db.session.query(func.count(Return.id))
        .join(Order, Return.order_id == Order.id)
        .filter(
            Order.product_id == product_id,
            Return.reason.in_(["too_small", "too_large"]),
        )
        .scalar()
    )

    if not size_return_count:
        return 0

    too_small_count = (
        db.session.query(func.count(Return.id))
        .join(Order, Return.order_id == Order.id)
        .filter(Order.product_id == product_id, Return.reason == "too_small")
        .scalar()
    )

    too_large_count = (
        db.session.query(func.count(Return.id))
        .join(Order, Return.order_id == Order.id)
        .filter(Order.product_id == product_id, Return.reason == "too_large")
        .scalar()
    )

    total_returns = (
        db.session.query(func.count(Return.id))
        .join(Order, Return.order_id == Order.id)
        .filter(Order.product_id == product_id)
        .scalar()
    )

    if not total_returns:
        return 0

    if too_small_count / total_returns > SHIFT_THRESHOLD:
        return 1  # shift up — customers say this product runs small
    if too_large_count / total_returns > SHIFT_THRESHOLD:
        return -1  # shift down — customers say this product runs large
    return 0


def _shift_size(size: str, direction: int) -> str:
    """Shift size up (+1) or down (-1) within the size ladder."""
    if direction == 0 or size not in SIZE_ORDER:
        return size
    idx = SIZE_ORDER.index(size)
    new_idx = max(0, min(len(SIZE_ORDER) - 1, idx + direction))
    return SIZE_ORDER[new_idx]


def _confidence_label(distance: float) -> tuple[str, str]:
    """
    Map euclidean distance to a confidence label and Bootstrap colour class.
    Distance thresholds are in cm (3-measurement combined).
    """
    if distance < 5:
        return "High", "success"
    elif distance < 12:
        return "Medium", "warning"
    else:
        return "Low", "danger"


def recommend_size(product_id: int, chest: float, waist: float, hip: float) -> dict:
    """
    Recommend a size for a product given user measurements.

    Returns a dict with:
        size         - recommended size string
        raw_size     - closest match before return-feedback adjustment
        adjusted     - True if size was shifted due to return feedback
        confidence   - 'High' | 'Medium' | 'Low'
        color        - Bootstrap badge color
        distance     - euclidean distance to nearest chart entry
        bias         - shift direction applied (0, 1, -1)
    """
    charts = SizeChart.query.filter_by(product_id=product_id).all()
    if not charts:
        return {
            "size": None,
            "raw_size": None,
            "adjusted": False,
            "confidence": "Unknown",
            "color": "secondary",
            "distance": None,
            "bias": 0,
        }

    # Find the closest size by Euclidean distance
    closest = min(charts, key=lambda sc: _euclidean_distance(sc, chest, waist, hip))
    distance = _euclidean_distance(closest, chest, waist, hip)
    raw_size = closest.size

    # Apply return-feedback bias
    bias = _get_return_bias(product_id, raw_size)
    final_size = _shift_size(raw_size, bias)

    confidence, color = _confidence_label(distance)

    return {
        "size": final_size,
        "raw_size": raw_size,
        "adjusted": bias != 0,
        "confidence": confidence,
        "color": color,
        "distance": round(distance, 2),
        "bias": bias,
    }
