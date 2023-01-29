# resources
# https://www.r-bloggers.com/2022/03/new-r-package-yfr/

library(yfR)

df.stocks <- yf_collection_get("SP500", 
                           first_date = Sys.Date() - 360,
                           last_date = Sys.Date())

head(df.stocks)