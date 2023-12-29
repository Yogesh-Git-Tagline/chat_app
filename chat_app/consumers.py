from channels.generic.websocket import AsyncWebsocketConsumer
import json
import base64


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('Websocket Connected')
        await self.accept()

    async def disconnect(self, code):
        print('Disconnected')

    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data.get('msg')
        image_content = data.get('image_content')

        if image_content:
            image_path = '/Users/mac/Desktop/Blog_API/chat_project/chat_app/static/myimage/' + \
                data.get('image_name')

            binary_image_content = base64.b64decode(image_content)

            with open(image_path, 'wb') as image_file:
                image_file.write(binary_image_content)

            await self.channel_layer.group_add("image_group", self.channel_name)
            await self.channel_layer.group_send(
                "image_group",
                {
                    "type": "send.image",
                    "image_path": image_path,
                    "image_name": data.get('image_name'),
                },
            )
        await self.channel_layer.group_add("image_group", self.channel_name)
        await self.channel_layer.group_send(
            'image_group',
            {
                'type': 'chat.message',
                'message': text
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']
                                             ))

    async def send_image(self, event):
        await self.send(text_data=json.dumps({
            'type': 'image',
            'image_path': event['image_path'],
            'image_name': event['image_name'],
        }))
