# Generate test data

import os
import json

os.sys.path.append(os.getcwd())
from app.src import models


def gen_users():
    """ Generate users """
    print('Generating users ...')

    instances = []
    with open('script/data/users.json') as fh:
        users = json.load(fh)
        for data in users:
            u = models.User(**data)
            u.save()
            instances.append(u)
    return instances


if __name__ == '__main__':
    new_users = gen_users()
