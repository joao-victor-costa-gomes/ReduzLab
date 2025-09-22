# LIBRARIES
from flask import render_template, request, current_app, url_for
# BLUEPRINT
from app.main import bp
# LOCAL FUNCTIONS
from app.utils.decorators import require_dataset
from app.core.data_processor import process_data_for_reduction
from app.core.visualizer import Visualizer
# ALGORITHM & VALIDATION
from app.algorithms.lle import LLE
from app.utils.algorith_parameters_validation.lle_parameter_validation import validate_lle_parameters
from app.utils.algorithm_debug_functions.lle_debug import print_lle_parameters

from flask_babel import gettext as _

@bp.route('/lle', methods=['GET', 'POST'])
@require_dataset
def lle_page(df, table_html, validation_results):
    # Get column names from the DataFrame to populate the dropdowns
    column_options = df.columns.tolist()
    # Post-processing data
    plot_url = None
    metrics = None
    csv_url = None
    # Other variables
    param_error = None
    scroll_to_results = False
    scroll_to_params = False
    advanced_params_open = False

    # Handle the form submission
    if request.method == 'POST':
        advanced_params_open = request.form.get('advanced_params_open') == 'true'
        params, param_error = validate_lle_parameters(request.form, df)

        if not param_error:
            if current_app.config.get('DEBUG'):
                print_lle_parameters(params)

            # Applying TSNE algorithm
            try:
                X, y = process_data_for_reduction(df, params)
                lle_reducer = LLE(params)
                results, error = lle_reducer.fit_transform(X)
                if error:
                    raise Exception(error)
                
                # Generate and Save Visualization
                visualizer = Visualizer(
                    algorithm_name="LLE", 
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
                    _('Execution Time (s)'): f"{results['execution_time']:.4f}",
                }
                scroll_to_results = True
            except Exception as e:
                param_error = _('An error occurred during processing: %(error)s', error=e)

        if param_error:
            scroll_to_params = True

    return render_template('algorithms_pages/lle_page.html',
                           algorithm_name="LLE",
                           table_html=table_html,
                           validation_results=validation_results,
                           column_options=column_options,
                           param_error=param_error,
                           plot_url=plot_url,
                           metrics=metrics,
                           csv_url=csv_url,
                           scroll_to_results=scroll_to_results,
                           scroll_to_params=scroll_to_params,
                           advanced_params_open=advanced_params_open,
                           form_data=request.form)