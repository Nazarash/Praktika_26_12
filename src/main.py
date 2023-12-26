from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging

# Пример данных для сущностей
entities = [
    {'id': 1, 'name': 'Entity 1'},
    {'id': 2, 'name': 'Entity 2'},
    {'id': 3, 'name': 'Entity 3'},
    {'id': 4, 'name': 'Entity 4'},
    {'id': 5, 'name': 'Entity 5'},
]

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CRUDRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        entity_id = int(self.path.split('/')[-1])
        entity = next((item for item in entities if item['id'] == entity_id), None)
        if entity:
            response = {'data': entity}
            self.wfile.write(json.dumps(response).encode())
            logger.info(f"GET request for entity with ID {entity_id}")
        else:
            self.send_response(404)
            self.wfile.write(b'Entity not found')
            logger.error(f"GET request for non-existing entity with ID {entity_id}")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        new_entity = json.loads(post_data.decode())

        # Генерация уникального ID для новой сущности
        new_entity_id = max(item['id'] for item in entities) + 1
        new_entity['id'] = new_entity_id
        entities.append(new_entity)

        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = {'message': 'Entity created successfully', 'id': new_entity_id}
        self.wfile.write(json.dumps(response).encode())
        logger.info(f"POST request. New entity created with ID {new_entity_id}")

    def do_DELETE(self):
        entity_id = int(self.path.split('/')[-1])
        entity = next((item for item in entities if item['id'] == entity_id), None)

        if entity:
            entities.remove(entity)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = {'message': 'Entity deleted successfully'}
            self.wfile.write(json.dumps(response).encode())
            logger.info(f"DELETE request. Entity with ID {entity_id} deleted")
        else:
            self.send_response(404)
            self.wfile.write(b'Entity not found')
            logger.error(f"DELETE request for non-existing entity with ID {entity_id}")


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, CRUDRequestHandler)
    print('Server is running on port 8000')
    httpd.serve_forever()
