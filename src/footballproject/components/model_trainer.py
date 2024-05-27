import os 
import sys
from dataclasses import dataclass
from src.footballproject.exception import CustomException
from src.footballproject.logger import logging
from src.footballproject.utils import evaluate_models, save_object
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
# from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifact','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Split training and test input data")
            X_train, y_train, X_test, y_test = (train_array[:,:-1],train_array[:,-1],
                                                test_array[:,:-1],test_array[:,-1])
            
            # smote = SMOTE(k_neighbors=5, random_state=42)
            # X_train, y_train = smote.fit_resample(X_train, y_train)


            models = {
                "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=9, random_state=42,class_weight='balanced',min_samples_split=3),
                "Logistic Regression": LogisticRegression(random_state=42,C = 1, max_iter= 100, penalty= 'l1', solver = 'saga'),
                "KNN": KNeighborsClassifier(algorithm='auto', n_neighbors= 3),
                "Linear SVCr": LinearSVC(C=10, random_state=42,dual=False, max_iter=1000, tol=1e-6,class_weight='balanced',penalty='l1'),
            }

            model_report: dict = evaluate_models(X_train, y_train, X_test, y_test, models)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = [model_key for model_key, value in model_report.items() if value == best_model_score]
        
            logging.info(f"Best Model- Name: {best_model_name} and Accuracy: {best_model_score}%")

            save_object(file_path=self.model_trainer_config.trained_model_file_path,
                    obj=best_model_name)

            return best_model_score
            

        except Exception as e:
            raise CustomException(e,sys)