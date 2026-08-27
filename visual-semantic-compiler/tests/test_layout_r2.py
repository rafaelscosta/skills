import copy, importlib.util, json, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
core=load('layout_core',ROOT/'scripts'/'layout_core.py')
lv=load('validate_layout',ROOT/'scripts'/'validate_layout.py')
rag=json.loads((ROOT/'examples'/'concept-bridge-rag.json').read_text())
refund=json.loads((ROOT/'examples'/'clarify-refund-flow.json').read_text())
class LayoutR2Tests(unittest.TestCase):
    def test_canonical_examples_layout_valid(self):
        for ir in [rag,refund]:
            layout=core.build_layout(ir,'a'*64); r=lv.validate(layout)
            self.assertEqual(r['status'],'valid',r['errors'])
    def test_edge_through_node_fails(self):
        layout=core.build_layout(rag,'a'*64)
        n=next(x for x in layout['nodes'] if x['id']=='store'); n.update({'x':360,'y':130})
        r=lv.validate(layout)
        self.assertIn('edge-through-node',{e['code'] for e in r['errors']})
    def test_node_overlap_fails(self):
        layout=core.build_layout(rag,'a'*64); layout['nodes'][1]['x']=layout['nodes'][0]['x']; layout['nodes'][1]['y']=layout['nodes'][0]['y']
        r=lv.validate(layout); self.assertIn('node-overlap',{e['code'] for e in r['errors']})
    def test_crossing_fails_when_zero_crossings_required(self):
        layout={'schema_version':'visual-layout/v1','representation_type':'architecture','reading_direction':'left-to-right','viewport':{'width':600,'height':400,'padding':40},'nodes':[{'id':'a','x':40,'y':40,'width':80,'height':40},{'id':'b','x':480,'y':300,'width':80,'height':40},{'id':'c','x':40,'y':300,'width':80,'height':40},{'id':'d','x':480,'y':40,'width':80,'height':40}], 'edges':[{'id':'e1','from':'a','to':'b','kind':'flow','points':[[120,60],[480,320]]},{'id':'e2','from':'c','to':'d','kind':'flow','points':[[120,320],[480,60]]}], 'lifelines':[],'constraints':{'target_zero_crossings':True},'text_equivalent':'x'}
        r=lv.validate(layout); self.assertIn('edge-crossing',{e['code'] for e in r['errors']})
    def test_sequence_layout_valid(self):
        ir=copy.deepcopy(rag);ir['representation']['type']='sequence';ir['representation']['reading_direction']='top-to-bottom'
        for i,r in enumerate(ir['relationships'],1):r['order']=i
        layout=core.build_layout(ir,'b'*64);r=lv.validate(layout)
        self.assertEqual(r['status'],'valid',r['errors']);self.assertEqual(len(layout['lifelines']),len(ir['entities']))
    def test_story_strip_layout_valid(self):
        ir=copy.deepcopy(rag);ir['representation']={'class':'narrative-visual','type':'story-strip','reading_direction':'top-to-bottom','primary_question':'Como acontece?'};ir['entities']=[];ir['relationships']=[];ir['narrative_beats']=[{'id':'b1','title':'Você envia','action':'A pergunta sai','order':1},{'id':'b2','title':'O sistema responde','action':'A resposta volta','order':2}]
        layout=core.build_layout(ir,'c'*64);r=lv.validate(layout);self.assertEqual(r['status'],'valid',r['errors'])
    def test_unsupported_type_fails_closed(self):
        ir=copy.deepcopy(rag);ir['representation']['type']='bpmn'
        with self.assertRaises(ValueError):core.build_layout(ir,'d'*64)
    def test_artifact_validator_rejects_external_runtime(self):
        av=load('validate_artifact',ROOT/'scripts'/'validate_artifact.py')
        raw=b'<html><head><meta name="visual-semantic-ir-sha256" content="' + b'a'*64 + b'"><script src="https://x"></script></head><body><svg role="img"><title id="diagram-title">x</title><desc id="diagram-desc">x</desc></svg><script id="visual-receipt"></script></body></html>'
        r=av.validate_bytes(raw,'a'*64);self.assertEqual(r['status'],'invalid');self.assertIn('external-runtime',{e['code'] for e in r['errors']})
    def test_render_html_delivery_with_mocked_semantic_validator(self):
        rh=load('render_html',ROOT/'scripts'/'render_html.py'); rh.semantic_validate=lambda path:{'status':'valid','input_sha256':'e'*64}
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'rag.html'; lay=Path(td)/'rag.layout.json'; receipt=rh.deliver(ROOT/'examples'/'concept-bridge-rag.json',out,lay)
            self.assertEqual(receipt['status'],'success');self.assertTrue(out.exists());self.assertTrue(lay.exists())
            self.assertEqual(receipt['artifact_validation']['status'],'valid');self.assertEqual(receipt['perceptual_review'],'pending')
    def test_supported_structural_smoke_matrix(self):
        variants=[]
        base={'schema_version':'visual-semantic-ir/v1','source_skill':'test','intent':{'question':'q','audience':'a','language':'pt-BR'},'narrative_beats':[],'views':[],'constraints':{'target_zero_crossings':False},'omissions':[],'text_equivalent':'x'}
        x=copy.deepcopy(base);x['representation']={'class':'structural-diagram','type':'state','reading_direction':'left-to-right','primary_question':'q'};x['entities']=[{'id':'s1','label':'Draft','kind':'state'},{'id':'s2','label':'Done','kind':'state'}];x['relationships']=[{'id':'t1','from':'s1','to':'s2','kind':'transition','semantic':'finish'},{'id':'t2','from':'s2','to':'s1','kind':'transition','semantic':'reopen'}];x['groups']=[];variants.append(x)
        for typ,kind in [('dataflow','data'),('hierarchy','containment'),('causal','causation')]:
            x=copy.deepcopy(base);x['representation']={'class':'structural-diagram','type':typ,'reading_direction':'left-to-right','primary_question':'q'};x['entities']=[{'id':'a','label':'A','kind':'component'},{'id':'b','label':'B','kind':'component'}];x['relationships']=[{'id':'r','from':'a','to':'b','kind':kind,'semantic':'relates'}];x['groups']=[];variants.append(x)
        x=copy.deepcopy(base);x['representation']={'class':'structural-diagram','type':'structural-comparison','reading_direction':'top-to-bottom','primary_question':'q'};x['entities']=[{'id':'a','label':'A','kind':'component'},{'id':'b','label':'B','kind':'component'}];x['relationships']=[];x['groups']=[{'id':'g1','label':'One','kind':'comparison-side','members':['a']},{'id':'g2','label':'Two','kind':'comparison-side','members':['b']}];variants.append(x)
        for ir in variants:
            layout=core.build_layout(ir,'f'*64);r=lv.validate(layout);self.assertEqual(r['status'],'valid',(ir['representation']['type'],r['errors']))
    def test_archify_adapter_architecture_only(self):
        aa=load('adapt_archify',ROOT/'scripts'/'adapt_archify.py'); c=aa.adapt(rag)
        self.assertEqual(c['diagram_type'],'architecture');self.assertEqual(c['meta']['quality_profile'],'showcase')
        self.assertEqual(len(c['components']),len(rag['entities']));self.assertEqual(len(c['connections']),len(rag['relationships']))
        bad=copy.deepcopy(rag);bad['representation']['type']='flow'
        with self.assertRaises(ValueError):aa.adapt(bad)
if __name__=='__main__':unittest.main()
