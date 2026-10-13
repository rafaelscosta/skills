import argparse,json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[2]
def validate_handoff(contract,manifest,qa):
 errors=[]
 for value,relative in [(contract,'video-edit-contract/references/video-edit-contract.schema.json'),(manifest,'footage-intelligence/references/asset-manifest.schema.json'),(qa,'supervising-video-editor/references/editorial-qa.schema.json')]:
  schema=json.loads((ROOT/relative).read_text());Draft202012Validator.check_schema(schema)
  errors.extend(e.message for e in Draft202012Validator(schema).iter_errors(value))
 if errors:return errors
 assets={a['id']:a for a in manifest['assets']}
 if len(assets)!=len(manifest['assets']):errors.append('duplicate asset IDs')
 for segment in manifest['segments']:
  asset=assets.get(segment['asset_id'])
  if asset is None:errors.append('unknown segment asset')
  elif asset['inspected'] is not True or not asset['source_locator']:errors.append('observed segment requires an inspected, located asset')
 return errors
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('contract',type=Path);parser.add_argument('manifest',type=Path);parser.add_argument('qa',type=Path);args=parser.parse_args()
 errors=validate_handoff(*[json.loads(p.read_text()) for p in [args.contract,args.manifest,args.qa]])
 print(json.dumps({'scope':'SOURCE_CONTRACT_ONLY','errors':errors,'passed':not errors},indent=2));raise SystemExit(bool(errors))
