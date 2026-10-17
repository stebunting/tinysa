import tinySA

f1 = 470 * 1000000
f2 = 530 * 1000000

device = tinySA.tinySA()
device.resume()
# device.set_frequencies(f1, f2)
device.cmd("rbw 30")
device.cmd("calc off")
device.cmd(f"scan {f1} {f2}")

frequencies = []
device.send_command("frequencies\r")
r = device.fetch_data()
for line in r.split('\n'):
    if line:
        frequencies.append(float(line))

levels = []
device.send_command("data 2\r")
r = device.fetch_data()
for line in r.split('\n'):
    if line:
        levels.append(float(line))

assert(len(frequencies) == len(levels))

f = open("test.csv", "w")
for i in range(len(frequencies)):
    print("%.3f;" % (frequencies[i] / 1000000), "%2.2f" % levels[i], file=f)

