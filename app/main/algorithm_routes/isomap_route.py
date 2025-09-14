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
from app.utils.form_validator import validate_base_parameters
from app.utils.algorithm_debug_functions.isomap_debug import print_isomap_parameters

@bp.route('/isomap', methods=['GET', 'POST'])
@require_dataset
def isomap_page(df, table_html, validation_results):
    column_options = df.columns.tolist()
    param_error = None
    plot_url = None
    metrics = None
    csv_url = None
    scroll_to_results = False

    if request.method == 'POST':
        params, param_error = validate_base_parameters(request.form, df)

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
                    'Execution Time (s)': f"{results['execution_time']:.4f}",
                }
                scroll_to_results = True
            except Exception as e:
                param_error = f"An error occurred during processing: {e}"

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
                           form_data=request.form)