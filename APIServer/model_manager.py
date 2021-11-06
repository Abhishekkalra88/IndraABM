from lru import LRU
from multiprocessing import Process, Pipe, cpu_count
from APIServer.model_api import run_model, create_model, create_model_for_test
from APIServer.api_utils import json_converter
from APIServer.model_process import createModelProcess, Message, CommunicationType

from db.model_db import get_model_by_id

modelManager = None

class ModelProcessAttrs:
    def __init__(self, process, parent_conn, model_id):
        self.process = process
        self.parent_conn = parent_conn
        self.model_id = model_id

class ModelManager:
    def __init__(self):
        print("Creating new model manager")
        self.processes = LRU(cpu_count() * 5 + 1)       # Not too many processes but also not too less

    def get_model(self, exec_key):
        return self.processes[exec_key]
    
    def to_json(self):
        ret_json = {}
        for key,val in self.processes.items():
            ret_json[key] = get_model_by_id(val.model_id).name
        return ret_json

    def spawn_model(self, model_id, payload, indra_dir):
        parent_conn, child_conn = Pipe()
        new_process = Process(target=createModelProcess, args=(child_conn, model_id, payload, indra_dir))
        mp = ModelProcessAttrs(new_process, parent_conn, model_id)
        new_process.start()
        model = parent_conn.recv()
        self.processes[model.exec_key] = mp
        return model

    def run_model(self, exec_key, runtime):
        modelProcess = self.processes[exec_key]
        if(modelProcess is None):
            return None
        message = Message(CommunicationType.RUN_MODEL, {runtime})
        modelProcess.parent_conn.send(message)
        model = modelProcess.parent_conn.recv()
        return model

modelManager = ModelManager()