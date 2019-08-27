# Setup

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
