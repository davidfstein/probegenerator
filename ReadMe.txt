### Download Docker
https://www.docker.com/get-started

### Prepare Mount Folder
Create a folder called whatever you like. I will refer to it as MountFolder. Clone ProbeGenerator and OligoMiner from 
github into MountFolder.

### Edit the env file
The env_file stores arguments to be passed to the container when it is run.
The arguments 'l', 'L', 'g', 'G', 't', 'T', 's', and 'F' all correspond to arguments to the OligoMiner blockParse script, and their descriptions can be found in OligoMiner.
'seq_path' corresponds to the path to the fasta file that holds your sequence.
'path_to_block_parse' corresponds to the path to the blockParse.py script in OligoMiner.
'path_to_probe_generatorpy' corresponds to the path to the probeGenerator.py script in ProbeGenerator.
'bed_output_path' corresponds to the path at which you would like your bed file to be created by blockParse. Do not include the ".bed" extension.
'initiator' correspond to the name of the amplifier you would like to use.
'left_init_seq' is the left amplifier sequence.
'left_spacer' is the spacer to be used with the left amplifier sequence
'right_init_seq' is the right amplifier sequence
'right_spacer' is the spacer to be used with the right amplifier sequence
Update the env file with the appropriate arguments for your needs. 

### Run the container
```
docker run --env-file={path/to/env_file} -v ~/{path/to/MountFolder}:/app dstein96/probegenerator:latest
```
After running the container you should see a csv file containing the probe information in your MountFolder.

### Troubleshooting
If a new version of the probegenerator is released on docker you will need to pull the latest image in order to
utilize the latest functionality. There are two ways to achieve this. The latest version of the image will be accessible under two tags,
'latest' and the highest numerical version value. For instance, if there are images tagged with 0.1 and 0.2 and latest, then both 
the image tagged 'latest' and '0.2' correspond to the most up to date image. If you have never used the image with the tag you would like to
access, then you can simply update the run command to:
```
docker run --env-file={path/to/env_file} -v ~/{path/to/MountFolder}:/app dstein96/probegenerator:{tag}
```
If you have used the tagged version before, but it has been updated then you will need to delete the old image from 
your local docker repository. To do so run the following command:
```
docker rmi dstein96/probegenerator:{tag}
```
Now when you run the 'docker run' command, docker will pull in the latest version from the remote repository.

Similarly, if the probegenerator code is updated on github, you will need to pull the latest version. You can either delete the probegenerator 
folder and clone it again, or simply from the root of probegenerator run:
```
git pull origin master
```
