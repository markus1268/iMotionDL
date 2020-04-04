firmware_cmd = []
parameter_cmd = []
script_cmd = []
parse_mode = 0

with open("test\huayi.ldf", "r") as f:
    for line in f:
        if line[0] == '%':
            if '%:Firmware Data Section Begin' in line:
                parse_mode = 0
            elif '%:Parameters Data Section Begin' in line:
                parse_mode = 1
            elif '%:Script Data Section Begin' in line:
                parse_mode = 2
        elif line[0] == '#':
            pass
        elif line[0] == '\n':
            pass
        else:
            if parse_mode == 0:
                firmware_cmd.append(bytes.fromhex(line))
            elif parse_mode == 1:
                parameter_cmd.append(bytes.fromhex(line))
            elif parse_mode == 2:
                script_cmd.append(bytes.fromhex(line))
print('Firmware Data: {}'.format(len(firmware_cmd)))
print('Parameter Data: {}'.format(len(parameter_cmd)))
for i in parameter_cmd:
    print(i.hex(' '))
print('Script Data: {}'.format(len(script_cmd)))
for i in script_cmd:
    print(i.hex(' '))
