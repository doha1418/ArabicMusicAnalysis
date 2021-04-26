source("Run_Analysis.R")

PSDAnalysis(type="Standard", plot=FALSE, generateCSV=TRUE,from=2,
            timeLength=10,movingAverage = FALSE, 
            directory="../audio/Music/EasternScales/MyFileList.csv", file_name="../audio/Music/EasternScales/PSDoutputDemonstration.csv")

power_spectrum_wav( file_name= "../audio/Music/Instrumental/AlaHasbiWedad.wav"
                    , start_time = 60, end_time = 70, MV = FALSE,title="AlaHasbiWedad")

power_spectrum_wav_butterLowpass( file_name="../audio/Music/TaqaseemAbadiAljawhar.wav"
                                  , start_time = 10, end_time = 20,MV = FALSE, title="Abadi Taqaseem")

