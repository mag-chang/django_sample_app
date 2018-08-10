from typing import List

class VolumeDiscount(object):
    def __init__(self, threshold_hour, price, calculated_price=None):
        """
        従量料金の累積時間による割引のためのオブジェクト
        :param threshold_hour: 時間のしきい値
        :param price: その時間を超過した場合の料金
        :param calculated_price: 割引計算済みの料金(calculate_discount関数にてセット)
        """
        self.threshold_hour = threshold_hour
        self.price = price
        self.calculated_price = calculated_price


def deco_check_zero_hour(func):
    """
    lesson_hourが0なら、0をreturnする
    """
    def _deco_check_zero_hour(*args, **kwargs):
        if args[1] == 0:
            return 0
        return func(*args, **kwargs)
    return _deco_check_zero_hour


class Logics(object):

    @deco_check_zero_hour
    def calculate_english(self, lesson_hour):
        """
        英語の料金計算
        :param lesson_hour: 累計時間
        :return: 従量の割引など、全て計算済みの合計金額
        """
        base_price = 5000
        volume_price = 3500
        return base_price + (lesson_hour * volume_price)

    @deco_check_zero_hour
    def calculate_programming(self, lesson_hour):
        """
        プログラミングの料金計算
        :param lesson_hour: 累計時間
        :return: 従量の割引など、全て計算済みの合計金額
        """
        base_price = 20000
        include_hour = 5
        volume_price = 3500

        volume_discount_list = [
            VolumeDiscount(20, 3000),
            VolumeDiscount(35, 2800),
            VolumeDiscount(50, 2500),
        ]

        calculated_discount_list, not_discount_hour = self.calculate_discount(volume_discount_list, lesson_hour)

        # 割引対象外時間から基本含有時間を減算後、通常料金で計算して基本料金を加える
        total_price = base_price + (volume_price * (not_discount_hour - include_hour))

        # 割引計算済みの料金があれば加算
        for volume_discount in calculated_discount_list:
            if volume_discount.calculated_price:
                total_price = total_price + volume_discount.calculated_price

        return total_price

    @deco_check_zero_hour
    def calculate_finance(self, lesson_hour):
        """
        ファイナンスの料金計算
        :param lesson_hour: 累計時間
        :return: 従量の割引など、全て計算済みの合計金額
        """
        volume_price = 3300

        volume_discount_list = [
            VolumeDiscount(20, 2800),
            VolumeDiscount(50, 2500),
        ]

        calculated_discount_list, not_discount_hour = self.calculate_discount(volume_discount_list, lesson_hour)

        # 割引対象外時間 * 通常料金で計算
        total_price = volume_price * not_discount_hour

        # 割引計算済みの料金があれば加算
        for volume_discount in calculated_discount_list:
            if volume_discount.calculated_price:
                total_price = total_price + volume_discount.calculated_price

        return total_price

    def calculate_discount(self, volume_discount_list: List[VolumeDiscount], lesson_hour: int):
        """
        一定時間を超えた分の割引後の計算結果を返却する
        :param volume_discount_list: VolumeDiscountオブジェクトのList
        :param lesson_hour: 累計時間
        :return: (値引き後価格を設定したVolumeDiscountオブジェクトのList, 値引き対象外の残りの時間)
        """
        subtraction_hour = lesson_hour
        calculated_discount_list = []

        # VolumeDiscountのリストを時間しきい値降順でソートしてループ
        for volume_discount in sorted(volume_discount_list, key=lambda x:x.threshold_hour, reverse=True):
            calculated_volume_discount = VolumeDiscount(
                volume_discount.threshold_hour,
                volume_discount.price,
            )

            # 累積時間の値がしきい値を超えていれば、累積時間からしきい値を減算した時間 * 価格を計算
            if volume_discount.threshold_hour < subtraction_hour:
                calculated_hour = subtraction_hour - (volume_discount.threshold_hour)
                calculated_volume_discount.calculated_price = volume_discount.price * calculated_hour
                # 累積時間から、割引計算済みの時間を減算して、次の割引レンジに当てはまるかを判定する
                subtraction_hour = subtraction_hour - calculated_hour

            calculated_discount_list.append(calculated_volume_discount)

        # 割引計算結果を追加したVolumeDiscountのリストと、割引対象外時間のタプルを返却
        return calculated_discount_list, subtraction_hour
