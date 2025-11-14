"""
Keras model wrapper for sklearn compatibility.
Makes Keras/TensorFlow models work with the existing Aimodel infrastructure.
"""
import logging
from typing import Optional

import numpy as np
from enforce_typing import enforce_types
from sklearn.base import BaseEstimator, ClassifierMixin

logger = logging.getLogger("keras_wrapper")

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    logger.warning("TensorFlow not available. CNN-GRU models will not work.")


@enforce_types
class KerasClassifierWrapper(BaseEstimator, ClassifierMixin):
    """
    Wrapper to make Keras models sklearn-compatible.
    Implements fit(), predict(), and predict_proba() methods.
    """
    
    def __init__(self, model_builder, epochs=50, batch_size=32, verbose=0, random_state=None):
        """
        @arguments
          model_builder -- function that takes (n_features, n_classes) and returns a Keras model
          epochs -- number of training epochs
          batch_size -- batch size for training
          verbose -- verbosity level (0=silent, 1=progress)
          random_state -- random seed for reproducibility
        """
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow is required for CNN-GRU models. Install with: pip install tensorflow")
        
        self.model_builder = model_builder
        self.epochs = epochs
        self.batch_size = batch_size
        self.verbose = verbose
        self.random_state = random_state
        self.model_ = None
        self.n_features_ = None
        self.n_classes_ = None
        self.classes_ = None  # Required by sklearn's CalibratedClassifierCV
        
        # Set random seeds for reproducibility
        if random_state is not None:
            tf.random.set_seed(random_state)
            np.random.seed(random_state)
    
    def fit(self, X, y):
        """
        Train the Keras model.
        
        @arguments
          X -- 2d array [n_samples, n_features]
          y -- 1d array [n_samples] with class labels (0, 1, ...)
        """
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow is required")
        
        X = np.asarray(X, dtype=np.float32)
        y = np.asarray(y, dtype=np.int32)
        
        self.n_features_ = X.shape[1]
        self.classes_ = np.unique(y)  # Store unique class labels (required by sklearn)
        self.n_classes_ = len(self.classes_)
        
        # Reshape X for CNN input: (n_samples, timesteps, features)
        # For time series, we treat each feature as a timestep
        # If autoregressive_n is used, features are already time-ordered
        # We'll reshape to (n_samples, n_features, 1) for 1D CNN
        X_reshaped = X.reshape(X.shape[0], X.shape[1], 1)
        
        # Build model
        self.model_ = self.model_builder(X.shape[1], self.n_classes_)
        
        # Compile model
        if self.n_classes_ == 2:
            # Binary classification
            loss = 'binary_crossentropy'
        else:
            # Multi-class classification
            loss = 'sparse_categorical_crossentropy'
        
        self.model_.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss=loss,
            metrics=['accuracy']
        )
        
        # Early stopping to prevent overfitting
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='loss',
            patience=10,
            restore_best_weights=True,
            verbose=0
        )
        
        # Train model
        self.model_.fit(
            X_reshaped,
            y,
            epochs=self.epochs,
            batch_size=min(self.batch_size, len(X)),
            verbose=self.verbose,
            callbacks=[early_stopping],
            shuffle=True
        )
        
        return self
    
    def predict(self, X):
        """
        Predict class labels.
        
        @arguments
          X -- 2d array [n_samples, n_features]
        
        @return
          y_pred -- 1d array [n_samples] with predicted class labels
        """
        if self.model_ is None:
            raise ValueError("Model must be fitted before prediction")
        
        X = np.asarray(X, dtype=np.float32)
        X_reshaped = X.reshape(X.shape[0], X.shape[1], 1)
        
        y_proba = self.model_.predict(X_reshaped, verbose=0)
        y_pred = np.argmax(y_proba, axis=1)
        
        return y_pred
    
    def predict_proba(self, X):
        """
        Predict class probabilities.
        
        @arguments
          X -- 2d array [n_samples, n_features]
        
        @return
          y_proba -- 2d array [n_samples, n_classes] with class probabilities
        """
        if self.model_ is None:
            raise ValueError("Model must be fitted before prediction")
        
        X = np.asarray(X, dtype=np.float32)
        X_reshaped = X.reshape(X.shape[0], X.shape[1], 1)
        
        y_proba = self.model_.predict(X_reshaped, verbose=0)
        
        # Handle binary classification (sigmoid output is 1D, need to convert to 2D)
        if self.n_classes_ == 2 and y_proba.ndim == 1:
            # Convert [p] to [[1-p, p]]
            y_proba = np.column_stack([1 - y_proba, y_proba])
        elif self.n_classes_ == 2 and y_proba.shape[1] == 1:
            # Convert [[p]] to [[1-p, p]]
            y_proba = np.column_stack([1 - y_proba.flatten(), y_proba.flatten()])
        
        return y_proba


def build_cnn_gru_model(n_features: int, n_classes: int) -> keras.Model:
    """
    Build CNN-GRU hybrid model for time series classification.
    
    Architecture:
    1. 1D CNN layers for feature extraction
    2. GRU layers for temporal pattern recognition
    3. Dense layers for classification
    
    @arguments
      n_features -- number of input features (timesteps)
      n_classes -- number of output classes
    
    @return
      model -- compiled Keras model
    """
    if not TENSORFLOW_AVAILABLE:
        raise ImportError("TensorFlow is required")
    
    inputs = keras.Input(shape=(n_features, 1))
    
    # CNN layers for feature extraction
    x = layers.Conv1D(filters=64, kernel_size=3, activation='relu', padding='same')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Conv1D(filters=64, kernel_size=3, activation='relu', padding='same')(x)
    x = layers.MaxPooling1D(pool_size=2)(x)
    x = layers.Dropout(0.2)(x)
    
    x = layers.Conv1D(filters=128, kernel_size=3, activation='relu', padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling1D(pool_size=2)(x)
    x = layers.Dropout(0.2)(x)
    
    # Reshape for GRU (remove feature dimension)
    x = layers.Reshape((x.shape[1], x.shape[2]))(x)
    
    # GRU layers for temporal patterns
    x = layers.GRU(128, return_sequences=True, dropout=0.2, recurrent_dropout=0.2)(x)
    x = layers.GRU(64, return_sequences=False, dropout=0.2, recurrent_dropout=0.2)(x)
    
    # Dense layers for classification
    x = layers.Dense(64, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(32, activation='relu')(x)
    
    # Output layer
    if n_classes == 2:
        outputs = layers.Dense(1, activation='sigmoid')(x)
    else:
        outputs = layers.Dense(n_classes, activation='softmax')(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs)
    
    return model


def build_lstm_model(n_features: int, n_classes: int) -> keras.Model:
    """
    Build LSTM model for time series classification.
    
    @arguments
      n_features -- number of input features (timesteps)
      n_classes -- number of output classes
    
    @return
      model -- compiled Keras model
    """
    if not TENSORFLOW_AVAILABLE:
        raise ImportError("TensorFlow is required")
    
    inputs = keras.Input(shape=(n_features, 1))
    
    # LSTM layers
    x = layers.LSTM(128, return_sequences=True, dropout=0.2, recurrent_dropout=0.2)(inputs)
    x = layers.LSTM(64, return_sequences=False, dropout=0.2, recurrent_dropout=0.2)(x)
    
    # Dense layers
    x = layers.Dense(64, activation='relu')(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(32, activation='relu')(x)
    
    # Output layer
    if n_classes == 2:
        outputs = layers.Dense(1, activation='sigmoid')(x)
    else:
        outputs = layers.Dense(n_classes, activation='softmax')(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs)
    
    return model

