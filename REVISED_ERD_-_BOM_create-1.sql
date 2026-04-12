-- Created by Redgate Data Modeler (https://datamodeler.redgate-platform.com)
-- Last modification date: 2026-03-07 20:24:53.345

-- tables
-- Table: assemblies
CREATE TABLE assemblies (
    parts_number varchar(10)  NOT NULL,
    CONSTRAINT assemblies_pk PRIMARY KEY (parts_number)
);

-- Table: parts
CREATE TABLE parts (
    number varchar(10)  NOT NULL,
    name varchar(80)  NOT NULL,
    CONSTRAINT parts_uk_01 UNIQUE (name) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT parts_name_length CHECK (( length ( name ) >= 3 )) NOT DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT parts_number_length CHECK (( length ( number ) >= 1 )) NOT DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT parts_pk PRIMARY KEY (number)
);

-- Table: piece_parts
CREATE TABLE piece_parts (
    parts_number varchar(10)  NOT NULL,
    vendors_name varchar(80)  NOT NULL,
    CONSTRAINT piece_parts_pk PRIMARY KEY (parts_number)
);

-- Table: usages
CREATE TABLE usages (
    parts_number varchar(10)  NOT NULL,
    assemblies_parts_number varchar(10)  NOT NULL,
    quantity int  NOT NULL,
    CONSTRAINT usages_quantity_length CHECK (( quantity BETWEEN 1 AND 20 )) NOT DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT usages_pk PRIMARY KEY (parts_number,assemblies_parts_number)
);

-- Table: vendors
CREATE TABLE vendors (
    name varchar(80)  NOT NULL,
    CONSTRAINT vendors_name_length CHECK (( length ( name ) >= 3 )) NOT DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT vendors_pk PRIMARY KEY (name)
);

-- foreign keys
-- Reference: assemblies_parts_fk_01 (table: assemblies)
ALTER TABLE assemblies ADD CONSTRAINT assemblies_parts_fk_01
    FOREIGN KEY (parts_number)
    REFERENCES parts (number)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: piece_parts_parts_fk_01 (table: piece_parts)
ALTER TABLE piece_parts ADD CONSTRAINT piece_parts_parts_fk_01
    FOREIGN KEY (parts_number)
    REFERENCES parts (number)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: piece_parts_vendors_fk_01 (table: piece_parts)
ALTER TABLE piece_parts ADD CONSTRAINT piece_parts_vendors_fk_01
    FOREIGN KEY (vendors_name)
    REFERENCES vendors (name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: usages_assemblies_fk_01 (table: usages)
ALTER TABLE usages ADD CONSTRAINT usages_assemblies_fk_01
    FOREIGN KEY (assemblies_parts_number)
    REFERENCES assemblies (parts_number)  
    DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: usages_parts_fk_01 (table: usages)
ALTER TABLE usages ADD CONSTRAINT usages_parts_fk_01
    FOREIGN KEY (parts_number)
    REFERENCES parts (number)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

