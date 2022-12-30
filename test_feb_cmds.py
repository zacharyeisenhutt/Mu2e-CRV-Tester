"""Tests for CRV FEB that can be done with just a bare board."""
import pytest
import sockexpect
import re
import time 
from warnings import warn
biaslist = [br'Bias_0',br'Bias_1',br'Bias_2',br'Bias_3',br'Bias_4',br'Bias_5',br'Bias_6',br'Bias_7']
N_SIPM = 64
N_HISTO_BINS = 512
HISTO_CONTROL = 0x10
HISTO_COUNT_INTERVAL = 0x11 
HISTO_POINTER_AFE0 = 0x14 
HISTO_POINTER_AFE1 = 0x15 
HISTO_PORT_AFE0 = 0x16 
HISTO_PORT_AFE1 = 0x17 
HISTO_CONTROL_ALL = 0x311 
CSR = 0x00 

@pytest.fixture(scope="session")
def feb_connection():
    """Make a test fixture for pytest to reuse the same feb_connnection
    for all tests."""
    # pylint: disable=import-outside-toplevel
    sock = make_feb_socket()
    yield sock
    sock.close()

def make_feb_socket():
    """Make connection to the FEB.
    Assumes that FEB has address 172.16.10.10 and port 5002.
    """
    import socket
    ip, port = ('172.16.10.10', 5002)
    sock = socket.socket()
    sock.connect((ip, port))
    sock.settimeout(3.0)
    return sock

def test_ID(feb_connection): # pylint: disable=redefined-outer-name
    s = sockexpect.SockExpect(feb_connection)
    s.send(b'ID\r\n')
    s.expect(br'Serial Number.*\n')
    print(s.before)
    print(s.after)
    match = re.search( br'uC ECC ReBoots : 0\r\n', s.before)
    assert match != None, "Failed 0 uB ECC ReBoots test"
    match = re.search( br'FPGA ECC Errors: 0\r\n', s.before)
    assert match != None, "Failed 0 FPGA ECC Errors test"
    

def test_ADC(feb_connection): # pylint: disable=redefined-outer-name
    s = sockexpect.SockExpect(feb_connection)
    s.send(b'ADC\r\n')
    s.expect(br'1.2v_Pos *')
    print("Before: " + repr(s.before))
    print("Match: " + repr(s.match))
    print("data: " + repr(s.data))
    s.expect(br'-*[0-9.]+')
    print("Before: " + repr(s.before))
    print("Match: " + repr(s.match))
    v = float(s.match.group(0))
    # TODO: compare v to expected values 1.2
    # TODO: repeat above for 1.8v_Pos, etc.....
    print(" *** The voltage is """, v, " !!!!")
    print("data: " + repr(s.data))
    s.expect(br'Temp_C.*\n')
    print("Before: " + repr(s.before))
    print("Match: " + repr(s.match))
    print("data: " + repr(s.data))
    s.data.clear()

def test_SD(feb_connection):
    s = sockexpect.SockExpect(feb_connection)
    feb_connection.settimeout(45.0) # FIXME! Change to 45 s
    nfailures = 0
    for ifpga in range(1,5):
        s.before.clear()
        s.data.clear()
        s.sendline(bytes(f'SD {ifpga}', 'ascii'))
        s.expect(br'Test.*\n')
        print(f'SD {ifpga}: Before: {s.before}, Data: {s.data}')
        if b'Tested Okay' not in s.data:
            warn(f'FPGA {ifpga} failed SD test')
            nfailures += 1
    assert nfailures == 0
    
def test_fs(feb_connection):
    s= sockexpect.SockExpect(feb_connection)
    s.send(b'FS\r\n')
    FSlist = [br"FlashMan :",br"FlashDev :",br"Flash FPGA ByteCnt", br"Flash FPGA SumCheck"]
    FSvaluelist = [b"01",b"7e0201",b"802570",b"9C4A"]
    writelist = ["This is the FlashMan value","This is the FlashDev value",
    "This is the Flash FPGA Byte Cnt value","This is the Flash FPGA SumCheck value"]
    for i in range(len(FSvaluelist)):
        s.expect(FSlist[i])
        s.expect(br'-*[0-9.a-zA-Z]+')
        FSval=(s.match.group(0))
        w=writelist[i]
        print(" ****", w, FSval," !!!!")
        assert FSval==FSvaluelist[i]

