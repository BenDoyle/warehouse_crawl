MORGUES=data/morgues/ OUTPUT=data/ python processors/morgue_splitter/morgue_splitter-0.23.py;
path=data/0.23/notes/ python parsers/altars.py;
path=data/0.23/notes/ python parsers/bought.py;
path=data/0.23/notes/ python parsers/fell.py;
path=data/0.23/notes/ python parsers/found.py;
path=data/0.23/notes/ python parsers/identified.py;
path=data/0.23/notes/ python parsers/killed.py;
path=data/0.23/notes/ python parsers/learned.py;
path=data/0.23/notes/ python parsers/mutation.py;
path=data/0.23/notes/ python parsers/noticed.py;
path=data/0.23/notes/ python parsers/orb.py;
path=data/0.23/notes/ python parsers/shaft.py;
path=data/0.23/notes/ python parsers/skill_progression.py;
path=data/0.23/notes/ python parsers/unlearned.py;
path=data/0.23/notes/ python parsers/upgrades.py;
path=data/0.23/notes/ python parsers/win.py;
path=data/0.23/notes/ python parsers/worship.py;
path=data/0.23/notes/ python parsers/xp_progression.py;
path=data/0.23/action_totals/ python parsers/action_totals.py;
path=data/0.23/final_abilities/ python parsers/final_abilities_parser.py;
path=data/0.23/final_altars/ python parsers/final_altars_parser.py;
path=data/0.23/final_skills/ python parsers/final_skills_parser.py;
path=data/0.23/final_stats/ python parsers/final_stats_parser.py;
path=data/0.23/final_vanquished/ python parsers/final_vanquished_parser.py;
path=data/0.23/game_seed/ python parsers/game_seed_parser.py;
path=data/0.23/game_version/ python parsers/game_version_parser.py;

cat data/0.23/notes/altars/*.csv > data/0.23/altars.csv;
cat data/0.23/notes/bought/*.csv > data/0.23/bought.csv;
cat data/0.23/notes/fell/*.csv > data/0.23/fell.csv;
cat data/0.23/notes/found/*.csv > data/0.23/found.csv;
cat data/0.23/notes/identified/*.csv > data/0.23/identified.csv;
cat data/0.23/notes/killed/*.csv > data/0.23/killed.csv;
cat data/0.23/notes/learned/*.csv > data/0.23/learned.csv;
cat data/0.23/notes/mutation/*.csv > data/0.23/mutation.csv;
cat data/0.23/notes/noticed/*.csv > data/0.23/noticed.csv;
cat data/0.23/notes/orb/*.csv > data/0.23/orb.csv;
cat data/0.23/notes/shaft/*.csv > data/0.23/shaft.csv;
cat data/0.23/notes/skill_progression/*.csv > data/0.23/skill_progression.csv;
cat data/0.23/notes/unlearned/*.csv > data/0.23/unlearned.csv;
cat data/0.23/notes/upgrades/*.csv > data/0.23/upgrades.csv;
cat data/0.23/notes/win/*.csv > data/0.23/win.csv;
cat data/0.23/notes/worship/*.csv > data/0.23/worship.csv;
cat data/0.23/notes/xp_progression/*.csv > data/0.23/xp_progression.csv;

cat data/0.23/action_totals/*.csv > data/0.23/action_totals.py;
cat data/0.23/final_abilities/*.csv > data/0.23/final_abilities_parser.py;
cat data/0.23/final_altars/*.csv > data/0.23/final_altars_parser.py;
cat data/0.23/final_skills/*.csv > data/0.23/final_skills_parser.py;
cat data/0.23/final_stats/*.csv > data/0.23/final_stats_parser.py;
cat data/0.23/final_vanquished/*.csv > data/0.23/final_vanquished_parser.py;
cat data/0.23/game_seed/*.csv > data/0.23/game_seed_parser.py;
cat data/0.23/game_version/*.csv > data/0.23/game_version_parser.py;



