source("AnalysisScript.R")
directories<-read.csv("../audio/Music/Directories.csv",header = TRUE,stringsAsFactors=FALSE)

gradient<- c()

for (dir in c(1:11)){
  print(directories[dir,"Directory"])
  gradient<-append(gradient,power_spectrum_wav( file_name=directories[dir,"Directory"]
                  , start_time = 1, end_time = 7, title=directories[dir,"TrackName"]))
  
  
}
print(gradient)
power_spectrum_wav("../audio/WhiteNoise2.wav", start_time = 1, end_time = 7, title="White Noise")

power_spectrum_wav_butterLowpass("../audio/WhiteNoise2.wav", start_time = 1, end_time = 10, title="White Noise Voss and Clarke's Model")




