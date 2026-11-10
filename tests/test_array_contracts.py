import unittest
from copy import deepcopy

from plc_agent.array_contracts import analog_field_matches
from plc_agent.data_contracts import real32
from plc_agent.scan_contract import ScanContract, check_contract_trace


def channel(**changes):
    return dict(dict(enable=True,hiLIM=100.,loLIM=0.,bipolar=False,measuringMode=0,retVal=7,outputValue=-999.),**changes)

class ArrayContractTests(unittest.TestCase):
    def test_pump_ties_readonly_and_stop_priority(self):
        i=dict(mode=True,start=True,stop=False,pumpGroup=[dict(priority=-1,selection=False,RunComd=False) for _ in range(5)])
        before=deepcopy(i);m=ScanContract('PUB007');o=m.step(i)
        self.assertEqual([p['RunComd'] for p in o['pumpGroup']],[True,True,True,False,False]);self.assertEqual(i,before)
        self.assertFalse(any(p['RunComd'] for p in m.step(dict(i,stop=True))['pumpGroup']))
        bad=deepcopy(o);bad['pumpGroup'][0]['priority']=0
        self.assertEqual(check_contract_trace('PUB007',[dict(inputs=i,outputs=bad)])['status'],'VIOLATED')

    def test_pump_configuration_change_without_start_preserves_commands(self):
        pumps=[dict(priority=j,selection=True,RunComd=j<2) for j in range(5)]
        o=ScanContract('PUB007').step(dict(mode=True,start=False,stop=False,pumpGroup=pumps))
        self.assertEqual(o['pumpGroup'],pumps)

    def test_unequal_lengths_preserve_skipped_channel_and_inputs(self):
        i=dict(count=1,analogValues=[27648],channels=[channel(),channel(outputValue=33.)]);saved=deepcopy(i)
        o=ScanContract('PUB008').step(i)
        self.assertEqual(o['channels'][0]['outputValue'],100.)
        self.assertEqual(o['channels'][1],i['channels'][1]);self.assertEqual(i,saved)
        with self.assertRaises(ValueError):ScanContract('PUB008').step(dict(i,count=2))

    def test_invalid_mode_wins_and_preserves_output(self):
        i=dict(count=1,analogValues=[1],channels=[channel(measuringMode=9,hiLIM=0,loLIM=10)])
        o=ScanContract('PUB008').step(i)
        self.assertEqual(o['channels'][0]['retVal'],0x8001)
        self.assertEqual(o['channels'][0]['outputValue'],-999.)

    def test_real_rounding_tolerance_does_not_apply_to_readonly_or_preserved(self):
        i=dict(count=1,analogValues=[27648],channels=[channel(hiLIM=1000000.1)])
        expected=ScanContract('PUB008').step(i)['channels'];actual=deepcopy(expected)
        actual[0]['outputValue']=real32(expected[0]['outputValue'])
        self.assertTrue(analog_field_matches('channels',actual,expected,i))
        actual[0]['hiLIM']+=0.000001
        self.assertFalse(analog_field_matches('channels',actual,expected,i))
        i['channels'][0]['enable']=False;expected=ScanContract('PUB008').step(i)['channels'];actual=deepcopy(expected)
        actual[0]['outputValue']+=0.000001
        self.assertFalse(analog_field_matches('channels',actual,expected,i))

    def test_bipolar_int_max_uses_wide_intermediate(self):
        o=ScanContract('PUB008').step(dict(count=1,analogValues=[32767],channels=[channel(bipolar=True,loLIM=-27648.,hiLIM=27648.)]))
        self.assertEqual(o['channels'][0]['outputValue'],32767.)
