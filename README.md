# Setup

## virtualenv

Pyenv needs to be installed on your system.  If you're on MacOS with Homebrew, it's as easy as:

```
brew install pyenv
```

Otherwise, see the [installation instructions in the pyenv repo](https://github.com/pyenv/pyenv#installation).

Once pyenv is installed, you can setup the rest with:

```bash
make
```

This will install:
- python 3.6.5
- virtualenv (and create a virtualenv under `.venv`)
- all PIP dependencies within the virtualenv

## Docker

Running within a [docker container](https://www.docker.com) does not require any changes to your local system and is likely easier to run on different host systems.

### Build the image

The first step is to build a docker image with the required dependencies. This is based on a lightweight python image running linux Alpine.

```
docker build -t dcss .  # "dcss" can be any name you want to give your image
```

### Run a container

Once the image is compiled, you can run any command in a container:

```
docker run -i dcss:latest py.test tests  # use the same image name as the docker build command (e.g. "dcss")
```
or
```
docker run -i dcss:latest bin/runner my_app.yml  # use the same image name as the docker build command (e.g. "dcss")
```

### Clean up

Every time you run `docker run`, a new container is built from the image. Docker makes efficient use of hard drive space but you can clean up old instances by running

```
docker container prune
```

# Other commands/tasks

Activate the virtualenv

```bash
. .venv/bin/activate
```

Delete your current virtualenv and rebuild it from a clean state

```bash
make clean-env
make
```

Run tests

```bash
make test
```

Run a pipeline
```bash
bin/runner apps/download.yml
```

# Other dependencies

## Postgres

## Morgue file repository

- http://crawl.develz.org/morgues/
- http://crawl.berotato.org/crawl/morgue/

## DCSS Log generation code

https://github.com/crawl/crawl/blob/6199648b78d653beca72b6d47ebc822e34984531/crawl-ref/source/chardump.cc

## Make it go!

`bin/runner apps/download.yml`
