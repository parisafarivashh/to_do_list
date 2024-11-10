from channels.generic.websocket import AsyncJsonWebsocketConsumer


class UserConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        self.group_name = ''
        if user.is_authenticated:
            self.group_name = f"user_{user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

        else:
            await self.close()

    async def disconnect(self, message):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.close()

    async def receive(self, text_data):
        # Send the same message back to the WebSocket
        await self.send_json({'message': text_data})

    async def send_data(self, event):
        await self.send(text_data=event["data"])

