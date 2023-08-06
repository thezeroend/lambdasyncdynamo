import json
import logging
import boto3
import os

logging.basicConfig(level=logging.INFO)
dynamodb = boto3.client('dynamodb')

dynamo_table_name = os.getenv("DYNAMO_TABLE") or "teste"
# dynamo_table_name = "teste"

def create_record(body):
    """
    Cria um novo registro na tabela DynamoDB.

    Esta função recebe um dicionário contendo os campos 'client_id' e 'gateway_id'
    para criar um novo registro na tabela DynamoDB. A função tenta inserir o registro,
    verificando se os atributos 'client_id' e 'gateway_id' não existem previamente
    na tabela.

    Args:
        body (dict): Um dicionário contendo 'client_id' e 'gateway_id' para o novo registro.

    Returns:
        dict or bool: Um dicionário representando a resposta da criação no DynamoDB
                      se a criação for bem-sucedida, ou False se a condição de verificação
                      (attribute_not_exists) falhar.

    Example:
        Exemplo de uso da função:

        >>> record_to_create = {
        ...     'client_id': '123',
        ...     'gateway_id': '456'
        ... }
        >>> result = create_record(record_to_create)
        >>> print(result)
        {'ResponseMetadata': {'RequestId': '...', 'HTTPStatusCode': 200, ...}}
    """
    client_id = body.get('client_id')
    gateway_id = body.get('gateway_id')

    try:
        response = dynamodb.put_item(
            TableName=dynamo_table_name,
            Item={
                'client_id': {'S': client_id},
                'gateway_id': {'S': gateway_id}
            },
            ConditionExpression='attribute_not_exists(client_id) AND attribute_not_exists(gateway_id)'
        )
        return response
    except dynamodb.exceptions.ConditionalCheckFailedException:
        return False

def delete_record(body):
    """
    Deleta um registro da tabela DynamoDB.

    Esta função recebe um dicionário contendo os campos 'client_id' e 'gateway_id'
    que identificam o registro a ser excluído. A função tenta excluir o registro da
    tabela DynamoDB, verificando se os atributos 'client_id' e 'gateway_id' existem
    no registro antes da exclusão.

    Args:
        body (dict): Um dicionário contendo 'client_id' e 'gateway_id' para identificar o registro.

    Returns:
        dict or bool: Um dicionário representando a resposta da exclusão do DynamoDB
                      se a exclusão for bem-sucedida, ou False se a condição de verificação
                      (attribute_exists) falhar.

    Example:
        Exemplo de uso da função:

        >>> record_to_delete = {
        ...     'client_id': '123',
        ...     'gateway_id': '456'
        ... }
        >>> result = delete_record(record_to_delete)
        >>> print(result)
        {'ResponseMetadata': {'RequestId': '...', 'HTTPStatusCode': 200, ...}}
    """
    client_id = body.get('client_id')
    gateway_id = body.get('gateway_id')
    
    try:
        response = dynamodb.delete_item(
            TableName=dynamo_table_name,
            Key={
                'client_id': {'S': client_id},
                'gateway_id': {'S': gateway_id}
            },
            ConditionExpression='attribute_exists(client_id) AND attribute_exists(gateway_id)'
        )
        return response
    except dynamodb.exceptions.ConditionalCheckFailedException:
        return False

def get_body(record):
    """
    Obtém o corpo JSON de um registro.

    Esta função recebe um registro (geralmente de um evento) e extrai o corpo JSON dele,
    convertendo-o em um dicionário Python.

    Args:
        record (dict): O registro contendo um campo 'body' que contém uma carga JSON.

    Returns:
        dict: Um dicionário Python representando o conteúdo do corpo JSON do registro.

    Example:
        Exemplo de uso da função:

        >>> event_record = {
        ...     'body': '{"action": "delete","gateway_id": "12345","client_id": "12345-12345"}'
        ... }
        >>> result = get_body(event_record)
        >>> print(result)
        {'action': 'delete','gateway_id': '12345','client_id': '12345-12345'}
    """
    payload = record.get('body')
    return json.loads(payload)

def lambda_handler(event, context):
    logging.info('Iniciando Execução')

    total_records = len(event.get('Records'))
    read_records = 0
    if total_records > 0:
        for record in event['Records']:
            response = None
            body = get_body(record)
            logging.debug(f"Body: {body}")

            if body is not None:
                if body['action'] == "create":
                    response = create_record(body)

                    if response is False:
                        logging.info("Registro já existente na base!")
                    else:
                        logging.info("Registro criado com sucesso!")

                if body['action'] == "delete":
                    response = delete_record(body)

                    if response is False:
                        logging.info("Registro não encontrado!")
                    else:
                        logging.info("Registro deletado com sucesso!")
            else:
                logging.error("Body não encontrado")

            read_records += 1
    else:
        logging.error("Total de records menor que 1.")

    
    return {
        'statusCode': 200,
        'body': json.dumps(f"Total de Records: {total_records} - Read Records: {read_records}")
    }
