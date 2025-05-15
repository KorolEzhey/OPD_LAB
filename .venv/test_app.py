import unittest
from app import app

class VolumeCalculatorGetTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def get_text(self, resp):
        return resp.data.decode('utf-8')

    def test_index_shows_form(self):
        # Просто GET без параметров — должны получить страницу 200
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        text = self.get_text(resp)
        self.assertIn('<select name="shape"', text)

    def test_sphere_volume(self):
        resp = self.app.get('/?shape=sphere&radius=3&precision=1')
        self.assertEqual(resp.status_code, 200)
        text = self.get_text(resp)
        self.assertIn('113.1', text)

    def test_cube_volume(self):
        resp = self.app.get('/?shape=cube&side=4')
        self.assertEqual(resp.status_code, 200)
        text = self.get_text(resp)
        self.assertIn('64', text)

    def test_cylinder_volume(self):
        resp = self.app.get('/?shape=cylinder&radius=2&height=5&precision=2')
        self.assertEqual(resp.status_code, 200)
        text = self.get_text(resp)
        self.assertIn('62.83', text)

    def test_cone_volume(self):
        # r=2,h=6, precision=2 → 25.13
        resp = self.app.get('/?shape=cone&radius=2&height=6&precision=2')
        self.assertEqual(resp.status_code, 200)
        text = self.get_text(resp)
        self.assertIn('25.13', text)

    def test_rect_prism_volume(self):
        # width=2,height=3,depth=4, precision=0 → 24
        resp = self.app.get('/?shape=rect_prism&width=2&height=3&depth=4&precision=0')
        self.assertEqual(resp.status_code, 200)
        text = self.get_text(resp)
        self.assertIn('24', text)

    def test_invalid_shape(self):
        resp = self.app.get('/?shape=triangle&side=3&precision=2')
        self.assertEqual(resp.status_code, 200)
        text = self.get_text(resp)
        self.assertIn('Недопустимая фигура', text)

    def test_negative_parameter(self):
        resp = self.app.get('/?shape=cube&side=-5&precision=2')
        self.assertEqual(resp.status_code, 200)
        text = self.get_text(resp)
        self.assertIn("Параметр 'Сторона' должен находиться в диапазоне [0.0, 1000.0]", text)

    def test_non_numeric_parameter(self):
        resp = self.app.get('/?shape=sphere&radius=abc&precision=2')
        self.assertEqual(resp.status_code, 200)
        text = self.get_text(resp)
        self.assertIn("Параметр 'Радиус' должен быть числом", text)

    def test_invalid_precision(self):
        resp = self.app.get('/?shape=cube&side=2&precision=-1')
        self.assertEqual(resp.status_code, 200)
        text = self.get_text(resp)
        self.assertIn('Точность должна быть целым неотрицательным числом', text)

    def test_missing_parameter(self):
        # так называемый shape задан, но radius не передан
        resp = self.app.get('/?shape=sphere&precision=2')
        self.assertEqual(resp.status_code, 200)
        text = self.get_text(resp)
        # при попытке float('') — ошибка «должен быть числом»
        self.assertIn("Параметр 'Радиус' должен быть числом", text)

if __name__ == '__main__':
    unittest.main()