def test_set(feb_connection):
    s=sockexpect.SockExpect(feb_connection)
    s.send(b'SET\r\n')
    setlist=[br'LOCAL IP ADDR :',br'G/W IP ADDR   :',br'SUBNET MASK   :',
    br'MAC ADDRESS   :',br'Telnet Port 0 :',br'Telnet Port 1 :',
    br'Telnet Port 2 :',br'TCP Timeout   :',br'TCP Retry     :']
    setvaluelist=[b'172.16.10.10',b'10.131.32.1',b'255.255.248.0',
    b'00.80.55.ee.00.05',b'5000',b'5001',b'5002',b'0100',b'0006']
    writelist=["This is the Local IP addr","This is the G/W IP addr","This is the Subnet Mask","This is the Mac addr",
    "This is the Telnet Port 0 value","This is the Telnet Port 1 value","This is the Telnet Port 2 value",
    "This is the TCP Timeout value", "This is the TCP Retry value"]
    for i in range(len(setvaluelist)):
        s.expect(setlist[i])
        s.expect(br'-*[0-9.a-zA-Z]+')
        setval=(s.match.group(0))
        w=writelist[i]
        print("****", w, setval," !!!!")
        assert setval==setvaluelist[i]

def test_pr(feb_connection):
    s=sockexpect.SockExpect(feb_connection)
    s.send(b'PR\r\n')
    s.expect(br'data=')
    s.expect(br'-*[0-9.A-Z]+')
    prval=(s.match.group(0))
    print("**** The MDIO physical link reg value is", prval, "!!!!")
    
        
def test_STAT(feb_connection):
    s=sockexpect.SockExpect(feb_connection)
    s.send(b'STAT\r\n')
    FPGAregslist=[br"Time Stamp     :",br"Pulse Trg Dly  :",
    br"Spill Error    :",br"FlashGate CSR  :",br"FlshGateOnTime :",br"FlshGateOffTime:",
    br"Trigger Cntrl  :",br"PipeLine Dly   :",br"Sample Length  :",
    br"Test Pulser    :",br"TstPulsLen\(sec\):",br"TstPulsGap\(sec\):"]
    FPGAregsvalue=[b'00',b'0',b'0',b'0',b'4',b'8',b'2',b'10',b'80',b'237',b'2',b'4']
    FPGAregswrite=["This is the Time Stamp value","This is the Pulse Trigger Delay value",
    "This is the Spill Error value","This is the FlashGate CSR value",
    "This is the Flash Gate On Time value","This is the Flash Gate Off Time value",
    "This is the Trigger Control value","This is the Pipe Line Delay value",
    "This is the Sample Length value","This is the Test Pulser value",
    "This is the Test Pulse length (in seconds) value","This is the Test Pulse Gap (in seconds) value"]
    uC_intlist=[br"MuxChan        :",br"Trig Src RJ45  :",br"Link Dir XMIT  :"]
    uC_intvalue=[b'3',b'0',b'1']
    uC_intwrite=["This is the Mux channel value",
    "This is the Trigger SRC RJ45 value","This is the Link Directory XMIT value"]
    uC_floatlist=[br"BiasVolt Ch0   :",br"BiasVolt Ch1   :",br"BiasVolt Ch2   :",
    br"BiasVolt Ch3   :",br"BiasVolt Ch4   :",br"BiasVolt Ch5   :",
    br"BiasVolt Ch6   :",br"BiasVolt Ch7   :"]
    uC_floatvalue=[0.11,0.11,0.17,0.50,0.11,0.42,0.63,0.11]
    uC_floatwrite=["This is the Bias Voltage Channel 0","This is the Bias Voltage Channel 1",
    "This is the Bias Voltage Channel 2","This is the Bias Voltage Channel 3",
    "This is the Bias Voltage Channel 4","This is the Bias Voltage Channel 5",
    "This is the Bias Voltage Channel 6","This is the Bias Voltage Channel 7"]
    for i in range(len(FPGAregsvalue)):
        s.expect(FPGAregslist[i])
        s.expect(br'-*[0-9.]+')
        regsvalue=(s.match.group(0))
        w=FPGAregswrite[i]
        print(" ****", w, f," !!!!")
        assert regsvalue==FPGAregsvalue[i]
    for i in range(len(uC_intvalue)):
        s.expect(uC_intlist[i])
        s.expect(br'-*[0-9.]+')
        intvalue=(s.match.group(0))
        w=uC_intwrite[i]
        print(" ****", w, f," !!!!")
        assert intvalue==uC_intvalue[i]
    for i in range(len(uC_floatvalue)):
        s.expect(uC_floatlist[i])
        s.expect(br'-*[0-9.]+')
        floatvalue=float(s.match.group(0))
        w=uC_floatwrite[i]  
        print(" ****", w, f," !!!!")
        assert abs(floatvalue-uC_floatvalue[i])<.5  


