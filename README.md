# Lambda Functions for DynamoDB Synchronization

Este repositório contém funções Lambda em Python 3.8 para realizar operações básicas em uma tabela do Amazon DynamoDB, com foco na sincronização de dados.

## Objetivo

O objetivo principal dessas funções é proporcionar uma solução de sincronização eficiente para uma base de dados do DynamoDB. As operações incluem busca de registros com base em IDs de cliente e gateway, criação de registros e exclusão de registros, todas as quais são essenciais para manter a consistência dos dados em um ambiente distribuído.

## Funções

### `get_body(record)`

Esta função obtém o corpo JSON de um registro.

### `create_record(body)`

Esta função cria um novo registro na tabela DynamoDB.

### `delete_record(body)`

Esta função exclui um registro da tabela DynamoDB com base no client_id e gateway_id.


## Exemplos de Uso

```python
# Exemplo de uso da função get_body
record = {
    'body': '{"action": "delete","gateway_id": "12345","client_id": "12345-12345"}'
}
result = get_body(record)
print(result)

# Exemplo de uso da função create_record
record_to_create = {
    'client_id': '123',
    'gateway_id': '456',
    'action': 'create'
}
result = create_record(record_to_create)
print(result)

# Exemplo de uso da função delete_record
record_to_delete = {
    'client_id': '123',
    'gateway_id': '456',
    'action': 'delete'
}
result = delete_record(record_to_delete)
print(result)
```

## Configuração

Certifique-se de ter as funções `get_body`, `create_record` e `delete_record` definidas corretamente e de configurar as permissões adequadas para o Lambda acessar o DynamoDB e gravar logs.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).