source("Run_Analysis.R")

PSDAnalysis(type="Standard", plot=FALSE, generateCSV=TRUE,from=2,
            timeLength=10,movingAverage = FALSE, 
            directory="../improvSamples/Directories.csv", file_name="../improvSamples/PSDoutput10sec.csv")

power_spectrum_wav( file_name= "../audio/bach.wav"
                    , start_time = 0, end_time = 10, MV = FALSE,title="Bach")

power_spectrum_wav_butterLowpass( file_name="../audio/Music/TaqaseemAbadiAljawhar.wav"
                                  , start_time = 10, end_time = 20,MV = FALSE, title="Abadi Taqaseem")

