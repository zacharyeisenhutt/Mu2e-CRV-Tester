import sockexpect 
import test_feb_cmds as tst 
feb=tst.make_feb_socket()
s=sockexpect.SockExpect(feb)
