source("AnalysisScript.R")

power_spectrum_wav("./audio/EasternScales/Ajam_C.wav", start_time = 1, end_time = 20, title="Ajam_C")

power_spectrum_wav_butterLowpass("./audio/EasternScales/BayatiRe.wav", start_time = 1, end_time = 12, title="BayatiRe")




