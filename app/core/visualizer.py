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
            fig = px.scatter(df_plot, x=axis_labels[0], y=axis_labels[1], 
                             color=self.params['target_column'], title=self.params['plot_title'])
        else: # 3D
            fig = px.scatter_3d(df_plot, x=axis_labels[0], y=axis_labels[1], z=axis_labels[2],
                                color=self.params['target_column'], title=self.params['plot_title'])
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