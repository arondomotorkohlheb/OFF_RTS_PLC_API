import matlab.engine
eng = matlab.engine.start_matlab()
eng.cd('C:\\backup\\Study\MSc\research_assignment\git\OFF_RTS_PLC_API\RTS)
print(eng.pwd())