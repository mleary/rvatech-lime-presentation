# rvatech-lime-presentation
Presentation materials for our talk at the 2024 RVATech Data + AI summit on March 28th, 2024.  Tracking project related work [here](https://github.com/users/mleary/projects/2)

Using local interpretable model-agnostic explanations to explain model outputs to your customers.

## To use this repo

### Building datasets

1. run `data/01_generate_data_numpy.py` to generate fake dataset for modeling
  * This produces 10,000 records (which you can change)
  * The `calculate_accident_reported` function determines what features/columns will be predictive of an accident.  You can adjust this to meet your purpose/intent.
  * OUTPUT: This will generate `data/generated_data_numpy.csv` which creates a dataset of car insurance policies (with variables such as Model, Color, etc.) and also has a predictor column of `Accident_Reported` which is 1 (accident reported) or 0 (no accident).

2. [Optional] run `02_check_generate_data_numpy.py` to test the outcomes of a basic GLM model. With this, you would expect to see the variables you have set as important in step 1 showing up as key predictors.

3. run `03_build_model.ipynb` to build a model (with train / test split) to predict whether or not a policy will have an accident.
  * OUTPUT: This will generate `data/predictions.csv` which adds a column `Predictions` that is the models prediction for that record.

### Generating LIME outputs

1. Run `demo.ipynb` to generate an output of `explanations.csv`. You can step through this process as well to see how LIME works!

### Running dash apps for examples

For our presentation, we have several dash apps to mock-up how we could use predictive models and LIME in insurance dashboards.  We will list those out, and the required dataset needed to run.

1) `initial_app.py` -  represents a basic dashboard with info on each policy.
  * uses the `data/generated_data_numpy.csv` 

2) `predictions_app.py` - takes the basic dashboard and adds in a column showing a prediction from a predictive model.
  * uses the `predictions.csv`

3) `final_app.py` - takes the prediction_app and add in the ability to see what is driving the individual predictions on hover
  * uses the `predictions.csv` and `explanations.csv`