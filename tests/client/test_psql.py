import uuid

import pytest
from sqlalchemy import BOOLEAN, Column, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from openeo_fastapi.client.psql.models import JobORM, UdpORM, UserORM


def test_db_setup_and_userorm_model(mock_engine):
    """A test to validate the basic structure of our ORMs and get_engine functions."""

    _uid = uuid.uuid4()
    user = UserORM(user_id=_uid, oidc_sub="someone@egi.eu")

    session = sessionmaker(mock_engine)
    with session.begin() as sesh:
        sesh.add(user)

    with session.begin() as sesh:
        right_user = select(UserORM).filter_by(user_id=_uid)
        wrong_user = select(UserORM).filter_by(user_id=uuid.uuid4())

        assert sesh.scalars(right_user).first()
        assert not sesh.scalars(wrong_user).first()


def test_job_model(mock_engine):
    """ """

    user_uid = uuid.uuid4()
    job_uid = uuid.uuid4()

    user = UserORM(user_id=user_uid, oidc_sub="someone@egi.eu")
    job = JobORM(
        job_id=job_uid,
        user_id=user_uid,
        status="created",
        process={"id":{"data":"x"}},
    )

    session = sessionmaker(mock_engine)
    with session.begin() as sesh:
        sesh.add(user)
        sesh.add(job)

    with session.begin() as sesh:
        found_job = select(JobORM).filter_by(job_id=job_uid)

        assert sesh.scalars(found_job).first()

def test_udpor_model(mock_engine):
    """ """

    _uid = uuid.uuid4()
    process_graph_uid = "SOMEPGID"

    user = UserORM(user_id=_uid, oidc_sub="someone@egi.eu")
    processgraph = UdpORM(
        id=process_graph_uid,
        user_id=_uid,
        process_graph={"process": {"args": "one"}},
    )

    session = sessionmaker(mock_engine)
    with session.begin() as sesh:
        sesh.add(user)
        sesh.add(processgraph)

    with session.begin() as sesh:
        found_pg = select(UdpORM).filter_by(id=process_graph_uid)

        assert sesh.scalars(found_pg).first()


def test_models_extendable(mock_engine):
    """Test the existing models can be extended and used to revise the database."""

    _uid = uuid.uuid4()

    # Extend the UserORM class
    class ExtendedUserORM(UserORM):
        """ORM for the UserORM table."""

        new_value = Column(BOOLEAN, nullable=False)

    # Try to revise the database using the extended UserORM
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
    a_user = ExtendedUserORM(user_id=_uid, oidc_sub="someone@egi.eu", new_value=True)

    session = sessionmaker(mock_engine)
    with session.begin() as sesh:
        sesh.add(a_user)

    with session.begin() as sesh:
        extended_UserORM = select(ExtendedUserORM).filter_by(user_id=_uid)

        assert sesh.scalars(extended_UserORM).first().new_value == True

    # Using the non-extended model should now raise an error
    old_user = UserORM(user_id=uuid.uuid4(), oidc_sub="someone@egi.eu")

    with pytest.raises(IntegrityError):
        with session.begin() as sesh:
            sesh.add(old_user)
