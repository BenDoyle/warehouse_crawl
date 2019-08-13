DROP TABLE IF EXISTS action_totals;
CREATE TABLE action_totals (
    player          VARCHAR(255),
    game_date       VARCHAR(255),
    game_time       VARCHAR(255),
    action_category VARCHAR(255),
    action          VARCHAR(255),
    level_group     VARCHAR(255),
    count           INTEGER
);

DROP TABLE IF EXISTS game_seed;
CREATE TABLE game_seed (
    player     VARCHAR(255),
    game_date  VARCHAR(255),
    game_time  VARCHAR(255),
    seed       VARCHAR(255)
);

DROP TABLE IF EXISTS game_version;
CREATE TABLE game_version (
    player        VARCHAR(255),
    game_date     VARCHAR(255),
    game_time     VARCHAR(255),
    full_version  VARCHAR(255),
    major         INTEGER,
    minor         INTEGER,
    patch         INTEGER,
    build         VARCHAR(255),
    style         VARCHAR(255)
);

DROP TABLE IF EXISTS final_abilities;
CREATE TABLE final_abilities (
    player        VARCHAR(255),
    game_date     VARCHAR(255),
    game_time     VARCHAR(255),
    ability       VARCHAR(255)
);

DROP TABLE IF EXISTS final_altars;
CREATE TABLE final_altars (
    player        VARCHAR(255),
    game_date     VARCHAR(255),
    game_time     VARCHAR(255),
    god           VARCHAR(255)
);

DROP TABLE IF EXISTS final_skills;
CREATE TABLE final_skills (
    player        VARCHAR(255),
    game_date     VARCHAR(255),
    game_time     VARCHAR(255),
    status        VARCHAR(255),
    rank          DECIMAL(3,1),
    skill         VARCHAR(255)
);

DROP TABLE IF EXISTS final_stats;
CREATE TABLE final_stats
(
    player             VARCHAR(255),
    game_date          VARCHAR(255),
    game_time          VARCHAR(255),
    name               VARCHAR(255),
    title              VARCHAR(255),
    species_background VARCHAR(255),
    turns              BIGINT,
    time               VARCHAR(255),
    hp                 INTEGER,
    max_hp             INTEGER,
    ac                 INTEGER,
    str                INTEGER,
    xl                 INTEGER,
    next_xl            INTEGER,
    mp                 INTEGER,
    max_mp             INTEGER,
    ev                 INTEGER,
    int                INTEGER,
    god                VARCHAR(255),
    gold               INTEGER,
    sh                 INTEGER,
    dex                INTEGER,
    spell_levels       INTEGER,
    max_spell_levels   INTEGER,
    rFire              VARCHAR(255),
    rCold              VARCHAR(255),
    rNeg               VARCHAR(255),
    rPois              VARCHAR(255),
    rElec              VARCHAR(255),
    rCorr              VARCHAR(255),
    SeeInvis           VARCHAR(255),
    Gourm              VARCHAR(255),
    Faith              VARCHAR(255),
    Spirit             VARCHAR(255),
    Reflect            VARCHAR(255),
    Harm               VARCHAR(255),
    MR                 VARCHAR(255),
    Stlth              VARCHAR(255),
    HPRegen            DECIMAL(8, 2),
    MPRegen            DECIMAL(8, 2),
    weapon             VARCHAR(255),
    shield             VARCHAR(255),
    armour             VARCHAR(255),
    helmet             VARCHAR(255),
    cloak              VARCHAR(255),
    gloves             VARCHAR(255),
    boots              VARCHAR(255),
    amulet             VARCHAR(255),
    ring_right         VARCHAR(255),
    ring_left          VARCHAR(255),
    status_effects     VARCHAR(255),
    modifiers          VARCHAR(255),
    abilities          VARCHAR(255)
);

DROP TABLE IF EXISTS final_vanquished;
CREATE TABLE final_vanquished
(
    player         VARCHAR(255),
    game_date      VARCHAR(255),
    game_time      VARCHAR(255),
    vanquished_by  VARCHAR(255),
    number         INTEGER,
    creature       VARCHAR(255),
    location       VARCHAR(255)
);


COPY action_totals FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/action_totals.csv' WITH (FORMAT csv, DELIMITER '~');
COPY game_seed FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/game_seed.csv' WITH (FORMAT csv, DELIMITER '~');
COPY game_version FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/game_version.csv' WITH (FORMAT csv, DELIMITER '~');
COPY final_abilities FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/final_abilities.csv' WITH (FORMAT csv, DELIMITER '~');
COPY final_altars FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/final_altars.csv' WITH (FORMAT csv, DELIMITER '~');
COPY final_skills FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/final_skills.csv' WITH (FORMAT csv, DELIMITER '~');
COPY final_stats FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/final_stats.csv' WITH (FORMAT csv, DELIMITER '~');
COPY final_vanquished FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/final_vanquished.csv' WITH (FORMAT csv, DELIMITER '~');

COPY altars FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/altars.csv' WITH (FORMAT csv, DELIMITER '~');
COPY bought FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/bought.csv' WITH (FORMAT csv, DELIMITER '~');
COPY fell FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/fell.csv' WITH (FORMAT csv, DELIMITER '~');
COPY found FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/found.csv' WITH (FORMAT csv, DELIMITER '~');
COPY identified FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/identified.csv' WITH (FORMAT csv, DELIMITER '~');
COPY killed FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/killed.csv' WITH (FORMAT csv, DELIMITER '~');
COPY learned FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/learned.csv' WITH (FORMAT csv, DELIMITER '~');
COPY mutation FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/mutation.csv' WITH (FORMAT csv, DELIMITER '~');
COPY noticed FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/noticed.csv' WITH (FORMAT csv, DELIMITER '~');
COPY orb FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/orb.csv' WITH (FORMAT csv, DELIMITER '~');
COPY shaft FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/shaft.csv' WITH (FORMAT csv, DELIMITER '~');
COPY skill_progression FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/skill_progression.csv' WITH (FORMAT csv, DELIMITER '~');
COPY unlearned FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/unlearned.csv' WITH (FORMAT csv, DELIMITER '~');
COPY upgrades FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/upgrades.csv' WITH (FORMAT csv, DELIMITER '~');
COPY win FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/win.csv' WITH (FORMAT csv, DELIMITER '~');
COPY worship FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/worship.csv' WITH (FORMAT csv, DELIMITER '~');
COPY xp_progression FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/xp_progression.csv' WITH (FORMAT csv, DELIMITER '~');
