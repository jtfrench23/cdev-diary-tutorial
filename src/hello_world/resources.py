# Generated as part of Quick Start project template 
import json
import os

from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from cdev.resources.simple.api import Api
from cdev.resources.simple.xlambda import simple_function_annotation
from cdev.resources.simple.relational_db import RelationalDB, db_engine
from cdev import Project as cdev_project

from .models import Entry
from .utils import Response
from cdev.resources.simple.static_site import StaticSite
myFrontend = StaticSite("demofrontend", content_folder="src/content", index_document='index.html')
 



myProject = cdev_project.instance()

## Routes
DemoApi = Api("demoapi")

hello_route = DemoApi.route("/hello_world", "GET")

create_entries_route = DemoApi.route("/entry/create", "POST")

get_entries_route = DemoApi.route("/entry/get", "GET")


## DB
myDB = RelationalDB(
  "demo_db",
  db_engine.aurora_postgresql,
  "username",
  "password",
  "default_diaryDB"
)

## Functions

cluster_arn = os.environ.get("CLUSTER_ARN")
secret_arn = os.environ.get("SECRET_ARN")
database_name = os.environ.get("DB_NAME")

engine = create_engine(f'postgresql+auroradataapi://:@/{database_name}',
                    connect_args=dict(aurora_cluster_arn=cluster_arn, secret_arn=secret_arn))


@simple_function_annotation("hello_world_function", events=[hello_route.event()], 
environment={"CLUSTER_ARN": myDB.output.cluster_arn, "SECRET_ARN": myDB.output.secret_arn, "DB_NAME": myDB.database_name}, 
permissions=[myDB.available_permissions.DATABASE_ACCESS, myDB.available_permissions.SECRET_ACCESS])
def hello_world(event, context):
    print('Hello from inside your Function!')

    session = Session(engine)

    stmt = select(Entry).where(Entry.title == 'test')

    for entry in session.scalars(stmt):
        print(entry)

    return {
        "status_code": 200,
        "message": "Hello Outside World!"
    }

@simple_function_annotation("create_entry_function", events=[create_entries_route.event()], 
environment={"CLUSTER_ARN": myDB.output.cluster_arn, "SECRET_ARN": myDB.output.secret_arn, "DB_NAME": myDB.database_name}, 
permissions=[myDB.available_permissions.DATABASE_ACCESS, myDB.available_permissions.SECRET_ACCESS])
def create_entry(event, context):
    print('Hello from inside your entry creation Function!')

    session = Session(engine)
    data = json.loads(event.get("body"))
    try:
        session.add(Entry(title=data.get("title"), content=data.get("content")))
        session.commit()
        return Response(200, body = json.dumps({"message": "Created entry"}))
    except Exception as e:
        print(str(e))
        return Response(400, body = json.dumps({"message":"entry creation failed"}))

def posts_serializer(obj_list):
    data = []
    for object in obj_list:
        dictionary = {
            'id':object.id,
            'title':object.title,
            'content':object.content
        }
        data.append(dictionary)
    print("data complete")
    return data

@simple_function_annotation("get_entries_function", events=[get_entries_route.event()], 
environment={"CLUSTER_ARN": myDB.output.cluster_arn, "SECRET_ARN": myDB.output.secret_arn, "DB_NAME": myDB.database_name}, 
permissions=[myDB.available_permissions.DATABASE_ACCESS, myDB.available_permissions.SECRET_ACCESS])
def get_posts(event, context):
    print('Hello from inside your get posts Function!')

    session = Session(engine)
    try:
        posts: Entry = session.query(Entry).order_by('id').all()
        data = posts_serializer(posts)
        return Response(200, body=json.dumps(data))
    except Exception as e:
        return Response(400, body=json.dumps({"message": str(e)}))

## Output
myProject.display_output("Base API URL", DemoApi.output.endpoint)
myProject.display_output("Routes", DemoApi.output.endpoints)

myProject.display_output("Base API URL", DemoApi.output.endpoint)
myProject.display_output("Routes", DemoApi.output.endpoints)
myProject.display_output("Static Site URl", myFrontend.output.site_url)