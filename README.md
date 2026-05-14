
init() on 2026.05.13 as part of study examples for online course on Computer Vision with OpenCV

DOCKER BUILD
    docker compose up --build -d

RUN
    docker exec -it open_cv python src/numpy_002.py
    docker exec -it open_cv python src/opencv_001.py
    docker exec -it open_cv python src/openCv_002.py
    http://127.0.0.1:8888/lab



LOCAL BUILD OUTSIDE DOCKER (so I can use display for opening images and interact with them)
    """"
    in Linux $: python3 -m venv venv
    in Linux $: source venv/bin/activate
    in Linux $: pip install -r requirements.txt
run
    in Linux $: python src/openCv_004.py
deactivate
    in Linux $: deactivate
    """



RESOURCES

    NumPy   https://numpy.org/
    
    OpenCV  https://pypi.org/project/opencv-python/

    pillow  https://pypi.org/project/pillow/
            https://pillow.readthedocs.io/en/stable/

requirements.txt
    numpy
    matplotlib
    pillow
    opencv-python


