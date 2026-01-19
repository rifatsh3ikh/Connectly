from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        await self.accept()

    async def receive(self, text_data):
        from django.contrib.auth.models import User  # ✅ IMPORT HERE (SAFE)

        data = json.loads(text_data)
        message = data.get("message")

        sender = self.scope["user"]
        receiver_id = data.get("receiver_id")

        receiver = User.objects.get(id=receiver_id)

        # your message save logic here
