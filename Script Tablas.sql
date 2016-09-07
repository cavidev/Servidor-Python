create database VeterinariaEyC;

use VeterinariaEyC;

create table Usuario
(
	login 		varchar(20),
    pass 		varchar(20),
    nombre		varchar(20),
    permiso 	varchar(20),
    foto 		longblob,
    CONSTRAINT pk_login PRIMARY KEY (login)
);

create table Medicamento(
	nombre		varchar(20),
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
    peso				int,
    dosis				int,
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

INSERT INTO Usuario VALUES 	("Blanco707","2016","Esteban Blanco","Admin","234iji423jj432kb4223nasdnsdvn"),
							("Palida","leidyladecompu","Leidy Chacón","Normal","234iji423jj432kb4223nasdnsdvn");
                            
INSERT INTO Animal VALUES 	("Perro", "Ladra", "234iji423jj432kb4223nasdnsdvn"),
							("Gato", "Ronronea", "234iji423jj432kb4223nasdnsdvn");
                            
INSERT INTO Medicamento VALUES 	("Acetaminofen","Cura todo","234iji423jj432kb4223nasdnsdvn"),
								("Violeta", "Contra heridas en la piel","234iji423jj432kb4223nasdnsdvn");
                                
INSERT INTO Enfermedad VALUES 	("Sarna","Se ponen feos","234iji423jj432kb4223nasdnsdvn"),
								("Distemper", "Moquillo","234iji423jj432kb4223nasdnsdvn");
                                
INSERT INTO Dosis VALUES 	(1,"Gato","Violeta","Sarna",30,10),
							(2,"Perro","Acetaminofen","Distemper",5,2);
                            
INSERT INTO Prescripcion VALUES 	(1,"Blanco707","Perro","Distemper",30,1),
									(2,"Blanco707","Gato","Sarna",5,2);
