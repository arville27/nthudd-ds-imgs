# NTHU-DD datasets image extractor

Converts videos from the NTHU-DD dataset into a series of images. This tool is designed to be easily consumed by `tf.keras.utils.image_dataset_from_directory`

## Requirements
- Python >=3.8

## How to use
- Configure `config.py`
- Install dependencies
```
pip install -r requirements.txt
```
- Run the tool
```
python main.py -h
```
```
usage: main.py [-h] [--execute-path-extract] [--only-check] [--populate-missing-label] {training,evaluation,testing}

NTHU-DD Datasets preprocessor

positional arguments:
  {training,evaluation,testing}
                        Datasets type to extract images from

options:
  -h, --help            show this help message and exit
  --execute-path-extract
                        Execute path_extractor before process datasets
  --only-check          Only check datasets completion without processing
  --populate-missing-label
                        Automatically populate label missing value either by infer its value or ask user depending by its missing value length
```

