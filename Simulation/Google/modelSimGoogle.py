import numpy as np
import pandas as pd


def param_gen(n_agents):
    par_names = ["tau", "alpha1", "alpha2"]
    all_pars = []
    par = np.zeros((n_agents, len(par_names)))
    par[:,0] = np.random.lognormal(-2, 0.5, n_agents)
    par[:,1] = np.random.uniform(0, 1, n_agents)
    par[:,2] = np.random.uniform(0, 1, n_agents)
    
    for ag in range(n_agents):
        pars = dict(zip(par_names, par[ag, :]))
        all_pars.append(pars)
    return all_pars


def modelSim(allPars, bandit_a, bandit_b, conflicting_user_reviews, obsLearn="predErr", demoNum=8):
    taus = []
    alpha1s = []
    alpha2s = []
    scoreboard = []
    values = []
    ids = []
    demoChoice = []
    demoReviews = []
    block = []
    games = []
    
    agent = 0
    no_comparisons = 0
    for ag in range(len(allPars)):
        pars = allPars[ag]
        if (agent % 1000 == 0): print(agent)
        agent += 1
        
        index = 0
        for bandit_a_sample, bandit_b_sample, conflicting_user_review in zip(bandit_a, bandit_b, conflicting_user_reviews):
            no_comparisons += 1
            choices = []
            reviews = []
            vals = np.zeros(2) 
            sampled_reviews_A = np.random.choice(bandit_a_sample, demoNum, replace=False)
            sampled_reviews_B = np.random.choice(bandit_b_sample, demoNum, replace=False)
            
            for demo in range(demoNum):
                outcomes = [sampled_reviews_A[demo], sampled_reviews_B[demo]]

                # Randomly show a review
                dchoice = np.random.choice([0,1])
                review = outcomes[dchoice] 

                choices.append(dchoice)
                reviews.append(review)

                if obsLearn == "predErr":
                    if review == 1:
                        vals[dchoice] = vals[dchoice] + pars["alpha1"] * (1 - vals[dchoice])
                    else:
                        vals[dchoice] = vals[dchoice] + pars["alpha2"] * (-1 - vals[dchoice])
                else:
                    raise ValueError("Unknown obsLearn method")
            
            values.append(vals.copy())
            vals = vals - np.max(vals)
            pol = np.exp(vals / pars["tau"])
            pol = pol / np.sum(pol)
            pchoice = np.random.choice([0,1], p=pol)

            # Score the agent based on the conflicting user's reviews
            if pchoice == 0: 
                score = conflicting_user_review[0]
            else:
                score = conflicting_user_review[1]
           
       
            ids.append(ag)
            block.append(index)
            taus.append(pars["tau"])
            alpha1s.append(pars["alpha1"])
            alpha2s.append(pars["alpha2"])
            scoreboard.append(score)
            demoChoice.append(choices)
            demoReviews.append(reviews)
            index += 1
    
 
    data = pd.DataFrame(
        zip(ids, block, taus, alpha1s, alpha2s, scoreboard, values, demoChoice, demoReviews),
        columns=["id", "block", "tau", "alpha1", "alpha2", "score", "values", "dchoice", "review"]
    )
    print(no_comparisons)

    return data
