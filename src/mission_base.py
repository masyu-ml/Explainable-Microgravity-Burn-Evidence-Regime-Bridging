"""Fix Material Brief audio contamination from adjacent clips; no physics changes."""
import json as _json
import voice_sync as _prior
import original as _ember

_js = _ember.APP_JS
_anchor = "const VOICE_CLIPS="
_start = _js.index(_anchor)
_end = _js.index(";", _start)
_clips = _json.loads(_js[_start + len(_anchor):_end])
_fix = {"desc_pmma":[45.48,63],"desc_sibal":[63.46,79.79],"desc_cellulose":[80.3,97.13],"desc_ldpe":[97.63,113.26],"desc_nca":[113.78,129.36],"desc_threshold":[129.89,143.01]}
assert len(_fix) == 6
for _key, (_begin, _finish) in _fix.items():
    assert _key in _clips["base"], "Missing brief: " + _key
    assert _begin < _finish
    _clips["base"][_key] = [_begin, _finish]
_order = list(_fix.values())
assert all(_order[i][1] + 0.3 < _order[i + 1][0] for i in range(len(_order) - 1)), "Clip boundaries overlap"
_ember.APP_JS = (
    _js[:_start] + _anchor + _json.dumps(_clips, separators=(",", ":")) + ";"
    + _js[_end + 1:]
)
app = _ember.app
