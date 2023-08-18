# ER-TQR

**Entity Replacement Strategy for Temporal Knowledge Graph Query Relaxation**

## Installation

The implementation is based on CronKGQA in [Question Answering over Temporal Knowledge Graphs](https://arxiv.org/abs/2106.01515) and their code from https://github.com/apoorvumang/CronKGQA. You can find more installation details there.
We use TComplEx KG Embeddings as implemented in https://github.com/facebookresearch/tkbc.

Install ER-TQR requirements

`conda install --file requirements.txt -c conda-forge`

## Dataset and pretrained models download

For the CRONQuestions dataset and pretrained models : Download and unzip ``data.zip`` and ``models.zip`` in the root directory.

Drive: https://drive.google.com/drive/folders/1aS2s5sZ0qlDpGZ9rdR7HcHym23N3pUea?usp=sharing.

Create new subdirectories of root directories /data and /model, and add the downloaded files to each of these subdirectories.

You can refer to the link  https://github.com/apoorvumang/CronKGQA. 

## Running the code

#### preprocessing datasets：

**For ICEWS05-15, ICEWS14**:

`cd ICEWS`

`cd tkbc`

`python process_icews.py` 

 **For CRONQuestions:**

`cd CRONQuestions`

`python qa_datasets.py`

#### train and test：

**For ICEWS05-15:**

`cd ICEWS`

`cd tkbc`

`python learner.py --dataset ICEWS05-15 --model ER-TQR_Quaternion --rank 1200 --emb_reg 1e-3 --time_reg 1e-1 --valid_freq 5 --max_epoch 200 --learning_rate 0.1 --batch_size 128 --cycle 1440`

**For ICEWS14:**

`cd ICEWS`

`cd tkbc`

`python learner.py --dataset ICEWS14 --model ER-TQR_Quaternion --rank 1200 --emb_reg 3e-3 --time_reg 3e-2 --valid_freq 5 --max_epoch 20 --learning_rate 0.1 --batch_size 128 --cycle 120`

**For CRONQusetions:**

`cd CRONQuestions`

`python .train.py --model ER-TQR --max_epoch 20 --learning_rate 0.1 --batch_size 128`

