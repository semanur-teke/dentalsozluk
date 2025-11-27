"""
Unit tests for terms models.
"""
import pytest
from django.utils import timezone
from datetime import timedelta
from terms.models import DentalTerm, ErrorReport


@pytest.mark.django_db
class TestDentalTerm:
    """Test cases for DentalTerm model."""

    def test_create_dental_term(self):
        """Test creating a DentalTerm instance."""
        term = DentalTerm.objects.create(
            title="Diş Çürüğü",
            description="Diş minesi bozulması",
            english_equivalent="Tooth Decay",
            latin_equivalent="Caries dentium"
        )
        assert term.title == "Diş Çürüğü"
        assert term.slug == "dis-curugu"

    def test_slug_auto_generation(self):
        """Test that slug is automatically generated from title."""
        term = DentalTerm.objects.create(
            title="Ortodonti",
            description="Test"
        )
        assert term.slug == "ortodonti"

    def test_slug_uniqueness(self):
        """Test that duplicate titles get unique slugs."""
        term1 = DentalTerm.objects.create(
            title="Implant",
            description="Test 1"
        )
        term2 = DentalTerm.objects.create(
            title="Implant",
            description="Test 2"
        )
        assert term1.slug == "implant"
        assert term2.slug == "implant-1"

    def test_str_representation(self):
        """Test __str__ method returns title."""
        term = DentalTerm.objects.create(
            title="Test Terim",
            description="Test"
        )
        assert str(term) == "Test Terim"


@pytest.mark.django_db
class TestErrorReport:
    """Test cases for ErrorReport model."""

    def test_create_error_report(self, dental_term):
        """Test creating an ErrorReport instance."""
        report = ErrorReport.objects.create(
            term=dental_term,
            session_key="test_session_123"
        )
        assert report.term == dental_term
        assert report.session_key == "test_session_123"

    def test_recently_reported_within_timeframe(self, dental_term):
        """Test recently_reported returns True for recent reports."""
        ErrorReport.objects.create(
            term=dental_term,
            session_key="session_123"
        )

        result = ErrorReport.recently_reported(
            term_id=dental_term.id,
            session_key="session_123",
            within_seconds=60
        )
        assert result is True

    def test_recently_reported_outside_timeframe(self, dental_term):
        """Test recently_reported returns False for old reports."""
        # Create report with old timestamp
        old_report = ErrorReport.objects.create(
            term=dental_term,
            session_key="session_456"
        )
        # Manually set created time to 2 hours ago
        old_time = timezone.now() - timedelta(hours=2)
        ErrorReport.objects.filter(id=old_report.id).update(created=old_time)

        result = ErrorReport.recently_reported(
            term_id=dental_term.id,
            session_key="session_456",
            within_seconds=60
        )
        assert result is False

    def test_recently_reported_different_session(self, dental_term):
        """Test recently_reported returns False for different session."""
        ErrorReport.objects.create(
            term=dental_term,
            session_key="session_abc"
        )

        result = ErrorReport.recently_reported(
            term_id=dental_term.id,
            session_key="different_session",
            within_seconds=60
        )
        assert result is False
