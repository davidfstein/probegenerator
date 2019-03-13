### Download Docker
https://www.docker.com/get-started

### Build the image
From the root of the project run the following:
```
docker build --tag=probegenerator .
```

### Edit the env file
The env_file stores arguments to be passed to the container when it is run.
Update the env file with the appropriate arguments for your needs. 

### Run a container
```
docker run --env-file={path/to/env_file} -v ~/{path/to/this/repo}:/app probegenerator
```