import unittest
from aip_project import *
from tkinter import *


class sumsTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(alldelete([]), [])

    def test_2(self):
        self.assertEqual(alldelete([Label(), Frame(), Button()]), [])

    def test_3(self):
        self.assertEqual(nadpis_ball(0), 'баллов')

    def test_4(self):
        self.assertEqual(nadpis_ball(1), 'балл')

    def test_5(self):
        self.assertEqual(nadpis_ball(2), 'балла')

    def test_6(self):
        self.assertEqual(nadpis_ball(5), 'баллов')

    def test_7(self):
        self.assertEqual(nadpis_ball(10), 'баллов')

    def test_8(self):
        self.assertEqual(nadpis_ball(21), 'балл')

    def test_9(self):
        self.assertEqual(nadpis_ball(23), 'балла')

    def test_10(self):
        self.assertEqual(nadpis_ball(30), 'баллов')

    def test_11(self):
        self.assertEqual(nadpis_ball(32), 'балла')

    def test_12(self):
        self.assertEqual(nadpis(0), 'К сожалению вы не сдали экзамен. Готовьтесь усерднее!')

    def test_13(self):
        self.assertEqual(nadpis(49), 'Вы сдали экзамен, но результат не высокий. Возможно стоит подготовиться еще.')

    def test_14(self):
        self.assertEqual(nadpis(68),
                         'Вы сдали экзамен, результат примерно такой же как у большинства по стране. Еще немного и ты будешь лучше остальных!')

    def test_15(self):
        self.assertEqual(nadpis(69), 'Вы сдали экзамен, результат очень хороший. Осталось выучить самое сложное!')

    def test_16(self):
        self.assertEqual(nadpis(90), 'Вы сдали экзамен, результат впечатляет. Сможешь написать на 100? Я в тебя верю!')

    def test_17(self):
        self.assertEqual(raschitprocenti(7), 33)

    def test_18(self):
        self.assertEqual(raschitprocenti(21), 84)

    def test_19(self):
        self.assertEqual(raschitprocenti(12), 62)

    def test_20(self):
        self.assertEqual(raschitprocenti(28), 98)

    def test_21(self):
        self.assertEqual(raschitprocenti(32), 100)

    def test_22(self):
        self.assertEqual(srballvtoroichasti([]), 0)

    def test_22(self):
        var = []
        # арифметическая прогрессия
        for i in range(3 + 1):
            var.append(IntVar())
            Radiobutton(variable=var[i], value=1)
            var[i].set(i)
        self.assertEqual(srballvtoroichasti(var), 6)

    def test_23(self):
        var = []
        # арифметическая прогрессия
        for i in range(10 + 1):
            var.append(IntVar())
            Radiobutton(variable=var[i], value=1)
            var[i].set(i)
        self.assertEqual(srballvtoroichasti(var), 55)


if __name__ == "__main__":
    unittest.main()
