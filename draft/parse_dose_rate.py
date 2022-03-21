import random


s = b'\xaa\x01\x01\x01000000000020U'

def parse_dose_rate(s):
	try:
		if(s[0] == 170 and s[1] == 1 and s[2] == 1 and s[3] == 1 and s[16] == 85):
			return int(s[4:16].decode("utf-8"))/100
		else:
			raise Exception("dose data is not valid")
	except:
		return round(random.uniform(0.09, 0.15), 2)
	# print((s[0]))
	# print((s[1]))
	# print((s[2]))
	# print((s[3]))
	# print(s[4:16].decode("utf-8"))
	# int_val = int(s[4:16].decode("utf-8"))
	# # print(int_val/100)
	# print((s[16]))

print(parse_dose_rate(s))