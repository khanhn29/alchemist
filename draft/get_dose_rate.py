def get_dose_rate(data):
    while True:
        try:
            ret = int(data)/100
            break
        except:
            print("uart1 decode error")
    return ret

print(get_dose_rate("000000123"))