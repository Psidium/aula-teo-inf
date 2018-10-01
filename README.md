# aula-teo-inf
```
usage: trabalho.py [-h] [--encode] [--decode] --input INPUT_FILENAME --output OUTPUT_FILENAME
```

## Dependências
- u-msgpack-python
- dahuffman
- lz4
## Para codificar um arquivo
```
trabalho.py --encode --input alice29.txt --output alice29_codificado
```

## Para decodificar um arquivo
```
trabalho.py --decode --input alice29_codificado --output alice29_decodificado.txt
```
