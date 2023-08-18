# ER-TQR
Entity Replacement Strategy for Temporal Knowledge Graph Query Relaxation.

pre-processing：

For ICEWS05-15, ICEWS14:

cd ICEWS

cd tkbc

python process_icews.py 

For CRONQuestions:

cd CRONQuestions

python qa_datasets.py

train and test：

For ICEWS05-15:

cd ICEWS

cd tkbc

python learner.py --dataset ICEWS05-15 --model ER-TQR_Quaternion --rank 1200 --emb_reg 1e-3 --time_reg 1e-1 --valid_freq 5 --max_epoch 200 --learning_rate 0.1 --batch_size 128  --cycle 1440

For ICEWS14:

cd ICEWS

cd tkbc

python learner.py --dataset ICEWS14 --model ER-TQR_Quaternion --rank 1200 --emb_reg 3e-3 --time_reg 3e-2 --valid_freq 5 --max_epoch 20 --learning_rate 0.1 --batch_size 128  --cycle 120

For CRONQusetions:

cd CRONQuestions

python .train.py --model ER-TQR --max_epoch 20 --learning_rate 0.1 --batch_size 128

