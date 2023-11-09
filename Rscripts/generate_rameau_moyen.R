N_max_ord = 6   ### global variable representing the number of metamers without any ramification below the axis tip






#' function that determines the rank of the ramification with the largest number of leaves
#'
#' @param NFTOT the total number of leaves on the primary axis
#' @param rank_max_order rank at which the maximal number of leaves is reached if the primary axis is long enough
#' @param rank_ini the rank below which there is no ramification
#'
#' @return
#' @export
#'
#' @examples
determine_rank_max = function(NFTOT, rank_max_order = 8, rank_ini)
{
  
  if (NFTOT > 24)  {rang = rank_max_order}
  else if  (NFTOT < rank_max_order) { return(FALSE) } 
  else {rang = rank_ini + (rank_max_order - rank_ini)/16 * (NFTOT - rank_max_order)}
  return(round(rang,0))
  
}


#' Function that compute the ramification profile (non normalized at this step)
#'
#' @param in_order  the order of the ramification
#' @param in_order_max  the order of the primary internode above which the number of secondary internodes is assumed equal to zero 
#' @param NFTOT Total number of leaves on the primary shoot
#' @param rank_init rank below which there is no ramification
#' @param N_init ratio [0,1] of the number of internode on the first secondary axis compared to the longest ramification
#' @param N_max_order the number of metamers between the axis tip and the last ramification (assumed to be equal to 9)
#' @param sd_rand parameter that control the randomness of number of leaves distribution along the primary axes, low values induce large variation, put 100 for instance if you do not want any variability
#'
#' @return
#' @export
#'
#' @examples
compute_ind_NFII = function(in_order, in_order_max, NFTOT,  rank_init = 3, N_init = 0.1, sd_rand = 0.5, N_max_order = N_max_ord)
{
  
  
  if (NFTOT < N_max_order) { #print('ici') 
    NFII_init = 0}
  
  
  else
  {
    
    N_max_order_ = determine_rank_max(NFTOT,N_max_order,rank_init)
    
    ifelse (N_max_order_ <= rank_init,
            {
              a1=0
              b1=0
              a2 =0
              b2 = 0
            },
            {a1 = (1 - N_init) / (N_max_order_ - rank_init)
            
            b1 = N_init - a1 * rank_init
            ifelse (in_order_max <= N_max_order_ , {a2= 0
            b2 = 0} , 
            {a2 = -1 / (in_order_max - N_max_order_)
            b2 = 1 - a2*N_max_order_})
            })
    
    
    
    if (in_order <= rank_init) {  #print("first_step") 
      NFII_init = 0}
    if ((in_order > rank_init) & (in_order <= N_max_order_)) { #print("second_step") 
      NFII_init = a1 * (in_order) + b1}
    if (in_order > N_max_order_) {
      #print("last_step") 
      NFII_init = a2 * in_order + b2}
    
  }
  
  NFII = max(0, NFII_init)
  
  return(NFII)
}



#' Function that computes the normalized profile (sum of all the number of leaves of secondary axes equal to 0)
#'
#' @param NFI 
#'
#' @return
#' @export
#'
#' @examples
compute_profile = function(NFI,sd_rand=4){
  
  Non_normalised_profile  = c()  
  for (i in (1:NFI))
  {
    
    number = compute_ind_NFII(i, in_order_max = (NFI - N_max_ord), NFTOT = NFI)
    number = max(0,number +  rnorm(1, number, number/sd_rand))
    Non_normalised_profile = c(Non_normalised_profile, number)
    ifelse(sum(Non_normalised_profile) !=0, 
           {normalised_profile = Non_normalised_profile/sum(Non_normalised_profile)},
           {normalised_profile = Non_normalised_profile})
    
  }
  return(normalised_profile)
}









