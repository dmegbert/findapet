CREATE TABLE public.dog
(
  id                         serial PRIMARY KEY NOT NULL,
  name                       text               NOT NULL,
  description                text,
  energy_level               int,
  exercise_requirements      int,
  playfulness                int,
  affection_level            int,
  friendliness_to_dogs       int,
  friendliness_to_other_pets int,
  friendliness_to_strangers  int,
  watchfulness               int,
  ease_of_training           int,
  grooming_requirements      int,
  heat_sensitivity           int,
  vocality                   int,
  weight                     numrange,
  height                     numrange,
  history                    text,
  personality                text,
  care_overview              text,
  category_id                int,
  family_id                  int,
  area_of_origin_id          int,
  date_of_origin_id          int
);
CREATE UNIQUE INDEX dog_id_uindex
  ON public.dog (id);
CREATE UNIQUE INDEX dog_name_uindex
  ON public.dog (name);

CREATE TABLE public.category
(
  id   serial PRIMARY KEY NOT NULL,
  name text
);
CREATE UNIQUE INDEX category_id_uindex
  ON public.category (id);
CREATE UNIQUE INDEX category_name_uindex
  ON public.category (name);

ALTER TABLE public.dog
  ADD CONSTRAINT dog_category_id_fk
FOREIGN KEY (category_id) REFERENCES public.category (id) ON DELETE CASCADE ON UPDATE CASCADE;


CREATE TABLE public.family
(
  id   serial PRIMARY KEY NOT NULL,
  name text               NOT NULL
);
CREATE UNIQUE INDEX family_id_uindex
  ON public.family (id);
CREATE UNIQUE INDEX family_name_uindex
  ON public.family (name);


CREATE TABLE public.area_of_origin
(
  id   serial PRIMARY KEY NOT NULL,
  name text               NOT NULL
);

CREATE UNIQUE INDEX area_of_origin_id_uindex
  ON public.area_of_origin (id);
CREATE UNIQUE INDEX area_of_origin_uindex
  ON public.area_of_origin (name);


ALTER TABLE public.dog
  ADD CONSTRAINT dog_area_of_origin_id_fk
FOREIGN KEY (area_of_origin_id) REFERENCES public.area_of_origin (id) ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE public.date_of_origin
(
  id   serial PRIMARY KEY NOT NULL,
  name text               NOT NULL
);
CREATE UNIQUE INDEX date_of_origin_id_uindex
  ON public.date_of_origin (id);
CREATE UNIQUE INDEX date_of_origin_name_uindex
  ON public.date_of_origin (name);

ALTER TABLE public.dog
  ADD CONSTRAINT dog_date_of_origin_id_fk
FOREIGN KEY (date_of_origin_id) REFERENCES public.date_of_origin (id) ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE public.other_dog_name
(
  id   serial PRIMARY KEY NOT NULL,
  name text               NOT NULL
);
CREATE UNIQUE INDEX other_dog_name_id_uindex
  ON public.other_dog_name (id);
CREATE UNIQUE INDEX other_dog_name_name_uindex
  ON public.other_dog_name (name);
COMMENT ON TABLE public.other_dog_name
IS 'Joined to dog via dog_to_other_dog_name table';


CREATE TABLE public.dog_to_other_dog_name
(
  id                serial PRIMARY KEY NOT NULL,
  dog_id            int                NOT NULL,
  other_dog_name_id int
);
CREATE UNIQUE INDEX dog_to_other_dog_name_id_uindex
  ON public.dog_to_other_dog_name (id);
COMMENT ON TABLE public.dog_to_other_dog_name
IS 'joins dog to other dog names';


ALTER TABLE public.dog_to_other_dog_name
  ADD CONSTRAINT dog_to_other_dog_name_dog_id_fk
FOREIGN KEY (dog_id) REFERENCES public.dog (id);


ALTER TABLE public.dog_to_other_dog_name
  ADD CONSTRAINT dog_to_other_dog_name_other_dog_name_id_fk
