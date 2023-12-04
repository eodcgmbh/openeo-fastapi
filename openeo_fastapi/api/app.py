from attrs import Factory, define, field
from fastapi import FastAPI, Response


@define
class OpenEOApi:
    """Factory for creating FastApi applications conformant to the OpenEO Api specification."""

    client: field()
    app: field(default=Factory(lambda self: FastAPI))

    def register_get_capabilities(self):
        """Register landing page (GET /).

        Returns:
            None
        """
        self.app.add_api_route(
            name="capabilities",
            path="/",
            response_class=Response,
            response_model_exclude_unset=False,
            response_model_exclude_none=True,
            methods=["GET"],
            endpoint=self.client.get_capabilities,
        )
