# @Time    : 2020/11/30 10:45 上午
# @Author  : Seven
# @File    : bitmap
# @Desc    : 位图


class Bitmap(object):
    def __init__(self, _max: int, array: list = None):
        """
        @param _max: Bitmap 最大位数
        """
        self.size = self.calc_elem_index(_max, True)
        self.array = array if array else [0] * self.size

    @staticmethod
    def calc_elem_index(num: int, up: bool = False) -> int:
        """up为True则为向上取整, 否则为向下取整"""
        if up:
            return int((num + 31 - 1) // 31)  # 向上取整
        return num // 31

    @staticmethod
    def calc_bit_index(num: int) -> int:
        return num % 31

    def set(self, num: int):
        """对应对位设置为True"""
        elem_index = self.calc_elem_index(num)
        byte_index = self.calc_bit_index(num)
        elem = self.array[elem_index]
        self.array[elem_index] = elem | (1 << byte_index)

    def clean(self, index: int):
        """对应位置设置False"""
        elem_index = self.calc_elem_index(index)
        byte_index = self.calc_bit_index(index)
        elem = self.array[elem_index]
        self.array[elem_index] = elem & (~(1 << byte_index))

    def test(self, index: int) -> bool:
        elem_index = self.calc_elem_index(index)
        byte_index = self.calc_bit_index(index)
        if self.array[elem_index] & (1 << byte_index):
            return True
        return False

    @staticmethod
    def list_to_bitmap(_max: int, list_size: int, _list: list) -> 'Bitmap':
        """
        列表转换到bitmap
        @param _max: 多少位
        @param list_size: 列表有多少位
        @param _list: 列表
        @return:
        """
        bit_map = Bitmap(_max)

        # 1. 开启全部
        for i in range(_max):
            bit_map.set(i)
        # 1. 将列表的位先关闭
        for i in range(list_size):
            bit_map.clean(i)
        # 2. 开启列表对应位
        for index, value in enumerate(_list):
            bit_map.set(value - 1)

        return bit_map

    @staticmethod
    def to_list(list_size: int, _ids: int) -> list:
        """
        bitmap转换到列表
        @param list_size: 列表有多少位
        @param _ids: 整型
        """
        bit_map = Bitmap(0, [_ids])

        bit_list = []
        for i in range(list_size):
            if bit_map.test(i):
                bit_list.append(i + 1)
        return bit_list


if __name__ == '__main__':
    # 测试
    bitmap = Bitmap(16)
    bitmap.set(0)
    bitmap.clean(1)

    print(bitmap.test(0))
    print(bitmap.test(1))

    # -----------实际应用-----------
    # 开启全部
    msg_ids = [1, 2, 3]
    bitmap = Bitmap.list_to_bitmap(16, 3, msg_ids)
    print('msg_ids to bit', bitmap.array)
    assert 1111111111111111 == int("{0:b}".format(int(bitmap.array[0])))
    # 转换回来
    bitmap_to_msg_ids = Bitmap.to_list(3, bitmap.array[0])
    print('bit to msg_ids', bitmap_to_msg_ids)
    assert msg_ids == bitmap_to_msg_ids

    # 关闭全部
    msg_ids = []
    bitmap = Bitmap.list_to_bitmap(16, 3, msg_ids)
    print('msg_ids to bit', bitmap.array)
    assert 1111111111111000 == int("{0:b}".format(int(bitmap.array[0])))
    # 转换回来
    bitmap_to_msg_ids = Bitmap.to_list(3, bitmap.array[0])
    print('bit to msg_ids', bitmap_to_msg_ids)
    assert msg_ids == bitmap_to_msg_ids

    # 开启1
    msg_ids = [1]
    bitmap = Bitmap.list_to_bitmap(16, 3, msg_ids)
    print('msg_ids to bit', bitmap.array)
    assert 1111111111111001 == int("{0:b}".format(int(bitmap.array[0])))
    # 转换回来
    bitmap_to_msg_ids = Bitmap.to_list(3, bitmap.array[0])
    print('bit to msg_ids', bitmap_to_msg_ids)
    assert msg_ids == bitmap_to_msg_ids

    # 开启3
    msg_ids = [3]
    bitmap = Bitmap.list_to_bitmap(16, 3, msg_ids)
    print('msg_ids to bit', bitmap.array)
    assert 1111111111111100 == int("{0:b}".format(int(bitmap.array[0])))
    # 转换回来
    bitmap_to_msg_ids = Bitmap.to_list(3, bitmap.array[0])
    print('bit to msg_ids', bitmap_to_msg_ids)
    assert msg_ids == bitmap_to_msg_ids
