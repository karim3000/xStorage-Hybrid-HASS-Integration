from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
from pymodbus.framer import FramerType

HOST = "192.168.40.70"   # You can override this dynamically if needed
PORT = 8899
UNIT = 1
READ_REGISTER = 3078

def read_register_sync(register: int) -> int:
    client = ModbusTcpClient(HOST, port=PORT, framer=FramerType.SOCKET)

    if not client.connect():
        print(f"Failed to connect to {HOST}:{PORT}")
        return

    print(f"Connected to {HOST}:{PORT}")

    try:
        # 3) READ a register
        print(f"Reading register {READ_REGISTER}...")
        rr3 = client.read_input_registers(READ_REGISTER, count=1, device_id=UNIT)
        if rr3.isError():
            print("Read failed:", rr3)
        else:
            print("Read value:", rr3.registers[0])

    except ModbusException as e:
        print("Modbus error:", e)

    finally:
        client.close()
        print("Connection closed.")


    return rr3.registers[0]

def write_register_sync(register: int, value: int) -> None:
    client = ModbusTcpClient(HOST, port=PORT, framer=FramerType.SOCKET)

    if not client.connect():
        print(f"Failed to connect to {HOST}:{PORT}")
        return

    print(f"Connected to {HOST}:{PORT}")

    try:
        # 1) WRITE value 1 to first register
        print(f"Writing 1 to register {register}...")
        rr1 = client.write_register(register, value=value, device_id=UNIT)
        if rr1.isError():
            print("Write 1 failed:", rr1)
        else:
            print("Write 1 OK")

    except ModbusException as e:
        print("Modbus error:", e)

    finally:
        client.close()
        print("Connection closed.")