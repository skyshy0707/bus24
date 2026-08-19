import json
import logging

from django.urls import path
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from djangochannelsrestframework.consumers import view_as_consumer
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.scope_utils import ensure_async
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed

logger = logging.getLogger(__name__)


class GenericDRFConsumer(GenericAsyncAPIConsumer):
    """
    Generic consumer that wraps DRF views
    Receives stream name from scope and delegates to appropriate DRF view
    """
    
    async def reply(self, action=None, data=None, errors=None, status=200, request_id=None):
        """
        Override reply to match frontend expected format
        Frontend expects: {request_id: "...", payload: {errors: [], status: 200}}
        """
        payload = {
            'errors': errors or [],
            'status': status,
        }
        
        if data is not None:
            payload['data'] = data
        
        response = {
            'request_id': request_id,
            'payload': payload
        }
        
        await self.send_json(response)
    
    async def handle_action(self, action: str, request_id: str, **kwargs):
        """
        Handle action by delegating to the appropriate DRF view based on stream name
        """
        # Get the stream name from scope
        stream = self.scope.get('stream_name')
        if not stream:
            raise ValueError("stream_name not found in scope")
        
        # Get the view class path for this stream from the mapping
        view_path = self.scope.get('view_class_path')
        if not view_path:
            raise ValueError(f"No view class path mapped for stream: {stream}")
        
        # Import the view class
        module_path, class_name = view_path.rsplit('.', 1)
        module = __import__(module_path, fromlist=[class_name])
        view_class = getattr(module, class_name)
        
        # Priority mapping for actions (check methods in priority order)
        # create: POST preferred over PUT
        # update: PATCH preferred over PUT
        action_priority = {
            "create": ["POST", "PUT"],
            "retrieve": ["GET"],
            "destroy": ["DELETE"],
            "update": ["PATCH", "PUT"],
            "list": ["GET"],
        }
        
        # Filter actions to only those where view class has the corresponding HTTP method
        available_actions = {}
        for action_name, methods in action_priority.items():
            # Find the first available method in priority order
            for http_method in methods:
                method_name = http_method.lower()
                if hasattr(view_class, method_name):
                    available_actions[action_name] = http_method
                    break
        
        logger.info(f"AVAILABLE ACTIONS: {available_actions}")
        
        # Set actions on self (GenericDRFConsumer)
        self.actions = available_actions
        
        # Create a view_as_consumer for the DRF view
        # view_as_consumer returns an instance, not a class
        consumer = view_as_consumer(view_class.as_view())
        consumer.scope = self.scope
        consumer.base_send = self.base_send
        consumer.actions = self.actions
        
        # Override check_permissions on the inner consumer to pass HTTP method instead of action name
        original_check_permissions = consumer.check_permissions
        async def check_permissions_with_http_method(action: str, **kwargs):
            http_method = self.actions.get(action, action)
            for permission in await consumer.get_permissions(action=action, **kwargs):
                if not await ensure_async(permission.has_permission)(
                    scope=self.scope, consumer=consumer, action=http_method, **kwargs
                ):
                    logger.info(f"RAISE PAERMISSION DENIED: {self.scope, "http_method", http_method}")
                    raise PermissionDenied()
        consumer.check_permissions = check_permissions_with_http_method
        
        # Override handle_action on the inner consumer to add debugging
        original_handle_action = consumer.handle_action
        async def handle_action_with_debug(action: str, request_id: str, **kwargs):
            try:
                logger.info(f"[DEBUG] Starting handle_action for action={action}, request_id={request_id}")
                logger.info(f"[DEBUG] Available actions: {consumer.actions}")
                logger.info(f"[DEBUG] Action in self.actions: {action in consumer.actions}")
                
                await consumer.check_permissions(action, **kwargs)
                logger.info(f"[DEBUG] Permissions check passed")
                
                if action not in consumer.actions:
                    logger.error(f"[DEBUG] Action {action} not in available actions!")
                    raise MethodNotAllowed(method=action)
                
                logger.info(f"[DEBUG] Calling view with action={action}")
                content, status = await consumer.call_view(action=action, **kwargs)
                logger.info(f"[DEBUG] View returned status={status}")
                
                await consumer.reply(
                    action=action, request_id=request_id, data=content, status=status
                )
                logger.info(f"[DEBUG] Reply sent successfully")
                
            except Exception as exc:
                logger.error(f"[DEBUG] Exception in handle_action: {type(exc).__name__}: {exc}", exc_info=True)
                # Use consumer's handle_exception to ensure proper response format
                await consumer.handle_exception(exc, action=action, request_id=request_id)
        
        consumer.handle_action = handle_action_with_debug
        
        # Override get_view_args to extract path parameters from kwargs
        # The library expects parameters in kwargs.get("parameters"), but we also support direct kwargs
        original_get_view_args = consumer.get_view_args
        def get_view_args_with_params(action: str, **kwargs):
            # Extract parameters from the parameters dict if present
            parameters = kwargs.get("path_params", {})
            # Also check for direct path parameters in kwargs (like 'id', 'pk', etc.)
            # Remove known non-parameter keys
            known_keys = {'action', 'request_id', 'data', 'headers', 'query', 'query_params', 'path_params'}
            for key in list(kwargs.keys()):
                if key not in known_keys:
                    parameters[key] = kwargs[key]
            return [], parameters
        consumer.get_view_args = get_view_args_with_params
        
        # Override call_view with full copy of original + debugging
        from djangochannelsrestframework.consumers import request_from_scope
        from rest_framework.response import Response
        
        @database_sync_to_async
        def call_view_with_debug(action: str, **kwargs):
            logger.info(f"[DEBUG call_view] ===== START =====")
            logger.info(f"[DEBUG call_view] action={action}, kwargs={kwargs}")
            logger.info(f"[DEBUG call_view] self.scope id: {id(self.scope)}")
            logger.info(f"[DEBUG call_view] self.scope keys: {list(self.scope.keys())}")
            logger.info(f"[DEBUG call_view] self.scope type: {type(self.scope)}")
            logger.info(f"[DEBUG call_view] headers in scope: {self.scope.get('headers', 'NOT FOUND')}")
            logger.info(f"[DEBUG call_view] headers type: {type(self.scope.get('headers', None))}")
            
            # Step 1: request_from_scope
            logger.info(f"[DEBUG call_view] Calling request_from_scope...")
            try:
                request = request_from_scope(self.scope)
                logger.info(f"[DEBUG call_view] request_from_scope succeeded")
                logger.info(f"[DEBUG call_view] request.method: {getattr(request, 'method', 'N/A')}")
                logger.info(f"[DEBUG call_view] request.GET: {getattr(request, 'GET', 'N/A')}")
                logger.info(f"[DEBUG call_view] request.POST: {getattr(request, 'POST', 'N/A')}")
                logger.info(f"[DEBUG call_view] request.headers: {getattr(request, 'headers', 'N/A')}")
                
                # Add headers from scope to request if present
                # Headers were added to scope in receive_json from WebSocket payload
                scope_headers = self.scope.get('headers', [])
                if scope_headers:
                    logger.info(f"[DEBUG call_view] Adding headers from scope: {scope_headers}")
                    for header_name, header_value in scope_headers:
                        # ASGI headers are bytes, decode to string
                        header_name_str = header_name.decode('utf-8') if isinstance(header_name, bytes) else header_name
                        header_value_str = header_value.decode('utf-8') if isinstance(header_value, bytes) else header_value
                        # Convert header name to HTTP_ format for META
                        # X-User-Agent -> HTTP_USER_AGENT
                        # X-Sec-CH-Device-Memory -> HTTP_SEC_CH_DEVICE_MEMORY
                        if header_name_str.startswith('X-'):
                            # Remove X- prefix and convert to standard HTTP_ format
                            meta_key = f'HTTP_{header_name_str[2:].upper().replace("-", "_")}'
                        else:
                            meta_key = f'HTTP_{header_name_str.upper().replace("-", "_")}'
                        request.META[meta_key] = header_value_str
                    logger.info(f"[DEBUG call_view] request.META after update: {dict(request.META)}")
                
                # Add client_ip from payload if present
                # This is the real client IP obtained via WebRTC on frontend
                if 'client_ip' in kwargs:
                    client_ip = kwargs.get('client_ip')
                    # Set as HTTP_X_REAL_IP (standard nginx header format)
                    request.META['HTTP_X_REAL_IP'] = client_ip
                    # Clear X-Forwarded-For to avoid using proxy IP
                    request.META['HTTP_X_FORWARDED_FOR'] = ''
                    logger.info(f"[DEBUG call_view] Set client IP: {client_ip}")
            except Exception as e:
                logger.error(f"[DEBUG call_view] request_from_scope FAILED: {e}", exc_info=True)
                raise
            
            # Step 2: get_view_args
            logger.info(f"[DEBUG call_view] Getting view args...")
            args, view_kwargs = consumer.get_view_args(action=action, **kwargs)
            logger.info(f"[DEBUG call_view] args={args}, view_kwargs={view_kwargs}")
            
            # Step 3: set request properties
            logger.info(f"[DEBUG call_view] Setting request.method={self.actions[action]}")
            request.method = self.actions[action]
            
            # Convert data dict to JSON bytes for DRF to parse
            import json as json_module
            data_dict = kwargs.get("data", {})
            json_string = json_module.dumps(data_dict)
            json_bytes = json_string.encode('utf-8')
            
            # Parse JSON data and set it directly on request
            # This bypasses DRF's body parsing which expects a stream attribute
            parsed_data = json_module.loads(json_string)
            
            # Set the request body
            request._body = json_bytes
            
            # Set stream attribute for DRF parsers (they expect this)
            from io import BytesIO
            request.stream = BytesIO(json_bytes)
            
            # Set content type so DRF knows how to parse the body
            request.META['CONTENT_TYPE'] = 'application/json'
            request.META['CONTENT_LENGTH'] = str(len(json_bytes))
            
            # For POST requests, also set POST to QueryDict of the data
            from django.http import QueryDict
            request.POST = QueryDict('', mutable=True)
            for key, value in data_dict.items():
                if isinstance(value, list):
                    request.POST.setlist(key, value)
                else:
                    request.POST[key] = value

            # Directly set DRF's cached data to avoid re-parsing
            # DRF's request.data property will return this
            request._data = parsed_data
            request._full_data = parsed_data

            logger.info(f"[DEBUG call_view] request._body set to: {json_bytes}")
            logger.info(f"[DEBUG call_view] request.POST set to: {dict(request.POST)}")
            logger.info(f"[DEBUG call_view] request.META CONTENT_TYPE: {request.META.get('CONTENT_TYPE')}")
            logger.info(f"[DEBUG call_view] request.META CONTENT_LENGTH: {request.META.get('CONTENT_LENGTH')}")
            
            # Step 4: set query params
            logger.info(f"[DEBUG call_view] Setting query params...")
            for key, value in kwargs.get("query", {}).items():
                if isinstance(value, list):
                    request.GET.setlist(key, value)
                else:
                    request.GET[key] = value
            logger.info(f"[DEBUG call_view] request.GET after: {dict(request.GET)}")
            
            # Step 5: get view
            logger.info(f"[DEBUG call_view] Getting view class...")
            view = getattr(consumer.__class__, 'view', None)
            logger.info(f"[DEBUG call_view] view: {view}")
            
            # Step 6: call view
            logger.info(f"[DEBUG call_view] Calling view...")
            try:
                response = view(request, *args, **view_kwargs)
                logger.info(f"[DEBUG call_view] view returned successfully")
                logger.info(f"[DEBUG call_view] response type: {type(response)}")
                logger.info(f"[DEBUG call_view] response status_code: {getattr(response, 'status_code', 'N/A')}")
            except Exception as e:
                logger.error(f"[DEBUG call_view] view call FAILED: {e}", exc_info=True)
                raise
            
            # Step 7: process response
            status = response.status_code
            logger.info(f"[DEBUG call_view] Processing response, status={status}")
            
            if isinstance(response, Response):
                logger.info(f"[DEBUG call_view] Response is DRF Response")
                data = response.data
                logger.info(f"[DEBUG call_view] Returning data from Response")
                return data, status
            
            # For non-DRF responses, render if needed and return content
            if hasattr(response, 'render') and not response.is_rendered:
                response.render()
            
            response_content = response.content
            if isinstance(response_content, bytes):
                try:
                    response_content = response_content.decode("utf-8")
                except Exception as e:
                    response_content = response_content.hex()
            
            logger.info(f"[DEBUG call_view] ===== END SUCCESS =====")
            return response_content, status
        
        consumer.call_view = call_view_with_debug
        
        # Call the consumer's handle_action
        await consumer.handle_action(action, request_id, **kwargs)
        return


