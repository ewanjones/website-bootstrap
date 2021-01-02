from contextlib import ContextDecorator
from unittest import mock

from django.db import transaction


class database_transaction(ContextDecorator):
    """
    Mock out Django's `get_connection()` so a function/method can be decorated
    with `@transaction.atomic` and the test doesn't need to use `requires_db`.
    Can be used in tests as a context manager or decorator.

    This also mocks transaction.on_commit() so that any callable passed to it will be
    executed immediately.
    """

    def __enter__(self):
        self.patchers = [
            mock.patch.object(transaction, "get_connection"),
            # Immediately call the function passed to transaction.on_commit.
            mock.patch.object(
                transaction, "on_commit", side_effect=lambda func: func()
            ),
        ]
        for patcher in self.patchers:
            patcher.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for patcher in self.patchers:
            patcher.stop()
        return False
