from typing import List

class VolumeDiscount(object):
    def __init__(self, threshold_hour, price, calculated_price=None):
        self.threshold_hour = threshold_hour
        self.price = price
        self.calculated_price = calculated_price

def calculate_english(lesson_hour):
    base_price = 5000
    volume_price = 3500

    return base_price + lesson_hour * volume_price

def calculate_programming(lesson_hour):
    base_price = 20000
    include_hour = 5
    volume_price = 3500

    volume_discount_list = [
        VolumeDiscount(20, 3000),
        VolumeDiscount(35, 2800),
        VolumeDiscount(50, 2500),
    ]

    # subtraction_hour = lesson_hour
    # calculate_discount_price_list = []
    #
    # for price_range in sorted(volume_discount_list, key=lambda x:x['threshold_hour'], reverse=True):
    #     if price_range['threshold_hour'] < subtraction_hour:
    #         calculated_hour = subtraction_hour - (price_range['threshold_hour'])
    #         calculate_discount_price_list.append(
    #             price_range['discount_price'] * calculated_hour
    #         )
    #         subtraction_hour = subtraction_hour - calculated_hour

    calculated_discount_list, not_discount_hour = calculate_discount(volume_discount_list, lesson_hour)

    total_price = base_price + (volume_price * (not_discount_hour - include_hour))

    for volume_discount in calculated_discount_list:
        if volume_discount.calculated_price:
            total_price = total_price + volume_discount.calculated_price

    return total_price


def calculate_discount(volume_discount_list: List[VolumeDiscount], lesson_hour: int):
    """
    一定時間を超えた分の割引後の計算結果を返却する
    :param volume_discount_list: VolumeDiscountオブジェクトのList
    :param lesson_hour: 累計時間
    :return: (値引き後価格を設定したVolumeDiscountオブジェクトのList, 値引き対象外の残りの時間)
    """
    subtraction_hour = lesson_hour
    calculated_discount_list = []

    for volume_discount in sorted(volume_discount_list, key=lambda x:x.threshold_hour, reverse=True):
        calculated_volume_discount = VolumeDiscount(
            volume_discount.threshold_hour,
            volume_discount.price,
        )

        if volume_discount.threshold_hour < subtraction_hour:
            calculated_hour = subtraction_hour - (volume_discount.threshold_hour)
            calculated_volume_discount.calculated_price = volume_discount.price * calculated_hour
            subtraction_hour = subtraction_hour - calculated_hour

        calculated_discount_list.append(calculated_volume_discount)

    return (calculated_discount_list, subtraction_hour)
