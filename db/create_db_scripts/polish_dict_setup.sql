CREATE TEXT SEARCH DICTIONARY pl_ispell (
  TEMPLATE = ispell,
  DictFile = polish,
  AffFile  = polish,
  StopWords = polish   
);

-- Create config with default parser
CREATE TEXT SEARCH CONFIGURATION polishv2 ( PARSER = default );

-- Chain ispell with simple: first try ispell, fallback to simple
ALTER TEXT SEARCH CONFIGURATION polishv2
  ALTER MAPPING FOR asciiword, asciihword, hword_asciipart,
                     word, hword, hword_part, numword
  WITH pl_ispell, simple;