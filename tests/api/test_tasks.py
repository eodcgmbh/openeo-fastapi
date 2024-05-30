from fakeredis import FakeStrictRedis
from rq import Queue

from openeo_fastapi.api.types import Status
from openeo_fastapi.client.jobs import Job
from openeo_fastapi.client.psql.engine import get


def test_trigger_job(test_job):
    """ """
    queue = Queue(is_async=False, connection=FakeStrictRedis())

    queue.enqueue_in(**manager.queue_job(test_job))

    job = get(Job, str(test_job.job_id))

    assert job.status == Status.queued


def test_poll_job():
    """ """
    assert True


def test_task_manager():
    """ """
    assert True
