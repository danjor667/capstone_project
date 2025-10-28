import socketio
from django.conf import settings

# Create Socket.IO server
sio = socketio.AsyncServer(
    cors_allowed_origins="*",
    async_mode='asgi'
)

@sio.event
async def connect(sid, environ, auth):
    print(f'Client {sid} connected')
    await sio.emit('connected', {'status': 'Connected to CKD Dashboard'}, room=sid)

@sio.event
async def disconnect(sid):
    print(f'Client {sid} disconnected')

@sio.event
async def subscribe(sid, data):
    patient_id = data.get('patientId')
    if patient_id:
        await sio.enter_room(sid, f'patient_{patient_id}')
        await sio.emit('subscription_confirmed', {'patientId': patient_id}, room=sid)

# Socket.IO ASGI application
socketio_app = socketio.ASGIApp(sio)