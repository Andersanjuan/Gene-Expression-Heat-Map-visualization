from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import seaborn as sns

app = Flask(__name__)

# Define default sample groups and visualization parameters
sample_groups = {'Control': ['Sample1', 'Sample2'], 'Treatment': ['Sample3', 'Sample4']}
heatmap_params = {'cmap': 'coolwarm', 'yticklabels': True, 'xticklabels': True, 'figsize': (12, 10)}

@app.route('/')
def index():
    return render_template('index.html', groups=sample_groups)

@app.route('/visualize', methods=['POST'])
def visualize():
    # Get user-defined sample groups and heatmap parameters
    groups = {k: v.split(',') for k, v in request.form.items() if k != 'cmap'}
    cmap = request.form.get('cmap', 'coolwarm')

    # Load gene expression data
    gene_expr = pd.read_csv('gene_expression_data.csv')

    # Subset gene expression data by sample group
    grouped_data = {}
    for group, samples in groups.items():
        grouped_data[group] = gene_expr[gene_expr['Sample'].isin(samples)]

    # Generate heatmap visualization of gene expression data
    sns.set_style("white")
    sns.set(font_scale=0.8)
    heatmap_params['cmap'] = cmap
    g = sns.clustermap(
        gene_expr.set_index('Gene Expression'),
        **heatmap_params
    )

    # Save visualization to file
    g.savefig('static/heatmap.png')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
