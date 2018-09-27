##### House Data Exploratory Analysis
rm(list=ls())
library(dplyr)
library(Rcpp)
library(Amelia)
library(mice)
library(lattice)
library(ggplot2)
library(caret)
library(randomForest)
library(neuralnet)
library(rpart)

# get data
train <- read.csv('./train.csv')


#find the demetion of the data 
dim(train)

# structure of train data
str(train)

# find how many N/A data in each colunm
colSums(sapply(train,is.na))

# take numeric to factor
train$MSSubClass <- as.factor(train$MSSubClass)
train$MoSold <- as.factor(train$MoSold)
train$YrSold <- as.factor(train$YrSold)

str(train)

# drow the miss value map
missmap(train[-1], col=c('grey','steelblue'), y.cex = 0.5, x.cex = 0.8) # from Amelia pakages

# get the missing value persentage for each colunm
sort(sapply(train, function(x){sum(is.na(x))/1480}), decreasing=TRUE)

# eclude colunm which missing value percentage is bigger than 40%
exclude <- c('PoolQC','MiscFeature','Alley','Fence','FireplaceQu')
include <- setdiff(names(train),exclude)
train <- train[include]

# ues mice funcion to impute missing value
train_new <- mice(train,m=2,method = 'cart',printFlag = FALSE)

# plot Lot Frontage
xyplot(train_new, LotFrontage~LotArea)

# complete missing value
train_new <- complete(train_new)# fills in the missing data

# check if there are missing value 
sum(sapply(train_new,function(x){sum(is.na(x))}))

# normalize data
normalizeData <- function(x)
{
    z <- (x - min(x,na.rm = TRUE))/(max(x,na.rm = TRUE) - min(x,na.rm = TRUE))
    return(z)
    
}
nom_data <- train_new[setdiff(names(train_new),c('Id'))]

for(i in 1:ncol(nom_data)){
    if(is.numeric(nom_data[,i])){
        nom_data[,i] <- normalizeData(nom_data[,i])
    }
    if(!is.numeric(nom_data[,i])){
        nom_data[,i] <- normalizeData(as.integer(nom_data[,i]))
    }
}
nom_data$SalePrice <- train_new$SalePrice

# Split training data and test data
len <- nrow(nom_data)
idx <- seq(from=1, to=len, by=5)
test_data <- nom_data[idx,]
test_price <- test_data$SalePrice
train_data <- nom_data[-idx,]
test_data <- test_data[setdiff(names(test_data),c('SalePrice'))]

# check Resutl Function, use RMSE value
?RMSE()


# Random Forest
?randomForest

# Decision Tree
rpart_1 <- rpart(SalePrice~., data = train_data)
Prediction_2 <- predict(rpart_1, newdata = test_data)
RMSE(log(test_price),log(Prediction_2))

# Predict with Random Forest
for_1 <- randomForest(SalePrice~.,data=train_data)
Prediction_1 <- predict(for_1, newdata = test_data)
RMSE(log(test_price),log(Prediction_1))



mse <- function(x,y){
    res <- (sum((log(x) - log(y))^2)/length(y))^(1/2)
    
    return(res)
}
mse(test_price,Prediction_1)


# Neutral Network
?neuralnet
out_put <- "SalePrice"
in_put <- setdiff(names(test_data),c('SalePrice'))
dd <-paste(in_put,collapse = "+")
modeldata <- neuralnet(SalePrice~MSSubClass+MSZoning+LotFrontage+LotArea+Street+LotShape+LandContour+Utilities+LotConfig+LandSlope+Neighborhood+Condition1+Condition2+BldgType+HouseStyle+OverallQual+OverallCond+YearBuilt+YearRemodAdd+RoofStyle+RoofMatl+Exterior1st+Exterior2nd+MasVnrType+MasVnrArea+ExterQual+ExterCond+Foundation+BsmtQual+BsmtCond+BsmtExposure+BsmtFinType1+BsmtFinSF1+BsmtFinType2+BsmtFinSF2+BsmtUnfSF+TotalBsmtSF+Heating+HeatingQC+CentralAir+Electrical+X1stFlrSF+X2ndFlrSF+LowQualFinSF+GrLivArea+BsmtFullBath+BsmtHalfBath+FullBath+HalfBath+BedroomAbvGr+KitchenAbvGr+KitchenQual+TotRmsAbvGrd+Functional+Fireplaces+GarageType+GarageYrBlt+GarageFinish+GarageCars+GarageArea+GarageQual+GarageCond+PavedDrive+WoodDeckSF+OpenPorchSF+EnclosedPorch+X3SsnPorch+ScreenPorch+PoolArea+MiscVal+MoSold+YrSold+SaleType+SaleCondition,train_data, hidden=200, threshold=0.01)
results <- compute(modeldata, test_data)
result <- as.data.frame(results$net.result)
RMSE(log(test_price),log(result))

?RMSE()


