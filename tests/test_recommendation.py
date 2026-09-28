"""Unit tests for the size recommendation engine."""

import pytest
from app.services.recommendation import (
    recommend_size,
    _euclidean_distance,
    _shift_size,
    _confidence_label,
    SIZE_ORDER,
)
from app.models import SizeChart


class TestEuclideanDistance:
    """Tests for the distance helper."""

    def test_perfect_match_is_zero(self):
        sc = SizeChart(chest=94, waist=74, hip=100)
        assert _euclidean_distance(sc, 94, 74, 100) == 0.0

    def test_known_distance(self):
        sc = SizeChart(chest=94, waist=74, hip=100)
        # distance = sqrt((4**2)+(4**2)+(4**2)) = sqrt(48)
        import math

        expected = math.sqrt(48)
        assert abs(_euclidean_distance(sc, 90, 70, 96) - expected) < 0.01

    def test_asymmetric_dimensions(self):
        sc = SizeChart(chest=94, waist=74, hip=100)
        d = _euclidean_distance(sc, 94, 74, 106)  # only hip differs by 6
        assert abs(d - 6.0) < 0.01


class TestShiftSize:
    """Tests for the size-shift logic."""

    def test_no_shift(self):
        assert _shift_size("M", 0) == "M"

    def test_shift_up(self):
        assert _shift_size("M", 1) == "L"

    def test_shift_down(self):
        assert _shift_size("M", -1) == "S"

    def test_shift_up_at_max_clamps(self):
        assert _shift_size("XXL", 1) == "XXL"

    def test_shift_down_at_min_clamps(self):
        assert _shift_size("XS", -1) == "XS"

    def test_invalid_size_returns_unchanged(self):
        assert _shift_size("INVALID", 1) == "INVALID"


class TestConfidenceLabel:
    """Tests for confidence categorisation."""

    def test_high_confidence(self):
        label, color = _confidence_label(2.0)
        assert label == "High"
        assert color == "success"

    def test_medium_confidence(self):
        label, color = _confidence_label(8.0)
        assert label == "Medium"
        assert color == "warning"

    def test_low_confidence(self):
        label, color = _confidence_label(15.0)
        assert label == "Low"
        assert color == "danger"

    def test_boundary_high_medium(self):
        label, _ = _confidence_label(4.99)
        assert label == "High"
        label2, _ = _confidence_label(5.0)
        assert label2 == "Medium"

    def test_boundary_medium_low(self):
        label, _ = _confidence_label(11.99)
        assert label == "Medium"
        label2, _ = _confidence_label(12.0)
        assert label2 == "Low"


class TestRecommendSize:
    """Integration tests for recommend_size (uses DB fixtures)."""

    def test_recommend_exact_medium(self, app, sample_product):
        with app.app_context():
            result = recommend_size(sample_product.id, 94, 74, 100)
            assert result["size"] == "M"
            assert result["confidence"] == "High"
            assert result["adjusted"] is False

    def test_recommend_closest_to_large(self, app, sample_product):
        with app.app_context():
            # Measurements close to L
            result = recommend_size(sample_product.id, 100, 80, 106)
            assert result["size"] == "L"

    def test_recommend_no_size_chart(self, app, db):
        """Product with no size chart returns None size."""
        from app.models import Product

        p = Product(name="Empty", brand="X", brand_id=1, category="tops", price=10)
        db.session.add(p)
        db.session.commit()
        with app.app_context():
            result = recommend_size(p.id, 94, 74, 100)
            assert result["size"] is None

    def test_recommend_xs_measurements(self, app, sample_product):
        with app.app_context():
            result = recommend_size(sample_product.id, 82, 62, 88)
            assert result["size"] == "XS"

    def test_recommend_xxl_measurements(self, app, sample_product):
        with app.app_context():
            result = recommend_size(sample_product.id, 112, 92, 118)
            assert result["size"] == "XXL"

    def test_return_bias_shifts_up(self, app, db, sample_product):
        """If >30% of returns are too_small, recommended size shifts up."""
        from app.models import User, Order, Return

        # Create a user
        u = User(username="biasuser", email="bias@test.com", role="customer")
        u.set_password("pass")
        db.session.add(u)
        db.session.flush()

        # Create 4 orders with too_small returns (>30% of product returns)
        for _ in range(4):
            o = Order(
                user_id=u.id, product_id=sample_product.id, size="M", status="returned"
            )
            db.session.add(o)
            db.session.flush()
            r = Return(order_id=o.id, reason="too_small")
            db.session.add(r)

        db.session.commit()

        with app.app_context():
            # M measurements — without bias would get M, with bias should get L
            result = recommend_size(sample_product.id, 94, 74, 100)
            assert result["bias"] == 1
            assert result["adjusted"] is True
            assert result["raw_size"] == "M"
            assert result["size"] == "L"

    def test_return_bias_shifts_down(self, app, db, sample_product):
        """If >30% of returns are too_large, recommended size shifts down."""
        from app.models import User, Order, Return

        u = User(username="biasuser2", email="bias2@test.com", role="customer")
        u.set_password("pass")
        db.session.add(u)
        db.session.flush()

        for _ in range(4):
            o = Order(
                user_id=u.id, product_id=sample_product.id, size="M", status="returned"
            )
            db.session.add(o)
            db.session.flush()
            r = Return(order_id=o.id, reason="too_large")
            db.session.add(r)

        db.session.commit()

        with app.app_context():
            result = recommend_size(sample_product.id, 94, 74, 100)
            assert result["bias"] == -1
            assert result["size"] == "S"
