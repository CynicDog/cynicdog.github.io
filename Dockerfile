FROM python:3.9-slim

RUN pip install --no-cache-dir \
    sentence-transformers \
    scikit-learn \
    pandas

COPY scripts /scripts

ENTRYPOINT ["python", "/scripts/analyize.py"]