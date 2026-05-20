import math

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

PI = 3.14


def calculate(shape, data):
    """Pure calculation logic — returns a dict with results or an error."""
    try:
        if shape == "rectangle":
            l = float(data["length"])
            b = float(data["breadth"])
            return {
                "type": "2d",
                "rows": [
                    ("Area", l * b, "sq units"),
                    ("Perimeter", 2 * (l + b), "units"),
                ],
                "formulas": {
                    "Area": "l × b",
                    "Perimeter": "2 × (l + b)",
                },
            }

        elif shape == "square":
            s = float(data["side"])
            return {
                "type": "2d",
                "rows": [
                    ("Area", s * s, "sq units"),
                    ("Perimeter", 4 * s, "units"),
                ],
                "formulas": {
                    "Area": "s²",
                    "Perimeter": "4s",
                },
            }

        elif shape == "circle":
            r = float(data["radius"])
            return {
                "type": "2d",
                "rows": [
                    ("Area", PI * r**2, "sq units"),
                    ("Circumference", 2 * PI * r, "units"),
                ],
                "formulas": {
                    "Area": "πr²",
                    "Circumference": "2πr",
                },
            }

        elif shape == "triangle":
            a = float(data["side1"])
            b = float(data["side2"])
            c = float(data["side3"])
            peri = a + b + c
            s = peri / 2
            area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
            return {
                "type": "2d",
                "rows": [
                    ("Area", area, "sq units"),
                    ("Perimeter", peri, "units"),
                ],
                "formulas": {
                    "Area": "√(s(s-a)(s-b)(s-c))",
                    "Perimeter": "a + b + c",
                },
            }

        elif shape == "equilateral_triangle":
            s = float(data["side"])
            return {
                "type": "2d",
                "rows": [
                    ("Area", (3**0.5 / 4) * s**2, "sq units"),
                    ("Perimeter", 3 * s, "units"),
                ],
                "formulas": {
                    "Area": "(√3/4) × s²",
                    "Perimeter": "3s",
                },
            }

        elif shape == "cube":
            s = float(data["side"])
            return {
                "type": "3d",
                "rows": [
                    ("LSA", 4 * s * s, "sq units"),
                    ("TSA", 6 * s * s, "sq units"),
                    ("Volume", s * s * s, "cu units"),
                ],
                "formulas": {
                    "LSA": "4s²",
                    "TSA": "6s²",
                    "Volume": "s³",
                },
            }

        elif shape == "cuboid":
            l = float(data["length"])
            b = float(data["breadth"])
            h = float(data["height"])
            return {
                "type": "3d",
                "rows": [
                    ("LSA", 2 * h * (l + b), "sq units"),
                    ("TSA", 2 * (l * b + b * h + h * l), "sq units"),
                    ("Volume", l * b * h, "cu units"),
                ],
                "formulas": {
                    "LSA": "2h(l + b)",
                    "TSA": "2(lb + bh + hl)",
                    "Volume": "l × b × h",
                },
            }

        elif shape == "cone":
            r = float(data["radius"])
            h = float(data["height"])
            slant = (r**2 + h**2) ** 0.5
            return {
                "type": "3d",
                "rows": [
                    ("CSA", PI * r * slant, "sq units"),
                    ("TSA", PI * r * (r + slant), "sq units"),
                    ("Volume", (1 / 3) * PI * r**2 * h, "cu units"),
                ],
                "formulas": {
                    "CSA": "πrl",
                    "TSA": "πr(r + l)",
                    "Volume": "⅓πr²h",
                },
            }

        elif shape == "cylinder":
            r = float(data["radius"])
            h = float(data["height"])
            return {
                "type": "3d",
                "rows": [
                    ("CSA", 2 * PI * r * h, "sq units"),
                    ("TSA", 2 * PI * r * (r + h), "sq units"),
                    ("Volume", PI * r**2 * h, "cu units"),
                ],
                "formulas": {
                    "CSA": "2πrh",
                    "TSA": "2πr(r + h)",
                    "Volume": "πr²h",
                },
            }

        elif shape == "prism":
            a = float(data["side_a"])
            b = float(data["side_b"])
            c = float(data["side_c"])
            h = float(data["height"])
            base_perimeter = a + b + c
            s = base_perimeter / 2
            base_area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
            lsa = base_perimeter * h
            return {
                "type": "3d",
                "rows": [
                    ("LSA", lsa, "sq units"),
                    ("TSA", lsa + 2 * base_area, "sq units"),
                    ("Volume", base_area * h, "cu units"),
                ],
                "formulas": {
                    "LSA": "Perimeter × h",
                    "TSA": "LSA + 2 × Base Area",
                    "Volume": "Base Area × h",
                },
            }

        elif shape == "square_pyramid":
            s = float(data["side"])
            h = float(data["height"])
            slant = (h**2 + (s / 2) ** 2) ** 0.5
            base_area = s * s
            lsa = 2 * s * slant
            return {
                "type": "3d",
                "rows": [
                    ("LSA", lsa, "sq units"),
                    ("TSA", base_area + lsa, "sq units"),
                    ("Volume", (1 / 3) * base_area * h, "cu units"),
                ],
                "formulas": {
                    "LSA": "2 × s × l",
                    "TSA": "s² + 2sl",
                    "Volume": "⅓ × s² × h",
                },
            }

        elif shape == "triangular_pyramid":
            s = float(data["side"])
            face_area = (3**0.5 / 4) * s * s
            return {
                "type": "3d",
                "rows": [
                    ("LSA", 3 * face_area, "sq units"),
                    ("TSA", 4 * face_area, "sq units"),
                    ("Volume", s * s * s / (6 * (2**0.5)), "cu units"),
                ],
                "formulas": {
                    "LSA": "3 × (√3/4 × s²)",
                    "TSA": "√3 × s²",
                    "Volume": "s³ / (6√2)",
                },
            }

        else:
            return {"error": "Invalid shape selected."}

    except (KeyError, ValueError):
        return {"error": "Please enter valid numeric values for all fields."}


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    selected_shape = "rectangle"

    if request.method == "POST":
        selected_shape = request.form.get("shape", "rectangle")
        result = calculate(selected_shape, request.form)

    return render_template(
        "index.html",
        result=result,
        selected_shape=selected_shape,
    )


@app.route("/calculate", methods=["POST"])
def calculate_api():
    """AJAX endpoint — returns JSON so the page never reloads."""
    shape = request.form.get("shape", "rectangle")
    result = calculate(shape, request.form)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
