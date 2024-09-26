"""OpenEO Api class for preparing the FastApi object from the client that is provided by the user.
"""
import attr
from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.responses import JSONResponse, RedirectResponse

from openeo_fastapi.api import models
from openeo_fastapi.client.auth import Authenticator

HIDDEN_PATHS = ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"]


@attr.define
class OpenEOApi:
    """Factory for creating FastApi applications conformant to the OpenEO Api specification."""

    client: attr.field
    app: attr.field
    router: APIRouter = attr.ib(default=attr.Factory(APIRouter))
    response_class: type[Response] = attr.ib(default=JSONResponse)

    def override_authentication(self, func):
        self.app.dependency_overrides[Authenticator.validate] = func

    def register_well_known(self):
        """Register well known endpoint (GET /.well-known/openeo)."""
        self.router.add_api_route(
            name=".well-known",
            path="/.well-known/openeo",
            response_model=models.WellKnownOpeneoGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_well_known,
        )

    def register_get_capabilities(self):
        """Register endpoint for capabilities (GET /)."""
        self.router.add_api_route(
            name="capabilities",
            path=f"{self.client.settings.OPENEO_PREFIX}" + "/",
            response_model=models.Capabilities,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_capabilities,
        )

    def register_get_conformance(self):
        """Register endpoint for api conformance (GET /conformance)."""
        self.router.add_api_route(
            name="conformance",
            path=f"{self.client.settings.OPENEO_PREFIX}/conformance",
            response_model=models.ConformanceGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_conformance,
        )

    def register_get_credentials_oidc(self):
        """Register endpoint for api conformance (GET /conformance)."""
        self.router.add_api_route(
            name="credentials_oidc",
            path=f"{self.client.settings.OPENEO_PREFIX}/credentials/oidc",
            response_model=models.CredentialsOidcGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_credentials_oidc,
        )

    def register_get_file_formats(self):
        """Register endpoint for supported file formats (GET /file_formats)."""
        self.router.add_api_route(
            name="file_formats",
            path=f"{self.client.settings.OPENEO_PREFIX}/file_formats",
            response_model=models.FileFormatsGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_file_formats,
        )

    def register_get_health(self):
        """Register endpoint for api health (GET /health)."""
        self.router.add_api_route(
            name="health",
            path=f"{self.client.settings.OPENEO_PREFIX}/health",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_health,
        )

    def register_get_user_info(self):
        """Register endpoint for user info (GET /me)."""
        self.router.add_api_route(
            name="me",
            path=f"{self.client.settings.OPENEO_PREFIX}/me",
            response_model=models.MeGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_user_info,
        )

    def register_get_udf_runtimes(self):
        """Register endpoint to list the supported udf runtimes (GET /udf_runtimes)."""
        self.router.add_api_route(
            name="udf_runtimes",
            path=f"{self.client.settings.OPENEO_PREFIX}/udf_runtimes",
            response_model=models.UdfRuntimesGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_udf_runtimes,
        )

    def register_validate_user_process_graph(self):
        """Register endpoint for validating a user process graph (GET /validation)."""
        self.router.add_api_route(
            name="validation",
            path=f"{self.client.settings.OPENEO_PREFIX}/validation",
            response_model=models.ValidationPostResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["POST"],
            endpoint=self.client.processes.validate_user_process_graph,
        )

    def register_run_sync_job(self):
        """Register endpoint for executing synchronous jobs (GET /result)."""
        self.router.add_api_route(
            name="result",
            path=f"{self.client.settings.OPENEO_PREFIX}/result",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["POST"],
            endpoint=self.client.jobs.process_sync_job,
        )

    def register_get_collections(self):
        """Register endpoint for listing available collections (GET /collections)."""
        self.router.add_api_route(
            name="collections",
            path=f"{self.client.settings.OPENEO_PREFIX}/collections",
            response_model=models.Collections,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.collections.get_collections,
        )

    def register_get_collection(self):
        """Register endpoint for getting a specific collection (GET /collections/{collection_id})."""
        self.router.add_api_route(
            name="collection",
            path=f"{self.client.settings.OPENEO_PREFIX}"
            + "/collections/{collection_id}",
            response_model=models.Collection,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.collections.get_collection,
        )

    def register_get_collection_items(self):
        """Register endpoint for getting collection items (GET /collections/{collection_id}/items)."""
        self.router.add_api_route(
            name="collection_items",
            path=f"{self.client.settings.OPENEO_PREFIX}/collections"
            + "/{collection_id}/items",
            response_model=models.Collections,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.collections.get_collection_items,
        )

    def register_get_collection_item(self):
        """Register endpoint for getting a specific collection item (GET /collections/{collection_id}/items/{item_id})."""
        self.router.add_api_route(
            name="collection_item",
            path=f"{self.client.settings.OPENEO_PREFIX}"
            + "/collections/{collection_id}/items/{item_id}",
            response_model=models.Collection,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.collections.get_collection_item,
        )

    def register_get_processes(self):
        """Register endpoint for listing all predefined processes (GET /processes)."""
        self.router.add_api_route(
            name="processes",
            path=f"{self.client.settings.OPENEO_PREFIX}/processes",
            response_model=models.ProcessesGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.processes.list_processes,
        )

    def register_list_user_process_graphs(self):
        """Register endpoint for listing user defined processes graphs (GET /processes_graphs)."""
        self.router.add_api_route(
            name="list_user_process_graphs",
            path=f"{self.client.settings.OPENEO_PREFIX}/process_graphs",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.processes.list_user_process_graphs,
        )

    def register_get_user_process_graph(self):
        """Register endpoint for getting a specific user defined processes graphs (GET /processes_graphs/{process_graph_id})."""
        self.router.add_api_route(
            name="get_user_process_graphs",
            path=f"{self.client.settings.OPENEO_PREFIX}/process_graphs"
            + "/{process_graph_id}",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.processes.get_user_process_graph,
        )

    def register_put_user_process_graph(self):
        """Register endpoint for creatings a user defined processes graph (PUT /processes_graphs/{process_graph_id})."""
        self.router.add_api_route(
            name="put_user_process_graphs",
            path=f"{self.client.settings.OPENEO_PREFIX}/process_graphs"
            + "/{process_graph_id}",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["PUT"],
            endpoint=self.client.processes.put_user_process_graph,
        )

    def register_delete_user_process_graph(self):
        """Register endpoint for deleting a user defined processes graph (DELETE /processes_graphs/{process_graph_id})."""
        self.router.add_api_route(
            name="delete_user_process_graphs",
            path=f"{self.client.settings.OPENEO_PREFIX}/process_graphs"
            + "/{process_graph_id}",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["DELETE"],
            endpoint=self.client.processes.delete_user_process_graph,
        )

    def register_get_jobs(self):
        """Register endpoint for listing all jobs (GET /jobs)."""
        self.router.add_api_route(
            name="get_jobs",
            path=f"{self.client.settings.OPENEO_PREFIX}/jobs",
            response_model=models.JobsGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.jobs.list_jobs,
        )

    def register_create_job(self):
        """Register endpoint for creating a new job (POST /jobs)."""
        self.router.add_api_route(
            name="post_job",
            path=f"{self.client.settings.OPENEO_PREFIX}/jobs",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["POST"],
            endpoint=self.client.jobs.create_job,
        )

    def register_update_job(self):
        """Register update jobs endpoint (POST /jobs/{job_id})."""
        self.router.add_api_route(
            name="post_job",
            path=f"{self.client.settings.OPENEO_PREFIX}/jobs" + "/{job_id}",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["PATCH"],
            endpoint=self.client.jobs.update_job,
        )

    def register_get_job(self):
        """Register endpoint for retreiving job metadata (GET /jobs/{job_id})."""
        self.router.add_api_route(
            name="get_job",
            path=f"{self.client.settings.OPENEO_PREFIX}/jobs" + "/{job_id}",
            response_model=models.BatchJob,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.jobs.get_job,
        )

    def register_delete_job(self):
        """Register endpoint for deleting the record of a batch job (GET /jobs/{job_id})."""
        self.router.add_api_route(
            name="delete_job",
            path=f"{self.client.settings.OPENEO_PREFIX}/jobs" + "/{job_id}",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["DELETE"],
            endpoint=self.client.jobs.delete_job,
        )

    def register_get_estimate(self):
        """Register endpoint for estimating a batch job (GET /jobs/{job_id})."""
        self.router.add_api_route(
            name="get_estimate",
            path=f"{self.client.settings.OPENEO_PREFIX}/jobs" + "/{job_id}/estimate",
            response_model=models.JobsGetEstimateGetResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.jobs.estimate,
        )

    def register_get_logs(self):
        """Register endpoint for retrieving job logs (GET /jobs/{job_id})."""
        self.router.add_api_route(
            name="get_logs",
            path=f"{self.client.settings.OPENEO_PREFIX}/jobs" + "/{job_id}/logs",
            response_model=models.JobsGetLogsResponse,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.jobs.logs,
        )

    def register_get_results(self):
        """Register endpoint for getting the results from a batch job (GET /jobs/{job_id})."""
        self.router.add_api_route(
            name="get_results",
            path=f"{self.client.settings.OPENEO_PREFIX}/jobs" + "/{job_id}/results",
            response_model=models.Collection,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.jobs.get_results,
        )

    def register_start_job(self):
        """Register endpoint for starting batch job processing (GET /jobs/{job_id})."""
        self.router.add_api_route(
            name="start_job",
            path=f"{self.client.settings.OPENEO_PREFIX}/jobs" + "/{job_id}/results",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["POST"],
            endpoint=self.client.jobs.start_job,
        )

    def register_cancel_job(self):
        """Register endpoint for cancelling job processing (GET /jobs/{job_id})."""
        self.router.add_api_route(
            name="cancel_job",
            path=f"{self.client.settings.OPENEO_PREFIX}/jobs" + "/{job_id}/results",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["DELETE"],
            endpoint=self.client.jobs.cancel_job,
        )

    def register_list_files(self):
        """Register endpoint for listing a user's fils (GET /files)."""
        self.router.add_api_route(
            name="list_files",
            path=f"{self.client.settings.OPENEO_PREFIX}/files",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.files.list_files,
        )

    def register_download_file(self):
        """Register endpoint for downloading a specific file (GET /files/{path})."""
        self.router.add_api_route(
            name="download_file",
            path=f"{self.client.settings.OPENEO_PREFIX}/files" + "/{path:path}",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.files.download_file,
        )

    def register_upload_file(self):
        """Register endpoint for uploading a new file (PUT /files/{path})."""
        self.router.add_api_route(
            name="upload_file",
            path=f"{self.client.settings.OPENEO_PREFIX}/files" + "/{path:path}",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["PUT"],
            endpoint=self.client.files.upload_file,
        )

    def register_delete_file(self):
        """Register endpoint for deleting a new file (DELETE /files/{path})."""
        self.router.add_api_route(
            name="delete_file",
            path=f"{self.client.settings.OPENEO_PREFIX}/files" + "/{path:path}",
            response_model=None,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["DELETE"],
            endpoint=self.client.files.delete_file,
        )

    def register_core(self):
        """
        Add application logic to the API layer.
        """
        self.register_get_conformance()
        self.register_get_credentials_oidc()
        self.register_get_health()
        self.register_get_user_info()
        self.register_run_sync_job()
        self.register_get_udf_runtimes()
        self.register_validate_user_process_graph()
        self.register_get_file_formats()
        self.register_get_collections()
        self.register_get_collection()
        self.register_get_collection_items()
        self.register_get_collection_item()
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
        """
        Register exception handler to turn python exceptions into expected OpenEO error output.
        """

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
        """
        Post-init hook responsible for setting up the application upon instantiation of the class.
        """
        # Register core endpoints
        self.register_core()
        self.register_get_capabilities()
        self.app.include_router(router=self.router)
        self.app.add_exception_handler(HTTPException, self.http_exception_handler)
