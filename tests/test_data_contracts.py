import unittest

from plc_agent.scan_contract import ScanContract, check_contract_trace


class DataContractTests(unittest.TestCase):
    def test_all_bit_positions_and_history(self):
        for bit in range(32):
            m = ScanContract("PUB002")
            mask = 1 << bit
            self.assertEqual(m.step({"value": mask})["risingBits"], mask)
            self.assertEqual(m.step({"value": mask})["noOfRisingBits"], 0)
            self.assertEqual(m.step({"value": 0})["fallingBits"], mask)

    def test_alarm_errors_preserve_history_and_recover(self):
        m = ScanContract("PUB003")
        i = dict(Value=101, hiLevel=100, loLevel=0, hystWindow=90)
        self.assertTrue(m.step(i)["hiAlarm"])
        self.assertTrue(m.step(dict(i, Value=50))["hiAlarm"])
        self.assertEqual(m.step(dict(i, loLevel=100))["status"], 0x8001)
        self.assertTrue(m.step(dict(i, Value=10))["hiAlarm"])
        self.assertFalse(m.step(dict(i, Value=9))["hiAlarm"])
        with self.assertRaises(ValueError):
            m.step(dict(i, hystWindow=-1))

    def test_invalid_window_samples_trigger_without_accepting_value(self):
        m = ScanContract("PUB009")
        i = dict(cyclicExecution=False, trigger=False, value=8.0, windowSize=2, reset=False)
        self.assertEqual(m.step(dict(i, trigger=True))["average"], 8.0)
        m.step(i)
        self.assertTrue(m.step(dict(i, trigger=True, windowSize=0, value=99))["error"])
        self.assertEqual(m.step(dict(i, trigger=True, value=100))["average"], 8.0)
        m.step(i)
        self.assertEqual(m.step(dict(i, trigger=True, value=4))["average"], 6.0)
        self.assertEqual(m.step(dict(i, windowSize=3))["average"], 0.0)

    def test_ipv4_ascii_nul_leading_zero_and_capacity(self):
        m = ScanContract("PUB014")
        for text in ("+1.2.3.4", "１.2.3.4", "1.2.3.4\n", "1.2.3.4294967296"):
            self.assertEqual(m.step({"ipText": text}), {"ipValue": 0})
        self.assertEqual(m.step({"ipText": "0" * 100 + "1.2.3.4"})["ipValue"], 16909060)
        self.assertEqual(m.step({"ipText": "1.2.3.4\0ignored"})["ipValue"], 16909060)
        with self.assertRaises(ValueError):
            m.step({"ipText": "0" * 255})

    def test_wrong_byte_order_is_rejected(self):
        result = check_contract_trace("PUB014", [{"inputs": {"ipText": "1.2.3.4"}, "outputs": {"ipValue": 67305985}}])
        self.assertEqual(result["status"], "VIOLATED")

    def test_recipe_management_crud_and_errors(self):
        m = ScanContract("PUB017")
        rec1 = dict(recipeID=1, ingredientType=10, ingredientRatio=0.5, productionTemperature=80.0)
        rec2 = dict(recipeID=2, ingredientType=20, ingredientRatio=0.2, productionTemperature=60.0)
        # Query nonexistent recipe
        res = m.step(dict(addRecipe=False, deleteRecipe=False, modifyRecipe=False, queryRecipe=True, recipeIn=rec1))
        self.assertTrue(res["error"])
        self.assertEqual(res["status"], 0x8001)

        # Add recipe
        m.step(dict(addRecipe=False, deleteRecipe=False, modifyRecipe=False, queryRecipe=False, recipeIn=rec1))
        res = m.step(dict(addRecipe=True, deleteRecipe=False, modifyRecipe=False, queryRecipe=False, recipeIn=rec1))
        self.assertTrue(res["recipeAdded"])
        self.assertFalse(res["error"])
        self.assertEqual(res["status"], 0)

        # Duplicate add
        m.step(dict(addRecipe=False, deleteRecipe=False, modifyRecipe=False, queryRecipe=False, recipeIn=rec1))
        res = m.step(dict(addRecipe=True, deleteRecipe=False, modifyRecipe=False, queryRecipe=False, recipeIn=rec1))
        self.assertTrue(res["error"])
        self.assertEqual(res["status"], 0x8002)

        # Query existing recipe
        m.step(dict(addRecipe=False, deleteRecipe=False, modifyRecipe=False, queryRecipe=False, recipeIn=rec1))
        res = m.step(dict(addRecipe=False, deleteRecipe=False, modifyRecipe=False, queryRecipe=True, recipeIn=rec1))
        self.assertFalse(res["error"])
        self.assertEqual(res["recipeQueryResult"]["recipeID"], 1)

        # Modify nonexistent
        m.step(dict(addRecipe=False, deleteRecipe=False, modifyRecipe=False, queryRecipe=False, recipeIn=rec2))
        res = m.step(dict(addRecipe=False, deleteRecipe=False, modifyRecipe=True, queryRecipe=False, recipeIn=rec2))
        self.assertTrue(res["error"])
        self.assertEqual(res["status"], 0x8005)

        # Delete nonexistent
        m.step(dict(addRecipe=False, deleteRecipe=False, modifyRecipe=False, queryRecipe=False, recipeIn=rec2))
        res = m.step(dict(addRecipe=False, deleteRecipe=True, modifyRecipe=False, queryRecipe=False, recipeIn=rec2))
        self.assertTrue(res["error"])
        self.assertEqual(res["status"], 0x8004)

    def test_fifo_queue_wrap_overflow_and_reset(self):
        m = ScanContract("PUB018")
        binding = {"$binding": "buffer", "binding_id": "A", "retain_storage": True}
        # Dequeue from empty
        res = m.step(dict(enqueue=False, dequeue=True, reset=False, item=99, buffer=binding))
        self.assertEqual(res["status"], 0x8001)
        self.assertEqual(res["elementCount"], 0)
        self.assertEqual(res["item"], 99)

        # Enqueue item 10
        m.step(dict(enqueue=False, dequeue=False, reset=False, item=0, buffer=binding))
        res = m.step(dict(enqueue=True, dequeue=False, reset=False, item=10, buffer=binding))
        self.assertEqual(res["elementCount"], 1)
        self.assertEqual(res["status"], 0)

        # Enqueue item 20
        m.step(dict(enqueue=False, dequeue=False, reset=False, item=0, buffer=binding))
        res = m.step(dict(enqueue=True, dequeue=False, reset=False, item=20, buffer=binding))
        self.assertEqual(res["elementCount"], 2)
        self.assertEqual(res["status"], 0)

        # Enqueue when full (capacity 2 for binding A)
        m.step(dict(enqueue=False, dequeue=False, reset=False, item=0, buffer=binding))
        res = m.step(dict(enqueue=True, dequeue=False, reset=False, item=30, buffer=binding))
        self.assertEqual(res["status"], 0x8002)
        self.assertEqual(res["elementCount"], 2)

        # Reset priority
        res = m.step(dict(enqueue=True, dequeue=False, reset=True, item=40, buffer=binding))
        self.assertEqual(res["elementCount"], 0)
        self.assertEqual(res["status"], 0)
