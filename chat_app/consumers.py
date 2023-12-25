from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer


class MyConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('--WEBSOCKET CONNECTED--')

        """it is adding clients in 'chatting' group"""
        await self.channel_layer.group_add(
            'chatting',  # this is a group name
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'  # server is ready to accept data from client
        })

    async def websocket_receive(self, event):
        print('--MSG FROM CLINET:-', event['text'])

        """it is sends a message to a group named 'chatting' using the channel layer."""
        await self.channel_layer.group_send(
            'chatting',
            {
                # its indicating content of msg which is chat
                'type': 'chat.message',
                # it sets the actual clinet msg in 'message' key
                'message': event['text']
            }
        )
    """this function is for sending back client responce to client side for printing it on chat box"""
    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    """this method removes the group name from channel to disconnect client server connection"""
    async def websocket_disconnect(self, event):
        print('--WEBSOCKET DISCONNECTED--')
        await self.channel_layer.group_discard(
            'chatting',
            self.channel_name
        )
        raise StopConsumer  # it just disconnect connetion of client server
