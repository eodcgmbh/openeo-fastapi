import attr
from fastapi import APIRouter, HTTPException, Response
from starlette.responses import JSONResponse

from openeo_fastapi.api import responses

HIDDEN_PATHS = ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"]


@attr.define
class OpenEOApi:
    """Factory for creating FastApi applications conformant to the OpenEO Api specification."""

    client: attr.field
    app: attr.field
    router: APIRouter = attr.ib(default=attr.Factory(APIRouter))
    response_class: type[Response] = attr.ib(default=JSONResponse)

    def register_well_known(self):
        """Register well known page (GET /).


        Returns:
            None
        """
        self.router.add_api_route(
            name=".well-known",
            path="/.well-known/openeo",
            response_model=responses.WellKnownOpeneoGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_well_known,
        )

    def register_get_capabilities(self):
        """Register landing page (GET /).

        Returns:
            None
        """
        self.router.add_api_route(
            name="capabilities",
            path=f"/{self.client.settings.OPENEO_VERSION}" + "/",
            response_model=responses.Capabilities,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_capabilities,
        )

    def register_get_conformance(self):
        """Register conformance page (GET /conformance).
        Returns:
            None
        """
        self.router.add_api_route(
            name="conformance",
            path=f"/{self.client.settings.OPENEO_VERSION}/conformance",
            response_model=responses.ConformanceGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_conformance,
        )

    def register_get_file_formats(self):
        """Register supported file formats page (GET /file_formats).
        Returns:
            None
        """
        self.router.add_api_route(
            name="file_formats",
            path=f"/{self.client.settings.OPENEO_VERSION}/file_formats",
            response_model=responses.FileFormatsGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_file_formats,
        )

    def register_get_health(self):
        """Register api health endpoint (GET /health).
        Returns:
            None
        """
        self.router.add_api_route(
            name="health",
            path=f"/{self.client.settings.OPENEO_VERSION}/health",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_health,
        )

    def register_get_user_info(self):
        """Register conformance page (GET /me).
        Returns:
            None
        """
        self.router.add_api_route(
            name="me",
            path=f"/{self.client.settings.OPENEO_VERSION}/me",
            response_model=responses.MeGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_user_info,
        )

    def register_get_udf_runtimes(self):
        """Register supported udf runtimes (GET /udf_runtimes).
        Returns:
            None
        """
        self.router.add_api_route(
            name="udf_runtimes",
            path=f"/{self.client.settings.OPENEO_VERSION}/udf_runtimes",
            response_model=responses.UdfRuntimesGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.udf_runtimes,
        )

    def register_validate_user_process_graph(self):
        """Register validate user process graph (GET /validation).
        Returns:
            None
        """
        self.router.add_api_route(
            name="validation",
            path=f"/{self.client.settings.OPENEO_VERSION}/validation",
            response_model=responses.ValidationPostResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["POST"],
            endpoint=self.client.processes.validate_user_process_graph,
        )

    def register_run_sync_job(self):
        """Register run synchronous job (GET /result).
        Returns:
            None
        """
        self.router.add_api_route(
            name="result",
            path=f"/{self.client.settings.OPENEO_VERSION}/result",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["POST"],
            endpoint=self.client.jobs.process_sync_job,
        )

    def register_get_collections(self):
        """Register collection Endpoint (GET /collections).
        Returns:
            None
        """
        self.router.add_api_route(
            name="collections",
            path=f"/{self.client.settings.OPENEO_VERSION}/collections",
            response_model=responses.Collections,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.collections.get_collections,
        )

    def register_get_collection(self):
        """Register Endpoint for Individual Collection (GET /collections/{collection_id}).
        Returns:
            None
        """
        self.router.add_api_route(
            name="collection",
            path=f"/{self.client.settings.OPENEO_VERSION}"
            + "/collections/{collection_id}",
            response_model=responses.Collection,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.collections.get_collection,
        )

    def register_get_processes(self):
        """Register Endpoint for Processes (GET /processes).

        Returns:
            None
        """
        self.router.add_api_route(
            name="processes",
            path=f"/{self.client.settings.OPENEO_VERSION}/processes",
            response_model=responses.ProcessesGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.processes.list_processes,
        )

    def register_list_user_process_graphs(self):
        """Register Endpoint for User Processes Graphs (GET /processes_graphs).

        Returns:
            None
        """
        self.router.add_api_route(
            name="list_user_process_graphs",
            path=f"/{self.client.settings.OPENEO_VERSION}/process_graphs",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.processes.list_user_process_graphs,
        )

    def register_get_user_process_graph(self):
        """Register Endpoint for User Processes Graphs (GET /processes_graphs/{process_graph_id}).

        Returns:
            None
        """
        self.router.add_api_route(
            name="get_user_process_graphs",
            path=f"/{self.client.settings.OPENEO_VERSION}/process_graphs"
            + "/{process_graph_id}",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.processes.get_user_process_graph,
        )

    def register_put_user_process_graph(self):
        """Register Endpoint for User Processes Graphs (PUT /processes_graphs/{process_graph_id}).

        Returns:
            None
        """
        self.router.add_api_route(
            name="put_user_process_graphs",
            path=f"/{self.client.settings.OPENEO_VERSION}/process_graphs"
            + "/{process_graph_id}",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["PUT"],
            endpoint=self.client.processes.put_user_process_graph,
        )

    def register_delete_user_process_graph(self):
        """Register Endpoint for User Processes Graphs (DELETE /processes_graphs/{process_graph_id}).

        Returns:
            None
        """
        self.router.add_api_route(
            name="delete_user_process_graphs",
            path=f"/{self.client.settings.OPENEO_VERSION}/process_graphs"
            + "/{process_graph_id}",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["DELETE"],
            endpoint=self.client.processes.delete_user_process_graph,
        )

    def register_get_jobs(self):
        """Register Endpoint for Jobs (GET /jobs).

        Returns:
            None
        """
        self.router.add_api_route(
            name="get_jobs",
            path=f"/{self.client.settings.OPENEO_VERSION}/jobs",
            response_model=responses.JobsGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.jobs.list_jobs,
        )

    def register_create_job(self):
        """Register Endpoint for Jobs (POST /jobs).

        Returns:
            None
        """
        self.router.add_api_route(
            name="post_job",
            path=f"/{self.client.settings.OPENEO_VERSION}/jobs",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["POST"],
            endpoint=self.client.jobs.create_job,
        )

    def register_update_job(self):
        """Register Endpoint for Jobs (POST /jobs/{job_id}).

        Returns:
            None
        """
        self.router.add_api_route(
            name="post_job",
            path=f"/{self.client.settings.OPENEO_VERSION}/jobs" + "/{job_id}",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["PATCH"],
            endpoint=self.client.jobs.update_job,
        )

    def register_get_job(self):
        """Register Endpoint for Jobs (GET /jobs/{job_id}).

        Returns:
            None
        """
        self.router.add_api_route(
            name="get_job",
            path=f"/{self.client.settings.OPENEO_VERSION}/jobs" + "/{job_id}",
            response_model=responses.BatchJob,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.jobs.get_job,
        )

    def register_delete_job(self):
        """Register Endpoint for Jobs (GET /jobs/{job_id}).

        Returns:
            None
        """
        self.router.add_api_route(
            name="delete_job",
            path=f"/{self.client.settings.OPENEO_VERSION}/jobs" + "/{job_id}",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["DELETE"],
            endpoint=self.client.jobs.delete_job,
        )

    def register_get_estimate(self):
        """Register Endpoint for Jobs (GET /jobs/{job_id}).

        Returns:
            None
        """
        self.router.add_api_route(
            name="get_estimate",
            path=f"/{self.client.settings.OPENEO_VERSION}/jobs" + "/{job_id}/estimate",
            response_model=responses.JobsGetEstimateGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.jobs.estimate,
        )

    def register_get_logs(self):
        """Register Endpoint for Jobs (GET /jobs/{job_id}).

        Returns:
            None
        """
        self.router.add_api_route(
            name="get_logs",
            path=f"/{self.client.settings.OPENEO_VERSION}/jobs" + "/{job_id}/logs",
            response_model=responses.JobsGetLogsResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.jobs.logs,
        )

    def register_get_results(self):
        """Register Endpoint for Jobs (GET /jobs/{job_id}).

        Returns:
            None
        """
        self.router.add_api_route(
            name="get_results",
            path=f"/{self.client.settings.OPENEO_VERSION}/jobs" + "/{job_id}/results",
            response_model=responses.Collection,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.jobs.get_results,
        )

    def register_start_job(self):
        """Register Endpoint for Jobs (GET /jobs/{job_id}).

        Returns:
            None
        """
        self.router.add_api_route(
            name="start_job",
            path=f"/{self.client.settings.OPENEO_VERSION}/jobs" + "/{job_id}/results",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["POST"],
            endpoint=self.client.jobs.start_job,
        )

    def register_cancel_job(self):
        """Register Endpoint for Jobs (GET /jobs/{job_id}).

        Returns:
            None
        """
        self.router.add_api_route(
            name="cancel_job",
            path=f"/{self.client.settings.OPENEO_VERSION}/jobs" + "/{job_id}/results",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["DELETE"],
            endpoint=self.client.jobs.cancel_job,
        )

    def register_list_files(self):
        """Register Endpoint for Files (GET /files).

        Returns:
            None
        """
        self.router.add_api_route(
            name="list_files",
            path=f"/{self.client.settings.OPENEO_VERSION}/files",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.files.list_files,
        )

    def register_download_file(self):
        """Register Endpoint for Files (GET /files/{path}).

        Returns:
            None
        """
        self.router.add_api_route(
            name="download_file",
            path=f"/{self.client.settings.OPENEO_VERSION}/files" + "/{path}",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.files.download_file,
        )

    def register_upload_file(self):
        """Register Endpoint for Files (PUT /files/{path}).

        Returns:
            None
        """
        self.router.add_api_route(
            name="upload_file",
            path=f"/{self.client.settings.OPENEO_VERSION}/files" + "/{path}",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["PUT"],
            endpoint=self.client.files.upload_file,
        )

    def register_delete_file(self):
        """Register Endpoint for Files (DELETE /files/{path}).

        Returns:
            None
        """
        self.router.add_api_route(
            name="delete_file",
            path=f"/{self.client.settings.OPENEO_VERSION}/files" + "/{path}",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["DELETE"],
            endpoint=self.client.files.delete_file,
        )

    def register_core(self):
        """Register core OpenEO endpoints.

            GET /
            GET /capabilities
            GET /collections
            GET /collections/{collection_id}
            GET /processes
            GET /well_known


        Injects application logic (OpenEOApi.client) into the API layer.

        Returns:
            None
        """
        self.register_get_conformance()
        self.register_get_health()
        self.register_get_user_info()
        self.register_run_sync_job()
        self.register_get_udf_runtimes()
        self.register_validate_user_process_graph()
        self.register_get_file_formats()
        self.register_get_collections()
        self.register_get_collection()
        self.register_get_processes()
        self.register_list_user_process_graphs()
        self.register_get_user_process_graph()
        self.register_put_user_process_graph()
        self.register_delete_user_process_graph()
        self.register_get_jobs()
        self.register_create_job()
        self.register_update_job()
        self.register_get_job()
        self.register_delete_job()
        self.register_get_estimate()
        self.register_get_logs()
        self.register_get_results()
        self.register_start_job()
        self.register_cancel_job()
        self.register_list_files()
        self.register_download_file()
        self.register_upload_file()
        self.register_delete_file()
        self.register_well_known()

    def http_exception_handler(self, request, exception):
        """Register exception handler to turn python exceptions into expected OpenEO error output."""
        exception_headers = {
            "allow_origin": "*",
            "allow_credentials": "true",
            "allow_methods": "*",
        }
        from fastapi.encoders import jsonable_encoder

        return JSONResponse(
            headers=exception_headers,
            status_code=exception.status_code,
            content=jsonable_encoder(exception.detail),
        )

    def __attrs_post_init__(self):
        """Post-init hook.

        Responsible for setting up the application upon instantiation of the class.

        Returns:
            None
        """

        # Register core endpoints
        self.register_core()

        self.register_get_capabilities()
        self.app.include_router(router=self.router)
        self.app.add_exception_handler(HTTPException, self.http_exception_handler)
