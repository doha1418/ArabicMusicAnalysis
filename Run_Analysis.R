source("AnalysisScript.R")


PSDAnalysis<- function(type="Standard", plot_=TRUE, movingAverage=TRUE, from=60,generateCSV=FALSE, timeLength=10, directory=""){
  directories<-read.csv(directory,header = TRUE,stringsAsFactors=FALSE)
  gradient<- cbind("Track Name","Correlation")
  
  #calculate the time to be analysed
  to<-from+timeLength
  
  if(type=="Standard"){
    for (dir in c(1:length(directories[,1]))){
      print(directories[dir,"Directory"])
      gradient<-rbind(gradient,c(directories[dir,"TrackName"],power_spectrum_wav( file_name=directories[dir,"Directory"]
                                                                                 , start_time = from, end_time = to, MV=movingAverage,plot=plot_,title=directories[dir,"TrackName"])))
      
    }
  }
  
  else if(type=="Butter"){
    for (dir in c(1:length(directories[,1]))){
      print(directories[dir,"Directory"])
      gradient<-rbind(gradient,c(directories[dir,"TrackName"],power_spectrum_wav_butterLowpass( file_name=directories[dir,"Directory"]
                                                                                                , start_time = 10, end_time = 11, plot=plot_,title=directories[dir,"TrackName"])))
    }
  }
  
  if(generateCSV==TRUE){
    write.csv(gradient,'powerSpectrumDemo.csv')
  }
  
  print(gradient)
  
}



