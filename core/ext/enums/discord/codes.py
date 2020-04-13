gateway_opcodes = {
    0:	{'Dispatch': 'dispatches an event'},
    1:	{'Heartbeat': 'used for ping checking'},
    2:	{'Identify': 'used for client handshake'},
    3:	{'Status Update': 'used to update the client status'},
    4:	{'Voice State Update': 'used to join/move/leave voice channels'},
    6:	{'Resume': 'used to resume a closed connection'},
    7:	{'Reconnect': 'used to tell clients to reconnect to the gateway'},
    8:	{'Request Guild Members': 'used to request guild members'},
    9:	{'Invalid Session': 'used to notify client they have an invalid session id'},
    10:	{'Hello': 'sent immediately after connecting, contains heartbeat and server debug information'},
    11:	{'Heartbeat ACK': 'sent immediately following a client heartbeat that was received'}
}

gateway_close_event_codes = {
    4000:	'unknown error',
    4001:	'unknown opcode',
    4002:	'decode error',
    4003:	'not authenticated',
    4004:	'authentication failed',
    4005:	'already authenticated',
    4007:	'invalid seq',
    4008:	'rate limited',
    4009:	'session timeout',
    4010:	'invalid shard',
    4011:	'sharding required'
}

voice_opcodes = {
    0:	{'Identify': 'begin a voice websocket connection'},
    1:	{'Select Protocol': 'select the voice protocol'},
    2:	{'Ready': 'complete the websocket handshake'},
    3:	{'Heartbeat': 'keep the websocket connection alive'},
    4:	{'Session Description': 'describe the session'},
    5:	{'Speaking': 'indicate which users are speaking'},
    6:	{'Heartbeat ACK': 'sent immediately following a received client heartbeat'},
    7:	{'Resume': 'resume a connection'},
    8:	{'Hello': 'the continuous interval in milliseconds after which the client should send a heartbeat'},
    9:	{'Resumed': 'acknowledge Resume'},
    13:	{'Client Disconnect': 'a client has disconnected from the voice channel'}
}

voice_close_event_codes = {
    4001:	'Unknown opcode',
    4003:	'Not authenticated',
    4004:	'Authentication failed',
    4005:	'Already authenticated',
    4006:	'Session no longer valid',
    4009:	'Session timeout',
    4011:	'Server not found',
    4012:	'Unknown Protocol',
    4014:	'Disconnected',
    4015:	'Voice server crashed',
    4016:	'Unknown Encryption Mode'
}

