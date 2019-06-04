import visa
import struct
import matplotlib.pyplot as plt
import numpy as np
time=0.41
def initialize():
	file=open('out.dat','w')
	rm=visa.ResourceManager('@py')
	PS=rm.open_resource('USB0::2391::32536::MY57380004::0::INSTR') 
	PS.timeout=None
	PS.write('*RST')
	PS.write('TRIG:SOUR EXT')
	PS.write('INIT:CONT OFF')
	PS.write('TRAC:STAT ON')
	PS.write('AVER:STAT OFF')
	PS.write('SENS:TRAC:TIME '+str(time))
	print("Init ok")
	start_flag=1;
	return [PS,rm,file]

def read(PS):
	PS.write('INIT')
	print("Read set")
	PS.write('TRAC:DATA? MRES')
	val=PS.read_raw()
	print("Read ok")
	offset=int(chr(val[1]))
	data=val[2+offset:-1] 
	split = [struct.unpack('>f',(data[4*i:4*i+4])) for i in range (0, int(len(data)/4))]
	power=np.array(split)
	return power

[PS,rm,file]=initialize()
i=1
power=[]
while (1):
	power.append(read(PS))
	file.write(str(np.reshape(power[i-1],(1,-1)))+"\n")
	print("read "+str(i))
	i+=1
file.close()



