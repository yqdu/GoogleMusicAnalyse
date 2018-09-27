*import original data;
PROC IMPORT OUT= WORK.games_original DATAFILE= "C:\Users\Think\Desktop\Project\games-features.csv" 
            DBMS=csv REPLACE;
     GETNAMES=YES;
RUN;

/*delete obviously unuseful cols
data games;
	set games_original
	 (keep=RecommendationCount RequiredAge  DLCCount  Metacritic SteamSpyPlayersEstimate PriceInitial SupportedLanguages 
	ControllerSupport	IsFree	FreeVerAvail	PurchaseAvail	SubscriptionAvail	PlatformWindows	PlatformLinux	
	PlatformMac	PCReqsHaveMin	PCReqsHaveRec	LinuxReqsHaveMin	LinuxReqsHaveRec	MacReqsHaveMin	MacReqsHaveRec	
	CategorySinglePlayer	CategoryMultiplayer	CategoryCoop	CategoryMMO	CategoryInAppPurchase	CategoryIncludeSrcSDK	
	CategoryIncludeLevelEditor	CategoryVRSupport	GenreIsNonGame	GenreIsIndie	GenreIsAction	GenreIsAdventure	
	GenreIsCasual	GenreIsStrategy	GenreIsRPG	GenreIsSimulation	GenreIsEarlyAccess	GenreIsFreeToPlay	GenreIsSports	
	GenreIsRacing	GenreIsMassivelyMultiplayer);
run;
*/

* to list all the unique values for char variables;
title "Frequency Counts for None-numberic Variables";
proc freq data=games_original;
	tables RequiredAge SupportedLanguages/ nocum nopercent;
run;

* replace missing char variables;
data games_filled1;
	set games_original;
	if SupportedLanguages in('English**languages with full audio support') then SupportedLanguages = 'English';
	if missing(SupportedLanguages) then SupportedLanguages = 'English';
	if missing(RequiredAge) then RequiredAge=0;
	if RequiredAge=1 then delete;
    if RequiredAge=7 then delete;
run;

* replace SupportedLanguages with english and english_and_others;
data games_filled2;
	set games_filled1;
	if SupportedLanguages in('English') then SupportedLanguages = 'english_only';
	else SupportedLanguages = 'english_and_others';
run;

* replacing missing value with mean value;
proc stdize data=games_filled2 reponly missing=mean out=games;
	var _numeric_;
run;

title"Frequency Counts for Character Variables";
proc freq data=games;
	tables RequiredAge SupportedLanguages/ nocum;
run;

* different means for different RequiredAge;
proc means data=games;
	class RequiredAge;
	var RecommendationCount;
	output out = age_means mean=mean;
run;

proc sgplot data=age_means;
	vbar RequiredAge/response=mean;
run;


* different means for different SupportedLanguages;
proc means data=games;
	class SupportedLanguages;
	var RecommendationCount;
	output out = language_means mean=mean;
run;

proc sgplot data=language_means;
	vbar SupportedLanguages/response=mean;
run;

/*
 Means of RecommendationCount for different Genre of games
*/
* genre action;
data games_action;
	set games;
	if GenreIsAction="Fals" then delete;
	if GenreIsAction="False" then delete;
	genre="action";
run;

proc means data=games_action;
	class genre;
	var RecommendationCount;
	output out=action_means mean=mean;
run;
proc reg data=games_action;
	model RecommendationCount=SteamSpyPlayersEstimate /vif stb;
quit;

* rpg;
data games_rpg;
	set games;
	if GenreIsRPG="False" then delete;
	if GenreIsRPG="Fals" then delete;
	genre="RPG";
run;

proc means data=games_rpg;
	class genre;
	var RecommendationCount;
	output out=rpg_means mean=mean;
run;
proc reg data=games_rpg;
	model RecommendationCount=SteamSpyPlayersEstimate /vif stb;
quit;

* sports;
data games_sports;
	set games;
	if GenreIsSports="False" then delete;
	if GenreIsSports="Fals" then delete;
	genre="Sports";
run;

proc means data=games_sports;
	class genre;
	var RecommendationCount;
	output out=sports_means mean=mean;
run;
proc reg data=games_sports;
	model RecommendationCount=SteamSpyPlayersEstimate /vif stb;
	
quit;

* racing;
data games_racing;
	set games;
	if GenreIsRacing="False" then delete;
	if GenreIsRacing="Fals" then delete;
	genre="Racing";
run;
proc means data=games_racing;
	class genre;
	var RecommendationCount;
	output out=racing_means mean=mean;
run;
proc reg data=games_racing;
	model RecommendationCount=SteamSpyPlayersEstimate /vif stb;
quit;

* strategy;
data games_strategy;
	set games;
	if GenreIsStrategy="False" then delete;
	if GenreIsStrategy="Fals" then delete;
	genre="Strategy";