def test_ADC(feb_connection): # pylint: disable=redefined-outer-name
    s = sockexpect.SockExpect(feb_connection)
    s.send(b'ADC\r\n')
    bytelist = [br'1.2v_Pos *',br'1.8v_Pos *',br'5.0v_Pos',br'10v_Pos',br'2.5v_Pos',br'5.0v_Neg',br'15v_Pos',br'3.3v_Pos']
    biasvolt = [1.2,1.8,5.0,10,2.5,5.0,15,3.3]
    for i in range(len(biasvolt)):
        s.expect(bytelist[i])
        s.expect(b'-*[0-9.]+')
        volt = float(s.match.group(0))
        expvolt = biasvolt[i]
        error =((expvolt-volt)/expvolt)*100
        assert abs(error)<10
        print(" **** This is the expected voltage", expvolt,"," " This is the actual voltage", volt, 
        "," "This is the error", error, "% !!!!")
    error=False
    for i in range(len(biaslist)):
        s.expect(biaslist[i])
        s.expect(b'-*[0-9.]+')
        biasvolt = float(s.match.group(0))
        if biasvolt>1:
            error=True  
        print(" **** Tbe bias volatge is", biasvolt, " !!!!")
    s.expect(br'Temp_C *')
    s.expect(b'-*[0-9.]+')
    temp=float(s.match.group(0))
    assert 18<temp<30
    print(" **** The temperature is", temp, "degC !!!!")
    s.data.clear()
    assert error==False
    
def test_all_bias(feb_connection):
    s = sockexpect.SockExpect(feb_connection)
    for fpga in range(4):
        for dac in range(22):
            check_one_bias_read_write(s,fpga,dac)
    
def check_one_bias_read_write(s,fpga, dac):
    """ dac number is 0-21 inclusive """
    assert 22>dac>=0
    addr=fpga*0x400+0x30+dac
    max_error=0
    errorflag=False
    dacval=[]
    voltread=[]
    for i in range(5):
        wdac=i*819
        s.data.clear()
        s.send(b"WR %x %x\r\n"%(addr, wdac))
        if dac>=20:
            time.sleep(0.820)
        s.send(b"RD %x\r\n"%addr)
        if WANT_DEBUG_MESSAGES:
            print(s.before, s.match, s.data)
        s.expect(b"[A-Z0-9]+")
        if WANT_DEBUG_MESSAGES:
            print(s.before, s.match, s.data)
        rdac=int(s.match.group(0),16)
        print(" **** The read DAC setting hex value is", rdac,"The written DAC setting hex value is",
         wdac,"The DAC used is", dac,"The FPGA used is",fpga," !!!!") 
        error=abs(wdac-rdac)
        dacval.append(wdac)
        if WANT_DEBUG_MESSAGES:
            print(dacval)
        if error>max_error:
            print("!!!!! wdac-rdac error!", wdac, rdac)
            errorflag=True
        volt, verrorflag=check_one_bias_ADC(s,fpga,dac,wdac)
        if verrorflag:
            print("!!!!!! check_one_bias_ADC error!")
            errorflag=True
        voltread.append(volt)
        print(voltread)
    if dac==20 or dac==21:
        x=np.array(dacval)  
        y=np.array(voltread)
        a,b =np.polyfit(x[0:5],y[0:5],1)
        plt.xlabel('Written DAC Setting')
        plt.ylabel('Observed Voltage Reading')
        plt.title('Bias Bus Observed Voltage vs Written Dac Setting')
        plt.scatter(x,y)
        plt.plot(x, a*x+b)
        plt.text(1,17, 'y= '+'{:.2f}'.format(b)+'+{:.2f}'.format(a)+'x', size =14)
        plt.show()
        header=['Written Dac Setting','Voltage Observed','Written Dac setting', 'Written FPGA value','slope and y-intercept for line of fit']
        data=[dacval,voltread, dac, fpga,(a,b)]
        print(data, "This be the printed data")
        with open(f'Data/Check_one_bias_{dac}_{time.strftime("%Y-%m-%d_%H-%M-%S")}.csv', 'w', encoding='UTF8', newline='') as f:
            writer=csv.writer(f)
            writer.writerow(header)
            for i in range(len(dacval)):
                writer.writerow([dacval[i], voltread[i], dac, fpga,(a,b)])
        
    if dac<16:
        s.send(b"WR %x 800\r\n"%addr)
    else:
        s.send(b"WR %x 0\r\n"%addr)
        if dac>=20:
            time.sleep(4)
    assert errorflag==False
    
