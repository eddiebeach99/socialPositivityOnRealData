### `data/`
This folder contains all necessary code to preprocess the raw review datasets into a standardized format suitable for simulation. This includes:
- Loading raw json datasets 
- Binarizing ratings and filtering items
- Outputting ready-to-use data for the simulations

### `simulation/`
1. **Bandit Identification:** Selects 50 bandits per dataset based on reward gaps and filtering criteria.
2. **Agent Simulations:** Runs agents with varying learning biases in different environments for each dataset.
(Both are contained in the modelSim python file)

### `analysis/`
Contains scripts for:
- Visualizing simulation results
- Analyzing bandit characteristics
- Creating all figures and plots used in the lab report

