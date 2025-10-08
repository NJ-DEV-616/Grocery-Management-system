import pytest
from project import validate_email_address, validate_password, get_valid_action

def main():
    test_validate_email_address()
    test_validate_password()
    test_get_valid_action_single()
    test_get_valid_action_multiple()

def test_validate_email_address():
    #Valid Emails
    assert validate_email_address('user@example.com') == True
    assert validate_email_address('user123@domain.org') == True

    # Invalid Emails
    assert validate_email_address('userdomain.com') == False
    assert validate_email_address('user@domain') == False
    assert validate_email_address('user@.com') == False
    assert validate_email_address('@domain.com') == False

def test_validate_password():
    # Valid passwords
    assert validate_password('Password@1') == True
    assert validate_password('Strong@123') == True

    # Too short/ too long
    assert validate_password('Abc@1') == False
    assert validate_password('Abcdefghijkl@123') == False

    # Missing uppercase
    assert validate_password('lower@123') == False

    # Missing lowercase
    assert validate_password('UPPPER@123') == False

    # Missing digit
    assert validate_password('Nodigit@') == False

    # Missing Special character
    assert validate_password('Password1') == False

def test_get_valid_action_single(monkeypatch):
    # always valid input
    monkeypatch.setattr("builtins.input", lambda _: "2")
    assert get_valid_action("Enter action(1-4): ", range(1, 5)) == 2

def test_get_valid_action_multiple(monkeypatch):
    # first invalid input, then valid input
    inputs = iter(['10', '3'])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert get_valid_action("Enter action(1-4): ", range(1, 5)) == 3

if __name__ == "__main__":
    main()
