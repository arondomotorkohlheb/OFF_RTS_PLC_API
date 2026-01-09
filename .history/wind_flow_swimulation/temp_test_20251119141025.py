import matlab.engine
eng = matlab.engine.start_matlab()
eng.cd()
print(eng.pwd())