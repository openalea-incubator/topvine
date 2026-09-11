import numpy as np
import pandas as pd
from typing import Iterable

### recuperation des donnees observees et calculs SF et longueur du rameau
# dat_observed = read.csv("C:/Users/joels/Desktop/Data Stage/All_Data/Data_Trait_Archi_Copy.csv", header = T, sep=",")
# total_SF_values = aggregate(dat_observed$SF, by = list(dat_observed$ID, dat_observed$Genotype), sum, na.rm=T)
# dat_observed_I = dat_observed[is.na(dat_observed$Rang_Secondaire),]
# total_length_values = aggregate(dat_observed_I$LEN, by = list(dat_observed_I$ID, dat_observed_I$Genotype), sum, na.rm=T)


def set_profile(
        intercept_0: float | int,
        intercept_1: float | int,
        max_normalized: float | int,
        norm_val: Iterable[float],
        value_max: float | int = 1
) -> list[float] :
    res_tot = []
    for norm_rank in norm_val:
        if norm_rank < max_normalized:
            res = (1 - intercept_0) / max_normalized * norm_rank + intercept_0
        else:
            res = (intercept_1 - 1) / (1 - max_normalized) * (norm_rank - max_normalized) + 1
        res_tot.append(float(res * value_max))

    return res_tot


def set_profile_primary_leaf_area(
    rank_internode_at_max_leaf_area: int,
    fraction_initial_to_max_leaf_area: float,
    nb_primary_internodes: int,
    leaf_area_max: float,
) -> list[float]:
    res: list[float] = []
    for rank in range(1, nb_primary_internodes + 1):
        print(rank)
        if rank < rank_internode_at_max_leaf_area:
            normalized_area = (
                        fraction_initial_to_max_leaf_area + (rank - 1) / (rank_internode_at_max_leaf_area - 1) * (
                        1 - fraction_initial_to_max_leaf_area))
        else:
            normalized_area = (nb_primary_internodes + 1 - rank) / (
                        nb_primary_internodes + 1 - rank_internode_at_max_leaf_area)
        res.append(leaf_area_max * normalized_area)

    return res


def set_profile_primary_internode_length(
        rank_internode_at_max_length: int,
        fraction_apical_to_max_length: float,
        nb_primary_internodes: int,
        length_max: float,
) -> list[float]:
    res: list[float] = []
    for rank in range(1, nb_primary_internodes + 1):
        print(rank)
        if rank < rank_internode_at_max_length:
            normalized_area = (rank - 1) / (rank_internode_at_max_length - 1)
        else:
            normalized_area = (fraction_apical_to_max_length + (1 - fraction_apical_to_max_length) * (
                        nb_primary_internodes + 1 - rank) / (nb_primary_internodes + 1 - rank_internode_at_max_length))
        res.append(length_max * normalized_area)

    return res


class Genotype(object):

    def __init__(self, NFI_mean=24.38,
                 NFI_sd=2.33,
                 SF_max_mean=279,
                 SF_max_sd=58.5,
                 IN_max_mean=11.71,
                 IN_max_sd=0.91,
                 slope_NFII_SFII=50,
                 slope_sd_NFII_SFII=2,
                 size_r_binorm=1.68,
                 mu_r_binorm=1.27,
                 max_normalized_rank_SF=0.34,
                 intercept_0_SF=0.26,
                 intercept_1_SF=0.20,
                 max_normalized_rank_IN=0.46,
                 intercept_0_IN=0.1,
                 intercept_1_IN=0.46,
                 name='generic genotype'
                 ):
        self.NFI_mean = NFI_mean
        self.NFI_sd = NFI_sd
        self.SF_max_mean = SF_max_mean
        self.SF_max_sd = SF_max_sd
        self.IN_max_mean = IN_max_mean
        self.IN_max_sd = IN_max_sd
        self.slope_NFII_SFII = slope_NFII_SFII
        self.slope_sd_NFII_SFII = slope_sd_NFII_SFII
        self.size_r_binorm = size_r_binorm
        self.mu_r_binorm = mu_r_binorm
        self.max_normalized_rank_SF = max_normalized_rank_SF
        self.intercept_0_SF = intercept_0_SF
        self.intercept_1_SF = intercept_1_SF
        self.max_normalized_rank_IN = max_normalized_rank_IN
        self.intercept_0_IN = intercept_0_IN
        self.intercept_1_IN = intercept_1_IN
        self.name = name

        # self.mean_shoot_length: float = sum(self.primary_internode_profile)
    @property
    def primary_internode_profile(self) -> list[float]:
            return set_profile(
        intercept_0=self.intercept_0_IN,
        intercept_1=self.intercept_1_IN,
        max_normalized=self.max_normalized_rank_IN,
        norm_val=[v  / round(self.NFI_mean) for v in range(1, round(self.NFI_mean) + 1)],
        value_max=self.IN_max_mean
    )


