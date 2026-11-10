import unittest
from plc_agent.dataset import load_tasks
from plc_agent.scan_contract import ScanContract,check_contract_trace

class ProcessContractTests(unittest.TestCase):
    def defaults(self,tid):
        t=next(t for t in load_tasks() if t['id']==tid)
        return {f['name']:False if f['type']=='BOOL' else 0 for f in t['interface'] if f['direction']=='INPUT'}

    def test_manual_each_actuator_toggles_independently(self):
        buttons=['valveAStart','valveBStart','valveCStart','valveDStart','mixMotorStart']
        outputs=['valveARun','valveBRun','valveCRun','valveDRun','mixMotorRun']
        for b,o in zip(buttons,outputs):
            m=ScanContract('PUB015');i=dict(self.defaults('PUB015'),estop=True)
            self.assertEqual(m.step(dict(i,**{b:True})),{n:n==o for n in outputs})
            m.step(i)
            self.assertFalse(any(m.step(dict(i,**{b:True})).values()))

    def test_batch_mode_change_is_domain_violation(self):
        m=ScanContract('PUB015');i=dict(self.defaults('PUB015'),estop=True,opeMode=True,autoStart=True)
        m.step(i)
        with self.assertRaises(ValueError):m.step(dict(i,processMode=True))

    def test_sequence_change_during_movement_rejected(self):
        m=ScanContract('PUB016');i=dict(self.defaults('PUB016'),processLength=2,processSequence=[2,5,0,0,0,0,0,0],sensor1=True,station1Start=True)
        m.step(i)
        with self.assertRaises(ValueError):m.step(dict(i,processSequence=[3,5,0,0,0,0,0,0]))

    def test_all_stopped_feed_and_wrong_discharge_rejected(self):
        i=dict(self.defaults('PUB020'),Mode=True,SensorFeed=True)
        result=check_contract_trace('PUB020',[dict(inputs=i,outputs=dict(MotorForward=False,MotorReverse=False,kick=False,CompletionLight=False,firingTemp=0))])
        self.assertEqual(result['status'],'VIOLATED')
        i=dict(self.defaults('PUB015'),estop=True,opeMode=True,autoStart=True)
        result=check_contract_trace('PUB015',[dict(inputs=i,outputs=dict(valveARun=False,valveBRun=False,valveCRun=False,valveDRun=True,mixMotorRun=False))])
        self.assertEqual(result['status'],'VIOLATED')

    def test_mechanical_arm_mode_change_and_safety(self):
        m = ScanContract('PUB019')
        base = dict(self.defaults('PUB019'), EmergencyStop=True, UpLimitSwitch=True, LeftLimitSwitch=True)
        # Manual mode opposing commands both suppressed
        res = m.step(dict(base, ManualMode=True, DownButton=True, UpButton=True))
        self.assertFalse(res['MoveDown'])
        self.assertFalse(res['MoveUp'])

        # Emergency stop clears all outputs
        res = m.step(dict(base, ManualMode=True, DownButton=True, EmergencyStop=False))
        self.assertFalse(res['MoveDown'])

        # Mode change suppresses commands on transition scan
        m = ScanContract('PUB019')
        m.step(dict(base, ManualMode=True))
        res = m.step(dict(base, SingleCycleMode=True, Start=True))
        self.assertFalse(any(res.values()))
