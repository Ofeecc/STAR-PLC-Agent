import unittest
from plc_agent.scan_contract import ScanContract, check_contract_trace

class DataContractTests(unittest.TestCase):
    def test_all_bit_positions_and_history(self):
        for bit in range(32):
            m=ScanContract('PUB002'); mask=1<<bit
            self.assertEqual(m.step({'value':mask})['risingBits'],mask)
            self.assertEqual(m.step({'value':mask})['noOfRisingBits'],0)
            self.assertEqual(m.step({'value':0})['fallingBits'],mask)

    def test_alarm_errors_preserve_history_and_recover(self):
        m=ScanContract('PUB003'); i=dict(Value=101,hiLevel=100,loLevel=0,hystWindow=90)
        self.assertTrue(m.step(i)['hiAlarm'])
        self.assertTrue(m.step(dict(i,Value=50))['hiAlarm'])
        self.assertEqual(m.step(dict(i,loLevel=100))['status'],0x8001)
        self.assertTrue(m.step(dict(i,Value=10))['hiAlarm'])
        self.assertFalse(m.step(dict(i,Value=9))['hiAlarm'])
        with self.assertRaises(ValueError):m.step(dict(i,hystWindow=-1))

    def test_invalid_window_samples_trigger_without_accepting_value(self):
        m=ScanContract('PUB009'); i=dict(cyclicExecution=False,trigger=False,value=8.,windowSize=2,reset=False)
        self.assertEqual(m.step(dict(i,trigger=True))['average'],8.)
        m.step(i)
        self.assertTrue(m.step(dict(i,trigger=True,windowSize=0,value=99))['error'])
        self.assertEqual(m.step(dict(i,trigger=True,value=100))['average'],8.)
        m.step(i)
        self.assertEqual(m.step(dict(i,trigger=True,value=4))['average'],6.)
        self.assertEqual(m.step(dict(i,windowSize=3))['average'],0.)

    def test_ipv4_ascii_nul_leading_zero_and_capacity(self):
        m=ScanContract('PUB014')
        for text in ('+1.2.3.4','１.2.3.4','1.2.3.4\n','1.2.3.4294967296'):
            self.assertEqual(m.step({'ipText':text}),{'ipValue':0})
        self.assertEqual(m.step({'ipText':'0'*100+'1.2.3.4'})['ipValue'],16909060)
        self.assertEqual(m.step({'ipText':'1.2.3.4\0ignored'})['ipValue'],16909060)
        with self.assertRaises(ValueError):m.step({'ipText':'0'*255})

    def test_wrong_byte_order_is_rejected(self):
        result=check_contract_trace('PUB014',[{'inputs':{'ipText':'1.2.3.4'},'outputs':{'ipValue':67305985}}])
        self.assertEqual(result['status'],'VIOLATED')
