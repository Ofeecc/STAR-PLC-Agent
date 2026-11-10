import unittest
from plc_agent.scan_contract import ScanContract,check_contract_trace
from plc_agent.timed_contracts import duration_ns
from plc_agent.functional import outputs_equal

class TimedContractTests(unittest.TestCase):
    def test_startup_must_not_credit_gap_during_inhibition(self):
        m=ScanContract('PUB005');i=dict(Gap_Exceeded=True,Weld_E_Stop_NC=True,DebounceTime='T#2s')
        self.assertTrue(m.step(i,9000)['Weld_Soft_Start_Active'])
        self.assertFalse(m.step(i,5000)['Operator_Alert'])
        self.assertFalse(m.step(i,1999)['Operator_Alert'])
        self.assertTrue(m.step(i,1)['Operator_Alert'])

    def test_debounce_completed_then_estop_requires_new_interval(self):
        m=ScanContract('PUB004');i=dict(VISCOSITY_OK=True,PASTE_E_STOP_NC=True,DebounceTime='T#1s',CycleTime='T#100ms')
        self.assertFalse(m.step(i,0)['VFD_RUN'])
        self.assertTrue(m.step(i,1000)['VFD_RUN'])
        self.assertFalse(m.step(dict(i,PASTE_E_STOP_NC=False),100)['VFD_RUN'])
        self.assertFalse(m.step(i,2000)['VFD_RUN'])
        self.assertFalse(m.step(i,999)['VFD_RUN'])
        self.assertEqual(m.step(i,1)['PUMP_RUNTIME_ACC'],'LTIME#200ms')

    def test_retrigger_restarts_hold_and_invalid_clears_it(self):
        m=ScanContract('PUB012');i=dict(THICKNESS_FAULT=True,THICKNESS_SIGNAL_VALID=True,CUTTING_RUN=False,FaultTimestamp=11,CycleTime='T#100ms')
        m.step(i,0);m.step(dict(i,THICKNESS_FAULT=False),400)
        o=m.step(dict(i,FaultTimestamp=22),50)
        self.assertEqual(o['Slab_Fault_History'],[22,11,0,0,0])
        self.assertTrue(m.step(dict(i,THICKNESS_FAULT=False),499)['THICKNESS_ALARM'])
        self.assertFalse(m.step(dict(i,THICKNESS_SIGNAL_VALID=False),1)['THICKNESS_ALARM'])
        self.assertEqual(m.step(dict(i,FaultTimestamp=33),0)['Slab_Fault_Counter'],3)

    def test_night_clears_timer_but_non_night_mode_switch_preserves(self):
        m=ScanContract('PUB013');i=dict(OCCUPANCY_DETECTED=True,ENERGY_SAVING_MODE=False,HVAC_MODE_SELECTOR=0)
        m.step(i,0)
        self.assertTrue(m.step(dict(i,HVAC_MODE_SELECTOR=1),30000)['SUPPLY_FAN_RUN'])
        self.assertFalse(m.step(dict(i,HVAC_MODE_SELECTOR=3),0)['SUPPLY_FAN_RUN'])
        self.assertFalse(m.step(i,40000)['SUPPLY_FAN_RUN'])

    def test_time_values_not_text_and_strings_still_exact(self):
        t={'interface':[dict(name='x',direction='OUTPUT',type='LTIME')]}
        self.assertTrue(outputs_equal(t,{'x':'LTIME#1s'},{'x':'LTIME#1000ms'}))
        t['interface'][0]['type']='STRING(100)'
        self.assertFalse(outputs_equal(t,{'x':'LTIME#1s'},{'x':'LTIME#1000ms'}))
        self.assertEqual(duration_ns('T#1h30m'),5400000000000)
        for v in ('T#1sBAD','T#-1s','1s','T#0.1ns'):
            with self.assertRaises(ValueError):duration_ns(v)

    def test_early_blower_is_rejected(self):
        rows=[dict(inputs=dict(DO_LOW=True,AERATION_E_STOP_NC=True),dt_ms=0,
                   outputs=dict(BLOWER_RUN=True,AERATION_BLOWER_CYCLE_COUNT=1))]
        self.assertEqual(check_contract_trace('PUB006',rows)['status'],'VIOLATED')

    def test_missing_timestamp_and_changed_debounce_are_rejected(self):
        m=ScanContract('PUB005');i=dict(Gap_Exceeded=True,Weld_E_Stop_NC=True,DebounceTime='T#2s')
        with self.assertRaises(ValueError):m.step(i)
        m.step(i,0)
        with self.assertRaises(ValueError):m.step(dict(i,DebounceTime='T#3s'),100)
