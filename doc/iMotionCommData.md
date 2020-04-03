**Application Mode (Jcom Communication)**
In the application mode, after reset the device will send 'FF' and enter Jcom mode.

Jcom Message Frame Structure:
| Flag | Seq | Res |                Message                     |CRC|
|------|-----|-----|--------------------------------------------|---|
|      |     |     | MO | Data[0] | Data[1] | Data[2] | Data[3] |   |
|------|-----|-----|----|---------|---------|---------|---------|---|
| 7E   |     |     |    |         |         |         |         |   |

Flag (1 byte)    : 7E
Seq (2 bit)      : sequence number
Res (2 bit)      : Reserved
MO (4 bit)       : Message Object
Data[x] (1 byte) : Data field / message payload
CRC (1 byte)     : CRC calculated over Message fields

Checking Communication:
Send:
7E 13 7E 13
Recv:
7E 17 7E 17
or
7E 1B 7E 1B

Change Mode to SBSL mode:
Send:
7E 02 80 31 51 81 10 FA F8 7E 87
Recv:
FE

Change Mode to Config mode:
Send:
7E 02 80 38 51 82 10 32 CD 7E 9C
Recv:
7E 01 7E 01

**Catch at Startup Method for changing the boot mode:**
Send: 00 with baudrate 57600, it's equal to sending low pulse on Rx for 155uS at power up.
Recv: 06

**Loader Command Set**
Loader Protocol:
Send Command Header:
| CLA | INS | P1 | P2 | Lx |
|-----|-----|----|----|----|

CLA : Class byte
INS : Instruction byte
P1  : Parameter byte 1
P2  : Parameter byte 2
Lx  : Number of data bytes sent (Lc) or expected (Le)

Receive Command Header Ack when Lx != 0 :
| INS |
|-----|

Send Data Lc bytes (optional, write command):
| Data[0] | ... | Data[Lc-1] |
|---------|-----|------------|

Receive Data Le bytes (optional, read command)
| Optional Le response data | STA1 | STA2 |
|---------------------------|------|------|

STA1 : Status Byte 1
STA2 : Status Byte 2

If the loader requires more time, it sends one or more 'Waiting Time Extension Requests' (60)

**Secure Bootstrap Loader Mode (SBSL)**

Standard baudrate mode (After reset, must send this command for baudrate negotiation)
Send : 00 6C
Recv : 5D

Enhanced baudrate mode
Send : 00 93
Recv : A2 <MSB of PDIV> <LSB of PDIV)
Send : <LSB of 'STEP'> <MSB of 'STEP'>
Recv : F0
Send : F0

Reset (it takes 100ms to reset)
Send : A0 00 00 00 00
Recv : 90 00

Flash Get SBSL Status (If command succesful the flash will be erased)
Send : A0 10 00 00 27
Recv : 10 --> INS ACK 
Recv : 53 42 53 4C C0 04 06 70 30 01 C1 03 00 00 00 C2 04 10 03 00 10 C3 10 02 27 0F 1F CC DF 57 C3 33 D3 1A BD 78 F9 60 B0 
Recv : 90 00 --> Status bytes

Flash Load Data
Send : A0 20 00 00 Lc nData
Recv : STA1 STA2

Flash Load Check Signature
Send : A0 21 00 00 00
Recv : STA1 STA2

**Config Mode**

Connect
Send : 00 6C
Recv : CD

Reset (it takes 100ms to reset)
Send : A0 00 00 00 00
Recv : 90 00

Get Status
Send : A0 10 00 00 1F
Recv : 10 --> INS ack
Recv : 
Recv : 90 00 --> Status bytes

Get Parameter Set Name
Send : A0 11 Page 00 13
Recv :
Recv :
Recv : 90 00

Get Parameter Set Value
Send : A0 12 Page 00 00
Recv : rParvStatus
Recv : 90 00

Change Boot mode
Send : A0 18 mode ~mode 00
Recv : 90 00
mode ~mode:
Boot Loader mode : 5D A2
Config mode : CD 32
Application mode : AD 52
Failsafe mode : AF 50

Download Parameter
Send : A0 20 Page 00 Lc nData
Recv : 90 00

Check Parameter
Send : A0 21 Page 00 00 
Recv : 90 00

Clear Parameter
Send : A0 22 Page 00 00
Recv : 90 00


