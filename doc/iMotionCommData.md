# iMotion Command Protocol for Device Programming
**Application Mode (MCE Protocol)**
In the application mode, after reset the device will send 'FF' and enter MCE protocol.

MCE Protocol
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
Recv : 20 --> INS ack
Recv : STA1 STA2

Flash Load Check Signature
Send : A0 21 00 00 00
Recv : STA1 STA2

**Config Mode**

Connect (autobaurate command)
Send : 00 6C
Recv : CD

Reset (it takes 100ms to reset)
Send : A0 00 00 00 00
Recv : 90 00

Get Status
Send : A0 10 00 00 23
Recv : 10 --> INS ack
Recv : 43 4F 4E 46 C0 0C 05 00 01 11 80 40 00 0A 00 15 00 01 C1 0F 01 FF FF FF FF FF FF FF FF FF FF FF FF FF FF
Recv : 90 00 --> Status bytes

Get Parameter Set Name
Send : A0 11 Page 00 13
Recv : 11 --> INS ack
Recv : 50 41 52 53 C2 0D 00 01 5F 01 00 48 55 41 59 49 5F 35 6B
Recv : 90 00

Get Parameter Set Value
Send : A0 12 Page 00 00
Recv : 12 --> INS ack
Recv : 50 41 52 56 C3 BE 00 01 5F 30 00 00 00 00 00 20 01 CF 01 8F 0B DA 03 34 0C E8 03 00 00 00 00 60 00 AF 04 32 00 00 00 E8 03 E8 03 00 00 00 00 00 00 00 10 64 00 3F 00 0C 00 00 10 CD 00 E9 13 CC 0C 00 12 BF 01 E9 13 6F 0A 07 14 F0 00 C0 12 C8 00 10 00 06 03 00 40 A7 0D D7 01 0B 00 72 2C 14 2E AB 2A 80 00 1F 0F 90 07 38 07 DA 03 A0 23 20 00 33 03 D4 10 41 01 09 03 00 10 1C 07 D9 04 D9 04 00 00 00 00 00 00 08 00 01 00 02 00 84 00 78 00 48 71 00 08 88 13 70 17 03 00 03 64 00 00 00 00 00 00 55 55 48 01 DA 00 C0 00 00 08 3E 05 40 00 04 00 33 03 E8 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Recv : 90 00

Change Boot mode
Send : A0 18 mode ~mode 00
Recv : 90 00
mode ~mode:
Boot Loader mode : 5D A2
Config mode : CD 32

Application mode : AD 52
Send : A0 18 AD 52 00
Recv : 90 00
Recv : FF

Failsafe mode : AF 50

Download Parameter
Send : A0 20 Page 01 Lc nData
Recv : 20 --> INS ack
Recv : 90 00

Check Parameter
Send : A0 21 Page 01 00 
Recv : 90 00

Clear Parameter
Send : A0 22 Page 01 00
Recv : 90 00

**Jcom Protocol**
Jcom Message Frame Structure:
| Flag | Seq | Res | MO | Data[0] | Data[1] | Data[2] | Data[3] | CRC |
|------|-----|-----|----|---------|---------|---------|---------|-----|
| 7E   |     |     |    |         |         |         |         |     |

Flag (1 byte)    : 7E
Seq (2 bit)      : sequence number
Res (2 bit)      : Reserved
MO (4 bit)       : Message Object
Data[x] (1 byte) : Message Data field / message payload
CRC (1 byte)     : CRC calculated over Message fields (Message Object & Message Data field)