#' Function that compute the leaf area profile along the primary axis
#' In that specific case, the function return a value in % that correspond to a "dilation" factor modifying the size of the reference leaf shape used in TopVine
#'
#' @param rank insertion rank of the leaf on the primary shoot
#' @param NFTot total number of leaves on the primary shoot
#' @param SFmax maximal individual leaf area along the shoot
#' @param rank_max rank at which the leaf area reached its maximal size
#' @param NFin number of leaves corresponding to the leaves that displayed lower sizes at the top of the shoot (leaves that do not finish their elongation) 
#' @param rand random parameter to simulate some variation around the mean leaf area low value correspond to high variability and vice versa
#'
#' @return
#' @export
#'
#' @examples
compute_SF = function(rank,  NFTot, SFmax, rank_max=6, NFin=8, rand = 8)
{
  
  if (rank < rank_max)
  { 
    Min = SFmax / 10
    SF = ((SFmax - Min) / rank_max) * rank  + Min
  }
  
  if ((rank >= rank_max) & (rank <= (NFTot -NFin )))
  {
    SF = SFmax
  }
  if (rank > (NFTot - NFin )) 
  {
    SF = -SFmax / NFin * rank +  SFmax/NFin *NFTot
  }
  SF = rnorm(1,SF,SF/rand) 
  
  return(SF*106/100)     
  
}






#' Function that compute the total number of secondary leaves from the number of primary leaves
#' This function exists because we have  random number of leaves on primary axis when generating a new shoot
#' Thus we did some extrapolation to estimate the number of secondary axis given the observation performed for a given number of leaves on primary axis
#' Here I used many assumption that came from previous measurements of Louarn and Pallas.  
#' @param NFI actual number of primary leaves
#' @param measured_NFI number of primary leaves measured in field condition (input data)
#' @param measured_NFII number of secondary leaves measured in field condition (input data)
#'
#' @return
#' @export
#'
#' @examples
get_NFII_from_NFI = function(NFI, measured_NFI, measured_NFII)
{
  
  NFII_computed = c()  
  
  Rapp = measured_NFII/measured_NFI
  
  A = 1 + 2/3*(18/(60-18)) -2/3*(1/(60-18))*measured_NFI
  rapp_max = Rapp/A
  #print(rapp_max)
  
  for (NFIi in (1:60)){
    if (NFIi <= 18)   #### 18  is assumed to be the rank at which the ratio between secondary and primary axis number is maximal (simulation based on data of Louarn and Pallas)
    {
      estimated_rapp = rapp_max /( 18 - N_max_ord) * NFIi + rapp_max*(1- (18/(18-N_max_ord)))
    }
    else 
    { 
      a = -(2/3)*(rapp_max) / (60-18)  ### we assumed based on Louarn and Pallas dataset that the ratio was equal to one third of its maximal values when NFI is equal to 60
      b = rapp_max - a * 18 
      estimated_rapp  = a*NFIi + b
      #print("ici")
    }
    NFII_computed = c(NFII_computed, estimated_rapp*NFIi)
  }
  NFII_computed[NFII_computed < 0] = 0
  rank_max_SFII = which(NFII_computed == max(NFII_computed))[1]
  if (rank_max_SFII < 60) {NFII_computed[c((rank_max_SFII+1): length(NFII_computed))] = max(NFII_computed)}
  return(NFII_computed[NFI])
}






#' This function generate shoot based on observation performed at a given date on shoot displaying different number of leaves on primary and secondary axes
#' and different maximal individual leaf area
#' @param NFI observed number of primary leaves
#' @param SF observed maximal individual leaf area
#' @param NFII observed number of secondary leaves
#' @param rand parameter that is used to randomly modify the number of leaves on the primary axis (low values = high variability)
#'
#' @return
#' @export
#'
#' @examples
generate_shoot = function(NFI, SF, NFII, rand = 4)
{ NFI_ = round(rnorm(1,NFI,NFI/4),0)   
  NFII_ = round(get_NFII_from_NFI(NFI_,NFI, NFII),0)
  print(NFI_)
  print(NFII_)
  dat_result = as.data.frame(matrix(nrow= (NFI_ + 1), ncol = 3))
  dat_result[1,] = c(NFI_, 0, 0)
  for (i in (2:(NFI_+1)))
  {
    dat_result[i,2] = compute_SF((i-1), NFI_, SF)
    dat_result[i,3] = 2/3*dat_result[i,2]
  }
  dat_result[c(2:dim(dat_result)[1]), 1] = round(compute_profile(NFI_,rand)*NFII_,0)
  return(dat_result)
  
}


#


#### Exemple d'utilisation pour le génotype ABOUHOU
rameau_moyen = generate_shoot(24, 400/3, 82)  ### ne pas oublier de diviser par 3 la surface foliaire, +++ il faut mettre des nombres ronds, sinon la fonction ne va pas fonctionner
write.table(rameau_moyen, "rameau_moyen_ABOUHOU.txt", row.names = F, col.names = F)

