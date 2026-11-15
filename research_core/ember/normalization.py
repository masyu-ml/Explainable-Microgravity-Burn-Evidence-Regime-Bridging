from __future__ import annotations
import re

ALIASES={
 "PMMA":{"pmma","polymethyl methacrylate","polymethylmethacrylate","acrylic","clear pmma","black pmma"},
 "SIBAL":{"sibal","sibal fabric","cotton fiberglass","cotton/fiberglass","75% cotton 25% fiberglass","sibal cotton fiberglass"},
 "KIMWIPES":{"kimwipes","kimwipe","thin cellulose","cellulose research fuel"},
 "LDPE":{"ldpe","low density polyethylene","ldpe insulation","ldpe insulated wire"},
 "MYLAR_G":{"mylar","mylar g"},
 "ULTEM_1000":{"ultem","ultem 1000"},
 "NOMEX_HT90_40":{"nomex","nomex ht90-40","nomex ht90 40"},
 "HDPE":{"hdpe","high density polyethylene"},
 "DELRIN":{"delrin","pom","polyoxymethylene"},
}
GEOM={
 "ROD":{"rod","pmma rod","clear pmma rod","black pmma rod","cylinder","cylindrical rod","rod axial stagnation","axial stagnation rod","stagnation rod","rod concurrent","concurrent rod"},
 "THICK_SLAB":{"slab","thick slab","thick slab concurrent","concurrent slab","slab concurrent","thick pmma slab","pmma thick slab","concurrent flame spread slab"},
 "THIN_FABRIC_CONCURRENT":{"thin fabric concurrent","sibal concurrent","fabric concurrent","concurrent fabric"},
 "THIN_SHEET_CONCURRENT":{"thin sheet concurrent","kimwipes concurrent","cellulose concurrent"},
 "THIN_SHEET_OPPOSED_NCA":{"thin sheet opposed nca","nca","narrow channel apparatus","pmma nca","thin pmma opposed"},
 "WIRE_OPPOSED":{"wire opposed","ldpe wire","insulated wire","opposed wire","downward wire"},
}
EARTH_G_ATOL=1e-3
MICRO_G_ATOL=1e-6
def normalize_text(value:str)->str:
 s=value.strip().lower().replace("_"," ").replace("-"," "); return re.sub(r"\s+"," ",s)
def canonical_material(value:str):
 v=normalize_text(value)
 for k,vals in ALIASES.items():
  if v in {normalize_text(x) for x in vals}: return k
 return None
def canonical_geometry(value:str):
 v=normalize_text(value)
 for k,vals in GEOM.items():
  if v in {normalize_text(x) for x in vals}: return k
 return None
def is_earth_gravity(g:float)->bool:return abs(float(g)-1.0)<=EARTH_G_ATOL
def is_microgravity(g:float)->bool:return abs(float(g))<=MICRO_G_ATOL
def is_endpoint_gravity(g:float)->bool:return is_earth_gravity(g) or is_microgravity(g)
