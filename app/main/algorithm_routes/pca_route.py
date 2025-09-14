# LIBRARIES
from flask import render_template, request, current_app, url_for
# BLUEPRINT
from app.main import bp
# LOCAL FUNCTIONS
from app.utils.decorators import require_dataset
from app.core.data_processor import process_data_for_reduction
from app.core.visualizer import Visualizer
# ALGORITHM & VALIDATION
from app.algorithms.pca import PCA
from app.utils.form_validator import validate_base_parameters
from app.utils.algorithm_debug_functions.pca_debug import print_pca_parameters

@bp.route('/pca', methods=['GET', 'POST'])
@require_dataset
def pca_page(df, table_html, validation_results):
    # Get column names from the DataFrame to populate the dropdowns
    column_options = df.columns.tolist()
    # Post-processing data
    plot_url = None
    metrics = None
    csv_url = None
    # Other variables
    param_error = None
    scroll_to_results = False

    # Handle the form submission
    if request.method == 'POST':
        params, param_error = validate_base_parameters(request.form, df)

        if not param_error:
            if current_app.config.get('DEBUG'):
                print_pca_parameters(params)
            try:
                # Applying PCA algorithm
                X, y = process_data_for_reduction(df, params)
                pca_reducer = PCA(params)
                results, error = pca_reducer.fit_transform(X)
                if error:
                    raise Exception(error)
                
                # Generate and Save Visualization
                visualizer = Visualizer(
                    algorithm_name="PCA",
                    reduced_data=results['reduced_data'],
                    target_series=y,
                    params=params
                )
                plot_filename = visualizer.save_plot()
                csv_filename = visualizer.save_reduced_data()
                
                # Prepare results for the template
                plot_url = url_for('main.serve_result_file', filename=plot_filename)
                csv_url = url_for('main.serve_result_file', filename=csv_filename)
                metrics = {
                    'Execution Time (s)': f"{results['execution_time']:.4f}",
                    'Explained Variance (%)': f"{results['explained_variance']:.2f}"
                }
                scroll_to_results = True
            except Exception as e:
                param_error = f"An error occurred during processing: {e}"

    return render_template('algorithms_pages/pca_page.html',
                           algorithm_name="PCA",
                           table_html=table_html,
                           validation_results=validation_results,
                           column_options=column_options,
                           param_error=param_error,
                           plot_url=plot_url,
                           metrics=metrics,
                           csv_url=csv_url,
                           scroll_to_results=scroll_to_results,
                           form_data=request.form)