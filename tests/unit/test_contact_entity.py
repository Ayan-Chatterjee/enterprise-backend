"""Unit test for Contact entity"""
import pytest
from src.domain.entities.contact import Contact


def test_contact_creation():
    """Test creating a contact"""
    contact = Contact(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="1234567890",
        message="Interested in property",
        status="new",
    )
    
    assert contact.first_name == "John"
    assert contact.full_name() == "John Doe"
    assert contact.status == "new"


def test_contact_validation():
    """Test contact validation"""
    with pytest.raises(ValueError):
        Contact(
            first_name="",
            last_name="Doe",
            email="john@example.com",
        )


def test_contact_requires_contact_method():
    """Test that contact requires email or phone"""
    with pytest.raises(ValueError):
        Contact(
            first_name="John",
            last_name="Doe",
        )
