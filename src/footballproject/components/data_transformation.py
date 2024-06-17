import os
import sys
from src.footballproject.exception import CustomException
from src.footballproject.logger import logging
from src.footballproject.utils import save_object
import pandas as pd
import numpy as np

from dataclasses import dataclass
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, MinMaxScaler, StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin


class Feature_Engineering(BaseEstimator, TransformerMixin):
    def __init__(self):

        logging.info("Started Feature Engineering")

    
    def time_series(self, df):
        
        # df['Home_Attacking_Form'] = df.groupby('Home')['xG_Home'].transform(lambda x: x.rolling(5, 1).mean())
        # df['Home_Assisting_Form'] = df.groupby('Home')['xGA_Home'].transform(lambda x: x.rolling(5, 1).mean())
        # df['Away_Attacking_Form'] = df.groupby('Away')['xG_Away'].transform(lambda x: x.rolling(5, 1).mean())
        # df['Away_Assisting_Form'] = df.groupby('Away')['xGA_Away'].transform(lambda x: x.rolling(5, 1).mean()

        df['xG_Diff'] = df['xG_Home'] - df['xG_Away']
        df['xGA_Diff'] = df['xGA_Home'] - df['xGA_Away']

        df['xGA_Ratio_Home'] = df['xGA_Home'] / (df['xG_Home'] + 0.1)
        df['xGA_Ratio_Away'] = df['xGA_Away'] / (df['xG_Away'] + 0.1)


    def transform_data(self, df):
        try:
            df.drop(['G_Home', 'G_Away','Date','Referee'], axis=1, inplace=True)

            self.time_series(df)

            # df.drop(['xG_Home','xG_Away','xGA_Home','xGA_Away','Home','Away'], axis=1,inplace=True)
            df.drop(['Home','Away'], axis=1,inplace=True)
            logging.info("dropping columns from our original dataset")
            
            return df

        except Exception as e:
            raise CustomException(e,sys)

    def fit(self,X,y=None):
        return self
        
    def transform(self,X:pd.DataFrame,y=None):
        try:    
            transformed_df=self.transform_data(X)
                
            return transformed_df
        except Exception as e:
            raise CustomException(e,sys) from e


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifact','preprocessor.pkl')
    feature_engg_obj_path = os.path.join('artifact','feature_eng.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation(self):
        try:
            

            numerical_columns = [
                'xG_Home','xG_Away','xGA_Home','xGA_Away','xG_Diff','xGA_Diff','xGA_Ratio_Home','xGA_Ratio_Away'
            ]

            ordinal_columns = [
                "Temp", "Humidity", "Wind", "Home_Fatigue", "Away_Fatigue","Referee_Bias"
            ]

            # categorical_columns = ["Referee_Bias"]

            categories_1 = [['Low', 'Moderate', 'High']] * 5
            categories_2 = ['Home','Away']
            categories_1.append(categories_2)


            num_pipeline=Pipeline(steps=[
                ('scalar',StandardScaler())

            ])

            # cat_pipeline=Pipeline(steps=[
            #     ("one_hot_encoder",LabelEncoder()),
            #     ("scaler",StandardScaler())
            # ])

            ord_pipeline=Pipeline(steps=[
                ('ordinal', OrdinalEncoder(categories=categories_1)),
                ("scaler",StandardScaler())
            ])


            preprocessor = ColumnTransformer([
                ('numerical_pipeline', num_pipeline,numerical_columns ),
                # ('categorical_pipeline', cat_pipeline,categorical_columns ),
                ('ordinal_pipeline', ord_pipeline,ordinal_columns )
            ])

            
            logging.info("Pipeline Steps Completed")
            return preprocessor
    
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_feature_engineering(self):
        try:
            feature_engineering = Pipeline(steps = [("fe",Feature_Engineering())])

            return feature_engineering

        except Exception as e:
            raise CustomException( e,sys)

    def initiate_data_transformation(self, raw_path):
        try:
            # train_df=pd.read_csv(train_path)
            # test_df=pd.read_csv(test_path)

            df = pd.read_csv(raw_path)
            logging.info("Reading the train and test file")


            target_column_name="Result"

            X = df.drop(columns = target_column_name, axis = 1)
            y = df[target_column_name]

            

            fe_obj = self.initiate_feature_engineering()

            # train_df = fe_obj.fit_transform(train_df)
            # test_df = fe_obj.transform(test_df)

            X = fe_obj.fit_transform(X)

            

            preprocessing_obj=self.get_data_transformation()

            # X_train = train_df.drop(columns = target_column_name, axis = 1)
            # y_train = train_df[target_column_name]

            # X_test = test_df.drop(columns = target_column_name, axis = 1)
            # y_test = test_df[target_column_name]

            # X_train_arr = preprocessing_obj.fit_transform(X_train)
            # X_test_arr = preprocessing_obj.transform(X_test)

            X = preprocessing_obj.fit_transform(X)

            # train_arr = np.c_[X_train_arr, np.array(y_train)]
            # test_arr = np.c_[X_test_arr, np.array(y_test)]

    
            logging.info(f"Saving feature eng object")

            save_object(

                file_path=self.data_transformation_config.feature_engg_obj_path,
                obj=fe_obj
            )


            logging.info(f"Saving preprocessing object")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (

                X,
                y,
                self.data_transformation_config.preprocessor_obj_file_path
            )




        except Exception as e:
            raise CustomException( e,sys)
 