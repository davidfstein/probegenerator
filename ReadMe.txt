### Download Docker
https://www.docker.com/get-started

### Prepare Mount Folder
Create a folder called whatever you like. I will refer to it as MountFolder. Clone ProbeGenerator and OligoMiner from 
github into MountFolder.

### Edit the env file
The env_file stores arguments to be passed to the container when it is run.
The argument l, L, g, G, t, T, s, and F all correspond to arguments to the OligoMiner blockParse script, and their descriptions can be found in OligoMiner.
seq_path corresponds to the path to the fasta file that holds your sequence.
path_to_block_parse corresponds to the path to the blockParse.py script in OligoMiner.
path_to_probe_generatorpy corresponds to the path to the probeGenerator.py script in ProbeGenerator.
bed_output_path corresponds to the path at which you would like your bed file to be created by blockParse. Do not include the ".bed" extension.
Update the env file with the appropriate arguments for your needs. 

### Run the container
```
docker run --env-file={path/to/env_file} -v ~/{path/to/MountFolder}:/app dstein96/probegenerator:0.1
```
After running the container you should see a csv file containing the probe information in your MountFolder.