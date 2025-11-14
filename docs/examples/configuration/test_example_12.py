from dataclasses import dataclass

from polyfactory.factories import DataclassFactory


@dataclass
class Account:
    """User account model."""

    username: str
    email: str
    is_verified: bool
    verification_token: str


class AccountFactory(DataclassFactory[Account]):
    """Factory for Account with post_build hook."""

    @classmethod
    def post_build(cls, account: Account) -> Account:
        """Post-build hook to modify the created instance.

        This hook is called after the model instance is created,
        allowing you to run custom logic on the fully-generated object.
        """
        # Auto-verify accounts in test environment
        if account.username.startswith("test_"):
            account.is_verified = True
            account.verification_token = ""

        return account


def test_post_build_hook() -> None:
    # Regular account will have random is_verified value
    regular_account = AccountFactory.build(username="john_doe")
    assert regular_account.username == "john_doe"

    # Test account will be auto-verified by the post_build hook
    test_account = AccountFactory.build(username="test_user")
    assert test_account.is_verified is True
    assert test_account.verification_token == ""
