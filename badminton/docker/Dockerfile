FROM waleedka/modern-deep-learning
RUN pip3 install numpy scipy Pillow cython matplotlib scikit-image tensorflow>=1.3.0 keras>=2.0.8 opencv-python h5py imgaug IPython[all]
# RUN git clone https://<token>@github.com/rzadp/Mask_RCNN.git
RUN pip3 install graphviz pydot
RUN apt-get install tmux -y
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt-get install git-lfs

