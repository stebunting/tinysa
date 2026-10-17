https://tinysa.org/wiki/pmwiki.php?n=Main.USBInterface

Commands alphabetic sorted: actual_freq agc attenuate calc caloutput capture clearconfig color correction dac data deviceid freq frequencies help if if1 info level levelchange leveloffset lna lna2 load ext_gain marker mode modulation output pause rbw recall refresh release reset resume save saveconfig scan scanraw selftest spur sweep sweep_voltage sweeptime test threads time touch touchcal touchtest trace trigger ultra ultra_start usart vbat vbat_offset version zero

--- ch> actual_freq 30000000Hz

agc usage: agc 0..7|auto

attenuate usage: attenuate 0..31|auto

calc usage: calc off|minh|maxh|maxd|aver4|aver16|quasip

caloutput usage: caloutput off|30|15|10|4|3|2|1

capture # shows no help text

requests a screen dump to be send in binary format of 480x320 pixels of each 2 bytes?
clearconfig usage: clearconfig {protection key}

color usage: color {id} {rgb24}

0: 0x000000
1: 0xF8FCF8
2: 0x808080
3: 0xE0E4E0
4: 0x000000
5: 0xD0D0D0
6: 0xF8FC00
7: 0x00FC00
8: 0xF80000
9: 0xF800F8
10: 0x18E000
11: 0xF80000
12: 0x0000F8
13: 0xF8FCF8
14: 0x808080
15: 0x00FC00
16: 0x808080
17: 0x000000
18: 0xF8FCF8
19: 0x0000F8
20: 0xF88080
21: 0x00FC00
22: 0x888C88
23: 0xD8DCD8
24: 0x505050
25: 0xC0C4C0
26: 0xF8FCF8
27: 0x00FC00
28: 0x00FCF8
29: 0xF8FC00
30: 0x000000
31: 0x000000
correction usage: correction low|lna|high 0-19 frequency(Hz) value(dB)

dac usage: dac {value(0-4095)} current value: 1922

data # shows no help text -23.000000000 -23.000000000 ...

ch> deviceid deviceid 0

freq usage: freq {frequency(Hz)}

frequencies # shows no help text 1781737 3563474 ...

help # maybe alphabetic order? e.g. Commands: version reset freq time dac sweep_voltage saveconfig clearconfig data frequencies scan scanraw zero sweep test touchcal touchtest pause resume caloutput save recall trace trigger marker usart capture refresh touch release vbat vbat_offset help info color if if1 lna2 agc actual_freq attenuate level sweeptime leveloffset levelchange modulation rbw mode spur lna ultra ultra_start load ext_gain output deviceid selftest correction calc threads

if usage: if {433M..435M} 977.119 376 MHz

if1 usage: if1 {975M..979M} 977.119 376 MHz

info tinySA Ultra 2019-2020 Copyright @Erik Kaashoek 2016-2020 Copyright @edy555 SW licensed under GPL. See: https://github.com/erikkaashoek/tinySA Version: tinySA4_v1.3-82-g857be08 Build Time: May 6 2021 - 18:52:24 Kernel: 4.0.0 Compiler: GCC 7.2.1 20170904 (release) [ARM/embedded-7-branch revision 255204] Architecture: ARMv7E-M Core Variant: Cortex-M4F Port Info: Advanced kernel mode Platform: STM32F303xC Analog & DSP

k (Temperature) 38.86

level # shows no help text

levelchange usage: levelchange -70..+70

leveloffset usage: levelchange -70..+70 ch> leveloffset leveloffset low 0.2 leveloffset high 100.0 leveloffset low output 0.0 leveloffset high output 0.0 leveloffset switch 0.0 leveloffset lna -0.9

lna usage: lna off|on

lna2 usage: lna2 0..7|auto

load ext_gain # shows no help text

marker 1 419 746059136 -73.687500032 2 188 334966592 -84.125000000

mode usage: mode low|high input|output

modulation usage: modulation off|am|nfm|wfm|extern|freq 100..6000

output deviceid usage: output on|off

pause # shows no help text

rbw usage: rbw 0.3..600|auto # 600 should be 850kHz

recall recall {id}

refresh usage: refresh off|on

release # shows no help text

reset # shows no help text Performing reset # CPU?

no more communication, needs POR
resume # shows no help text

save # What parameters? save {id}

saveconfig # shows no help text Config saved.

scan usage: scan {start(Hz)} {stop(Hz)} [points] [outmask]

scanraw usage: scanraw {start(Hz)} {stop(Hz)} [points]

selftest usage: selftest (1-3) [arg] # 3?

spur usage: spur off|on|auto

sweep # shows no help text 0 800000000 450

sweep_voltage usage: sweep_voltage {value(0-3.3)} current value: 3.299999968

sweeptime usage: sweeptime 0.003..60

test # shows no help text

threads stklimit| |stk free| addr|refs|prio| state| name 20000200|20000404|00000188|20000E60| 0| 128| CURRENT| main 20000CE8|20000D34|0000008C|20000E08| 0| 1| READY| idle 20003E30|2000416C|00000290|200043A0| 0| 127| READY| sweep

ch> time 2021/05/07 14:04:00 usage: time {[y|m|d|h|min|sec] 0-99} or {b 0xYYMMDD 0xHHMMSS}

touch # shows no help text

?
touchcal

touchtest

trace # shows no help text 0 dBm ACTUAL 10.000000000 0.000000000

trigger trigger {value} trigger {auto|normal|single}

ultra usage: ultra off|on

ultra_start usage: ultra_start {0..4290M} 750.000 000 MHz

ch> usart no help

vbat 3958 mV

vbat_offset 220

version tinySA4_v1.3-82-g857be08

zero usage: zero {level} 174dBm
