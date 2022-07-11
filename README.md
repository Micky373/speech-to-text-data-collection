# speech-to-text-data-collection
A speech to text data collection using Apache Kafka, Apache spark, Airflow, and S3 bucket

**Table of Contents**

  - [Overview](#overview)
  - [Project Structure](#project-structure)
    - [data:](#data)
    - [notebooks:](#notebooks)
    - [scripts](#scripts)
    - [tests:](#tests)
    - [logs:](#logs)
    - [root folder](#root-folder)
  - [Installation guide](#installation-guide)
  - [LICENCE](#license)

## Overview
 
This week, 10 Academy is your client. Recognizing the value of large data sets for speech-t0-text data sets, and seeing the opportunity that there are many text corpuses for both languages, and understanding that complex data engineering skills is valuable to your profile for employers, this week’s task is simple: design and build a robust, large scale, fault tolerant, highly available Kafka cluster that can be used to post a sentence and receive an audio file. 

By the end of this project, you should produce a tool that can be deployed to process posting and receiving text and audio files from and into a data lake, apply transformation in a distributed manner, and load it into a warehouse in a suitable format to train a speech-t0-text model. 


## Project Structure
The repository has a number of files including python scripts, jupyter notebooks, pdfs and text files. Here is their structure with a brief explanation.

## Data
The purpose of this week’s challenge is to build a data engineering pipeline that allows recording millions of Amharic and Swahili speakers reading digital texts in-app and web platforms. 

There are a number of large text corpora we will use, but for the purpose of testing the backend development, you can use the recently released Amharic news text classification dataset with baseline performance dataset:   

[IsraelAbebe/An-Amharic-News-Text-classification-Dataset](IsraelAbebe/An-Amharic-News-Text-classification-Dataset)

Alternative data 
Ready-made Amharic data collected from different sources  [here](https://arxiv.org/pdf/2103.05639.pdf)


## Usage
### Docker-compose
Both the front-end and the back-end could be run on a docker container.
<br>

**1. Clone the repo**
```
git clone https://github.com/GrpHu/speech-to-text-data-collection
```
**2. cd into repo**
```
cd speech-to-text-data-collection
```
**3.Start docker container:**
```
docker-compose up -d
```

## notebooks
- [EDA.ipynb]: a jupyter notebook for exploratory data analysis
## scripts

## tests:
- the folder containing unit tests for components in the scripts

## logs:
- the folder containing log files (if it doesn't exist it will be created once logging starts)

## License
[MIT](https://choosealicense.com/licenses/mit/)


[back to top](#Table-of-Contents)



