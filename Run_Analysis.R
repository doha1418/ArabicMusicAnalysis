source("AnalysisScript.R")
directories<-read.csv("../audio/Music/Directories.csv",header = TRUE,stringsAsFactors=FALSE)

gradient<- cbind("Track Name","Correlation")

for (dir in c(1:length(directories[,1]))){
  print(directories[dir,"Directory"])
  gradient<-rbind(gradient,c(directories[dir,"TrackName"],power_spectrum_wav( file_name=directories[dir,"Directory"]
                  , start_time = 10, end_time = 11, title=directories[dir,"TrackName"])))
}

#Voss and Clarke filtering simulation
power_spectrum_wav_butterLowpass("../audio/WhiteNoise2.wav", start_time = 10, end_time = 20, title="Firuz")




