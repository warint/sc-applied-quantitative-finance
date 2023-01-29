
library(prophet)
library(dplyr)
library(yfR)

# set options for algorithm
my_ticker <- 'TSLA'
first_date <- Sys.Date() - 360
last_date <- Sys.Date()

# fetch data
stats <- yf_get(tickers = my_ticker, 
                first_date = first_date,
                last_date = last_date)

head(stats)

#daily data points starting from 2014–01–0

stats <- stats |> mutate(ds = ref_date) |> mutate(y = price_adjusted)
#View(summary(stats))
plot(y ~ ds, stats, type = "l")


m <- prophet(stats, daily.seasonality=TRUE, yearly.seasonality=TRUE)

future <- make_future_dataframe(m, periods = 90)
forecast <- predict(m, future)

plot(m, forecast)

tail(forecast[c('ds', 'yhat', 'yhat_lower', 'yhat_upper')])
tail(forecast)

prophet_plot_components(m, forecast)
