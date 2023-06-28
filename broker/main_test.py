import pytest
from main import parseHandshakeProtocol, validadeWSHandshakeHeaders, generateWSAcceptanceHeader

def test_parseHandshakeProtocol():
    handshake_string = str(b"GET / HTTP/1.1\r\nHost: 127.0.0.1:65000\r\nConnection: Upgrade\r\nUpgrade: websocket\r\nSec-WebSocket-Version: 13\r\nSec-WebSocket-Key: PDqBCFQgl2m2gYn8Vtk3JQ==\r\nSec-WebSocket-Extensions: permessage-deflate;\r\n")

    handshake_headers = parseHandshakeProtocol(handshake_string)
    assert handshake_headers['Host'] == "127.0.0.1:65000"
    assert handshake_headers['Connection'] == "Upgrade"
    assert handshake_headers['Upgrade'] == "websocket"
    assert handshake_headers['Sec-WebSocket-Version'] == "13"
    assert handshake_headers['Sec-WebSocket-Key'] == "PDqBCFQgl2m2gYn8Vtk3JQ=="
    assert handshake_headers['Sec-WebSocket-Extensions'] == "permessage-deflate;"

def test_validadeWSHandshakeHeaders_success():
    handshake_headers = {
        "Connection": "Upgrade",
        "Upgrade" : "websocket",
        "Sec-WebSocket-Key" : "PDqBCFQgl2m2gYn8Vtk3JQ==",
    }

    validadeWSHandshakeHeaders(handshake_headers)

def test_validadeWSHandshakeHeaders_connectionFailure():
    handshake_headers = {
        "Connection": "",
        "Upgrade" : "websocket",
        "Sec-WebSocket-Key" : "PDqBCFQgl2m2gYn8Vtk3JQ==",
    }
    
    with pytest.raises(Exception):
        validadeWSHandshakeHeaders(handshake_headers)

def test_validadeWSHandshakeHeaders_upgradeFailure():
    handshake_headers = {
        "Connection": "Upgrade",
        "Upgrade" : "",
        "Sec-WebSocket-Key" : "PDqBCFQgl2m2gYn8Vtk3JQ==",
    }

    with pytest.raises(Exception):
        validadeWSHandshakeHeaders(handshake_headers)

def test_validadeWSHandshakeHeaders_keyFailure():
    handshake_headers = {
        "Connection": "Upgrade",
        "Upgrade" : "websocket",
        "Sec-WebSocket-Key" : "",
    }

    with pytest.raises(Exception):
        validadeWSHandshakeHeaders(handshake_headers)

def test_generateWSAcceptanceHeader_emptyKey():
    key = ""
    acceptance_key = generateWSAcceptanceHeader(key)
    assert acceptance_key == "MjlmODdkNDA4YjBjNTU5NzI1ZWIxMTBmNjMxM2M3Y2Q2ZjEyNjdjYw=="

def test_generateWSAcceptanceHeader_randomKey():
    key = "PDqBCFQgl2m2gYn8Vtk3JQ=="
    acceptance_key = generateWSAcceptanceHeader(key)
    assert acceptance_key == "ZWIxZmExZTU2MmRmMjI0MmQ2MmQ5ODFhYmEwZDEzYzg4MjA1YjlhYw=="