import json


import os


from sqlalchemy import select, create_engine


from sqlalchemy.orm import Session


from .models import Entry


from .utils import Response


cluster_arn = os.environ.get("CLUSTER_ARN")


secret_arn = os.environ.get("SECRET_ARN")


database_name = os.environ.get("DB_NAME")


engine = create_engine(f'postgresql+auroradataapi://:@/{database_name}',
                    connect_args=dict(aurora_cluster_arn=cluster_arn, secret_arn=secret_arn))


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


def get_posts(event, context):
    print('Hello from inside your get posts Function!')

    session = Session(engine)
    try:
        posts: Entry = session.query(Entry).order_by('id').all()
        data = posts_serializer(posts)
        return Response(200, body=json.dumps(data))
    except Exception as e:
        return Response(400, body=json.dumps({"message": str(e)}))
