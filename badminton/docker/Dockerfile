FROM waleedka/modern-deep-learning
RUN apt-get update
RUN pip3 install numpy scipy Pillow cython matplotlib scikit-image tensorflow>=1.3.0 keras>=2.0.8 opencv-python h5py imgaug IPython[all] graphviz pydot
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt-get install tmux vim git-lfs -y
