import pytest
from sqlalchemy import BOOLEAN, Column, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from openeo_fastapi.client.psql.engine import get_engine
from openeo_fastapi.client.psql.models import User


@pytest.mark.serial
def test_db_setup(mock_engine):
    """A test to validate the basic structure of our ORMs and get_engine functions."""
    import uuid

    user_uid = uuid.uuid4()
    user = User(user_id=user_uid, oidc_sub="someone@egi.eu")

    session = sessionmaker(mock_engine)
    with session.begin() as sesh:
        sesh.add(user)

    with session.begin() as sesh:
        right_user = select(User).filter_by(user_id=user_uid)
        wrong_user = select(User).filter_by(user_id=uuid.uuid4())

        assert sesh.scalars(right_user).first()
        assert not sesh.scalars(wrong_user).first()


def test_db_models_extendable(mock_engine):
    """Test the existing models can be extended and used to revise the database."""

    import uuid

    user_uid = uuid.uuid4()

    # Extend the user class as we intend a user to do
    class ExtendedUser(User):
        """ORM for the user table."""

        new_value = Column(BOOLEAN, nullable=False)

    # Try to revise the database using the extended base
    import os
    from pathlib import Path

    from alembic import command
    from alembic.config import Config

    from tests.conftest import ALEMBIC_DIR

    os.chdir(Path(ALEMBIC_DIR))
    alembic_cfg = Config("alembic.ini")

    command.revision(alembic_cfg, f"openeo-fastapi-extended", autogenerate=True)
    command.upgrade(alembic_cfg, "head")

    # See if the revision has been extended
    a_user = ExtendedUser(user_id=user_uid, oidc_sub="someone@egi.eu", new_value=True)

    session = sessionmaker(mock_engine)
    with session.begin() as sesh:
        sesh.add(a_user)

    with session.begin() as sesh:
        extended_user = select(ExtendedUser).filter_by(user_id=user_uid)

        assert sesh.scalars(extended_user).first().new_value == True

    # Using the non-extended model should now raise an error
    old_user = User(user_id=uuid.uuid4(), oidc_sub="someone@egi.eu")

    with pytest.raises(IntegrityError):
        with session.begin() as sesh:
            sesh.add(old_user)
