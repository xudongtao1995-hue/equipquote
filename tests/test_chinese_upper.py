import unittest
from equipquote import amount_to_chinese_upper

class TestChineseUpper(unittest.TestCase):
    def test_integer(self):
        self.assertEqual(amount_to_chinese_upper(0), "零元整")
        self.assertEqual(amount_to_chinese_upper(10), "壹拾元整")
        self.assertEqual(amount_to_chinese_upper(1001), "壹仟零壹元整")

    def test_cents(self):
        self.assertEqual(amount_to_chinese_upper("1234.56"), "壹仟贰佰叁拾肆元伍角陆分")
        self.assertEqual(amount_to_chinese_upper("100.10"), "壹佰元壹角整")

    def test_wan(self):
        self.assertEqual(amount_to_chinese_upper(35000), "叁万伍仟元整")

if __name__ == "__main__":
    unittest.main()