class Chat(AsyncJsonWebsocketConsumer):

    # Map stream names to DRF view class paths (as strings)
    export_consumers = {
        "message:create": "api.views.MessageCreate",
        "message:retrieve": "api.views.MessageView",
        "message:destroy": "api.views.MessageDelete",
        "message:update": "api.views.MessageUpdate",
        "message:shoutbox": "api.views.ShoutBox",
    }

    async def connect(self):
        print("=" * 50)
        print("WEBSOCKET CONNECTION ATTEMPT")
        print("=" * 50)
        logger.info("WebSocket connection attempt")
        await self.accept()
        print("WEBSOCKET CONNECTION ACCEPTED")
        logger.info("WebSocket connection accepted")
        
        # Send a test message to confirm connection
        await self.send_json({
            'type': 'connection.established',
            'message': 'WebSocket connected successfully'
        })

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected with code: {close_code}")

    async def receive_json(self, content, **kwargs):
        """
        Handle incoming JSON messages from WebSocket
        The frontend sends: {stream: "message:create", payload: {action, request_id, data, ...}}
        We need to extract and forward to djangochannelsrestframework
        """
        print("=" * 50)
        print("RECEIVE_JSON CALLED!")
        print(f"Content type: {type(content)}")
        print(f"Content: {content}")
        print("=" * 50)
        logger.info(f"Received JSON: {content}")
        
        # Extract from frontend format
        stream = content.get('stream')
        payload = content.get('payload', {})
        request_id = payload.get('request_id')
        
        print(f"Processing stream: {stream}, request_id: {request_id}")
        logger.info(f"Processing stream: {stream}, request_id: {request_id}")
        
        try:
            # Check if we have a consumer for this streamа
            if stream in self.export_consumers:
                view_class_path = self.export_consumers[stream]
                logger.info(f"Routing to view: {view_class_path}")
                # Create an instance of the generic DRF consumer
                consumer = GenericDRFConsumer()
                
                # Set the scope with stream name and view class path
                consumer.scope = self.scope
                consumer.scope['stream_name'] = stream
                consumer.scope['view_class_path'] = view_class_path
                
                # Add headers from payload to scope if present
                # ASGI spec requires headers as list of tuples with bytes: [(b'header-name', b'value'), ...]
                if 'headers' in payload:
                    headers_dict = payload.get('headers', {})
                    headers_list = []
                    for key, value in headers_dict.items():
                        # Convert string keys/values to bytes as required by ASGI spec
                        header_name = key.encode('utf-8') if isinstance(key, str) else key
                        header_value = value.encode('utf-8') if isinstance(value, str) else value
                        headers_list.append((header_name, header_value))

                    logger.info(f"NATIVE HEADERS: {self.scope.get('headers', [])}")
                    headers_list.extend(self.scope.get('headers', []))
                    consumer.scope['headers'] = headers_list

                
                # Set base_send to enable the consumer to send responses back
                consumer.base_send = self.base_send
                
                # Prepare the message in djangochannelsrestframework format
                # The consumer expects: {action: "create", request_id: "...", data: {...}, ...}
                dcrf_message = {
                    'action': payload.get('action'),
                    'request_id': request_id,
                }
                
                # Add data if present
                if 'data' in payload:
                    dcrf_message['data'] = payload.get('data')
                
                # Add headers if present
                if 'headers' in payload:
                    dcrf_message['headers'] = payload.get('headers')
                
                # Add path parameters (like id for update/destroy)
                if 'id' in payload:
                    dcrf_message['id'] = payload.get('id')
                
                # Add path_params dict if present (for multiple parameters)
                if 'path_params' in payload:
                    dcrf_message['path_params'] = payload.get('path_params')
                
                # Add query params if present
                if 'query_params' in payload:
                    dcrf_message['query'] = payload.get('query_params')
                
                print(f"Calling consumer with message: {dcrf_message}")
                logger.info(f"Calling consumer with message: {dcrf_message}")
                
                # Call the consumer's receive_json method
                logger.info(f"SCOPE: {consumer.scope}")
                await consumer.receive_json(dcrf_message)
                
                logger.info(f"Consumer receive_json completed")
            else:
                logger.warning(f"No consumer found for stream: {stream}")
                await self.send(text_data=json.dumps({
                    'request_id': request_id,
                    'payload': {
                        'errors': f'Unknown stream: {stream}',
                        'status': 400
                    }
                }))
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            await self.send(text_data=json.dumps({
                'request_id': request_id,
                'payload': {
                    'errors': str(e),
                    'status': 500
                }
            }))