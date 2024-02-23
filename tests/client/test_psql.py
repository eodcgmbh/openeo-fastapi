import pytest
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from openeo_fastapi.client.psql.models import User


def test_db_works(mock_engine):
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
