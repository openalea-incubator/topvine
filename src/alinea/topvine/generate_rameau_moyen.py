import numpy as np
import pandas as pd
### recuperation des donnees observees et calculs SF et longueur du rameau
# dat_observed = read.csv("C:/Users/joels/Desktop/Data Stage/All_Data/Data_Trait_Archi_Copy.csv", header = T, sep=",")
# total_SF_values = aggregate(dat_observed$SF, by = list(dat_observed$ID, dat_observed$Genotype), sum, na.rm=T)
# dat_observed_I = dat_observed[is.na(dat_observed$Rang_Secondaire),]
# total_length_values = aggregate(dat_observed_I$LEN, by = list(dat_observed_I$ID, dat_observed_I$Genotype), sum, na.rm=T)


def get_normalized_value(intercept_0, intercept_1, max_normalized, norm_val):

  res_tot = []
  for i in range(0,len(norm_val)):
      norm_rank = norm_val[i]
      if (norm_rank < max_normalized):
        res= (1-intercept_0)/max_normalized*norm_rank + intercept_0
      if (norm_rank >= max_normalized):
        res = (intercept_1-1)/(1-max_normalized)*(norm_rank-max_normalized) + 1
      res_tot.append(res)

  return(res_tot)

class Genotype(object):

    def __init__(self,NFI_mean =  24.38,
        NFI_sd = 2.33,
        SF_max_mean = 279,
        SF_max_sd = 58.5,
        IN_max_mean =  11.71,
        IN_max_sd = 0.91,
        slope_NFII_SFII = 98.25,
        intercept_NFII_SFII = -69.42,
        size_r_binorm = 1.68,
        mu_r_binorm = 1.27,
        max_normalized_rank_SF=0.34,
        intercept_0_SF=0.26,
        intercept_1_SF=0.20,
        max_normalized_rank_IN=0.46,
        intercept_0_IN=0.1,
        intercept_1_IN=0.46,
        name='generic'
                 ):
        self.NFI_mean = NFI_mean
        self.NFI_sd = NFI_sd
        self.SF_max_mean = SF_max_mean
        self.SF_max_sd = SF_max_sd
        self.IN_max_mean = IN_max_mean
        self.IN_max_sd = IN_max_sd
        self.slope_NFII_SFII = slope_NFII_SFII
        self.intercept_NFII_SFII = intercept_NFII_SFII
        self.size_r_binorm = size_r_binorm
        self.mu_r_binorm = mu_r_binorm
        self.max_normalized_rank_SF = max_normalized_rank_SF
        self.intercept_0_SF = intercept_0_SF
        self.intercept_1_SF = intercept_1_SF
        self.max_normalized_rank_IN = max_normalized_rank_IN
        self.intercept_0_IN = intercept_0_IN
        self.intercept_1_IN = intercept_1_IN
        norm_rank = np.arange(1, round(self.NFI_mean) + 1) / round(self.NFI_mean)
        norm_profile_IN = get_normalized_value(self.intercept_0_IN, self.intercept_1_IN, self.max_normalized_rank_IN, norm_rank)
        self.IN_profile = (np.array(norm_profile_IN) * self.IN_max_mean).tolist()
        self.mean_shoot_length = sum(self.IN_profile)
        self.name=name





def generate_rameau_moyen(g):
    NFI_ = int(round(np.random.normal(g.NFI_mean, g.NFI_sd,1)[0],0))
    # print(NFI_)
    SF_max = np.random.normal(g.SF_max_mean, g.SF_max_sd,1)[0]
    IN_max = np.random.normal(g.IN_max_mean, g.IN_max_sd,1)[0]
    dat_result = pd.DataFrame(np.zeros((NFI_ + 1, 4)))
    dat_result.columns = ["number_of_phytomers", "SF_I", "IN_I_length", "SF_II_tot"]
    dat_result.iloc[0] = [NFI_, 0, 0, 0]
    # np.random.negative_binomial(n=g.size_r_binorm, p=g.size_r_binorm / (g.size_r_binorm + g.mu_r_binorm),size=max(0,dat_result.shape[0]-7))
    dat_result.iloc[1:, 0] = 0
    dat_result.iloc[1:max(1,dat_result.shape[0] - 6), 0] = np.random.negative_binomial(n=g.size_r_binorm,
                                                                                p=g.size_r_binorm / (g.size_r_binorm + g.mu_r_binorm),
                                                                                size=max(0,dat_result.shape[0]-7))
    norm_rank = np.arange(1, NFI_ + 1) / NFI_
    norm_profile_SF = get_normalized_value(g.intercept_0_SF, g.intercept_1_SF, g.max_normalized_rank_SF, norm_rank)
    norm_profile_IN = get_normalized_value(g.intercept_0_IN, g.intercept_1_IN, g.max_normalized_rank_IN, norm_rank)
    SF_profile = (np.array(norm_profile_SF) * SF_max).tolist()
    IN_profile = (np.array(norm_profile_IN) * IN_max).tolist()
    dat_result.iloc[1:dat_result.shape[0], 1] = SF_profile
    dat_result.iloc[1:dat_result.shape[0], 2] = IN_profile
    dat_result.iloc[1:dat_result.shape[0], 3] = (np.array(dat_result.iloc[1:, 0]) * g.slope_NFII_SFII + g.intercept_NFII_SFII).tolist()
    dat_result.loc[dat_result["number_of_phytomers"] == 0, "SF_II_tot"] = 0
    return dat_result


def generate_rammoy_topvine(g):
    rameau = generate_rameau_moyen(g)
    rameau_top_vine = rameau[['number_of_phytomers', 'SF_I', 'SF_II_tot', 'IN_I_length']]
    rameau_top_vine.iloc[:, 1] = (np.array(rameau_top_vine.iloc[:, 1]) / 1.04).tolist()
    rameau_top_vine.loc[rameau_top_vine.iloc[:, 0] != 0, "SF_II_tot"] = (
            rameau_top_vine.loc[rameau_top_vine.iloc[:,0] != 0, "SF_II_tot"] /
            (1.04 * rameau_top_vine.loc[rameau_top_vine.iloc[:, 0] != 0, "number_of_phytomers"])
    )

    return rameau_top_vine

