"""
This file contains functions dealing with getting source code from a repo.
"""
import base64
import requests
from http import HTTPStatus

import db.model_db as model_db
from lib.utils import get_indra_home

GITHUB_API = 'https://api.github.com/repos/'
SOURCE_CODE_URL = GITHUB_API + 'TandonDevOps/IndraABM/contents/'

indra_dir = get_indra_home()


def path_from_model(model):
    return model.get('package') + '/' + model.get('module') + '.py'


def get_source_code(model_id):
    """
    Return the source code for a model.
    """
    model = model_db.get_model_by_id(model_id, indra_dir)
    if model is None:
        return None
    path = path_from_model(model)
    codebase_response = requests.get(SOURCE_CODE_URL + path)
    if codebase_response.status_code == HTTPStatus.OK:
        raw_content = codebase_response.json()['content']
        content_bytes = base64.b64decode(raw_content)
        return content_bytes.decode('ascii')
    else:
        return None
