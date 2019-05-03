# badminton-monorepo

[![CircleCI](https://circleci.com/gh/rzadp/badminton-monorepo.svg?style=svg&circle-token=260b0239f1bb8f50a316b0806c004d26a0e444bc)](https://circleci.com/gh/rzadp/badminton-monorepo)

This monorepository consists of the following subdirectories and submodules:

| Subdirectory | Description |
| --- | --- |
| badminton | This directory contains code built on top of Mask_RCNN to train and detect badminton courts. |
| frontend | React web app used to produce fake court images. |
| Mask_RCNN | Submodule pointing to forked Mask_RCNN project. |
| thesis | Where (hopefully) the thesis text is going to be. |
| via | Submodule pointing to VIA project used to annotate images. |

### Clone with submodules

`git clone --recurse-submodules https://github.com/rzadp/badminton-monorepo.git`

### Initialize LFS

LFS is used for >100 MB files that cannot be stored directly.
- Install LFS: https://git-lfs.github.com./
- `git lfs install`
- `git lfs pull`

### Run docker

For badminton project, docker needs to be installed and started: https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce

### Usage

Refer to READMEs in subdirectories.
