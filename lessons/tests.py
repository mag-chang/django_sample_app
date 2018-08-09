from django.test import TestCase
from lessons.calculate_logics import logics


class CalculateLogicTest(TestCase):

    def test_calculate_discount(self):
        in_list = [
            logics.VolumeDiscount(30, 3000),
            logics.VolumeDiscount(40, 2500),
        ]

        assert_list = sorted(in_list, key=lambda x:x.threshold_hour, reverse=True)

        result_list, result_hour = logics.calculate_discount(in_list, 20)
        self.compare_discount_result(result_list, result_hour, assert_list, 20)

        result_list, result_hour = logics.calculate_discount(in_list, 30)
        self.compare_discount_result(result_list, result_hour, assert_list, 30)

        assert_list[1].calculated_price = 15000
        result_list, result_hour = logics.calculate_discount(in_list, 35)
        self.compare_discount_result(result_list, result_hour, assert_list, 30)

        assert_list[1].calculated_price = 30000
        result_list, result_hour = logics.calculate_discount(in_list, 40)
        self.compare_discount_result(result_list, result_hour, assert_list, 30)

        assert_list[0].calculated_price = 12500
        result_list, result_hour = logics.calculate_discount(in_list, 45)
        self.compare_discount_result(result_list, result_hour, assert_list, 30)


    def compare_discount_result(self, result_list, result_hour, assert_list, assert_hour):
        for assert_obj, result_obj in zip(assert_list, result_list):
            self.assertEqual(assert_obj.threshold_hour, result_obj.threshold_hour)
            self.assertEqual(assert_obj.price, result_obj.price)
            self.assertEqual(assert_obj.calculated_price, result_obj.calculated_price)

        self.assertEqual(result_hour, assert_hour)


    def test_calculate_programming(self):
        self.assertEqual(logics.calculate_programming(30), 102500)
        self.assertEqual(logics.calculate_programming(32), 108500)
        self.assertEqual(logics.calculate_programming(80), 234500)
        self.assertEqual(logics.calculate_programming(60), 184500)