http = {  # FULL HTTP STATUS CODE LIST. Ones that have descriptions are most likely used by Discord.
    # 1xx Informational
    100: {'CONTINUE': ''},
    101: {'SWITCHING PROTOCOLS': ''},
    102: {'PROCESSING': 'WebDAV'},
    # 2xx Success
    200: {'OK': 'The request completed successfully'},
    201: {'CREATED': 'The entity was created successfully'},
    202: {'ACCEPTED': ''},
    203: {'NON-AUTHORITATIVE INFORMATION': ''},
    204: {'NO CONTENT':	'The request completed successfully but returned no content'},
    205: {'RESET CONTENT': ''},
    206: {'PARTIAL CONTENT': ''},
    207: {'MULTI-STATUS': 'WebDAV'},
    208: {'ALREADY REPORTED': 'WebDAV'},
    226: {'IM USED': ''},
    # 3xx Redirection
    300: {'MULTIPLE CHOICES': ''},
    301: {'MOVED PERMANENTLY': ''},
    302: {'FOUND': ''},
    303: {'SEE OTHER': ''},
    304: {'NOT MODIFIED': 'The entity was not modified (no action was taken)'},
    305: {'USE PROXY': ''},
    306: {'(UNUSED)': ''},
    307: {'TEMPORARY REDIRECT': ''},
    308: {'PERMANENT REDIRECT': '(experimental)'},
    # 4xx Client Error
    400: {'BAD REQUEST': 'The request was improperly formatted, or the server couldn\'t understand it'},
    401: {'UNAUTHORIZED': 'The Authorization header was missing or invalid'},
    402: {'PAYMENT REQUIRED': ''},
    403: {'FORBIDDEN': 'The Authorization token you passed did not have permission to the resource'},
    404: {'NOT FOUND': 'The resource at the location specified doesn\'t exist'},
    405: {'METHOD NOT ALLOWED': 'The HTTP method used is not valid for the location specified'},
    406: {'NOT ACCEPTABLE': ''},
    407: {'PROXY AUTHENTICATION REQUIRED': ''},
    408: {'REQUEST TIMEOUT': ''},
    409: {'CONFLICT': ''},
    410: {'GONE': ''},
    411: {'LENGTH REQUIRED': ''},
    412: {'PRECONDITION FAILED': ''},
    413: {'REQUEST ENTITY TOO LARGE': ''},
    414: {'REQUEST-URI TOO LONG': ''},
    415: {'UNSUPPORTED MEDIA TYPE': ''},
    416: {'REQUESTED RANGE NOT SATISFIABLE': ''},
    417: {'EXPECTATION FAILED': ''},
    418: {'I\'M A TEAPOT': 'RFC 2324'},
    420: {'ENHANCE YOUR CALM': 'Twitter'},
    422: {'UNPROCESSABLE ENTITY': 'WebDAV'},
    423: {'LOCKED': 'WebDAV'},
    424: {'FAILED DEPENDENCY': 'WebDAV'},
    426: {'UPGRADE REQUIRED': ''},
    428: {'PRECONDITION REQUIRED': ''},
    429: {'TOO MANY REQUESTS': 'You\'ve made too many requests, see Rate Limits'},
    431: {'REQUEST HEADER FIELDS TOO LARGE': ''},
    444: {'NO RESPONSE': 'Nginx'},
    449: {'RETRY WITH': 'Microsoft'},
    451: {'UNAVAILABLE FOR LEGAL RESASONS': ''},
    499: {'CLIENT CLOSED REQUEST': 'Nginx'},
    # 5xx Server Error
    502: {'GATEWAY UNAVAILABLE': 'There was not a gateway available to process your request. Wait a bit and retry'},
    '5xx': {'SERVER ERROR': 'The server had an error processing your request (these are rare)'},
    500: {'INTERNAL SERVER ERROR': ''},
    501: {'NOT IMPLEMENTED': ''},
    503: {'SERVICE UNAVAILABLE': ''},
    504: {'GATEWAY TIMEOUT': ''},
    505: {'HTTP VERSION NOT SUPPORTED': ''},
    506: {'VARIANT ALSO NEGOTIATES': '(experimental)'},
    507: {'INSUFFICIENT STORAGE': 'WebDAV'},
    508: {'LOOP DETECTED': 'WebDAV'},
    509: {'BANDWIDTH LIMIT EXCEEDED': 'Apache'},
    510: {'NOT EXTENDED': ''},
    511: {'NETWORK AUTHENTICATION REQUIRED': ''},
    598: {'NETWORK READ TIMEOUT ERROR': ''},
    599: {'NETWORK CONNECT TIMEOUT ERROR': ''}
}

