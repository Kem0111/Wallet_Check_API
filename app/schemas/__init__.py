from .request.bodies.register import Register as BodyRegisterRequest
from .request.bodies.login import Login as BodyLoginRequest
from .request.bodies.wallet_address import AddressUpload as BodyAddressUploadRequest
from app.schemas.schema import ApplicationResponse, RouteReturnT

__all__ = ("BodyRegisterRequest",
           "BodyLoginRequest",
           "ApplicationResponse",
           "RouteReturnT",
           "BodyAddressUploadRequest")
