# Load the necessary libraries
library(dplyr)
library(rsample)
library(parsnip)
library(yardstick)

#####################
# Read and prep data
#####################
# read in the data and convert target variable to factor
df <- read.csv("./data/generated_data_numpy.csv")
df <- df %>%
  mutate(Accident_Reported = as.factor(Accident_Reported))

# Split the data into training and testing sets
data_split <- rsample::initial_split(df,
                                      prop = 0.75, 
                                      strata = Accident_Reported)
train_data <- rsample::training(data_split)
test_data  <- rsample::testing(data_split)

################################
# Specify the model fits
################################
glm_spec <- parsnip::logistic_reg() %>%
  parsnip::set_engine("glm") %>%
  parsnip::set_mode("classification")

# Specify the random forest model
rf_spec <- parsnip::rand_forest() %>%
  parsnip::set_engine("ranger", importance = "impurity") %>%
  parsnip::set_mode("classification")

################################
# Fit the models - Using different data across them
################################
# fit a basic glm
glm_fit <- glm_spec %>%
  parsnip::fit(Accident_Reported ~ ., data = train_data)

# fit a random forest
rf_fit <- rf_spec %>%
  parsnip::fit(Accident_Reported ~ ., data = train_data %>%
    select(-Driver_Hair_Color))

################################
# Make predictions & create final dataset
################################

# Make predictions
glm_preds <- predict(glm_fit, new_data = test_data) %>%
  dplyr::rename(glm_pred = .pred_class)

rf_preds <- predict(rf_fit, new_data = test_data) %>%
  dplyr::rename(rf_pred = .pred_class)

# If you want to add the predictions to the test_data dataframe
test_data <- dplyr::bind_cols(test_data, glm_preds, rf_preds)

################################
# Quick check, model performance
################################

metrics <- yardstick::metric_set(accuracy, f_meas)

# Compute the metrics for the glm model
glm_metrics <- test_data %>%
  metrics(truth = Accident_Reported, estimate = glm_pred)

# Compute the metrics for the random forest model
rf_metrics <- test_data %>%
  metrics(truth = Accident_Reported, estimate = rf_pred)

# Print the metrics
glm_metrics
rf_metrics

################################
# Write out final dataset
################################
write.csv(test_data, "./data/prepped_data.csv", row.names = FALSE)
