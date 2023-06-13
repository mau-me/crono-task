# Crono Task

## Table of Contents

- [Crono Task](#crono-task)
  - [Table of Contents](#table-of-contents)
  - [About ](#about-)
  - [Getting Started ](#getting-started-)
    - [Prerequisites](#prerequisites)
    - [Installing](#installing)
  - [Usage ](#usage-)
    - [Exemplos de execução](#exemplos-de-execução)
      - [iniciar](#iniciar)
      - [finalizar](#finalizar)
      - [listar](#listar)

## About <a name = "about"></a>

CLI para contabilizar a quantidade de tempo gasto com as suas atividades

## Getting Started <a name = "getting_started"></a>

### Prerequisites

```
Python3
MySQL
```

### Installing

Para executar o script é necessário os seguintes passos:

```
pip install mysql-connector-python
```

Também é necessário criar a base de dados no MySQL, e alterar as informações de acesso no script

## Usage <a name = "usage"></a>

A CLI possui três funcionalidades: iniciar, finalizar e listar
Ao executar a funcionalidade de listar deve ser passado como parâmetro a descrição da atividade

### Exemplos de execução

#### iniciar
```
python3 crono_task.py iniciar 'Development: implementar funcionalidade X'
```
#### finalizar
OBS: Se existir mais de uma atividade inicializada, as mesmas serão finalizadas na ordem inversa de criação.
```
python3 crono_task.py finalizar
```
#### listar
```
python3 crono_task.py listar
```