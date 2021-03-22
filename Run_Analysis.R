source("AnalysisScript.R")


PSDAnalysis<- function(type="Standard", plot=TRUE, generateCSV=FALSE, timeLength=10, directory){
  directories<-read.csv(directory,header = TRUE,stringsAsFactors=FALSE)
  gradient<- cbind("Track Name","Correlation")
  
  #calculate the time to be analysed
  from<-3
  to<-from+timeLength
  
  if(type=="Standard"){
    for (dir in c(1:length(directories[,1]))){
      print(directories[dir,"Directory"])
      gradient<-rbind(gradient,c(directories[dir,"TrackName"],power_spectrum_wav( file_name=directories[dir,"Directory"]
                                                                                  , start_time = from, end_time = to, title=directories[dir,"TrackName"])))
    }
  }
  else if(type=="Butter"){
    for (dir in c(1:length(directories[,1]))){
      print(directories[dir,"Directory"])
      gradient<-rbind(gradient,c(directories[dir,"TrackName"],power_spectrum_wav_butterLowpass( file_name=directories[dir,"Directory"]
                                                                                                , start_time = 10, end_time = 11, title=directories[dir,"TrackName"])))
    }
  }
  
}