json = {
    10001:  'Unknown account',
    10002:  'Unknown application',
    10003:  'Unknown channel',
    10004:  'Unknown guild',
    10005:  'Unknown integration',
    10006:  'Unknown invite',
    10007:  'Unknown member',
    10008:  'Unknown message',
    10009:	'Unknown overwrite',
    10010:	'Unknown provider',
    10011:	'Unknown role',
    10012:	'Unknown token',
    10013:	'Unknown user',
    10014:	'Unknown Emoji',
    10015:	'Unknown Webhook',
    20001:	'Bots cannot use this endpoint',
    20002:	'Only bots can use this endpoint',
    30001:	'Maximum number of guilds reached (100)',
    30002:	'Maximum number of friends reached (1000)',
    30003:	'Maximum number of pins reached (50)',
    30005:	'Maximum number of guild roles reached (250)',
    30010:	'Maximum number of reactions reached (20)',
    30013:	'Maximum number of guild channels reached (500)',
    30016:	'Maximum number of invites reached (1000)',
    40001:	'Unauthorized',
    50001:	'Missing access',
    50002:	'Invalid account type',
    50003:	'Cannot execute action on a DM channel',
    50004:	'Widget Disabled',
    50005:	'Cannot edit a message authored by another user',
    50006:	'Cannot send an empty message',
    50007:	'Cannot send messages to this user',
    50008:	'Cannot send messages in a voice channel',
    50009:	'Channel verification level is too high',
    50010:	'OAuth2 application does not have a bot',
    50011:	'OAuth2 application limit reached',
    50012:	'Invalid OAuth state',
    50013:	'Missing permissions',
    50014:	'Invalid authentication token',
    50015:	'Note is too long',
    50016:	'Provided too few or too many messages to delete. Must provide at least 2 and fewer than 100 messages to delete.',
    50019:	'A message can only be pinned to the channel it was sent in',
    50020:	'Invite code is either invalid or taken.',
    50021:	'Cannot execute action on a system message',
    50025:	'Invalid OAuth2 access token',
    50034:	'A message provided was too old to bulk delete',
    50035:	'Invalid Form Body',
    50036:	'An invite was accepted to a guild the application\'s bot is not in',
    50041:	'Invalid API version',
    90001:	'Reaction blocked',
    130000:	'Resource overloaded'
}

rpc = {
    1000: {'Unknown Error': 'sent when an unknown error occurred'},
    4000: {'Invalid Payload': 'sent when an invalid payload is received'},
    4002: {'Invalid Command': 'sent when the command name specified is invalid'},
    4003: {'Invalid Guild': 'sent when the guild id specified is invalid'},
    4004: {'Invalid Event': 'sent when the event name specified is invalid'},
    4005: {'Invalid Channel': 'sent when the channel id specified is invalid'},
    4006: {'Invalid Permissions': 'sent when the user doesn\'t have the permission required to access the requested resource'},
    4007: {'Invalid Client ID': 'sent when an invalid OAuth2 application ID is used to authorize or authenticate with'},
    4008: {'Invalid Origin': 'sent when an invalid OAuth2 application origin is used to authorize or authenticate with'},
    4009: {'Invalid Token': 'sent when an invalid OAuth2 token is used to authorize or authenticate with'},
    4010: {'Invalid User': 'sent when the user id specified is invalid'},
    5000: {'OAuth2 Error': 'sent when a standard OAuth2 error occurred; check the data object for the OAuth 2 error information'},
    5001: {'Select Channel Timed Out': 'sent when an asynchronous SELECT_TEXT_CHANNEL/SELECT_VOICE_CHANNEL command times out'},
    5002: {'Get Guild Timed Out': 'sent when an asynchronous GET_GUILD command times out'},
    5003: {'Select Voice Force Required': 'sent when you try to join a user to a voice channel but the user is already in one'},
    5004: {'Capture Shortcut Already Listening': 'sent when you try to capture a shortcut key when already capturing one'}
}

rpc_close_event_codes = {
    4000: {'Invalid Client ID': 'sent when you connect to the RPC server with an invalid client ID'},
    4001: {'Invalid Origin': 'sent when you connect to the RPC server with an invalid origin'},
    4002: {'Ratelimited': 'sent when the RPC Server rejects your connection to a ratelimit'},
    4003: {'Token Revoke': 'sent when the OAuth2 token associated with a connection is revoked'},
    4004: {'Invalid Version': 'sent when the RPC Server version specified in the connection string is not valid'},
    4005: {'Invalid Encoding': 'sent when the encoding specified in the connection string is not valid'}
}