run;
proc means data=games_strategy;
	class genre;
	var RecommendationCount;
	output out=strategy_means mean=mean;
run;
proc reg data=games_strategy;
	model RecommendationCount=SteamSpyPlayersEstimate /vif stb;
quit;

* casual;
data games_casual;
	set games;
	if GenreIsCasual="False" then delete;
	if GenreIsCasual="Fals" then delete;
	genre="Casual";
run;
proc means data=games_casual;
	class genre;
	var RecommendationCount;
	output out=casual_means mean=mean;
run;
proc reg data=games_casual;
	model RecommendationCount=SteamSpyPlayersEstimate /vif stb;
quit;

* simulation;
data games_simulation;
	set games;
	if GenreIsSimulation="False" then delete;
	if GenreIsSimulation="Fals" then delete;
	genre="Simulation";
run;
proc means data=games_simulation;
	class genre;
	var RecommendationCount;
	output out=simulation_means mean=mean;
run;
proc reg data=games_simulation;
	model RecommendationCount=SteamSpyPlayersEstimate /vif stb;
quit;

data genre_means;
	set action_means rpg_means sports_means racing_means 
		strategy_means casual_means simulation_means;
run;

title "RecommendationCount for different genre of games";
proc sgplot data=genre_means;
	vbar genre/response=mean;
run;

/*
data numericalize
*/
data games2;
 set games;
  /*
  RecommendationCount   
  DLCCount  
  Metacritic 
  SteamSpyPlayersEstimate 
  PriceInitial
 */
  if RequiredAge=0 then age1=1; 
  else age1=0;
  if RequiredAge=6 then age2=1; 
  else age2=0;
  if RequiredAge=10 then age3=1; 
  else age3=0;
  if RequiredAge=12 then age4=1; 
  else age4=0;
  if RequiredAge=13 then age5=1; 
  else age5=0;
  if RequiredAge=14 then age6=1; 
  else age6=0;
  if RequiredAge=15 then age7=1; 
  else age7=0;
  if RequiredAge=16 then age8=1; 
  else age8=0;
  if RequiredAge=17 then age9=1; 
  else age9=0;
  if RequiredAge=18 then age10=1; 
  else age10=0;

  if SupportedLanguages="english_only" then language1=1;
  else language1=0;
  if SupportedLanguages="english_and_others" then language2=1;
  else language2=0;

  if ControllerSupport="False" then v_ControllerSupport=0;
  else v_ControllerSupport=1;
  if IsFree="False" then v_IsFree=0;
  else v_IsFree=1;
  if FreeVerAvail="False" then v_FreeVerAvail=0;
  else v_FreeVerAvail=1;
  if PurchaseAvail="False" then v_PurchaseAvail=0;
  else v_PurchaseAvail=1;
  if SubscriptionAvail="False" then v_SubscriptionAvail=0;
  else v_SubscriptionAvail=1;
  if PlatformWindows="Fals" then Platform1=0;
  else Platform1=1;
  if PlatformLinux="Fals" then Platform2=0;
  else Platform2=1;
  if PlatformMac="Fals" then Platform3=0;
  else Platform3=1;
  if PCReqsHaveMin="False" then v_PCReqsHaveMin=0;
  else v_PCReqsHaveMin=1;
  if PCReqsHaveRec="False" then v_PCReqsHaveRec=0;
  else v_PCReqsHaveRec=1;
  if LinuxReqsHaveMin="False" then v_LinuxReqsHaveMin=0;
  else v_LinuxReqsHaveMin=1;
  if LinuxReqsHaveRec="False" then v_LinuxReqsHaveRec=0;
  else v_LinuxReqsHaveRec=1;
  if MacReqsHaveMin="False" then v_MacReqsHaveMin=0;
  else v_MacReqsHaveMin=1;
  if MacReqsHaveRec="False" then v_MacReqsHaveRec=0;
  else v_MacReqsHaveRec=1;
  if CategorySinglePlayer="False" then Category1=0;
  else Category1=1;
  if CategoryMultiplayer="False" then Category2=0;
  else Category2=1;
  if CategoryCoop="False" then Category3=0;
  else Category3=1;
  if CategoryMMO="False" then Category4=0;
  else Category4=1;
  if CategoryInAppPurchase="False" then Category5=0;
  else Category5=1;
  if CategoryIncludeSrcSDK="False" then Category6=0;
  else Category6=1;
  if CategoryIncludeLevelEditor="False" then Category7=0;
  else Category7=1;
  if CategoryVRSupport="False" then Category8=0;
  else Category8=1;
  if GenreIsNonGame="False" then Genre1=0;
  else Genre1=1;
  if GenreIsIndie="False" then Genre2=0;
  else Genre2=1;
  if GenreIsAction="Fals" then Genre3=0;
  else Genre3=1;
  if GenreIsAdventure="False" then Genre4=0;
  else Genre4=1;
  if GenreIsCasual="False" then Genre5=0;
  else Genre5=1;
  if GenreIsStrategy="False" then Genre6=0;
  else Genre6=1;
  if GenreIsRPG="False" then Genre7=0;
  else Genre7=1;
  if GenreIsSimulation="False" then Genre8=0;
  else Genre8=1;
  if GenreIsEarlyAccess="False" then Genre9=0;
  else Genre9=1;
  if GenreIsFreeToPlay="False" then Genre10=0;
  else Genre10=1;
  if GenreIsSports="False" then Genre11=0;
  else Genre11=1;
  if GenreIsRacing="False" then Genre12=0;
  else Genre12=1;
  if GenreIsMassivelyMultiplayer="False" then Genre13=0;
  else Genre13=1;