def zero_all_bias(s, fpga):
    for dac in range(20):
        addr=fpga*0x400+0x30+dac
        s.send(b"WR %x 800\r\n"%addr)
    for dac in range(20,22):
        addr=fpga*0x400+0x30+dac
        s.send(b"WR %x 0\r\n"%addr)
    time.sleep(4)
        
    
        
def check_one_bias_ADC(s, fpga, dac, wdac, ptol=0.04):  
    """Checks bias setting vs readback
    and returns read back voltage
    s = socket connextion
    fpga = 0..3 fpga number
    dac = 0 to 21 -- dac that is being checked
    v = 0 to 4095
    ptol = The fractional tolerance"""
    if dac==20:
        itest=(2*fpga)+0
    elif dac==21:
        itest=(2*fpga)+1
    else:
        itest=-1
    s.send(b'ADC\r\n')
    s.expect(b"Temp_C")
    s.send(b'ADC\r\n')
    error=False
    volt=-1
    for i in range(len(biaslist)):
        s.expect(biaslist[i])
        s.expect(b'-*[0-9.]+')
        biasval = float(s.match.group(0))
        if WANT_DEBUG_MESSAGES:
            print(s.match)
            print(biasval)
        if i==itest:
            volt=biasval
            print("volts equals", volt, "wdac is equal to", wdac)
            expval=wdac*0.02
            if expval>70:
                expval=70
        else:
            expval=0
        if abs(biasval-expval)>4.0+ptol*expval:
            error=True
            print( f"Bias ADC {biaslist[i]} does not match expected; fpga {fpga} dac being tested {dac} expected {expval} volts and observed {biasval} volts")
    s.expect(b"Temp_C.*\r\n")   
    return volt, error

def takeEightHistos(intTime_ms, afeInputIdx):                                                                                                                         
    for fpga in range(0,3):
        s.send("WR %x %x\n" % (HISTO_COUNT_INTERVAL + 0x400*fpga, intTime_ms))
        s.send("WR %x %x\n" % (HISTO_POINTER_AFE0 + 0x400*fpga, 0))
        s.send("WR %x %x\n" % (HISTO_POINTER_AFE1 + 0x400*fpga, 0))
        for afe in range(0,1):
            s.send("WR %x %x\n" % (0x80+sipm+8*afe+0x400*fpga, 0xFE0))
    s.send("WR %x %x\n" % (HISTO_CONTROL_ALL, (sipm|0x60))
    #Will the system know what sipm is or do I need to go in and define it locally within the variable 
    #How can I locally define afeInputIdx to be an input index of integars from 0..7
    #Does this variable need an s component in the argument  
def readOneHisto(fpga, afe):
    s.send("WR %x %x\n" % (HISTO_POINTER_AFE0 + afe + 0x400*fpga)
    time.sleep(.01)
    s.clear()
    s.send(f"rdm {HISTO_PORT_AFE0 + afe + 0x400*fpga} 400\n")
    time.sleep(.01)
    histo=[int(len(N_HISTO_BINS))]
    for i in range(0,511) inclusive:
        s.send("RD %x %x\n" % (i, upperWord))
        s.send("RD %x %x\n" % (i+1, lowerWord))
        histo[i] = (upperWord << 16) | lowerWord
    return histo
    #s.clear() needs another component to clear feb input buffer of any input
    #for i in range(0,511) inclusive. Does inclusive imply range from (0,512)? 
    # How do I read one hexidecimal number and send it to upperword 
    #How do I read the next hexidecimal number and send it to the lowerword.
    
def takeAndReadAll64(intTime_ms):
    all_histos = [N_SIPM,N_HISTO_BINS]
    histos=np.zeros((N_SIPM,N_HISTO_BINS))
    for afeInputIdx in range(0,7):
        takeEightHistos(intTime_ms, afeInputIdx)
        time.sleep(intTime_ms + .001)
        for afe in range(0,1):
            sipm16 = afeInputIdx + 8*afe
            for fpga in range(0,3):
                ch = 16*fpga + sipm16
                histo=ReadOneHisto(fpga, afe)
                all_histos[ch, :]=histo
    return all_histos
    #Did I make the arrays correctly?
    #Need to define afeInputIdx locally somehow
    #Does takeEightHistos need and s component in its argument
    #Where do we define afe and is it local?
    #Where do we define fpga? 
        
