import importlib.util, json, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parent

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

core=load('layout_core_clarify',ROOT/'scripts'/'layout_core.py')
lv=load('validate_layout_clarify',ROOT/'scripts'/'validate_layout.py')
rh=load('render_html_clarify',ROOT/'scripts'/'render_html.py')
IR=json.loads((REPO/'clarify'/'evals'/'visual-integration'/'refund.ir.json').read_text())

class ClarifyFlowIntegrationTests(unittest.TestCase):
    def test_recovery_flow_layout_passes(self):
        layout=core.build_layout(IR,'a'*64)
        receipt=lv.validate(layout)
        self.assertEqual(receipt['status'],'valid',receipt['errors'])

    def test_recovery_edge_uses_outer_rail(self):
        layout=core.build_layout(IR,'a'*64)
        recovery=next(e for e in layout['edges'] if e['id']=='f6')
        normal_right=max(n['x']+n['width'] for n in layout['nodes'])
        self.assertGreater(max(p[0] for p in recovery['points']),normal_right)

    def test_long_operational_decision_expands_node(self):
        layout=core.build_layout(IR,'a'*64)
        eligible=next(n for n in layout['nodes'] if n['id']=='eligible')
        self.assertGreater(eligible['height'],core.NODE_H)
        self.assertGreaterEqual(len(core.wrap_label(eligible['label'])),2)

    def test_renderer_uses_multiline_tspans(self):
        layout=core.build_layout(IR,'a'*64)
        svg=rh.render_svg(IR,layout)
        self.assertIn('<tspan',svg)
        self.assertIn('Até 7 dias E sem consumo',svg)
        self.assertIn('premium?',svg)

if __name__=='__main__': unittest.main()
