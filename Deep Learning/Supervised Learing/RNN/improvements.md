## Ways I can improve the RNN

*Getting more training data:* I trained my model on the past 5 years of the Google stock prices but it would be even better to train it 
on the past 10 years.

*Increasing the number of timesteps:* the model remembered the stock prices from the 60 previous financial days to predict the stock price of
the next day. I could try to increase the number of timesteps, by choosing, for example, 120 timesteps (6 months).

*Adding some other indicators:* if I have the financial instinct that the stock price of some other companies might be correlated to the 
one of Google, you could add this other stock price as a new indicator in the training data. An example would be that the stock price of
Apple and Samsung are likely correlated as Apple uses Samsung components in their products.

*Adding more LSTM layers:* I built a RNN with four LSTM layers, but more could be used.

*Adding more neurons in the LSTM layers:* I highlight the fact that a high number of neurons in the LSTM layers responds better to the 
complexity of the problem and as a result I chose to include 50 neurons in each of the 4 LSTM layers. I could try an architecture with even more 
neurons in each of the 4 (or more) LSTM layers - fewer neurons does not yield a convergence of the loss.
