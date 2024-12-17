# Microsservicos-Sistemas-Distribuidos

## Parte 1

Consiste em um sistema de Gerenciamento de Pedidos em um restaurante, com tres microsserviços e um banco de dados maior com múltiplas tabelas

Estrutura do Banco de Dados

customers: Armazena informações dos clientes (ID, nome, email).
orders: Armazena os pedidos realizados (ID do pedido, ID do cliente, data do pedido, status, valor total).
products: armazena as informações do produto

A ideia era desenvolver uma aplicação composta por dois ou mais microsserviços. Utilizando uma comunicação indireta entre os microsserviços. Para a comunicação foi utilizado o RabbitMQ

Para rodar, basta executar o código de cada arquivo.py dentro da pasta.

## Parte 2

É a mesma ideia da primeira parte, porém, é um sistema de gerenciamento de pedidos em geral, não apenas de um restaurante, onde um dos serviços foi replicado utilizando uma API Gateway que foi implementada em python e um serviço de registro. O objetivo dessa parte é tratar o balanceamento de cargas e tolerância a falhas.

Para verificar o balanceamento de carga, basta fazer requisições, e será possível perceber que irão para ambos os serviços aleatoriamente. Para tratar a tolerância a falhas, basta parar de executar um serviço e verificar se o outro serviço tem a capacidade de continuar recebendo as requisições.

Para rodar, basta executar o código de cada arquivo.py dentro da pasta.
