"""
---
"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from routes.v1.base import api_router_v1
from core.config import settings
# from docs_string.exports import (
#     tags_doc_string
# )
# from app.db.session import engine
from services.exports import startup_service


def include_router(app_server):
    """---"""
    app_server.include_router(api_router_v1, prefix=settings.API_V1_STR)

    # @app_server.get("/docs", include_in_schema=False)
    # async def scalar_html():
    #     return get_scalar_api_reference(
    #         openapi_url=app.openapi_url,
    #         title=app.title,
    #     )


def configure_static(app_server):
    """---"""

    base_dir = os.path.dirname(__file__)
    # print(StaticFiles(directory=base_dir + "/static/uploads").all_directories)
    app_server.mount(
        "/static", StaticFiles(directory=base_dir + "/static/uploads"), name="static"
    )


def start_application():
    """---"""
    origins = ["*"]
    app_server = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description=settings.PROJECT_DESCRIPTION,
        # openapi_tags=tags_doc_string.TAGS_METADATA,
        # docs_url=None,
        redoc_url=None,
        # summary="Deadpool's favorite app. Nuff said.",
        contact={
            "name": "Transparência",
            "url": "http://transparecy.ao",
            "email": "est@transparency.ao",
        },
    )
    app_server.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # configure_static(app_server)
    # create_tables()       #new
    include_router(app_server)

    @app_server.on_event("startup")
    async def startup_event():
        print("\033[34m>>>>\033[36m Inicializando Roles\033[0m")
        await startup_service.create_role()

    @app_server.on_event("shutdown")
    async def shutdown_event():
        print("Bye")
    
    return app_server


app = start_application()
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, log_level="info", reload=True)
