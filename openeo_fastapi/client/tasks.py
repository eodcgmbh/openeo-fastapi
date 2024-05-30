from datetime import timedelta
from typing import Callable

from redis import Redis
from rq import Queue

from openeo_fastapi.api.types import Status
from openeo_fastapi.client.jobs import Job
from openeo_fastapi.client.psql.engine import Filter, _list, modify

MAX_POOL_SIZE = 10
Redis()


def queue_job(job: Job, _submit: Callable, _poll: Callable):
    """"""
    job.status = Status.queued
    modify(job)

    return {
        "time_delta": timedelta(seconds=10),
        "func": trigger_job,
        "job": job,
        "_submit": _submit,
        "_poll": _poll,
    }


def trigger_job(job: Job, _submit: Callable, _poll: Callable):
    """"""
    filter_queued = Filter(column_name="status", value="queued")

    queued_jobs = _list(list_model=Job.get_orm(), filter_with=filter_queued)

    if len(queued_jobs) >= MAX_POOL_SIZE:
        return {
            "time_delta": timedelta(seconds=10),
            "func": trigger_job,
            "job": job,
            "_submit": _submit,
            "_poll": _poll,
        }

    submitted = _submit(job.job_id)

    if not submitted:
        return {
            "time_delta": timedelta(seconds=10),
            "func": trigger_job,
            "job": job,
            "_submit": _submit,
            "_poll": _poll,
        }

    return {
        "time_delta": timedelta(seconds=10),
        "func": poll_running_job,
        "job": job,
        "_poll": _poll,
    }


def poll_running_job(job: Job, _poll: Callable):
    """"""

    status = _poll(job)

    if status in [Status.finished, Status.error]:
        job.status = status
        modify(job)
        return None

    return {
        "time_delta": timedelta(seconds=10),
        "func": poll_running_job,
        "job": job,
        "_poll": _poll,
    }
