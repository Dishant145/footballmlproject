import os 
import sys
from dataclasses import dataclass
from src.footballproject.exception import CustomException
from src.footballproject.logger import logging
from src.footballproject.utils import evaluate_models, save_object
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import mlflow.sklearn
from urllib.parse import urlparse
import dagshub
dagshub.init(repo_owner='Dishant145', repo_name='footballmlproject', mlflow=True)



@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifact','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def eval_metrics(self,actual, pred):
        accuracy = accuracy_score(actual, pred)
        precision = precision_score(actual, pred,average='weighted')
        recall = recall_score(actual, pred,average='weighted')
        f1 = f1_score(actual, pred,average='weighted')
        return accuracy, precision, recall, f1


    def initiate_model_trainer(self,X,y):
        try:
            logging.info("Split training and test input data")
            # X_train, y_train, X_test, y_test = (train_array[:,:-1],train_array[:,-1],
            #                                     test_array[:,:-1],test_array[:,-1])

            smote = SMOTE(k_neighbors=5, random_state=42)
            X, y = smote.fit_resample(X, y)


            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=42)

            
            models = {
                "Random Forest": RandomForestClassifier(n_estimators=150, max_depth=10, random_state=42,min_samples_split=3),
                "Logistic Regression": LogisticRegression(random_state=42,C = 10, max_iter= 1000, penalty= 'l1', solver = 'saga'),
                "KNN": KNeighborsClassifier(n_neighbors=7),
                "Linear SVC": LinearSVC(C=10, random_state=42,dual=False, max_iter=1000, tol=1e-6,class_weight='balanced',penalty='l1'),
                "Naive Bayes": GaussianNB(var_smoothing=1e-11)

            }

            model_report: dict = evaluate_models(X_train, y_train, X_test, y_test, models)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = [model_key for model_key, value in model_report.items() if value == best_model_score][0]
        
            logging.info(f"Best Model- Name: {best_model_name} and Accuracy: {best_model_score}%")
            # print(f"Best Model- Name: {best_model_name} and Accuracy: {best_model_score}%")

            print(model_report)

            best_model = models[best_model_name]
            
            model_names = list(models.keys())

            actual_model=""

            for model in model_names:
                if best_model_name == model:
                    actual_model = actual_model + model
            
            mlflow.set_registry_uri("https://dagshub.com/Dishant145/footballmlproject.mlflow")
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme        

            with mlflow.start_run():

                y_pred = best_model.predict(X_test)

                (accuracy, precision, recall,f1) = self.eval_metrics(y_test, y_pred)

                mlflow.log_metric("Accuracy", accuracy)
                mlflow.log_metric("Precision", precision)
                mlflow.log_metric("Recall",recall)
                mlflow.log_metric("F1",f1)


                if tracking_url_type_store != "file":

                    mlflow.sklearn.log_model(best_model_name, "model", registered_model_name=actual_model)
                else:
                    mlflow.sklearn.log_model(best_model_name, "model")




            
            save_object(file_path=self.model_trainer_config.trained_model_file_path,
                    obj=best_model)

            # with open("artifact/model.pkl", "rb") as model_in:
            #     classifier = pickle.load(model_in)
            # print(type(classifier)) 

            return y_pred
            

        except Exception as e:
            raise CustomException(e,sys)
            
