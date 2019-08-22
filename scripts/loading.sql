DROP TABLE IF EXISTS action_totals;
CREATE TABLE action_totals (
    player          VARCHAR(255),
    game_date_key   INTEGER,
    game_at         TIMESTAMP,
    action_category VARCHAR(255),
    action          VARCHAR(255),
    level_group     VARCHAR(255),
    count           INTEGER
);
COPY action_totals FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/action_totals.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM action_totals;

DROP TABLE IF EXISTS game_seed;
CREATE TABLE game_seed (
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    seed           VARCHAR(255)
);
COPY game_seed FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/game_seed.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM game_seed;

DROP TABLE IF EXISTS game_version;
CREATE TABLE game_version (
    player        VARCHAR(255),
    game_date_key INTEGER,
    game_at       TIMESTAMP,
    full_version  VARCHAR(255),
    major         INTEGER,
    minor         INTEGER,
    patch         INTEGER,
    build         INTEGER,
    build_detail  VARCHAR(255),
    style         VARCHAR(255),
    malformed     BOOLEAN
);
COPY game_version FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/game_version.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM game_version;

DROP TABLE IF EXISTS final_abilities;
CREATE TABLE final_abilities (
    player        VARCHAR(255),
    game_date_key INTEGER,
    game_at       TIMESTAMP,
    ability       VARCHAR(255)
);
COPY final_abilities FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/final_abilities.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM final_abilities;

DROP TABLE IF EXISTS final_altars;
CREATE TABLE final_altars (
    player        VARCHAR(255),
    game_date_key INTEGER,
    game_at       TIMESTAMP,
    god           VARCHAR(255)
);
COPY final_altars FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/final_altars.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT a.god, count(1) from final_altars as a group by a.god ORDER BY 2 DESC;

DROP TABLE IF EXISTS final_skills;
CREATE TABLE final_skills (
    player        VARCHAR(255),
    game_date_key INTEGER,
    game_at       TIMESTAMP,
    status        VARCHAR(255),
    rank          DECIMAL(3,1),
    skill         VARCHAR(255)
);
COPY final_skills FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/final_skills.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT skill, sum(rank) FROM final_skills group by 1 order by 2 desc;


DROP TABLE IF EXISTS final_stats;
CREATE TABLE final_stats
(
    player             VARCHAR(255),
    game_date_key      INTEGER,
    game_at            TIMESTAMP,
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
COPY final_stats FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/final_stats.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM final_stats WHERE hp IS NOT NULL ORDER BY hp DESC;

DROP TABLE IF EXISTS final_vanquished;
CREATE TABLE final_vanquished
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    vanquished_by  VARCHAR(255),
    number         INTEGER,
    creature       VARCHAR(255),
    location       VARCHAR(255)
);
COPY final_vanquished FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/final_vanquished.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT count(1) FROM final_vanquished;
SELECT * FROM final_vanquished;

DROP TABLE IF EXISTS altars;
CREATE TABLE altars
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255),
    ornamentation  VARCHAR(255),
    god            VARCHAR(255)
);
COPY altars FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/altars.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM altars;

DROP TABLE IF EXISTS bought;
CREATE TABLE bought
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255),

    bought         VARCHAR(255),
    price          INTEGER
);
COPY bought FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/bought.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM bought;

DROP TABLE IF EXISTS conclusion;
CREATE TABLE conclusion
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   VARCHAR(255),
    note           VARCHAR(255),

    final_status   VARCHAR(255),
    how            VARCHAR(255),
    who            VARCHAR(255)
);
COPY conclusion FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/conclusion.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM conclusion;

DROP TABLE IF EXISTS fell;
CREATE TABLE fell
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255),

    god         VARCHAR(255)
);
COPY fell FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/fell.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM fell;

DROP TABLE IF EXISTS found;
CREATE TABLE found
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255),

    found         VARCHAR(255)
);
COPY found FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/found.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM found;

DROP TABLE IF EXISTS identified;
CREATE TABLE identified
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255),

    identified     VARCHAR(255)
);
COPY identified FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/identified.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM identified;

DROP TABLE IF EXISTS killed;
CREATE TABLE killed
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255),

    monster_type   VARCHAR(255),
    monster        VARCHAR(255)
);
COPY killed FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/killed.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM killed;

