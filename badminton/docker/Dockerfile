FROM waleedka/modern-deep-learning
RUN apt-get update
RUN pip3 install numpy scipy Pillow cython matplotlib scikit-image tensorflow==1.12.0 keras==2.2.4 opencv-python h5py imgaug IPython[all] graphviz pydot
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt-get install tmux vim git-lfs -y
