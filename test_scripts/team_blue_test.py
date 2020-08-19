import requests, json
import signal

ports = {
    'Blue'   : [40001, 40002, 40003],
    'Yellow' : [30001, 30002, 30003]
}

next_mode = {
    'spinning'  : 'circling',
    'circling' : 'circling',
    'forward'  : 'backward',
    'backward' : 'spinning',
}

local = 'http://localhost'

def run_control_test(team = 'Blue', ports = ports):
    mode = 'forward'
    def change_mode(signum, frame):
        nonlocal mode
        mode = next_mode[mode]
        signal.alarm(2)
    
    signal.signal(signal.SIGALRM, change_mode)
    signal.alarm(4)

    while True:
        for port in ports[team]:
            url = local + ":" + str(port)
            vel1, vel2 = (0, 0)
            if mode == 'spinning':
                vel1, vel2 = (-10, 10)
            elif mode == 'circling':
                vel1, vel2 = (8, 5)
            elif mode == 'forward':
                vel1, vel2 = (2.5, 2.5)
            elif mode == 'backward':
                vel1, vel2 = (-2.5, -2.5)
            request = {
                'method'  : 'move',
                'params'  : [vel1, vel2],
                'jsonrpc' : '2.0',
                'id'      : 0
            }
            requests.post(url, json=request).json()