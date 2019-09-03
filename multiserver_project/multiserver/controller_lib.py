from multiserver.connection_lib import ClientConnection

import time
import json
import uuid
import threading
import queue
import MySQLdb

from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)

class Controller:
    def __init__(self, master_address=('', 9089), db_user='root', db_password='05011998', db_name='results'):
        self.master_connection = ClientConnection(master_address)
        self.db_connection = MySQLdb.connect(user=db_user, passwd=db_password, db=db_name)
        self.db_cursor = self.db_connection.cursor()
        self.connected_to_db = True

    def send_task_chunk(self, package_filename, package_name, package_version, module_name, function_name, arglists):
        "Sends a chunk of tasks that use same function but different args. Returns chunk's ID, which can be used to access results in a DB."

        chunk_id = uuid.uuid4().hex
        task_ids = []

        chunk_info = {
            'header': 'chunk_info',
            'body': {
                'id': chunk_id,
                'length': len(arglists),
            }
        }
        response = self.master_connection.get_response(chunk_info)

        for args in arglists:
            task_id = uuid.uuid4().hex
            task_ids.append(task_id)
            task = {
                'header': 'task',
                'body': {
                    'package_filename': package_filename,
                    'package_name': package_name,
                    'package_version': package_version,
                    'module_name': module_name,
                    'function_name': function_name,
                    'args': args,
                    'chunk_id': chunk_id,
                    'task_id': task_id
                }
            }
            response = self.master_connection.get_response(task)

        return chunk_id, task_ids

    def wait_for_chunk_completion(self, chunk_id):
        notice_request = {
            'header': 'finish_notice_request',
            'body': {
                'chunk_id': chunk_id
            }
         }
        response = self.master_connection.get_response(notice_request)

    def get_results_from_db(self, chunk_id):
        self.db_cursor.execute('SELECT * FROM results WHERE chunk_id = %s', (chunk_id,))
        self.db_connection.commit()
        return self.db_cursor.fetchall()
