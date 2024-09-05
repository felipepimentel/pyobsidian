import asyncio
import websockets
import json
from ..obsidian_helper import load_config, get_file_content, write_to_file
import os
import difflib

class RealtimeCollaboration:
    def __init__(self, config):
        self.config = config
        self.clients = set()
        self.file_versions = {}

    async def register(self, websocket):
        self.clients.add(websocket)
        await self.sync_client(websocket)

    async def unregister(self, websocket):
        self.clients.remove(websocket)

    async def sync_client(self, websocket):
        vault_path = self.config['obsidian']['vault_path']
        for file_path in os.listdir(vault_path):
            if file_path.endswith('.md'):
                content = get_file_content(os.path.join(vault_path, file_path))
                await websocket.send(json.dumps({
                    'type': 'sync',
                    'file': file_path,
                    'content': content
                }))

    async def broadcast(self, message):
        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def handle_edit(self, data):
        file_path = os.path.join(self.config['obsidian']['vault_path'], data['file'])
        new_content = data['content']
        
        if file_path in self.file_versions:
            old_content = self.file_versions[file_path]
            merged_content = self.merge_changes(old_content, new_content)
            write_to_file(file_path, merged_content)
            self.file_versions[file_path] = merged_content
        else:
            write_to_file(file_path, new_content)
            self.file_versions[file_path] = new_content

        await self.broadcast(json.dumps({
            'type': 'update',
            'file': data['file'],
            'content': self.file_versions[file_path]
        }))

    def merge_changes(self, old_content, new_content):
        differ = difflib.Differ()
        diff = list(differ.compare(old_content.splitlines(), new_content.splitlines()))
        merged = []
        for line in diff:
            if line.startswith('  ') or line.startswith('+ '):
                merged.append(line[2:])
        return '\n'.join(merged)

    async def handler(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                if data['type'] == 'edit':
                    await self.handle_edit(data)
        finally:
            await self.unregister(websocket)

    def start_server(self):
        config = load_config()
        server = websockets.serve(self.handler, "localhost", 6789)
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    config = load_config()
    collaboration = RealtimeCollaboration(config)
    collaboration.start_server()