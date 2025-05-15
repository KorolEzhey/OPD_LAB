from flask import Flask, render_template, request
import math

app = Flask(__name__)

MIN_VALUE = 0.0
MAX_VALUE = 1000.0

SHAPES = {
    'sphere': 'Сфера',
    'cube': 'Куб',
    'cylinder': 'Цилиндр',
    'cone': 'Конус',
    'rect_prism': 'Прямоугольный параллелепипед'
}

PARAM_NAMES = {
    'radius': 'Радиус',
    'side': 'Сторона',
    'height': 'Высота',
    'width': 'Ширина',
    'depth': 'Глубина'
}

SHAPE_PARAMS = {
    'sphere': ['radius'],
    'cube': ['side'],
    'cylinder': ['radius', 'height'],
    'cone': ['radius', 'height'],
    'rect_prism': ['width', 'height', 'depth']
}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = ''

    # это объединение args (GET) и form (POST).
    valsource = request.values
    shape_key = valsource.get('shape', '')

    # Если в GET или POST пришёл параметр shape — делаем расчёт.
    if shape_key:
        if shape_key not in SHAPE_PARAMS:
            error = "Недопустимая фигура"
        else:
            # точность
            prec_raw = valsource.get('precision', '').strip() or '2'
            try:
                precision = int(prec_raw)
                if precision < 0:
                    raise ValueError
            except ValueError:
                error = "Точность должна быть целым неотрицательным числом"

            params = {}
            if not error:
                for p in SHAPE_PARAMS[shape_key]:
                    raw = valsource.get(p, '').strip()
                    try:
                        v = float(raw)
                        if v < MIN_VALUE or v > MAX_VALUE:
                            error = f"Параметр '{PARAM_NAMES[p]}' должен находиться в диапазоне [{MIN_VALUE}, {MAX_VALUE}]"
                            break
                        params[p] = v
                    except ValueError:
                        error = f"Параметр '{PARAM_NAMES[p]}' должен быть числом"
                        break

            if not error:
                if shape_key == 'sphere':
                    vol = 4/3 * math.pi * params['radius']**3
                elif shape_key == 'cube':
                    vol = params['side']**3
                elif shape_key == 'cylinder':
                    vol = math.pi * params['radius']**2 * params['height']
                elif shape_key == 'cone':
                    vol = math.pi * params['radius']**2 * params['height'] / 3
                else:  # rect_prism
                    vol = params['width'] * params['height'] * params['depth']

                fmt = f"{vol:.{precision}f}"
                result = fmt.rstrip('0').rstrip('.') if '.' in fmt else fmt

    return render_template('index.html',
                           shapes=SHAPES,
                           shape_params=SHAPE_PARAMS,
                           param_names=PARAM_NAMES,
                           result=result,
                           error=error,
                           min_value=MIN_VALUE,
                           max_value=MAX_VALUE)

if __name__ == '__main__':
    app.run(debug=True)
