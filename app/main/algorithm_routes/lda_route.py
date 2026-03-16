# LIBRARIES
from flask import render_template, request, current_app, url_for
# BLUEPRINT
from app.main import bp
# LOCAL FUNCTIONS
from app.utils.decorators import require_dataset
from app.core.data_processor import process_data_for_reduction
from app.core.visualizer import Visualizer
# ALGORITHM & VALIDATION
from app.algorithms.lda import LDA
from app.utils.algorith_parameters_validation.lda_parameter_validation import validate_lda_parameters
from app.utils.algorithm_debug_functions.lda_debug import print_lda_parameters

from flask_babel import gettext as _

@bp.route('/lda', methods=['GET', 'POST'])
@require_dataset
def lda_page(df, table_html, validation_results):
    column_options = df.columns.tolist()
    plot_url = None
    metrics = None
    csv_url = None
    param_error = None
    scroll_to_results = False
    scroll_to_params = False
    advanced_params_open = False

    if request.method == 'POST':
        advanced_params_open = request.form.get('advanced_params_open') == 'true'
        params, param_error = validate_lda_parameters(request.form, df)

        if not param_error:
            target_col = params['target_column']
            if df[target_col].nunique() > 20: 
                param_error = _("LDA is a supervised algorithm for classification. The target column '%(target_col)s' has too many unique values and seems to be continuous. Please choose a categorical target.", target_col=target_col)

        if not param_error:
            if current_app.config.get('DEBUG'):
                print_lda_parameters(params)
            try:
                X, y = process_data_for_reduction(df, params)
                
                lda_reducer = LDA(params)
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

                sil_score = results.get('silhouette_score', 'N/A')
                sil_score_str = f"{sil_score:.4f}" if isinstance(sil_score, (int, float)) else sil_score

                db_score = results.get('davies_bouldin', 'N/A')
                db_score_str = f"{db_score:.4f}" if isinstance(db_score, (int, float)) else db_score
                
                # ATUALIZAÇÃO AQUI: Enviando as novas métricas para a tela do ReduzLab
                metrics = {
                    _('Execution Time (s)'): f"{results['execution_time']:.4f}",
                    _('Silhouette Score'): sil_score_str,
                    _('Davies-Bouldin Index'): db_score_str
                }
                
                if 'explained_variance' in results and results['explained_variance'] != 'N/A':
                    metrics[_('Explained Variance (%)')] = f"{results['explained_variance']:.2f}%"
                    
                if 'lda1_top' in results:
                    metrics[_('Top Impact on X-Axis (LDA1)')] = results['lda1_top']
                    
                if 'lda2_top' in results:
                    metrics[_('Top Impact on Y-Axis (LDA2)')] = results['lda2_top']

                scroll_to_results = True
            except Exception as e:
                param_error = _('An error occurred during processing: %(error)s', error=e)

        if param_error:
            scroll_to_params = True

    return render_template('algorithms_pages/lda_page.html', 
                           algorithm_name="LDA",
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