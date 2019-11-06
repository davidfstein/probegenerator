[![CircleCI](https://circleci.com/gh/davidfstein/probegenerator.svg?style=svg)](https://circleci.com/gh/davidfstein/probegenerator) ![Coverage](./probegenerator/res/images/coverage.svg) [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)  

# The iniator file
Create a file called "initiators.csv". This file will contain the initiator sequences for HCR. The file called "initiator.csv" in the res/examples directory in this project is an example of what your initiator file should look like. Copy the header line from that file and fill in the values as needed for your project. You may use as many initiators as desired in your intitiators file. 

# Edit the env file
Create a file called "env_file".
The env_file stores arguments to be passed to the docker container when it is run.
The arguments 'l', 'L', 'g', 'G', 't', 'T', 's', and 'F' all correspond to arguments to the OligoMiner blockParse script, and their descriptions can be found in the OligoMiner project: https://github.com/brianbeliveau/OligoMiner.
The following arguments tell the program where to find your files.
- 'seq_path' corresponds to the path to the fasta file that holds your sequence[s].
- 'path_to_bowtie_index' the path to the folder containing your reference index.
- 'bowtie_index_basename' the name of your reference index.
- 'initiator' the path to the file containing your initiators.  
  
You can copy and paste the contents of the env_file in this project and update the values as needed.

# Build bowtie2 index
A bowtie2 index is a data structure that stores long sequneces in a format that allows for fast, memory-efficient alignment. We need a bowtie2 index for whatever reference to which we would like to align our probes when checking for off-target hits. In order to create a bowtie2 index, we must install bowtie2. The instructions for installation are available here: http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#obtaining-bowtie-2. If you are not comfortable, creating your own bowtie2 index several pre-built indices are available from Illumina for common model organisms: https://support.illumina.com/sequencing/sequencing_software/igenome.html. 

If you choose to install bowtie2, you can build an index with the following command. You will need to provide the path to your reference sequence fasta file, a name for your index, and optionally a number of threads. Increasing the number of threads will speed up the creation of the index.
```
bowtie2-build --threads {# of threads you wish to use} -f {path/to/reference_fasta} {name_for_index}
```
For example
```
bowtie2-build --threads 8 -f ~/Users/doe/references/mouse.fa mouse_index
```
Or
```
bowtie2-build -f ~/Users/doe/references/mouse.fa mouse_index
```
The bowtie2-build command will create 6 files ending in .bt2. Place all the .bt2 files generated by the build command in a folder with the name you chose for the index. Move the folder you created into the MountFolder.

Note: You will need sufficient memory for the reference for which you would like to build your index. If you find that the command is failing, you may need to run it on a machine with a greater memory capacity. You can tweak your build with other parameters as described on the bowtie2 website: http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#the-bowtie2-build-indexer  

# Prepare Mount Folder
Create a folder called whatever you like. I will refer to it as MountFolder. Place the fasta file[s] with your sequences of interest in this folder, your bowtie2 index, the initiators file, and the env_file. By placing the files in this folder, you make them accessible to the docker container when you run the program. This folder is where the program output will be written.

# Run the container
```
docker run --env-file={path/to/env_file} -v ~/{path/to/MountFolder}:/data dstein96/probegenerator:0.7.50
```
After running the container you should see a folder called output containing the probe information in your MountFolder.

# Output
After running the program you should see a folder called "output" in your MountFolder. Inside the output folder will be folders for each initiator in your initiator file. Inside each initiator folder are folders for each of the genes you provided in your fasta file[s]. Each gene folder contains three files. A csv containing metadata about the probes, a .bam file containing the result of the bowtie alignment for selected probe pairs, and a .fa file containing the selected probe pair sequences with initiator sequences appended. Sequences that align to multiple regions in the reference are not included in the fasta file. Probe pairs in the orf are prioritized followed by pairs from the three prime UTR and finally the five prime UTR. 

# Troubleshooting
If a new version of the probegenerator is released on docker you will need to pull the latest image in order to utilize the latest functionality. The latest version of the image will be accessible under the highest numerical version value. For instance, if there are images tagged with 0.1 and 0.2, then the image tagged '0.2' corresponds to the most up to date image. 

Paths in the env_file are relative to the MountFolder. For instance, if your folder structure is 'MountFolder/genes.fasta', then the path to fasta file is './genes.fasta'.

Check the latest version of the docker image here: https://cloud.docker.com/repository/registry-1.docker.io/dstein96/probegenerator/tags

# Citation
Doi: 10.5281/zenodo.3516447

# References 
OligoMiner: A rapid, flexible environment for the design of genome-scale oligonucleotide in situ hybridization probes Brian J. Beliveau, Jocelyn Y. Kishi, Guy Nir, Hiroshi M. Sasaki, Sinem K. Saka, Son C. Nguyen, Chao-ting Wu, Peng Yin bioRxiv 171504; doi: https://doi.org/10.1101/171504

Choi HMT, Schwarzkopf M, Fornace ME, et al. Third-generation in situ hybridization chain reaction: multiplexed, quantitative, sensitive, versatile, robust. Development. 2018;145(12):dev165753. Published 2018 Jun 26. doi:10.1242/dev.165753