FOREIGN KEY (other_dog_name_id) REFERENCES public.other_dog_name (id);

CREATE TABLE public.dog_to_family
(
    id serial PRIMARY KEY NOT NULL,
    dog_id int NOT NULL,
    family_id int NOT NULL
);
CREATE UNIQUE INDEX dog_to_family_id_uindex ON public.dog_to_family (id);

ALTER TABLE public.dog_to_family
ADD CONSTRAINT dog_to_family_dog_id_fk
FOREIGN KEY (dog_id) REFERENCES public.dog (id);

ALTER TABLE public.dog_to_family
ADD CONSTRAINT dog_to_family_family_id_fk
FOREIGN KEY (family_id) REFERENCES public.family (id);

-- ******** ADD DATA *********** --
INSERT INTO category (name)
VALUES ('Hound'),
       ('Non-sporting'),
       ('Terrier'),
       ('Sporting'),
       ('Toy'),
       ('Herding'),
       ('Working');

INSERT INTO area_of_origin (name)
VALUES ('China'),
       ('Poland'),
       ('Scotland (Shetland Island)'),
       ('The Netherlands'),
       ('Australia'),
       ('England'),
       ('Mexico'),
       ('Hungary'),
       ('Cuba'),
       ('Belgium'),
       ('Japan'),
       ('Russia'),
       ('Madagascar'),
       ('Great Britain (Scotland)'),
       ('Alaska'),
       ('Middle East'),
       ('Wales'),
       ('Nova Scotia'),
       ('Iceland'),
       ('Israel'),
       ('Scotland'),
       ('Portugal'),
       ('Belgium, England'),
       ('Central Africa (Zaire and the Congo)'),
       ('Ireland'),
       ('Malta'),
       ('Spain'),
       ('South Africa'),
       ('United States'),
       ('Border of Scotland and England'),
       ('China, Tibet'),
       ('Germany'),
       ('Sweden'),
       ('France'),
       ('Yugoslavia'),
       ('France, Germany'),
       ('Italy'),
       ('Tibet'),
       ('Afghanistan'),
       ('Finland'),
       ('Germany, Central Europe'),
       ('Soviet Union'),
       ('Russia (Siberia)'),
       ('Turkey'),
       ('Canada'),
       ('Norway'),
       ('Switzerland'),
       ('Ibiza (Balearic Islands)'),
       ('Great Britain'),
       ('Mediterranean area');

INSERT INTO date_of_origin (name)
VALUES ('1600s'),
       ('1500s'),
       ('1950s'),
       ('Middle Ages'),
       ('1700s'),
       ('Unknown'),
       ('1200s'),
       ('1750'),
       ('About 1860'),
       ('Ancient times'),
       ('1900s'),
       ('Early 1200s'),
       ('1300s'),
       ('Unknown; possibly 1600s'),
       ('At least 1100s'),
       ('1100s'),
       ('1500s or earlier'),
       ('1800s'),
       ('Late 1800s'),
       ('Early 1900s'),
       ('Viking times');

INSERT INTO family (name)
VALUES ('Barbichon'),
       ('Bull'),
       ('Companion'),
       ('Flock guard'),
       ('Flockguard'),
       ('Gundog'),
       ('Hairless'),
       ('Herding'),
       ('Likestock dog'),
       ('Livestock'),
       ('Livestock dog'),
       ('Mastiff'),
       ('Mountain dog'),
       ('Northern'),
       ('Oriental'),
       ('Pinscher'),
       ('Pointer'),
       ('Primative'),
       ('Primitive'),
       ('Retriever'),
       ('Scenthound'),
       ('Schnauzer'),
       ('Setter'),
       ('Sheepdog'),
       ('Sighthound'),
       ('Spaniel'),
       ('Spitz'),
       ('Terrier'),
       ('Unknown'),
       ('Versatile hunting dog'),
       ('Water Dog'),
       ('Water dog');

SELECT * FROM dog;
