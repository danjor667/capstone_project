import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

class PatientUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
            return
        
        # Join general updates group
        self.general_group_name = "patient_updates"
        await self.channel_layer.group_add(
            self.general_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave general updates group
        await self.channel_layer.group_discard(
            self.general_group_name,
            self.channel_name
        )
        
        # Leave any patient-specific groups
        if hasattr(self, 'patient_group_name'):
            await self.channel_layer.group_discard(
                self.patient_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'subscribe':
                patient_id = data.get('patientId')
                if patient_id:
                    # Leave previous patient group if any
                    if hasattr(self, 'patient_group_name'):
                        await self.channel_layer.group_discard(
                            self.patient_group_name,
                            self.channel_name
                        )
                    
                    # Join new patient group
                    self.patient_group_name = f"patient_{patient_id}"
                    await self.channel_layer.group_add(
                        self.patient_group_name,
                        self.channel_name
                    )
                    
                    await self.send(text_data=json.dumps({
                        'type': 'subscription_confirmed',
                        'patientId': patient_id
                    }))
            
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
    
    # Handler for patient updates
    async def patient_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'patient-update',
            'patientId': event['patient_id'],
            'data': event['data']
        }))
    
    # Handler for new alerts
    async def new_alert(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new-alert',
            'patientId': event['patient_id'],
            'alert': event['alert']
        }))
    
    # Handler for lab results
    async def lab_result(self, event):
        await self.send(text_data=json.dumps({
            'type': 'lab-result',
            'patientId': event['patient_id'],
            'result': event['result']
        }))