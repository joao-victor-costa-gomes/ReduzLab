# LIBRARIES
from flask import render_template, request, current_app, url_for, session
# BLUEPRINT
from app.main import bp
# LOCAL FUNCTIONS
from app.utils.decorators import require_dataset
from app.core.data_processor import process_data_for_reduction
from app.core.visualizer import Visualizer
# ALGORITHM & VALIDATION
from app.algorithms.tsne import TSNE
# from app.utils.algorith_parameters_validation.tsne_parameter_validation import validate_tsne_parameters
from app.utils.form_validator import validate_base_parameters
from app.utils.algorithm_debug_functions.tsne_debug import print_tsne_parameters

@bp.route('/tsne', methods=['GET', 'POST'])
@require_dataset
def tsne_page(df, table_html, validation_results):
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
                print_tsne_parameters(params)

            try:
                # Applying TSNE algorithm
                X, y = process_data_for_reduction(df, params)  
                tsne_reducer = TSNE(params)
                results, error = tsne_reducer.fit_transform(X)
                if error:
                    raise Exception(error)
                
                # Generate and Save Visualization
                visualizer = Visualizer(
                    algorithm_name="T-SNE", 
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
                }
                scroll_to_results = True
            except Exception as e:
                param_error = f"An error occurred during processing: {e}"

    return render_template('algorithms_pages/tsne_page.html',
                           algorithm_name="T-SNE",
                           table_html=table_html,
                           validation_results=validation_results,
                           column_options=column_options,
                           param_error=param_error,
                           plot_url=plot_url,
                           metrics=metrics,
                           csv_url=csv_url,
                           scroll_to_results=scroll_to_results,
                           form_data=request.form)