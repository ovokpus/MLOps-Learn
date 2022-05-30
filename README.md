# mlops-learn

Documents Participation in MLOps Zoomcamp

---

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

---

## Links

[Introduction](https://github.com/ovokpus/mlops-learn/tree/main/01-intro)

---

[Experiment Tracking](https://github.com/ovokpus/mlops-learn/tree/main/02-experiment-tracking)

---

[]()
