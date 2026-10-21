"""Временная база SQLite для Django-тестов."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest import mock

from django.test import SimpleTestCase

from db.import_json import import_all


class TemporaryDatabaseTestCase(SimpleTestCase):
    """Перед тестами класса создаёт базу из JSON во временном каталоге."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls._tmp_dir = tempfile.TemporaryDirectory()
        db_path = Path(cls._tmp_dir.name) / "test.sqlite"
        import_all(db_path)
        cls._db_patch = mock.patch("db.database.DB_PATH", db_path)
        cls._db_patch.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._db_patch.stop()
        cls._tmp_dir.cleanup()
        super().tearDownClass()
