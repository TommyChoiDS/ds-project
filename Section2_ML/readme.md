# Ames 주택데이터를 이용한 집값예측 Machine Learning 프로젝트

2021.08.31 - 2021.09.07

Random Forest와 Boosting 모델을 이용한 회귀 모델링

사용 기술 : Pandas, Pandas Profiling, Random Forest, XGBoost, LGBM, CatBoost, eli5

---

- Ames 주택데이터를 이용하여 집값을 예측하는 Machine Learning 프로젝트
- 모델 성능을 올리기 위한 피처 엔지니어링
- Ames의 집값을 예측하기 위한 모델링
    - Random Forest를 이용하여 베이스라인 모델링
        - Random Forest RMSLE : 0.1481
    - XGBoost, LGBM, CatBoost를 이용하여 예측 성능 향상
        - CatBoost RMSLE : 0.1284
- 각 변수의 중요도를 평가하기 위해 Permutation Importance라는 XAI기법을 사용
