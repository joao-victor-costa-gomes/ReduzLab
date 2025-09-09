import os
import uuid
import pandas as pd
import plotly.express as px
from flask import current_app

class Visualizer:
    def __init__(self, algorithm_name, reduced_data, target_series, params):
        self.algorithm_name = algorithm_name
        self.reduced_data = reduced_data
        self.target_series = target_series
        self.params = params

    def _get_axis_labels(self):
        dim = self.params['dimension']
        return [f"{self.algorithm_name}{i+1}" for i in range(dim)]

    def create_plot(self):
        # Create a DataFrame for plotting
        axis_labels = self._get_axis_labels()
        df_plot = pd.DataFrame(self.reduced_data, columns=axis_labels)
        df_plot[self.params['target_column']] = self.target_series.values

        # Create the Plotly figure
        if self.params['dimension'] == 2:
            fig = px.scatter(df_plot, 
                             x=axis_labels[0], 
                             y=axis_labels[1], 
                             color=self.params['target_column'], 
                             title=self.params['plot_title'],) 
        else: # 3D
            fig = px.scatter_3d(df_plot, 
                                x=axis_labels[0], 
                                y=axis_labels[1], 
                                z=axis_labels[2],
                                color=self.params['target_column'], 
                                title=self.params['plot_title'],) 
            
        x_min = self.params.get('x_min')
        x_max = self.params.get('x_max')
        y_min = self.params.get('y_min')
        y_max = self.params.get('y_max')

        if x_min is not None and x_max is not None:
            if self.params['dimension'] == 3:
                fig.update_layout(scene_xaxis_range=[x_min, x_max])
            else:
                fig.update_layout(xaxis_range=[x_min, x_max])

        if y_min is not None and y_max is not None:
            if self.params['dimension'] == 3:
                fig.update_layout(scene_yaxis_range=[y_min, y_max])
            else:
                fig.update_layout(yaxis_range=[y_min, y_max])

        return fig

    def save_plot(self):
        fig = self.create_plot()
        results_folder = current_app.config['RESULTS_FOLDER']
        
        # Generate a unique filename for the plot
        unique_id = uuid.uuid4().hex
        file_extension = self.params['plot_type']
        filename = f"{self.algorithm_name}_{unique_id}.{file_extension}"
        full_path = os.path.join(results_folder, filename)

        # Save the file
        if file_extension == 'html':
            fig.write_html(full_path)
        else: # png
            fig.write_image(full_path)
            
        return filename
    
    def save_reduced_data(self):
        """
        Saves the reduced data and target column to a CSV file.
        Returns the filename.
        """
        # Get the column labels for the reduced data (e.g., ['PCA1', 'PCA2'])
        axis_labels = self._get_axis_labels()
        
        # Create a DataFrame from the numpy array of reduced data
        df_reduced = pd.DataFrame(self.reduced_data, columns=axis_labels)

        # Combine the reduced data with the target column
        # .reset_index(drop=True) is important to ensure correct alignment
        df_final = pd.concat([df_reduced, self.target_series.reset_index(drop=True)], axis=1)

        # Generate a unique filename for the CSV
        results_folder = current_app.config['RESULTS_FOLDER']
        unique_id = uuid.uuid4().hex
        filename = f"ReducedData_{self.algorithm_name}_{unique_id}.csv"
        full_path = os.path.join(results_folder, filename)

        # Save to CSV
        df_final.to_csv(full_path, index=False)

        return filename