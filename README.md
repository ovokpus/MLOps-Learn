# Machine Learning Development Operations Learning Project

## Documents Participation in MLOps Zoomcamp

---

When you are designing a machine learning system, your job doesn't end with building the model—and achieving a high accuracy score and a low validation error! For the model to be actually helpful—you will have to consider deploying it, and also ensure that the model's performance does not degrade over time. And MLOps is a set of _best practices_ for putting machine learning models into production.

![image](https://user-images.githubusercontent.com/47279635/168582280-52820583-d0bb-4b46-add4-b2fa4c09bc1b.png)

## 🎯 Steps in a Machine Learning Project

The various stages in a machine learning project can be broadly captured in the following three steps:

1. **Design**: In the `design` step, you are considering the problem at hand—to decide whether or not you'll need a machine learning algorithm to achieve the objective.
2. **Train**: Once you decide on using a machine learning algorithm, you `train` the model and optimize its performance on the validation dataset.
3. **Operate**: The `operate` state captures the performance of the model after it's deployed. Some of the questions that you'll answer throughout the course, include:

- If the performance of the model degrades, can you retrain the model in a cost-effective manner?
- How do you ensure that the deployed model performs as expected—that is, how do you monitor the model's performance in production?
- What are the challenges associated with monitoring ML models?

---

# 🗒 What is MLOps?

When machine learning (ML) is used to solve a business problem, one could argue that delivering the model output to the end-user in a reliable way is an integral part of the machine learning process.

## 🔁 ML Model Life-Cycle

For a clearer picture, we can look at a life-cycle of a machine learning model:

```mermaid
flowchart LR
    subgraph ML Model
        D([Monitor]) -.->|retrain when performance drops| B([1. Train])
        B --> C([2. Deploy])
        C --> D([3. Monitor])
        end
        A([Data & <br>Problem Design]) --->|if ML helps solve problem| B
```

- **Data & Problem Design**: Choose machine learning to solve a problem when there is no other more straightforward approach and the data has sufficient quality.
- 1️⃣ **Train**: Train and evaluate ML models and choose the best performing one.
- 2️⃣ **Deploy**: Integrate the chosen model into the production environment (web service, module, embedded system, etc.)
- 3️⃣ **Monitor**: Capture the model's performance in the production environment and define a threshold for an acceptable value.

Depending on the use case, team skills, and established best practices, each of the life-cycle stages could be realized manually or with more automation support. MLOps is a practice that could support the maturity of the life-cycle iterations.

## ⚙️ Machine Learning Operations (MLOps)

MLOps brings DevOps principles to machine learning. It is a set of best practices to put ML models into production and automate the life-cycle.

MLOps could help to

- track model iterations and reproduce results reliably,
- monitor model performance and deliver domain-specific metrics for ML,
- and deliver models safely and automatically into production.

## 📈 MLOps Maturity Model

The extent to which MLOps is implemented into a team or organization could be expressed as maturity. A framework for classifying different levels of MLOps maturity is listed below:

| Lvl |                                     | Overview                                                                                                                                                                                                                           | Use Case                                                                                                                                                                                                   |
| --: | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  0️⃣ | **No MLOps**                        | <ul><li>ML process highly manual</li><li>poor cooperation</li><li>lack of standards, success depends on an individual's expertise</li> </ul>                                                                                       | <ul><li>proof of concept (PoC)</li><li>academic project</li></ul>                                                                                                                                          |
|  1️⃣ | **DevOps but no MLOps**             | <ul><li>ML training is most often manual </li><li>software engineers might help with the deployment</li><li>automated tests and releases</li> </ul>                                                                                | <ul><li>bringing PoC to production</li></ul>                                                                                                                                                               |
|  2️⃣ | **Automated Training**              | <ul><li>ML experiment results are centrally tracked </li><li>training code and models are version controlled</li><li>deployment is handled by software engineers</li> </ul>                                                        | <ul><li>maintaining 2-3+ ML models</li></ul>                                                                                                                                                               |
|  3️⃣ | **Automated Model Deployment**      | <ul><li>releases are managed by an automated CI/CD pipeline</li><li>close cooperation between data and software engineers</li><li>performance of the deployed model is monitored, A/B tests for model selection are used</li></ul> | <ul><li>business-critical ML services</li></ul>                                                                                                                                                            |
|  4️⃣ | **Full MLOps Automated Operations** | <ul><li>clearly defined metrics for model monitoring</li><li>automatic retraining triggered when passing a model metric's threshold</li> </ul>                                                                                     | <ul><li>use only when a favorable trade-off between implementation cost and increase in efficiency is likely</li><li>retraining is needed often and is repetitive (has potential for automation)</li></ul> |

A high maturity level is not always needed because it comes with additional costs. The trade-off between automated model maintenance and the required effort to set up the automation should be considered. An ideal maturity level could be picked based on the use case / SLAs and the number of models deployed.

If you want to read more on maturity, visit [Microsoft's MLOps maturity model](https://docs.microsoft.com/en-us/azure/architecture/example-scenario/mlops/mlops-maturity-model).

---

## Links

[Introduction](https://github.com/ovokpus/mlops-learn/tree/main/01-intro)

---

[Experiment Tracking](https://github.com/ovokpus/mlops-learn/tree/main/02-experiment-tracking)

---

[]()