def get_positive_random_value(
        value_mean: float | int,
        value_sd: float | int,
) -> float:
    i = 0
    while True:
        if (res:=float(np.random.normal(value_mean, value_sd))) >= 0:
            return res
        i += 1
        if i > 100:
            raise ValueError(f"Couldn't generate a positive random number for mean ({value_mean}) and sd ({value_sd}).")


def generate_rameau_moyen(g: Genotype) -> pd.DataFrame:
    """Generates the topology data for an average shoot.

    Args:
        g: Genotype object

    Returns:
        DataFrame containing the following topology information for each primary internode:
            - "number_of_phytomers" (int): number of secondary internodes connected to the current primary internode
            - "SF_I" (float): (cm2) surface area of the primary leaf (float, >=0)
            - "IN_I_length" (float): (cm) length of the primary internode (float, >=0)
            - "SF_II_tot" (float): (cm2) sum of surface area of all secondary leaves (float, >=0)
            - "SF_II_mean" (float): (cm2) average surface area of secondary leaves (float, >=0)

    Notes:
        cf. Section IV.2.2.2 in PhD thesis of G. Louarn for details on the correction factor of leaf area (1.04)

    """
    leaf_area_correction_factor = 1.04
    nb_primary_phytomers = int(round(get_positive_random_value(value_mean=g.NFI_mean, value_sd=g.NFI_sd)))
    leaf_area_max = get_positive_random_value(value_mean=g.SF_max_mean, value_sd=g.SF_max_sd)
    internode_length_max = get_positive_random_value(value_mean=g.IN_max_mean, value_sd=g.IN_max_sd)

    profile_nb_secondary_phytomers = np.random.negative_binomial(
        n=g.size_r_binorm,
        p=g.size_r_binorm / (g.size_r_binorm + g.mu_r_binorm),
        size=max(0, nb_primary_phytomers - 6)).tolist() + [0] * 6

    norm_rank_primary_leaf = [v / nb_primary_phytomers for v in range(1, nb_primary_phytomers + 1)]

    profile_primary_leaf_area: list[float] = set_profile(
        intercept_0=g.intercept_0_SF,
        intercept_1=g.intercept_1_SF,
        max_normalized=g.max_normalized_rank_SF,
        norm_val=norm_rank_primary_leaf,
        value_max=leaf_area_max / leaf_area_correction_factor,
    )
    profile_internode_length: list[float] = set_profile(
        intercept_0=g.intercept_0_IN,
        intercept_1=g.intercept_1_IN,
        max_normalized=g.max_normalized_rank_IN,
        norm_val=norm_rank_primary_leaf,
        value_max=internode_length_max,
    )

    profile_secondary_leaf_area = [
        float(i * np.random.normal(g.slope_NFII_SFII, g.slope_sd_NFII_SFII)) / leaf_area_correction_factor
        for i in profile_nb_secondary_phytomers
    ]

    res = {
        "number_of_phytomers": profile_nb_secondary_phytomers,
        "SF_I": profile_primary_leaf_area,
        "IN_I_length": profile_internode_length,
        "SF_II_tot": profile_secondary_leaf_area,
        "SF_II_mean": [
            0 if nb_internodes == 0 else leaf_area / nb_internodes
            for leaf_area, nb_internodes in zip(profile_secondary_leaf_area, profile_nb_secondary_phytomers)
        ]
    }

    # keep legacy header row
    for k, v in res.items():
        v.insert(0, (0 if k!="number_of_phytomers" else nb_primary_phytomers))

    return pd.DataFrame(res)