library(stats)
library(seewave)
library(tuneR)

v.sound <- sin(2*pi*100*seq(0,1,length.out=8000))
wave.sound <- Wave(v.sound, start=0, end=1, frequency=8000)
ts.sound.sel <- window(ts.sound, start=0.25, end=0.30)
fd<- fft(ts.sound.sel)
fd<-log10(fd)
print((ts.sound.sel))

plot(fd, xlab="Frequency", ylab="Amplitude", col="blue")



