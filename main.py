from flask import Flask
from config import Config
from extensions import db, migrate
from models import *
from routes import register_routes
from cerbos.sdk.grpc.client import CerbosClient
from cerbos.engine.v1 import engine_pb2
from cerbos.request.v1 import request_pb2
from google.protobuf.struct_pb2 import Value

app = Flask(__name__)


principal = engine_pb2.Principal(
    id="john",
    roles={"employee"},
    policy_version="20210210",
    attr={
        "department": Value(string_value="marketing"),
        "geography": Value(string_value="GB"),
        "team": Value(string_value="design"),
    },
)

resource = engine_pb2.Resource(
    id="XX125",
    kind="leave_request",
    attr={
        "id": Value(string_value="XX125"),
        "department": Value(string_value="marketing"),
        "geography": Value(string_value="GB"),
        "team": Value(string_value="design"),
        "owner": Value(string_value="john"),
    }
)

plan_resource = engine_pb2.PlanResourcesInput.Resource(
    kind="leave_request",
    policy_version="20210210"
)

with CerbosClient("localhost:3593", tls_verify=False) as c:
    # Check a single action on a single resource
    if c.is_allowed("view", principal, resource):
        # perform some action
        pass

    # Get the query plan for "view" action
    plan = c.plan_resources(action="view", principal=principal, resource=plan_resource)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    register_routes(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)