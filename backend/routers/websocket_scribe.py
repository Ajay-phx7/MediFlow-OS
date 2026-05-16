from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import json
import asyncio

router = APIRouter()


class WebSocketManager:
    """Manage WebSocket connections for real-time transcription"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
    
    async def send_message(self, client_id: str, message: dict):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)


manager = WebSocketManager()


@router.websocket("/ws/scribe/{client_id}")
async def websocket_scribe_endpoint(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint for real-time audio transcription
    
    Client sends: Binary audio chunks
    Server sends: JSON messages with transcription updates
    
    Message format:
    {
        "type": "transcript_update",
        "speaker": "Doctor" | "Patient",
        "text": "transcribed text",
        "is_final": true | false,
        "timestamp": 123.45
    }
    """
    await manager.connect(websocket, client_id)

    async def safe_send_json(payload: dict) -> bool:
        """Best-effort JSON send that no-ops if the socket is already closed."""
        try:
            if websocket.client_state.name == "DISCONNECTED":
                return False
            await websocket.send_json(payload)
            return True
        except Exception:
            return False
    
    try:
        # Import services (lazy import to avoid startup errors if not configured)
        try:
            from config import config
            from services.speech_to_text_service import get_speech_service
            
            if not config.is_speech_configured():
                await safe_send_json({
                    "type": "error",
                    "message": "API keys not configured. Please set up .env file."
                })
                await websocket.close()
                return
            
            speech_service = get_speech_service()
        except Exception as e:
            await safe_send_json({
                "type": "error",
                "message": f"Service initialization failed: {str(e)}"
            })
            await websocket.close()
            return
        
        # Send ready message
        await safe_send_json({
            "type": "ready",
            "message": "WebSocket connection established. Ready to receive audio."
        })
        
        audio_buffer = bytearray()
        
        while True:
            # Receive audio data from client
            data = await websocket.receive()
            
            if "bytes" in data:
                # Binary audio data
                audio_buffer.extend(data["bytes"])
            
            elif "text" in data:
                # Handle text commands
                message = json.loads(data["text"])
                command = message.get("command")
                
                if command == "stop":
                    # Transcribe the complete recording as one media blob.
                    if len(audio_buffer) > 0:
                        try:
                            result = speech_service.transcribe_audio_stream(
                                bytes(audio_buffer),
                                content_type="audio/webm"
                            )

                            if result.get("formatted_transcript"):
                                await safe_send_json({
                                    "type": "transcript_final",
                                    "transcript": result["formatted_transcript"],
                                    "speaker_segments": result.get("speaker_segments", [])
                                })
                        except Exception as e:
                            await safe_send_json({
                                "type": "error",
                                "message": f"Final transcription error: {str(e)}"
                            })
                    
                    await safe_send_json({
                        "type": "stopped",
                        "message": "Transcription stopped"
                    })
                    break
                
                elif command == "ping":
                    await safe_send_json({
                        "type": "pong"
                    })
    
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except RuntimeError as e:
        # Starlette raises RuntimeError when receive() is called after disconnect.
        if "disconnect message has been received" not in str(e).lower():
            await safe_send_json({
                "type": "error",
                "message": f"WebSocket error: {str(e)}"
            })
        manager.disconnect(client_id)
    except Exception as e:
        await safe_send_json({
            "type": "error",
            "message": f"WebSocket error: {str(e)}"
        })
        manager.disconnect(client_id)
    finally:
        manager.disconnect(client_id)


# Made with Bob