# LIBRARIES
from flask import render_template, request, current_app, url_for
# BLUEPRINT
from app.main import bp
# LOCAL FUNCTIONS
from app.utils.decorators import require_dataset
from app.core.data_processor import process_data_for_reduction
from app.core.visualizer import Visualizer
# ALGORITHM & VALIDATION
from app.algorithms.isomap import Isomap
from app.utils.algorith_parameters_validation.isomap_parameter_validation import validate_isomap_parameters
from app.utils.algorithm_debug_functions.isomap_debug import print_isomap_parameters

from flask_babel import gettext as _

@bp.route('/isomap', methods=['GET', 'POST'])
@require_dataset
def isomap_page(df, table_html, validation_results):
    column_options = df.columns.tolist()
    param_error = None
    plot_url = None
    metrics = None
    csv_url = None
    scroll_to_results = False
    scroll_to_params = False
    advanced_params_open = False

    if request.method == 'POST':
        advanced_params_open = request.form.get('advanced_params_open') == 'true'
        params, param_error = validate_isomap_parameters(request.form, df)

        if param_error:
            scroll_to_params = True

        if not param_error:
            if current_app.config.get('DEBUG'):
                print_isomap_parameters(params)
            try:
                X, y = process_data_for_reduction(df, params)
                
                isomap_reducer = Isomap(params)
                results, error = isomap_reducer.fit_transform(X)
                if error:
                    raise Exception(error)
                
                visualizer = Visualizer(
                    algorithm_name="Isomap",
                    reduced_data=results['reduced_data'],
                    target_series=y,
                    params=params
                )
                plot_filename = visualizer.save_plot()
                csv_filename = visualizer.save_reduced_data()
                
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

    return render_template('algorithms_pages/isomap_page.html',
                           algorithm_name="Isomap",
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