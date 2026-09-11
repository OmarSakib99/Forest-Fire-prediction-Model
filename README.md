# Algerian Forest Fire Prediction

A Flask web application that predicts the Fire Weather Index (FWI) using a trained scikit-learn linear regression model and the Algerian forest fires dataset.

## Project Structure

```text
.
├── application.py
├── requirements.txt
├── models/
│   ├── linreg.pkl
│   ├── ridge.pkl
│   └── scaler.pkl
├── notebooks/
│   ├── Algerian_forest_fires_cleaned_dataset.csv
│   ├── Model Training.ipynb
│   └── Ridge,_Lasso_Regression.ipynb
└── templates/
    ├── home.html
    └── index.html
```

## Requirements

- Python 3.9 or later
- Flask
- NumPy
- pandas
- scikit-learn

## Installation

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

Start the Flask server from the project root:

```bash
python application.py
```

The application listens on all network interfaces at port `5002`:

```text
http://127.0.0.1:5002/predictdata
```

To access it from another device on the same network, replace `127.0.0.1` with the computer's local IP address, for example:

```text
http://192.168.0.53:5002/predictdata
```

Stop the server with `Ctrl+C` in the terminal running Flask.

## Routes

| Method | Route | Description |
|---|---|---|
| GET | `/` | Displays the basic index page. |
| GET | `/predictdata` | Displays the prediction form. |
| POST | `/predictdata` | Validates the submitted values and returns the predicted FWI. |

## Model Inputs

The current trained model expects these nine features in this order:

| Field | Description | Dataset range or values |
|---|---|---|
| `Temperature` | Noon maximum temperature in Celsius | 22 to 42 |
| `RH` | Relative humidity percentage | 21 to 90 |
| `Ws` | Wind speed in km/h | 6 to 29 |
| `Rain` | Total daily rainfall in millimeters | 0 to 16.8 |
| `FFMC` | Fine Fuel Moisture Code | 28.6 to 92.5 |
| `DMC` | Duff Moisture Code | 1.1 to 65.9 |
| `ISI` | Initial Spread Index | 0 to 18.5 |
| `Classes` | Fire classification | `Fire` or `Not Fire` |
| `Region` | Dataset region code | `0` or `1` |

The form converts `Not Fire` to `0` and `Fire` to `1` before prediction.

The predicted value is `FWI` (Fire Weather Index). `FWI` is the target value, so it is not entered manually.

### Dataset Fields Not Used by the Current Model

The original dataset also contains date fields, `DC`, and `BUI`. They are not submitted by the current form because:

- `day`, `month`, and `year` were removed during preprocessing.
- `DC` and `BUI` were removed during feature selection because of high correlation.
- `FWI` is the prediction target.

To use these fields, the model must be retrained with the corresponding preprocessing pipeline.

## Saved Model Files

- `models/linreg.pkl`: Linear regression model used for prediction.
- `models/scaler.pkl`: `StandardScaler` used to scale the nine model inputs.
- `models/ridge.pkl`: Additional Ridge model artifact retained from experimentation; it is not used by the current Flask application.

The scaler must be applied before passing the values to the regression model.

## Troubleshooting

### `404` for `/predictdata`

Make sure the correct application is running and that you are using port `5002`:

```bash
source .venv/bin/activate
python application.py
```

### `render_template()` missing a template name

Every call to `render_template()` must specify a template, such as:

```python
render_template("home.html")
```

### `view function did not return a valid response`

Every request branch must return a Flask response. The POST branch must return the rendered result page after prediction.

### `float() argument must be a string or a number, not 'NoneType'`

This means a submitted field is missing or has a different name from the expected form field. The current application accepts the current field names and common lowercase aliases.

### `LinearRegression` has no attribute `transform`

`linreg.pkl` is a regression model and cannot scale input data. Use `scaler.pkl` for `.transform()` and `linreg.pkl` for `.predict()`.

### `CTRL+C to quit`

This is normal Flask startup output. It indicates that the development server is running and can be stopped with `Ctrl+C`.

## Development Notes

This application uses Flask's development server and is intended for local development or demonstrations. For production deployment, use a production WSGI server and configure appropriate security and network settings.
