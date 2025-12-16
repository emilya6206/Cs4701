Convolutional Neural Networks Emily Arron ea3182

1. One hot encoding is method of representing qualtitative values quantitatively in order for them to be used by machine learning models by representing each variable (with n possible classes) as an n-length vector. To do this in keras, we use to_categorical from tensorflow.keras.utils, which then generates the one-hot vector for us.
2. Dropout is a technique to regulate overfitting by ignoring random neurons during training. This helps prevent overfitting because the model can no longer memorize the data, but rather is forced to learn how to recognize patterns.
3. ReLU is different from the sigmoid function as it outputs max(0,x), leading to faster training times and avoids the vanishing gradient, whereas sigmoid has the problem of the vanishing gradient, takes longer to compute, but reports all data from 0-1 so it is great for binary classification. 
4. The softmax function is necessary in the outer layer to convert the arbitary scores into probabilities that are easily understood, uniform, and interperatable.
5. The dimension of the output is the ((input width - filter size) / stride) + 1 so in our case, ((100 - 5) / 1) + 1 = 95/1 + 1 = 96. So the height and width is 96, and the depth is the number of filters, or 16. So the output dimensions are 96x96x16. The MaxPooling layer output dimensions are ((normalOutput - padding) / stride) + 1, where stride is the pool size and since MaxPooling only affects height and width, those will be (96 - 2) / 2) + 1 = 48. So the MaxPooling layer output will be 48x48x16. 


For my model, I chose to use a CNN with three convolutional layers (32, 64, and 128) with batch normalization and max pooling to extract features and reduce spatial size. By including dropout, I reduced the chance of overfitting, and the softmax layer included at the end predicts the 26 classes (1 for each letter of alphabet). 
