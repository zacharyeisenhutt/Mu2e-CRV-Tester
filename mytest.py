x=0
while x==0:
	namelist=[br'1.2v_Pos *',br'1.8v_Pos *',br'5.0v_Pos',br'10v_Pos',br'2.5v_Pos',br'5.0v_Neg',br'15v_Pos',br'3.3v_Pos']
	evlist=[1.2,1.8,5.0,10,2.5,5.0,15,3.3]
	for i in range(len(evlist)):
		s.expect(namelist[i])
		s.expect(b'-*[0-9.]+')
		v = float(s.match.group(0))
		ev=evlist[1]
		e=((ev-v)/ev)*100
		assert abs(e)< 10
		print(" **** This is the expected voltage", ev,"," " This is the actual voltage", v, "," "This is the error", e, "% !!!!")
s.data.clear()
y = 1
biaslist = [br'Bias_0',br'Bias_1',br'Bias_2',br'Bias_3',br'Bias_4',br'Bias_5',br'Bias_6',br'Bias_7']
while y==1:
	for i in range(len(biaslist)):
		s.expect(biaslist[i])
		s.expect(b'-*[0-9.]+')
		bv = float(s.match.group(0))
		assert bv<1
		print(" **** Tbe bias volatge is", bv, " !!!!")
s.data.clear()
s.expect(br'Temp_C.*\n')
s.expect(b'-*[0-9.]+')
temp=float(s.match.group(0))
assert 18<temp<30
print(" **** The temperature is", temp, "degC !!!!")
s.data.clear()	

if 69>=addr>=48:
			dac=addr-48
			fpga=0
			print("**** Your FPGA and DAC are", fpga,",", dac," !!!!")
		if 1093>=addr>=1072:
			dac=addr-1072
			fpga=1
			print("**** Your FPGA and DAC are", fpga,",", dac," !!!!")
		if 2117>=addr>=2096:
			dac=addr-2096
			fpga=2
			print("**** Your FPGA and DAC are", fpga,",", dac," !!!!")
		if 3141>=addr>=3120:
			dac=addr-3120
			fpga=3
			print("**** Your FPGA and DAC are", fpga,",", dac," !!!!")	

	
	

