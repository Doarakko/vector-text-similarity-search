#!/bin/sh
bert-serving-start -num_worker=1 -max_seq_len=NONE -model_dir /app/model
