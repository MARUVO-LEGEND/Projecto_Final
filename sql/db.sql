drop database magna_db;
create database magna_db;
use magna_db;
create table aluno(
    id_aluno INT PRIMARY KEY auto_increment,
    nome VARCHAR(100),
    n_i_escolar varchar(5) UNIQUE,
    n_i_turma varchar(2),
    foto_caminho varchar(100)  unique, 
    turma varchar(10),
    nascimento date,
    turno varchar(5)
);

create table administrador(
	id int primary key auto_increment,
	nome varchar(100),
    senha varchar(50)
);

INSERT INTO administrador (nome,senha) VALUES ("Mauro Martins","MM"),("Josemar Nzola","JN"),("Mario Pereira","MP");
INSERT INTO secretario (nome,senha,telefone,id_funcionario) VALUES ("Neide Sofia","NS","922 399 499","10009");
INSERT INTO porteiro (nome,senha,telefone,id_funcionario) VALUES ("Michaela Reis","MR","932 369 479","20009");
INSERT INTO monitor (nome,senha,telefone,id_funcionario) VALUES ("João Lourenço","JL","922 669 489","50009");
select * from administrador;

create table secretario(
	id_secretario int primary key auto_increment,
    nome varchar(100),
    senha varchar(50),
    telefone varchar(15),
    id_funcionario varchar(5)
	
);
create table porteiro(
	id_porteiro int primary key auto_increment,
    nome varchar(100),
    senha varchar(50) ,
    telefone varchar(15),
    id_funcionario varchar(5)
	
);
create table monitor(
	id_monitor int primary key auto_increment,
    nome varchar(100),
    senha varchar(50) ,
    telefone varchar(15),
    id_funcionario varchar(5)
	
);

create table monitoramento (
    id_registo int primary key auto_increment,
    data_hora_registo datetime,
    id_aluno int,
    localizacao varchar(50),
    tipo_activ varchar(20),
    foreign key (id_aluno) references aluno(id_aluno)
);

create table configuracao_sistema (
    id_configuracao int primary key auto_increment,
    config_reconhecimento_facial varchar(255),
    config_registo_faltas varchar(255)
);

alter table monitoramento
add column id_configuracao int,
add foreign key (id_configuracao) references configuracao_sistema(id_configuracao);


select * from aluno;
select * from secretario;
select * from monitor;
select * from projecto.monitoramento;




