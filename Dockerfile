FROM python:3

RUN apt-get update            && \
    apt-get -y install vim    && \
    apt-get install -y dos2unix

RUN pip install --upgrade pip && \
    pip --version             && \
    pip install autopep8      && \
    pip install mypy          && \
    pip install pylint        && \
    pip install pytesseract   && \
    pip install PLT           && \
    pip install cv2           && \
    pip list

RUN apt-get update \
  && apt-get -y install tesseract-ocr \ # required for pytesseract
  && apt-get -y install ffmpeg libsm6 libxext6 # required for opencv

CMD bash