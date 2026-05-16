import io
import json
from typing import Dict, List, Optional
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from openai import OpenAI

try:
    from config import config
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from config import config


class SpeechToTextService:
    """Service for speech-to-text transcription using IBM Watson with Grok/Groq fallback"""
    
    def __init__(self):
        """Initialize speech-to-text service with IBM Watson or Grok/Groq fallback"""
        self.use_groq = False
        self.fallback_provider = None
        self.speech_to_text = None
        self.groq_client = None
        
        # Try to initialize IBM Watson first
        if config.is_ibm_configured():
            try:
                authenticator = IAMAuthenticator(config.ibm_api_key)
                self.speech_to_text = SpeechToTextV1(authenticator=authenticator)
                self.speech_to_text.set_service_url(config.ibm_url)
                print("Using IBM Watson Speech-to-Text")
            except Exception as e:
                print(f"Failed to initialize IBM Watson: {e}")
                self.speech_to_text = None
        
        # Fall back to Grok / Groq if IBM is not configured or failed
        if self.speech_to_text is None:
            if config.is_grok_configured():
                try:
                    if config.grok_api_key:
                        self.groq_client = OpenAI(
                            api_key=config.grok_api_key,
                            base_url="https://api.x.ai/v1"
                        )
                        self.fallback_provider = "grok"
                    else:
                        self.groq_client = OpenAI(
                            api_key=config.groq_api_key,
                            base_url="https://api.groq.com/openai/v1"
                        )
                        self.fallback_provider = "groq"
                    self.use_groq = True
                    print(f"Using {self.fallback_provider.capitalize()} Speech-to-Text (fallback)")
                except Exception as e:
                    print(f"Failed to initialize Grok/Groq: {e}")
                    raise ValueError("Neither IBM Watson nor Grok/Groq API credentials are properly configured")
            else:
                raise ValueError("Neither IBM Watson nor Grok/Groq API credentials are configured")
    
    def transcribe_audio_file(self, audio_file_path: str) -> Dict:
        """
        Transcribe audio file with speaker diarization (IBM) or basic transcription (Grok/Groq)
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Dictionary containing transcript and speaker information
        """
        try:
            if self.use_groq:
                return self._transcribe_with_groq(audio_file_path)
            else:
                return self._transcribe_with_ibm(audio_file_path)
        
        except Exception as e:
            if not self.use_groq and config.is_grok_configured():
                print(f"IBM transcription failed, falling back to Grok/Groq: {e}")
                self.use_groq = True
                if self.groq_client is None:
                    self._initialize_fallback_client()
                return self._transcribe_with_groq(audio_file_path)
            print(f"Error transcribing audio: {e}")
            raise

    def _initialize_fallback_client(self):
        """Initialize the Grok/Groq fallback client when IBM transcription fails."""
        if config.grok_api_key:
            self.groq_client = OpenAI(
                api_key=config.grok_api_key,
                base_url="https://api.x.ai/v1"
            )
            self.fallback_provider = "grok"
        elif config.groq_api_key:
            self.groq_client = OpenAI(
                api_key=config.groq_api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            self.fallback_provider = "groq"
    
    def _transcribe_with_ibm(self, audio_file_path: str) -> Dict:
        """Transcribe using IBM Watson with speaker diarization"""
        with open(audio_file_path, 'rb') as audio_file:
            response = self.speech_to_text.recognize(
                audio=audio_file,
                content_type='audio/wav',
                speaker_labels=True,
                timestamps=True,
                word_confidence=True,
                smart_formatting=True,
                model='en-US_BroadbandModel'
            ).get_result()
        
        # Extract transcript and speaker information
        return self._process_watson_response(response)
    
    def _transcribe_with_groq(self, audio_source) -> Dict:
        """Transcribe using Grok/Groq (no speaker diarization)"""
        if isinstance(audio_source, (bytes, bytearray)):
            audio_file = io.BytesIO(audio_source)
            audio_file.name = "audio.webm"
        elif hasattr(audio_source, "read"):
            audio_file = audio_source
        else:
            with open(audio_source, 'rb') as file_handle:
                transcript = self.groq_client.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=file_handle
                )
                transcript_text = transcript.text
                return {
                    "transcript": transcript_text,
                    "formatted_transcript": transcript_text,
                    "speaker_segments": [],
                    "raw_response": {"text": transcript_text, "provider": self.fallback_provider or "grok"}
                }

        transcript = self.groq_client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file
        )
        
        # Format response to match IBM Watson structure
        transcript_text = transcript.text
        return {
            "transcript": transcript_text,
            "formatted_transcript": transcript_text,
            "speaker_segments": [],
            "raw_response": {"text": transcript_text, "provider": self.fallback_provider or "grok"}
        }
    
    def transcribe_audio_stream(self, audio_chunk: bytes, content_type: str = 'audio/wav') -> Dict:
        """
        Transcribe audio stream chunk
        Note: Grok/Groq don't provide incremental streaming transcripts here, so we transcribe the buffered chunk
        
        Args:
            audio_chunk: Audio data chunk
            content_type: Audio content type (default: 'audio/wav')
            
        Returns:
            Dictionary containing partial transcript
        """
        if self.use_groq:
            try:
                return self._transcribe_with_groq(audio_chunk)
            except Exception as e:
                return {
                    "transcript": "",
                    "formatted_transcript": "",
                    "speaker_segments": [],
                    "error": str(e)
                }
        
        try:
            response = self.speech_to_text.recognize(
                audio=audio_chunk,
                content_type=content_type,
                speaker_labels=True,
                timestamps=True,
                interim_results=True,
                model='en-US_BroadbandModel'
            ).get_result()
            
            return self._process_watson_response(response)
        
        except Exception as e:
            if not self.use_groq and config.is_grok_configured():
                print(f"IBM stream transcription failed, falling back to Grok/Groq: {e}")
                self.use_groq = True
                if self.groq_client is None:
                    self._initialize_fallback_client()
                return self._transcribe_with_groq(audio_chunk)
            print(f"Error transcribing audio stream: {e}")
            return {
                "transcript": "",
                "formatted_transcript": "",
                "speaker_segments": [],
                "error": str(e)
            }
    
    def _process_watson_response(self, response: Dict) -> Dict:
        """
        Process Watson API response and format transcript with speaker labels
        
        Args:
            response: Watson API response
        Returns:
            Formatted transcript data
        """
        results = response.get('results', [])
        speaker_labels = response.get('speaker_labels', [])
        
        # Extract full transcript
        transcript = ""
        for result in results:
            if result.get('final', False):
                alternatives = result.get('alternatives', [])
                if alternatives:
                    transcript += alternatives[0].get('transcript', '') + " "
        
        # Format transcript with speaker labels
        formatted_transcript = self._format_with_speakers(results, speaker_labels)
        
        # Extract speaker segments
        speaker_segments = self._extract_speaker_segments(speaker_labels)
        
        return {
            "transcript": transcript.strip(),
            "formatted_transcript": formatted_transcript,
            "speaker_segments": speaker_segments,
            "raw_response": response
        }
    
    def _format_with_speakers(self, results: List[Dict], speaker_labels: List[Dict]) -> str:
        """
        Format transcript with speaker labels (Doctor/Patient)
        
        Args:
            results: Watson results
            speaker_labels: Speaker label information
            
        Returns:
            Formatted transcript string
        """
        if not speaker_labels:
            # No speaker diarization, return plain transcript
            transcript = ""
            for result in results:
                if result.get('final', False):
                    alternatives = result.get('alternatives', [])
                    if alternatives:
                        transcript += alternatives[0].get('transcript', '') + " "
            return transcript.strip()
        
        # Group words by speaker
        speaker_segments = []
        current_speaker = None
        current_text = []
        
        for label in speaker_labels:
            speaker = label.get('speaker')
            word = label.get('final', False)
            
            if speaker != current_speaker:
                if current_text:
                    # Map speaker numbers to roles (0 = Doctor, 1 = Patient)
                    speaker_role = "Doctor" if current_speaker == 0 else "Patient"
                    speaker_segments.append(f"{speaker_role}: {' '.join(current_text)}")
                current_speaker = speaker
                current_text = []
            
            # Find the word text from results
            for result in results:
                if result.get('final', False):
                    alternatives = result.get('alternatives', [])
                    if alternatives:
                        timestamps = alternatives[0].get('timestamps', [])
                        for ts in timestamps:
                            if abs(ts[1] - label.get('from', 0)) < 0.1:
                                current_text.append(ts[0])
                                break
        
        # Add final segment
        if current_text:
            speaker_role = "Doctor" if current_speaker == 0 else "Patient"
            speaker_segments.append(f"{speaker_role}: {' '.join(current_text)}")
        
        return "\n".join(speaker_segments)
    
    def _extract_speaker_segments(self, speaker_labels: List[Dict]) -> List[Dict]:
        """
        Extract structured speaker segment information
        
        Args:
            speaker_labels: Speaker label information
            
        Returns:
            List of speaker segments with timestamps
        """
        segments = []
        current_speaker = None
        current_segment = None
        
        for label in speaker_labels:
            speaker = label.get('speaker')
            
            if speaker != current_speaker:
                if current_segment:
                    segments.append(current_segment)
                
                current_speaker = speaker
                speaker_role = "Doctor" if speaker == 0 else "Patient"
                current_segment = {
                    "speaker": speaker_role,
                    "from": label.get('from'),
                    "to": label.get('to'),
                    "confidence": label.get('confidence')
                }
            else:
                # Update end time of current segment
                if current_segment:
                    current_segment['to'] = label.get('to')
        
        # Add final segment
        if current_segment:
            segments.append(current_segment)
        
        return segments


# Singleton instance
_speech_service = None


def get_speech_service() -> SpeechToTextService:
    """Get or create singleton instance of SpeechToTextService"""
    global _speech_service
    if _speech_service is None:
        _speech_service = SpeechToTextService()
    return _speech_service


# Made with Bob