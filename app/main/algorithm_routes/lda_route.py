# LIBRARIES
from flask import render_template, request, current_app, url_for, session
# BLUEPRINT
from app.main import bp
# LOCAL FUNCTIONS
from app.utils.decorators import require_dataset
from app.core.data_processor import process_data_for_reduction
from app.core.visualizer import Visualizer
# ALGORITHM & VALIDATION
from app.algorithms.lda import LDA
from app.utils.form_validator import validate_base_parameters
from app.utils.algorithm_debug_functions.lda_debug import print_lda_parameters

@bp.route('/lda', methods=['GET', 'POST'])
@require_dataset
def lda_page(df, table_html, validation_results):
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
            # Specific validation for LDA: Target column should not be continuous
            target_col = params['target_column']
            if df[target_col].nunique() > 20: # Heuristic: more than 20 unique values might be continuous
                param_error = f"LDA is a supervised algorithm for classification. The target column '{target_col}' has too many unique values and seems to be continuous. Please choose a categorical target."

        if not param_error:
            if current_app.config.get('DEBUG'):
                print_lda_parameters(params)
            try:
                X, y = process_data_for_reduction(df, params)
                
                # Use the LDA class
                lda_reducer = LDA(params)
                # Pass both X and y to the fit_transform method
                results, error = lda_reducer.fit_transform(X, y)
                if error:
                    raise Exception(error)
                
                visualizer = Visualizer(
                    algorithm_name="LDA", 
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

    return render_template('algorithms_pages/lda_page.html', # We will create this next
                           algorithm_name="LDA",
                           table_html=table_html,
                           validation_results=validation_results,
                           column_options=column_options,
                           param_error=param_error,
                           plot_url=plot_url,
                           metrics=metrics,
                           csv_url=csv_url,
                           scroll_to_results=scroll_to_results,
                           form_data=request.form)