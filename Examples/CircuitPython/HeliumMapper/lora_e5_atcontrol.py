import time

class E5_ATControl:
    def __init__(self, uart):
        self.cmd = ""
        self.response = ""
        self._uart = uart
        
    def send_atcommand(self, cmd, expected_response, timeout = 0.1):
        # Clear the uart buffer and send the command if not none.
        if cmd != None:
            self.cmd = cmd
            self._uart.read()
            self._uart.write(bytes(cmd, "utf-8"));
    
        self.response = ""
        response_found = False
        
        stamp = time.monotonic()
        while (time.monotonic() - stamp) < timeout:
            if self._uart.in_waiting:
                data_bytes = self._uart.read(1)
                self.response += "".join([chr(b) for b in data_bytes])
                
                # If expected response is None, simply wait until timeout.
                if expected_response == None:
                    response_found = True
                
                elif expected_response in self.response:
                    response_found = True
                    break
                
        return response_found
