#file to be modified
library(seewave)
library(fftw)
library(tuneR)
library(audio)
library(forecast)



power_spectrum_wav<-function(file_name, start_time, end_time, title, plot=TRUE, MV){
  
  #load the song
  Song_sound <- load.wave(file_name)
  #extract a mono wav file in this case the left side is chosen
  song_left<-readWave(file_name)@left
  hdr2 <- readWave(file_name,
                   header=TRUE)
  song_left<- Wave(song_left, samp.rate=hdr2$sample.rate, bit=hdr2$bits)
  
  
  song_left<-ffilter(song_left,to=10000,output='Wave',bandpass = TRUE)
  
  song_left<-song_left*song_left #square the voltage
 
  
  #calculates the power spectral density against amplitude, then finds their log and plots it
  spectra_song<-spec(song_left, from=start_time, to=end_time, PSD=TRUE, col="red", correction="energy",scaled=FALSE,plot=FALSE)

  #push the data to the right in order to remove the first zero
  spectra_song[,1]=spectra_song[,1]+1
 
  
  spectra_song[,1:2]<-log10(spectra_song[,1:2])#change the spectral density to log
  
  x_axis<-spectra_song[,1]
  y_axis<-spectra_song[,2]
  
  #moving average set this as a seperate function
  if(MV==TRUE){
    movingAverage(spectra_song)
  }
  
  if(plot==TRUE){
    plot(spectra_song,type='l',main=title, xlab='log10(f) Hz', ylab='log10(Sv)')
  }
  
  #removing the first row to get rid of -infinity in order to calculate the gradient
 
  
  
  if(length(which(is.na(x_axis)))>0){
  #clear the NAs to find slope
    x_axis_cleared<-x_axis[-which(is.na(x_axis))]
    y_axis_cleared<-y_axis[-which(is.na(x_axis))]
    gradient<-cor(x_axis_cleared,y_axis_cleared, method="pearson")
  }
  else{
    gradient<-cor(x_axis,y_axis, method="pearson")
  }
  
  return(round(gradient, digits = 3))
  
}

power_spectrum_wav_butterLowpass<-function(file_name, start_time, end_time, title, plot=TRUE){
  
  
  #load the song
  Song_sound <- load.wave(file_name)
  #extract a mono wav file in this case the left side is chosen
  song_left<-readWave(file_name)@left
  hdr2 <- readWave(file_name,
                   header=TRUE)
  song_left<- Wave(song_left, samp.rate=hdr2$sample.rate, bit=hdr2$bits)
 
  song_left<-ffilter(song_left,to=10000,output='Wave',bandpass = TRUE) #bandpass filter max 10kHz
  song_left<-song_left*song_left #square the voltage
  
  #calculates the power spectral density against amplitude, then finds their log and plots it
  spectra_song<-spec(song_left, from=start_time, to=end_time, PSD=TRUE, col="red", correction="energy",scaled=FALSE,plot=TRUE)
  
  spectra_song[,1]=spectra_song[,1]+1
 
  
  butterSpec<- butter.H(spect=spectra_song, fc=20, n=1) #Butterworth filter max 20Hz

  
  butterSpec[,1:2]<-log10(butterSpec[,1:2])#change the spectral density to log
  
  if(plot==TRUE){
    plot(butterSpec,type='l', main=title, xlab='log10(f) Hz', ylab='log10(Sv)')
  }
  
  x_axis<-butterSpec[,1]
  y_axis<-butterSpec[,2]

  
  if(length(which(is.na(x_axis)))>0){
    #clear the NAs to find slope
    x_axis_cleared<-x_axis[-which(is.na(x_axis))]
    y_axis_cleared<-y_axis[-which(is.na(x_axis))]
    gradient<-cor(x_axis_cleared,y_axis_cleared, method="pearson")
  }
  else{
    gradient<-cor(x_axis,y_axis, method="pearson")
  }
  
  return(round(gradient, digits = 3))
  
}

movingAverage<- function(spectra_song){
  movingave<- filter(spectra_song, rep(1 / 50, 50), sides = 2)
   v2<-movingave[,2]
   x_axis_ave<-x_axis[-which(is.na(v2))]
   v2<-v2[-which(is.na(v2))]
   
   plot(x_axis_ave,v2,type='l',main="Moving average")
   gradient1<-lm(x_axis_ave ~ v2)
   print(gradient1)
}

#pass the whole spectrum with a vector that has an x and y value as col
butter.H <- function(spect, fc, n){
  
  freq=spect[,1]
  H=spect[,2]
  
  s <- freq/fc
  H <- 1/sqrt(1+s^(2*n))
 
  sp<-cbind(freq,H)
  
  
  return(sp) 
  
}
