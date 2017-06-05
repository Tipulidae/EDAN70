This folder contains csv-files converted to raw data that can be used for training. 
The different formats means:

.d1		Basic format: each instruction is 5+1 bytes: dt,dt,duration,duration,note,\128
.d2		Basic+velocity: each instruction is 6+1 bytes: dt,dt,duration,duration,note,velocity,\128
.d3		Basic+composer: each instruction is 6+1 bytes: dt,dt,duration,duration,note,composer,\128
.d4		Basic+velocity+composer: Each instruction is 7+1 bytes: dt,dt,duration,duration,note,velocity,composer,\128
		


The default format is d1. Change it by passing it as argument to csv2data or data2csv: "python csv2data INPUT OUTPUT d3"
