# import json

# data_to_send = (None, None)
# data_bytes = json.dumps(data_to_send)

# print(data_bytes.encode('utf-8'))

# received_data = data_bytes

# received_tuple = json.loads(received_data)
# print(f"Received tuple: {received_tuple}")

import struct

data_to_send = (1, -2)
data_bytes = struct.pack('!hh', *data_to_send)

print(data_bytes)

received_tuple = struct.unpack('!hh', data_bytes)
print(f"Received tuple: {received_tuple}")