run;

* data profile;
proc sgplot data=games_filled2;
 histogram RequiredAge;
 density RequiredAge;
 density RequiredAge/type=kernel;
 run;

 proc sgplot data=games_filled2;
 histogram RecommendationCount;
 density RecommendationCount;
 density RecommendationCount/type=kernel;
 run;


proc sgplot data=games2;
 histogram language1;
 density language1;
 density language1/type=kernel;
 run;

* keep uesful data;
data games3;
	set games2
	(keep=RecommendationCount DLCCount Metacritic SteamSpyPlayersEstimate PriceInitial
    v_ControllerSupport v_IsFree v_FreeVerAvail v_PurchaseAvail v_SubscriptionAvail
    Platform1-Platform3 Category1-Category8 Genre1-Genre13 age1-age9 language1);
/*
	RecommendationCount=log(RecommendationCount);
	DLCCount=log(DLCCount);
	Metacritic=log(Metacritic);
	SteamSpyPlayersEstimate=log(SteamSpyPlayersEstimate);
	PriceInitial=log(PriceInitial);
*/
run;


* normalize;
proc standard data=games3
				mean=0 std=1
				out=games_z;
	var RecommendationCount DLCCount Metacritic SteamSpyPlayersEstimate PriceInitial
    v_ControllerSupport v_IsFree v_FreeVerAvail v_PurchaseAvail v_SubscriptionAvail
    Platform1-Platform3 Category1-Category8 Genre1-Genre13 age1-age9 language1;
run;

/*
 try regression before pca
*/
proc reg data=games3;
     model RecommendationCount = DLCCount Metacritic SteamSpyPlayersEstimate PriceInitial
    v_ControllerSupport v_IsFree v_FreeVerAvail v_PurchaseAvail v_SubscriptionAvail
    Platform1-Platform3 Category1-Category8 Genre1-Genre13 age1-age9 language1/ vif stb;
quit;

*PCA;
proc princomp data=games_z out=games_pca;
	var RecommendationCount DLCCount Metacritic SteamSpyPlayersEstimate PriceInitial
    	v_ControllerSupport v_IsFree v_FreeVerAvail v_PurchaseAvail v_SubscriptionAvail
    	Platform1-Platform3 Category1-Category8 Genre1-Genre13 age1-age9 language1;
	run;
quit;

* stepwise regression;
proc reg data=games_pca  outest=games_muti_reg ;
     model    RecommendationCount   =  Prin1-Prin27 /  VIF  selection= stepwise dwProb STB   ;
      OUTPUT OUT=games_muti_reg_out  PREDICTED=predict   RESIDUAL=Res 
                      L95M=l95m  U95M=u95m  L95=l95 U95=u95
       rstudent=rstudent h=lev cookd=Cookd  dffits=dffit
     STDP=s_predicted  STDR=s_residual  STUDENT=student;  
quit;

* forward regression;
proc reg data=games_pca  outest=games_muti_reg ;
     model    RecommendationCount   =  Prin1-Prin27 /  VIF  selection= forward dwProb STB   ;
      OUTPUT OUT=games_muti_reg_out  PREDICTED=predict   RESIDUAL=Res 
                      L95M=l95m  U95M=u95m  L95=l95 U95=u95
       rstudent=rstudent h=lev cookd=Cookd  dffits=dffit
     STDP=s_predicted  STDR=s_residual  STUDENT=student;  
quit;

proc reg data=games_pca  outest=games_muti_reg ;
     model    RecommendationCount   =  Prin1-Prin27 /  VIF dwProb STB;
      OUTPUT OUT=games_muti_reg_out  PREDICTED=predict   RESIDUAL=Res 
                      L95M=l95m  U95M=u95m  L95=l95 U95=u95
       rstudent=rstudent h=lev cookd=Cookd  dffits=dffit
     STDP=s_predicted  STDR=s_residual  STUDENT=student;  
quit;

