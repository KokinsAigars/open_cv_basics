
init() on 2026.05.13 as part of study examples for online course on Computer Vision with OpenCV



DOCKER BUILD
    docker compose up --build -d

RUN
    docker exec -it open_cv python src/numpy_002.py
    docker exec -it open_cv python src/opencv_001.py
    docker exec -it open_cv python src/openCv_002.py
    http://127.0.0.1:8888/lab


LOCAL BUILD OUTSIDE DOCKER (so I can use display for opening images && video)
    """"
    in Linux $: python3 -m venv venv                in Window>  python -m venv venv
    in Linux $: source venv/bin/activate            in Window>  venv\Scripts\activate
    in Linux $: pip install -r requirements.txt     in Window>  pip install -r requirements.txt
run
    in Linux $: python src/openCv_004.py            in Window>  python src/video/video001.py
deactivate
    in Linux $: deactivate                          in Window>  deactivate
    """


requirements.txt
    numpy           https://numpy.org/
    matplotlib
    pillow          https://pypi.org/project/pillow/    https://pillow.readthedocs.io/en/stable/
    opencv-python   https://pypi.org/project/opencv-python/  https://docs.opencv.org/3.4/d0/de3/tutorial_py_intro.html
    requests        https://pypi.org/project/requests/

