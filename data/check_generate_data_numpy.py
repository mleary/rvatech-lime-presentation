import pandas as pd
import statsmodels.api as sm

df = pd.read_csv('./data/generated_data_numpy.csv')

X = df.drop(['Accident_Reported', 'Policy_Id'], axis=1)
y = df['Accident_Reported']

X = pd.get_dummies(X, drop_first=True)
X = X.astype('int64')

model = sm.GLM(y, X, family=sm.families.Binomial())
result = model.fit()

# Extract coefficients
coeff = result.params

# Sort coefficients by absolute values
sorted_coeff = coeff.abs().sort_values(ascending=False)

# Print sorted coefficients
print(sorted_coeff)


print(result.summary())
