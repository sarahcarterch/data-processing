# Base image from the github.com/opendatabs/data-processing repo
FROM ghcr.io/opendatabs/data-processing/base:latest

COPY uv.lock pyproject.toml /code/
RUN uv sync --frozen

COPY . /code/

CMD ["uv", "run", "-m", "etl"]


# Commands to run the container with the published image locally:
# docker pull ghcr.io/opendatabs/data-processing/aue_umweltlabor:latest
# docker run -it --rm -v /mnt/OGD-DataExch/Umweltlabor:/code/data_orig -v /data/dev/workspace/data-processing/aue_umweltlabor/data:/code/data -v /data/dev/workspace/data-processing/aue_umweltlabor/change_tracking:/code/change_tracking --name aue_rues ghcr.io/opendatabs/data-processing/aue_rues:latest
