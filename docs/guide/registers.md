## Editing the registers.

The endpoint registers are a loose abstraction defining what endpoints a register is responsible for, and also what code is expected to be executed for those endpoints.

The available registers can be imported as follows.

    from openeo_fastapi.client.jobs import JobsRegister
    from openeo_fastapi.client.files import FilesRegister
    from openeo_fastapi.client.processes import ProcessesRegister
    from openeo_fastapi.client.collections import CollectionsRegister

You will need to know how you are expected to overwrite the functionality of these registers, as the openeo-fastapi package does not define functionality for all available endpoints.

## How to overwrite an endpoint.

In the following example, we import the FileRegister, and overwrite the functionality for the list_files method. This will define a new response for that endpoint.  This is the framework for editing the functionality of the api endpoints.

    from openeo_fastapi.client.files import FilesRegister

    class OverwrittenFileRegister(FilesRegister):
        def __init__(self, settings, links) -> None:
            super().__init__(settings, links)

        def list_files(
            self,
            limit: Optional[int] = 10
        ):
            """ """
            return FilesGetResponse(
                files=[File(path="/somefile.txt", size=10)],
                links=[
                    Link(
                        href="https://eodc.eu/",
                        rel="about",
                        type="text/html",
                        title="Homepage of the service provider",
                    )
                ],
            )

In order to use this overwritten file register, we instantiate the register, and parse this to the OpenEOCore object. Now, when the api is next deployed, we will return the FilesGetResponse, and not the default HTTPException.

    extended_register = OverwrittenFileRegister(app_settings, test_links)

    client = OpenEOCore(
        ...
        files=extended_register,
        ...
    )

    api = OpenEOApi(client=client, app=FastAPI())

## How to add an endpoint

The registers can also be extended to include extra functionality. In order to do this, we again need to define a new child class for the register you want to extend.

We can define a new endpoint for the api as follows.

    from openeo_fastapi.api.types import Endpoint
    new_endpoint = Endpoint(
        path="/files/{path}",
        methods=["HEAD"],
    )

When defining the child register, the *_initialize_endpoints* method needs to be redefined to add the new_endpoint object. The new functionality can be defined under a new function, here *get_file_headers*.

    from openeo_fastapi.client.files import FilesRegister, FILE_ENDPOINTS

    class ExtendedFileRegister(FilesRegister):
        def __init__(self, settings, links) -> None:
            super().__init__(settings, links)
            self.endpoints = self._initialize_endpoints()

        def _initialize_endpoints(self) -> list[Endpoint]:
            endpoints = list(FILE_ENDPOINTS)
            endpoints.append(new_endpoint)
            return endpoints

        def get_file_headers(
            self, path: str, user: User = Depends(Authenticator.validate)
        ):
            """ """
            return Response(
                status_code=200,
                headers={
                    "Accept-Ranges": "bytes",
                },
            )

    client = OpenEOCore(
        ...
        files=extended_register,
        ...
    )

    api = OpenEOApi(client=client, app=FastAPI())

So far, we have made the new code available to the api, but the api does not know how or when to execute the new code. The following snippet will register the new path to the api server, along with the functionality.

    api.app.router.add_api_route(
        name="file_headers",
        path=f"/{api.client.settings.OPENEO_VERSION}/files" + "/{path}",
        response_model=None,
        response_model_exclude_unset=False,
        response_model_exclude_none=True,
        methods=["HEAD"],
        endpoint=api.client.files.get_file_headers,
    )