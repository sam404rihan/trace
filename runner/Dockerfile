# The sandbox every Run executes in. Built automatically by server.py.
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/lib

# Importable from your code: helpers (ListNode, TreeNode, ...), structures, algorithms
COPY helpers.py /lib/helpers.py
COPY structures /lib/structures
COPY algorithms /lib/algorithms
COPY runner/judge.py /judge/judge.py
COPY runner/prelude.py /judge/prelude.py

WORKDIR /tmp
USER 65534:65534
ENTRYPOINT ["python", "/judge/judge.py"]
