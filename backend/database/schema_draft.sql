-- ClimateLens – draft schema 

CREATE EXTENSION IF NOT EXISTS vector;

-- Where the data comes from
CREATE TABLE sources (
    id       SERIAL PRIMARY KEY,
    name     TEXT NOT NULL UNIQUE,      
    url      TEXT,
    license  TEXT                       
);

-- Countries, regions and the world
CREATE TABLE countries (
    id         SERIAL PRIMARY KEY,
    code       VARCHAR(10) NOT NULL UNIQUE,
    name       TEXT NOT NULL,
    kind       TEXT NOT NULL DEFAULT 'country'
               CHECK (kind IN ('country', 'region', 'world')),
    continent  TEXT
);

-- What is measured
CREATE TABLE indicators (
    id           SERIAL PRIMARY KEY,
    code         TEXT NOT NULL UNIQUE,       
    name         TEXT NOT NULL,               
    unit         TEXT NOT NULL,               
    frequency    TEXT NOT NULL
                 CHECK (frequency IN ('annual', 'monthly')),
    description  TEXT,
    source_id    INTEGER NOT NULL REFERENCES sources (id)
);

-- One measurement: a value for a country, an indicator and a period
CREATE TABLE observations (
    country_id    INTEGER NOT NULL REFERENCES countries (id),
    indicator_id  INTEGER NOT NULL REFERENCES indicators (id),
    period        DATE NOT NULL
                  CHECK (EXTRACT(DAY FROM period) = 1),
    value         DOUBLE PRECISION NOT NULL,
    loaded_at     TIMESTAMPTZ NOT NULL DEFAULT now(),

    PRIMARY KEY (country_id, indicator_id, period)
);

-- For the world map: one indicator, one period, all countries
CREATE INDEX idx_observations_indicator_period
    ON observations (indicator_id, period);

-- We transform the large format to the long format