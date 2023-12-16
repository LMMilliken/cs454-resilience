batch_size=64
dev_file=quamran_experiment/datset_final.json
test_file=quamran_experiment/datset_final.json
test_model=roberta/python/checkpoint-best-bleu/pytorch_model.bin #checkpoint for test
lr=5e-5
batch_size=32
beam_size=10
source_length=512
target_length=512
output_dir=roberta-gold-output/
epochs=10 

python run.py --do_test --model_type roberta --model_name_or_path roberta-base --load_model_path $test_model --dev_filename $dev_file --test_filename $test_file --output_dir $output_dir --max_source_length $source_length --max_target_length $target_length --beam_size $beam_size --eval_batch_size $batch_size --no_cuda