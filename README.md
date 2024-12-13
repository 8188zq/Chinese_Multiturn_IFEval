# Chinese_Multiturn_IFEval
## Single-turn create, generate and eval
create data:
```python
cd Chinese_Multiturn_IFEval
cd ../
python -m Chinese_Multiturn_IFEval.data.create_data_singleturn
```

generate:
```python
python ./Chinese_Multiturn_IFEval/generate_api_answer/generate_single_turn_gpt.py
```

eval:
```python
python -m Chinese_Multiturn_IFEval.evaluation_main   --input_data=./Chinese_Multiturn_IFEval/data/single_turn.jsonl   --input_response_data=./Chinese_Multiturn_IFEval/data/single_turn_response.jsonl   --output_dir=./Chinese_Multiturn_IFEval/data/
```

## Multi-turn create, generate and eval
create data:
```python
cd Chinese_Multiturn_IFEval
cd ../
python -m Chinese_Multiturn_IFEval.data.create_data_multiturn
```

generate:
```python
python ./Chinese_Multiturn_IFEval/generate_api_answer/generate_multi_turn_gpt.py
```

eval:
```python
python -m Chinese_Multiturn_IFEval.evaluation_main_multiturn   --input_data=./Chinese_Multiturn_IFEval/data/multi_turn_example.jsonl   --input_response_data=./Chinese_Multiturn_IFEval/data/multi_turn_response.jsonl   --output_dir=./Chinese_Multiturn_IFEval/data/multi_turn_res > log.txt
```