DROP TABLE IF EXISTS learned;
CREATE TABLE learned
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255),

    spell_level    INTEGER,
    spell_name     VARCHAR(255)
);
COPY learned FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/learned.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM learned;


DROP TABLE IF EXISTS mutation;
CREATE TABLE mutation
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255),

    status         VARCHAR(255),
    mutation       VARCHAR(255),
    source         VARCHAR(255)
);
COPY mutation FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/mutation.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM mutation;

DROP TABLE IF EXISTS noticed;
CREATE TABLE noticed
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255),

    monster_type   VARCHAR(255),
    monster        VARCHAR(255)
);
COPY noticed FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/noticed.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM noticed;

DROP TABLE IF EXISTS orb;
CREATE TABLE orb
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255)
);
COPY orb FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/orb.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM orb;

DROP TABLE IF EXISTS rune;
CREATE TABLE rune
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255),
    rune           VARCHAR(255)
);
COPY rune FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/rune.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM rune;

DROP TABLE IF EXISTS shaft;
CREATE TABLE shaft
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255),

    floors         INTEGER
);
COPY shaft FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/shaft.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM shaft;

DROP TABLE IF EXISTS skill_progression;
CREATE TABLE skill_progression
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255),

    skill_level    INTEGER,
    skill_name     VARCHAR(255)
);
COPY skill_progression FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/skill_progression.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM skill_progression;

DROP TABLE IF EXISTS unlearned;
CREATE TABLE unlearned
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255),

    spell_name     VARCHAR(255)
);
COPY unlearned FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/unlearned.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM unlearned;

DROP TABLE IF EXISTS upgrades;
CREATE TABLE upgrades
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255),

    major          INTEGER,
    minor          INTEGER,
    patch          INTEGER,
    build          INTEGER,
    build_detail   VARCHAR(255)
);
COPY upgrades FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/upgrades.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM upgrades;

DROP TABLE IF EXISTS win;
CREATE TABLE win
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   VARCHAR(255),
    note           VARCHAR(255)
);
COPY win FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/win.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM win;


DROP TABLE IF EXISTS worship;
CREATE TABLE worship
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255),

    god         VARCHAR(255)
);
COPY worship FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/worship.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM worship;


DROP TABLE IF EXISTS xp_progression;
CREATE TABLE xp_progression
(
    player         VARCHAR(255),
    game_date_key  INTEGER,
    game_at        TIMESTAMP,
    turn           INTEGER,
    branch         VARCHAR(255),
    branch_level   INTEGER,
    note           VARCHAR(255),

    xp_level       INTEGER,
    hp             INTEGER,
    mp             INTEGER
);
COPY xp_progression FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/0.23/summaries/xp_progression.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM xp_progression;



DROP TABLE IF EXISTS dimension_species_background;
CREATE TABLE dimension_species_background
(
    "Species Background Key"            INTEGER,
    "From Game Version"                 INTEGER,
    "To Game Version"                   INTEGER,
    "Species"                           VARCHAR(255),
    "Species Abreviated"                VARCHAR(255),
    "Background Group"                  VARCHAR(255),
    "Background"                        VARCHAR(255),
    "Background Abreviated"             VARCHAR(255),
    "Species And Background"            VARCHAR(255),
    "Species And Background Abreviated" VARCHAR(255)
);
COPY dimension_species_background FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/data/static/species_background.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM dimension_species_background;


DROP TABLE IF EXISTS dimension_locations;
CREATE TABLE dimension_locations
(
    "Location Key"                      INTEGER,
    "From Game Version"                 INTEGER,
    "To Game Version"                   INTEGER,
    "Abreviated Floor"                  VARCHAR(255),
    "Abreviated Branch"                 VARCHAR(255),
    "Branch Group"                      VARCHAR(255),
    "Branch"                            VARCHAR(255),
    "Branch Required"                   VARCHAR(255),
    "Floor Has Rune"                    VARCHAR(255)
);
COPY dimension_locations FROM '/Users/ben/src/github.com/bendoyle/warehouse_crawl/static/locations.csv' WITH (FORMAT csv, DELIMITER '~');
SELECT * FROM dimension_locations
