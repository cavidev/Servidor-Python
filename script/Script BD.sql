create database veterinariaEYC;

use veterinariaEYC;

create table Usuario
(
	login 		varchar(20),
    contrasena 		varchar(20),
    nombre		varchar(40),
    permiso 	varchar(20),
    foto 		longblob,
    CONSTRAINT pk_login PRIMARY KEY (login)
);

create table Medicamento(
	nombre		varchar(30),
    descripcion 	varchar(100),
    foto 		longblob,
    CONSTRAINT pk_nombreMed PRIMARY KEY (nombre)
);

create table Animal(
	nombre		varchar(20),
    descripcion 	varchar(100),
    foto 		longblob,
    CONSTRAINT pk_nombreA PRIMARY KEY (nombre)
);

create table Enfermedad(
	nombre		varchar(20),
    descripcion 	varchar(100),
    foto 		longblob,
    CONSTRAINT pk_nombreE PRIMARY KEY (nombre)
);

create table Dosis(
	id					int,
	animal				varchar(20),
    medicamento			varchar(20),
    enfermedad			varchar(20),
    minPeso				int,
    maxPeso				int,
    dosis 				int,
    CONSTRAINT pk_idDosis PRIMARY KEY (id),
    CONSTRAINT fk_Dosis_animal FOREIGN KEY (animal)
	REFERENCES Animal(nombre),
    CONSTRAINT fk_Dosis_medic FOREIGN KEY (medicamento)
	REFERENCES Medicamento(nombre),
    CONSTRAINT fk_Dosis_enferm FOREIGN KEY (enfermedad)
	REFERENCES Enfermedad(nombre)
);

create table Prescripcion(
	id					int,
    usuario				varchar(20),
	animal				varchar(20),
    enfermedad			varchar(20),
    peso				int,
    idDosis				int,
    CONSTRAINT pk_idPresc PRIMARY KEY (id),
    CONSTRAINT fk_Prescripcion_usuario FOREIGN KEY (usuario)
	REFERENCES Usuario(login),
    CONSTRAINT fk_Prescripcion_animal FOREIGN KEY (animal)
	REFERENCES Animal(nombre),
    CONSTRAINT fk_Prescripcion_enferm FOREIGN KEY (enfermedad)
	REFERENCES Enfermedad(nombre),
    CONSTRAINT fk_Prescripcion_idDosis FOREIGN KEY (idDosis)
	REFERENCES Dosis(id)
);


insert into Usuario values ("Blanco707","12345","Esteban Blanco","admin","qwsdsad");
select * from Usuario

insert into Animal values ("Perro","Ladra","asddsasdsd");
insert into Animal values ("Gato","Maulla","asddsasdsd");
insert into Enfermedad values ("Sarna","Feo","asddsasdsd");
insert into Medicamento values ("Tinta Violeta","Spray","asddsasdsd");
insert into Medicamento values ("m66","Spray","asddsasdsd");
insert into Dosis values(1,"Perro","Tinta Violeta","Sarna",2,10,20);
insert into Dosis values(2,"Gato","Tinta Violeta","Sarna",1,10,5);
insert into Dosis values(3,"Gato","Tinta Violeta","Sarna",1,10,5);

insert into Prescripcion values(1,"Blanco707","Perro","Sarna",5,1)