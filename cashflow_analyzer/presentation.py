from matplotlib import pyplot as plt

from cashflow_analyzer.__main__ import Model
from cashflow_analyzer.transactions import SCHEMA


def graph_interface(data, transaction_type, step):
    step_title = "years" if step == "yearly" else "months"
    type = "cashflow" if transaction_type == "all" else transaction_type
    x_axis = data[step_title] if step == "yearly" else data["years"].astype(str) + "-" + data["months"].astype(str)

    return Model(fig_size=(10, 5),
                 amount=data[SCHEMA["amount"]],
                 x_axis=x_axis,
                 x_label=step_title,
                 y_label=f"{type} in euro",
                 title=f"{type} over the {step_title}")


def plot_report(model: Model):
    fig, ax = plt.subplots(figsize=model.fig_size, tight_layout=True)
    ax.plot(model.x_axis, model.amount, '-X')
    ax.set_xlabel(model.x_label)
    ax.set_ylabel(model.y_label)
    ax.set_title(model.title)
    plt.grid()
    plt.xticks(model.x_axis, rotation='vertical')
    return fig


def to_pdfs(models, path):
    from matplotlib.backends.backend_pdf import PdfPages
    with PdfPages(path) as pdf:
        for model in models:
            pdf.savefig(plot_report(model))
            plt.close()
