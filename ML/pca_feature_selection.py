import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
import matplotlib.pyplot as plt
import seaborn as sns

class CKDFeatureSelector:
    def __init__(self):
        self.pca = None
        self.scaler = StandardScaler()
        self.selected_features = None
        self.feature_importance = None
    
    def load_and_preprocess_data(self, csv_path):
        """Load and preprocess CKD dataset"""
        df = pd.read_csv(csv_path)
        
        # Remove non-numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df_numeric = df[numeric_cols].copy()
        
        # Remove ID columns and target
        exclude_cols = ['PatientID', 'Diagnosis', 'DoctorInCharge']
        feature_cols = [col for col in df_numeric.columns if col not in exclude_cols]
        
        X = df_numeric[feature_cols]
        y = df_numeric['Diagnosis'] if 'Diagnosis' in df_numeric.columns else None
        
        # Handle missing values
        X = X.fillna(X.median())
        
        return X, y, feature_cols
    
    def perform_pca_analysis(self, X, n_components=None):
        """Perform PCA and analyze component importance"""
        # Standardize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Fit PCA
        if n_components is None:
            n_components = min(X.shape[0], X.shape[1])
        
        self.pca = PCA(n_components=n_components)
        X_pca = self.pca.fit_transform(X_scaled)
        
        # Calculate explained variance
        explained_variance_ratio = self.pca.explained_variance_ratio_
        cumulative_variance = np.cumsum(explained_variance_ratio)
        
        return X_pca, explained_variance_ratio, cumulative_variance
    
    def select_optimal_components(self, explained_variance_ratio, threshold=0.95):
        """Select number of components that explain threshold% of variance"""
        cumulative_variance = np.cumsum(explained_variance_ratio)
        n_components = np.argmax(cumulative_variance >= threshold) + 1
        return n_components
    
    def get_feature_importance_from_pca(self, feature_names, n_top_components=5):
        """Extract most important original features from top PCA components"""
        if self.pca is None:
            raise ValueError("PCA not fitted yet")
        
        # Get loadings (components)
        loadings = self.pca.components_[:n_top_components]
        
        # Calculate feature importance as sum of absolute loadings
        feature_importance = np.sum(np.abs(loadings), axis=0)
        
        # Create feature importance dataframe
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': feature_importance
        }).sort_values('importance', ascending=False)
        
        self.feature_importance = importance_df
        return importance_df
    
    def select_top_features(self, X, y, method='pca', n_features=15):
        """Select top features using different methods"""
        feature_names = X.columns.tolist()
        
        if method == 'pca':
            # Use PCA-based selection
            _, explained_var, _ = self.perform_pca_analysis(X)
            n_components = self.select_optimal_components(explained_var, threshold=0.95)
            importance_df = self.get_feature_importance_from_pca(feature_names, n_components)
            selected_features = importance_df.head(n_features)['feature'].tolist()
            
        elif method == 'univariate':
            # Use univariate statistical tests
            selector = SelectKBest(score_func=f_classif, k=n_features)
            X_selected = selector.fit_transform(X, y)
            selected_indices = selector.get_support(indices=True)
            selected_features = [feature_names[i] for i in selected_indices]
            
        elif method == 'mutual_info':
            # Use mutual information
            selector = SelectKBest(score_func=mutual_info_classif, k=n_features)
            X_selected = selector.fit_transform(X, y)
            selected_indices = selector.get_support(indices=True)
            selected_features = [feature_names[i] for i in selected_indices]
        
        self.selected_features = selected_features
        return selected_features
    
    def plot_pca_analysis(self, explained_variance_ratio, cumulative_variance):
        """Plot PCA analysis results"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot explained variance ratio
        ax1.bar(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio)
        ax1.set_xlabel('Principal Component')
        ax1.set_ylabel('Explained Variance Ratio')
        ax1.set_title('Explained Variance by Component')
        ax1.grid(True, alpha=0.3)
        
        # Plot cumulative explained variance
        ax2.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, 'bo-')
        ax2.axhline(y=0.95, color='r', linestyle='--', label='95% threshold')
        ax2.set_xlabel('Number of Components')
        ax2.set_ylabel('Cumulative Explained Variance')
        ax2.set_title('Cumulative Explained Variance')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_feature_importance(self, top_n=20):
        """Plot top feature importance"""
        if self.feature_importance is None:
            raise ValueError("Feature importance not calculated yet")
        
        plt.figure(figsize=(12, 8))
        top_features = self.feature_importance.head(top_n)
        
        sns.barplot(data=top_features, x='importance', y='feature')
        plt.title(f'Top {top_n} Most Important Features (PCA-based)')
        plt.xlabel('Importance Score')
        plt.tight_layout()
        plt.show()
    
    def generate_feature_report(self):
        """Generate comprehensive feature selection report"""
        if self.selected_features is None:
            raise ValueError("Feature selection not performed yet")
        
        report = {
            'selected_features': self.selected_features,
            'n_selected': len(self.selected_features),
            'feature_importance': self.feature_importance.to_dict('records') if self.feature_importance is not None else None
        }
        
        return report

# Usage example
def analyze_ckd_features():
    """Main function to analyze CKD features"""
    selector = CKDFeatureSelector()
    
    # Load data
    X, y, feature_names = selector.load_and_preprocess_data('Chronic_Kidney_Dsease_data.csv')
    print(f"Original dataset: {X.shape[1]} features, {X.shape[0]} samples")
    
    # Perform PCA analysis
    X_pca, explained_var, cumulative_var = selector.perform_pca_analysis(X)
    
    # Plot analysis
    selector.plot_pca_analysis(explained_var, cumulative_var)
    
    # Select optimal number of components (95% variance)
    optimal_components = selector.select_optimal_components(explained_var, threshold=0.95)
    print(f"Components needed for 95% variance: {optimal_components}")
    
    # Get feature importance and select top features
    importance_df = selector.get_feature_importance_from_pca(feature_names, optimal_components)
    top_features = selector.select_top_features(X, y, method='pca', n_features=15)
    
    print(f"\nTop 15 selected features:")
    for i, feature in enumerate(top_features, 1):
        print(f"{i:2d}. {feature}")
    
    # Plot feature importance
    selector.plot_feature_importance(top_n=20)
    
    # Generate report
    report = selector.generate_feature_report()
    
    return selector, report

if __name__ == "__main__":
    selector, report = analyze_ckd_features()