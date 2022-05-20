"""
Creator: Ivanovitch Silva
Date: 16 April 2022
Define classes used in the pipeline
"""
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import QuantileTransformer
from sklearn.preprocessing import PowerTransformer
import pandas as pd

# transform numerical features
class NumericalTransformer(BaseEstimator, TransformerMixin):
    # Class constructor method that takes a model parameter as its argument
    # model 0: MinMaxScaler
    # model 1: StandardScaler
    # model 2: MaxAbsScaler
    # model 3: RobustScaler
    # model 4: Normalizer
    # model 5: QuantileTransformer
    # model 6: PowerTransformer
    # model 7: without scaling

    def __init__(self, model=0, colnames=None):
        self.model = model
        self.colnames = colnames
        self.scaler = None

    # Fit is used only to learn statistical about Scalers
    def fit(self, X, y=None):
        df = pd.DataFrame(X, columns=self.colnames)
        # MinMaxScaler
        if self.model == 0:
            self.scaler = MinMaxScaler()
            self.scaler.fit(df)
        # StandardScaler
        elif self.model == 1:
            self.scaler = StandardScaler()
            self.scaler.fit(df)
        # MaxAbsScaler
        elif self.model == 2:
            self.scaler = MaxAbsScaler()
            self.scaler.fit(df)
        # RobustScaler
        elif self.model == 3:
            self.scaler = RobustScaler()
            self.scaler.fit(df)
        # Normalizer
        elif self.model == 4:
            self.scaler = Normalizer()
            self.scaler.fit(df)
        # QuantileTransformer
        elif self.model == 5:
            self.scaler = QuantileTransformer()
            self.scaler.fit(df)
        # PowerTransformer
        elif self.model == 6:
            self.scaler = PowerTransformer()
            self.scaler.fit(df)
        return self

    # return columns names after transformation
    def get_feature_names_out(self):
        return self.colnames

    # Transformer method we wrote for this transformer
    # Use fitted scalers
    def transform(self, X, y=None):
        df = pd.DataFrame(X, columns=self.colnames)

        # update columns name
        self.colnames = df.columns.tolist()

        # minmax
        if self.model == 0 or self.model == 1 or self.model == 2 or self.model == 3 or self.model == 4 or self.model == 5 or self.model == 6:
            # transform data
            df = self.scaler.transform(df)
        else:
            df = df.values

        return df 
    
    
    
    
    
    
    
    
    """
# Select a Feature
class FeatureSelector(BaseEstimator, TransformerMixin):
    # Class Constructor
    def __init__(self, feature_names):
        self.feature_names = feature_names

    # Return self nothing else to do here
    def fit(self, X, y=None):
        return self

    # Method that describes what this custom transformer need to do
    def transform(self, X, y=None):
        return X[self.feature_names]

# Handling categorical features
class CategoricalTransformer(BaseEstimator, TransformerMixin):
    # Class constructor method that takes one boolean as its argument
    def __init__(self, new_features=True, colnames=None):
        self.new_features = new_features
        self.colnames = colnames

    # Return self nothing else to do here
    def fit(self, X, y=None):
        return self

    def get_feature_names_out(self):
        return self.colnames.tolist()

    # Transformer method we wrote for this transformer
    def transform(self, X, y=None):
        df = pd.DataFrame(X, columns=self.colnames)

        # Remove white space in categorical features
        df = df.apply(lambda row: row.str.strip())

        # customize feature?
        # How can I identify what needs to be modified? EDA!!!!
        if self.new_features:

            # minimize the cardinality of native_country feature
            # check cardinality using df.native_country.unique()
            df.loc[df['native_country'] != 'United-States','native_country'] = 'non_usa'

            # replace ? with Unknown
            edit_cols = ['native_country', 'occupation', 'workclass']
            for col in edit_cols:
                df.loc[df[col] == '?', col] = 'unknown'

            # decrease the cardinality of education feature
            hs_grad = ['HS-grad', '11th', '10th', '9th', '12th']
            elementary = ['1st-4th', '5th-6th', '7th-8th']
            # replace
            df['education'].replace(to_replace=hs_grad,value='HS-grad',inplace=True)
            df['education'].replace(to_replace=elementary,value='elementary_school',inplace=True)

            # adjust marital_status feature
            married = ['Married-spouse-absent','Married-civ-spouse','Married-AF-spouse']
            separated = ['Separated', 'Divorced']

            # replace
            df['marital_status'].replace(to_replace=married, value='Married', inplace=True)
            df['marital_status'].replace(to_replace=separated, value='Separated', inplace=True)

            # adjust workclass feature
            self_employed = ['Self-emp-not-inc', 'Self-emp-inc']
            govt_employees = ['Local-gov', 'State-gov', 'Federal-gov']

            # replace elements in list.
            df['workclass'].replace(to_replace=self_employed,value='Self_employed',inplace=True)
            df['workclass'].replace(to_replace=govt_employees,value='Govt_employees',inplace=True)

        # update column names
        self.colnames = df.columns

        return df
"""